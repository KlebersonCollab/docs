# Padrões de Escalabilidade - Encurtador de URL (PT-BR)

> **Versão em Inglês**: [English Version](../scalability-patterns.md)

---

## Visão Geral

Este documento descreve os padrões de escalabilidade e evolução arquitetural necessários para lidar com tráfego de alto volume para um sistema encurtador de URL.

## Estratégia de Escalamento

### Escalamento Vertical vs Horizontal

#### Escalamento Vertical (❌ Não Adequado)

**Definição**: Adicionar mais recursos (CPU, RAM) a um servidor único

**Limitações**:
- Capacidade máxima limitada por hardware
- Ponto único de falha
- Não pode lidar com 12.760 requisições/segundo
- Caro em escala

#### Escalamento Horizontal (✅ Recomendado)

**Definição**: Adicionar mais servidores/instâncias

**Benefícios**:
- Escalabilidade linear
- Alta disponibilidade (sem ponto único de falha)
- Custo-efetivo (hardware comum)
- Pode escalar para qualquer capacidade necessária

## Load Balancing

### Propósito

Distribuir tráfego recebido entre múltiplas instâncias do backend.

### Arquitetura

```
                    ┌─────────────────┐
                    │ Load Balancer   │
                    └────────┬────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
        ┌───────▼──┐  ┌──────▼──┐  ┌──────▼──┐
        │ API-1    │  │ API-2    │  │ API-3    │
        └──────────┘  └──────────┘  └──────────┘
```

### Algoritmos de Load Balancing

#### 1. Round Robin
- Distribui requisições sequencialmente
- Simples e justo
- Bom para capacidade uniforme de servidor

#### 2. Least Connections
- Roteia para servidor com menos conexões ativas
- Melhor para tempos de processamento variados
- **Recomendado** para encurtador de URL

#### 3. Weighted Round Robin
- Ajusta para diferentes capacidades de servidor
- Útil para infraestrutura heterogênea

### Health Checks

```python
# Configuração do load balancer
intervalo_health_check = 30  # segundos
caminho_health_check = "/health"
limiar_insalubre = 3  # falhas consecutivas
limiar_saudavel = 2  # sucessos consecutivos
```

## Escalamento do Banco de Dados

### Por que Cassandra?

#### 1. Escalabilidade Horizontal

```
RDBMS Tradicional:
- Nó mestre único
- Escalamento apenas vertical
- Throughput de escrita limitado

Cassandra:
- Múltiplos nós (sem mestre)
- Escalamento horizontal
- Escalamento linear de escrita
```

#### 2. Otimizado para Escrita

- **Estrutura LSM-Tree**
- Escritas apenas append (sem atualizações)
- Perfeito para armazenamento de URL (principalmente escritas, atualizações ocasionais)

#### 3. Estratégia de Particionamento

```cql
-- Particionar por short_code
CREATE TABLE url_shortener (
    short_code TEXT PRIMARY KEY,  -- Chave de partição
    long_url TEXT,
    created_at TIMESTAMP
);
```

**Benefícios**:
- Cada short_code mapeia para nó específico
- Leituras paralelas entre nós
- Sem consultas cross-node necessárias

#### 4. Fator de Replicação

```cql
CREATE KEYSPACE url_shortener
WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'datacenter1': 3  -- 3 cópias de cada registro
};
```

**Benefícios**:
- Alta disponibilidade (sobrevive a 1-2 falhas de nó)
- Durabilidade de dados
- Ler da réplica mais próxima

### Cálculo de Capacidade

**Capacidade de Escrita**:
- 1.160 escritas/seg necessárias
- Cassandra: ~5.000 escritas/seg por nó
- Nós necessários: 1 (com 200% de margem)

**Capacidade de Leitura**:
- 11.600 leituras/seg necessárias
- Cache lida com 85% = 9.860 em cache/seg
- Banco de dados: 1.740 leituras/seg
- Cassandra: ~10.000 leituras/seg por nó
- Nós necessários: 1

**Replicação**:
- Fator de replicação 3
- **Mínimo de nós**: 3
- **Recomendado**: 5-7 nós (para performance + redundância)

## Estratégia de Cache

### Configuração de Cluster Redis

#### Arquitetura

```
                    ┌──────────────┐
                    │  API Server │
                    └──────┬───────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
    ┌───────▼───┐  ┌───────▼───┐  ┌───────▼───┐
    │ Redis-1   │  │ Redis-2   │  │ Redis-3   │
    │ (Master)  │  │ (Replica) │  │ (Replica) │
    └───────────┘  └───────────┘  └───────────┘
```

#### Propósito Duplo

**1. Geração de ID**

```python
# Contador atômico
next_id = redis.incr('url_counter')
```

**Requisitos**:
- Deve ser atômico (sem condições de corrida)
- Deve ser rápido (toda escrita precisa de ID)
- Alta disponibilidade crítica

**Configuração**:
- Redis Cluster (3-6 nós)
- Ou Redis Sentinel para auto-failover

**2. Cache de URL**

**Estratégia**: Cache de URLs Mais Frequentemente Acessadas

```python
# Cache URLs populares
redis.setex(f"url:{short_code}", TTL=3600, value=long_url)
```

**Benefícios**:
- Reduz carga no banco de dados em 80-90%
- Tempos de resposta mais rápidos (memória vs disco)
- Lida com carga de trabalho com muitas leituras

#### Estratégia de População de Cache

**1. Lazy Loading** (Atual)
- Cache na primeira leitura
- Implementação simples
- Pode cachear URLs impopulares

**2. Write-Through**
- Cache imediatamente na escrita
- Garante cache para novas URLs
- Pode desperdiçar cache em URLs raramente acessadas

**3. Abordagem Híbrida** (Recomendado)
- Write-through para novas URLs (TTL: 1 hora)
- Rastrear frequência de acesso
- Estender TTL para URLs populares (até 24 horas)

```python
def obter_url(codigo_curto: str) -> str:
    # Verificar cache primeiro
    cached = redis.get(f"url:{codigo_curto}")
    if cached:
        # Incrementar contador de acesso
        redis.incr(f"url:{codigo_curto}:hits")
        return cached
    
    # Consultar banco de dados
    url = cassandra.get(codigo_curto)
    
    # Cache com TTL inicial
    redis.setex(f"url:{codigo_curto}", 3600, url)
    
    # Se tornar popular, estender TTL
    hits = redis.get(f"url:{codigo_curto}:hits")
    if hits and hits > 100:  # Limiar popular
        redis.expire(f"url:{codigo_curto}", 86400)  # 24 horas
    
    return url
```

## Auto-Scaling

### Gerenciamento Dinâmico de Instâncias

#### Métricas para Escalonamento

```python
# Gatilhos de escalonamento
limiares_scale_up = {
    'uso_cpu': 70,  # %
    'latencia_requisicao_p95': 200,  # ms
    'comprimento_fila_requisicao': 100,
    'taxa_erro': 1  # %
}

limiares_scale_down = {
    'uso_cpu': 30,  # %
    'latencia_requisicao_p95': 50,  # ms
    'comprimento_fila_requisicao': 10,
    'taxa_erro': 0.1  # %
}
```

#### Política de Escalonamento

```yaml
# Configuração de auto-scaling
min_instancias: 3
max_instancias: 20
utilizacao_cpu_alvo: 60%
cooldown_scale_up: 300  # segundos
cooldown_scale_down: 600  # segundos
```

### Benefícios

1. **Otimização de Custos**: Escalar para baixo durante tráfego baixo
2. **Performance**: Escalar para cima durante tráfego de pico
3. **Confiabilidade**: Manter serviço durante picos de tráfego

## Implantação Multi-Região

### Arquitetura

```
Região 1 (US-East)          Região 2 (EU-West)
┌──────────────┐           ┌──────────────┐
│ Load Balancer│           │ Load Balancer│
│ API Servers  │           │ API Servers  │
│ Redis Cluster│           │ Redis Cluster│
│ Cassandra    │◄──────────►│ Cassandra    │
└──────────────┘           └──────────────┘
      │                            │
      └──────── Cross-Region ──────┘
            Replication
```

### Benefícios

1. **Distribuição Geográfica**
   - Latência menor (rotear para região mais próxima)
   - Melhor experiência do usuário

2. **Recuperação de Desastres**
   - Se uma região falhar, outras continuam
   - Failover automático

3. **Conformidade**
   - Requisitos de residência de dados
   - Regulamentações regionais

### Desafios

1. **Consistência de Dados**
   - Latência de replicação cross-region
   - Modelo de consistência eventual

2. **Geração de ID**
   - Deve ser globalmente única
   - Não pode usar mesmo contador em todas as regiões

**Solução**: Geração de ID ciente de região

```python
# Região 1: IDs começando em 14.000.000
# Região 2: IDs começando em 20.000.000
# Região 3: IDs começando em 30.000.000

OFFSET_ID_REGIAO = {
    'us-east': 14_000_000,
    'eu-west': 20_000_000,
    'asia-pac': 30_000_000
}

def obter_proximo_id():
    base_id = redis.incr('url_counter')
    offset_regiao = OFFSET_ID_REGIAO[os.environ['REGION']]
    return base_id + offset_regiao
```

## Otimização de Performance

### Otimização do Banco de Dados

#### Otimização de Leitura

1. **Design de Chave de Partição**
   - short_code como chave primária
   - Habilita lookup direto de nó
   - Sem scanning necessário

2. **Consistência de Leitura**
   - Usar ONE consistency (mais rápido)
   - Aceitável para lookup de URL (idempotente)

```python
# Leituras rápidas
result = session.execute(
    "SELECT long_url FROM url_shortener WHERE short_code = ?",
    [short_code],
    consistency_level=ConsistencyLevel.ONE
)
```

#### Otimização de Escrita

1. **Batch Writes** (se aplicável)
   - Agrupar múltiplas escritas
   - Reduz overhead de rede

2. **Escritas Assíncronas**
   - Fire-and-forget para analytics
   - Não bloquear resposta

### Otimização de Rede

#### Pool de Conexões

```python
# Reutilizar conexões de banco de dados
from cassandra.cluster import Cluster

cluster = Cluster(['node1', 'node2', 'node3'])
session = cluster.connect('url_shortener')
# Reutilizar session entre requisições
```

#### Conexões Keep-Alive

```python
# Pool de conexões Redis
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    decode_responses=True
)
redis_client = redis.Redis(connection_pool=redis_pool)
```

## Resumo de Planejamento de Capacidade

### Requisitos Atuais

| Métrica | Valor |
|---------|-------|
| Operações de escrita/seg | 1.160 |
| Operações de leitura/seg | 11.600 |
| Armazenamento (10 anos) | 36.5 TB |
| Registros (10 anos) | 365 bilhões |

### Necessidades de Infraestrutura

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| Instâncias de API | 13 | 15-20 |
| Nós Cassandra | 3 | 5-7 |
| Nós Redis | 3 | 3-6 |
| Load Balancers | 2 | 2 (ativo-passivo) |

### Projeções de Escalonamento

**Crescimento de 10x**:
- Instâncias de API: 150-200
- Nós Cassandra: 15-20
- Capacidade de cache: Escalar proporcionalmente

**Crescimento de 100x**:
- Requer estratégia de sharding
- Multi-região obrigatória
- Cache mais sofisticado

## Monitoramento e Alertas

### Métricas-Chave

1. **Throughput**
   - Requisições por segundo
   - Proporção de escritas vs leituras

2. **Latência**
   - P50, P95, P99
   - Latência de cache hit
   - Latência de consulta de banco

3. **Disponibilidade**
   - Percentual de uptime
   - Taxa de erro
   - Requisições falhadas

4. **Capacidade**
   - Tamanho do banco de dados
   - Uso de memória do cache
   - Instância CPU/memória

### Limiares de Alerta

```python
alertas = {
    'latencia_alta_p95': {
        'limiar': 200,  # ms
        'acao': 'Escalar instâncias de API'
    },
    'taxa_cache_hit_baixa': {
        'limiar': 0.70,  # 70%
        'acao': 'Revisar estratégia de cache'
    },
    'taxa_erro_alta': {
        'limiar': 0.01,  # 1%
        'acao': 'Investigar erros'
    },
    'pool_conexoes_db_esgotado': {
        'limiar': 0.90,  # 90%
        'acao': 'Aumentar tamanho do pool ou escalar DB'
    },
    'uso_cpu_alto': {
        'limiar': 0.80,  # 80%
        'acao': 'Escalar horizontalmente'
    }
}
```

---

**Documentos Relacionados**:
- [Design de Arquitetura](architecture-design.pt-br.md)
- [Métricas de Performance](performance-metrics.pt-br.md)

**Última Atualização**: Janeiro 2025
**Mantenedor**: Equipe Skynet

