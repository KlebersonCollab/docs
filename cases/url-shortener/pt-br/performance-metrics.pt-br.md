# Métricas de Performance - Encurtador de URL (PT-BR)

> **Versão em Inglês**: [English Version](../performance-metrics.md)

---

## Visão Geral

Este documento descreve as principais métricas de performance, cálculos e estratégias de monitoramento para um sistema encurtador de URL.

## Métricas de Performance Necessárias

### Requisitos de Throughput

#### Operações de Escrita
- **Alvo**: 1.160 escritas/segundo
- **Pico**: Assumir 2x = 2.320 escritas/segundo
- **Cálculo**:
  ```
  100.000.000 URLs/dia ÷ 24 horas ÷ 60 minutos ÷ 60 segundos
  = ~1.160 escritas/segundo
  ```

#### Operações de Leitura
- **Alvo**: 11.600 leituras/segundo
- **Pico**: Assumir 2x = 23.200 leituras/segundo
- **Cálculo**:
  ```
  1.160 escritas/seg × 10 (proporção leitura:escrita)
  = 11.600 leituras/segundo
  ```

### Requisitos de Latência

#### Encurtamento de URL (Escrita)
- **Alvo**: < 50ms (P95)
- **Detalhamento**:
  - Redis INCR: ~1ms
  - Codificação Base 62: < 1ms
  - Escrita Cassandra: ~10-20ms
  - Overhead de rede: ~5ms
  - **Total**: ~20-30ms média

#### Redirecionamento de URL (Leitura)
- **Cache Hit**: < 5ms (P95)
- **Cache Miss**: < 20ms (P95)
- **Detalhamento** (Cache Miss):
  - Verificação de cache: ~1ms
  - Consulta Cassandra: ~10ms
  - Escrita de cache: ~1ms
  - Rede: ~5ms
  - **Total**: ~17ms média

### Requisitos de Disponibilidade

- **Alvo**: 99.9% uptime (24x7)
- **Tempo de Inatividade Permitido**: ~8.76 horas/ano
- **Impacto**: Requer redundância em todas as camadas

## Cálculos de Armazenamento

### Total de Registros

```
100.000.000 URLs/dia × 365 dias/ano × 10 anos
= 365.000.000.000 registros (365 bilhões)
```

### Armazenamento Total

```
365 bilhões de registros × 100 bytes/registro
= 36.500.000.000.000 bytes
= 36.5 TB
```

### Espaço de Código Curto

**Cálculo Base 62**:
```
62^1 = 62
62^2 = 3.844
62^3 = 238.328
62^4 = 14.776.336
62^5 = 916.132.832
62^6 = 56.800.235.584
62^7 = 3.521.614.606.208 (3.5 trilhões)
```

**Mínimo Necessário**: 7 caracteres para 365 bilhões de códigos únicos

## Benchmarks de Performance

### Benchmarks de Componentes

#### Redis (Geração de ID)
- **Operação**: INCR (incremento atômico)
- **Latência**: ~1ms
- **Throughput**: 100.000+ ops/seg por nó
- **Capacidade**: Lida facilmente com 1.160 escritas/seg

#### Redis (Cache)
- **Operação**: GET/SET
- **Latência**: < 1ms
- **Throughput**: 100.000+ ops/seg por nó
- **Capacidade**: Lida facilmente com 11.600 leituras/seg (com múltiplos nós)

#### Cassandra (Leitura)
- **Operação**: SELECT por chave de partição
- **Latência**: 10-15ms (P95)
- **Throughput**: ~10.000 leituras/seg por nó
- **Com Cache**: Apenas 20% atinge banco = 2.320 leituras/seg necessárias
- **Nós Necessários**: 1 nó (com 400% de margem)

#### Cassandra (Escrita)
- **Operação**: INSERT
- **Latência**: 10-20ms (P95)
- **Throughput**: ~5.000 escritas/seg por nó
- **Nós Necessários**: 1 nó (com 200% de margem)

### Benchmarks do Sistema Completo

#### Latência End-to-End

**Encurtamento de URL**:
```
Load Balancer: ~2ms
Processamento API: ~1ms
Redis INCR: ~1ms
Codificação: <1ms
Escrita Cassandra: ~15ms
Resposta: ~5ms
─────────────────────
Total: ~25ms (P95: ~50ms)
```

**Redirecionamento de URL (Cache Hit)**:
```
Load Balancer: ~2ms
Processamento API: ~1ms
Redis GET: <1ms
Resposta: ~2ms
─────────────────────
Total: ~5ms (P95: ~10ms)
```

**Redirecionamento de URL (Cache Miss)**:
```
Load Balancer: ~2ms
Processamento API: ~1ms
Redis GET (miss): ~1ms
Leitura Cassandra: ~12ms
Redis SET: ~1ms
Resposta: ~3ms
─────────────────────
Total: ~20ms (P95: ~40ms)
```

## Performance do Cache

### Taxa de Cache Hit Alvo

- **Objetivo**: 85-90% de taxa de hit
- **Impacto**: Reduz carga no banco de dados em 85-90%

### Cálculo da Taxa de Cache Hit

```
Total de leituras: 11.600/seg
Cache hits (85%): 9.860/seg
Cache misses (15%): 1.740/seg
Consultas ao banco: 1.740/seg (reduzido de 11.600)
```

### Impacto da Estratégia de Cache

**Sem Cache**:
- 11.600 consultas ao banco/seg
- Requer 2-3 nós Cassandra
- Latência maior (15ms vs 5ms)

**Com Cache (85% hit rate)**:
- 1.740 consultas ao banco/seg
- Requer 1 nó Cassandra
- Latência menor (5ms para 85% das requisições)

## Métricas de Escalabilidade

### Capacidade de Escalamento Horizontal

#### Servidores de API
- **Capacidade de Instância Única**: ~1.000 req/seg
- **Capacidade Necessária**: 12.760 req/seg
- **Mínimo de Instâncias**: 13
- **Recomendado**: 15-20 (com 50% de margem)

#### Nós de Banco de Dados
- **Capacidade de Escrita por Nó**: ~5.000/seg
- **Escritas Necessárias**: 1.160/seg
- **Nós Necessários**: 1 (com 400% de margem)
- **Recomendado**: 3 (para fator de replicação 3)

#### Nós de Cache
- **Capacidade por Nó**: 100.000+ ops/seg
- **Ops Necessárias**: 11.600/seg
- **Nós Necessários**: 1 (com 800% de margem)
- **Recomendado**: 3 (para alta disponibilidade)

## Monitoramento de Métricas

### Indicadores-Chave de Performance (KPIs)

#### 1. Throughput de Requisições
```python
metricas = {
    'escritas_por_segundo': 1160,
    'leituras_por_segundo': 11600,
    'total_requisicoes_por_segundo': 12760
}
```

#### 2. Tempo de Resposta
```python
metricas_latencia = {
    'p50': 10,  # ms - Mediana
    'p95': 50,  # ms - Percentil 95
    'p99': 100,  # ms - Percentil 99
    'p999': 200  # ms - Percentil 99.9
}
```

#### 3. Performance do Cache
```python
metricas_cache = {
    'taxa_hit': 0.85,  # 85%
    'taxa_miss': 0.15,  # 15%
    'tamanho_cache': '10GB',
    'taxa_eviccao': 100  # por segundo
}
```

#### 4. Performance do Banco de Dados
```python
metricas_db = {
    'latencia_leitura_p95': 15,  # ms
    'latencia_escrita_p95': 20,  # ms
    'taxa_consulta': 1740,  # por segundo (com cache)
    'uso_pool_conexoes': 0.6  # 60%
}
```

#### 5. Taxas de Erro
```python
metricas_erro = {
    'taxa_erro': 0.001,  # 0.1%
    'taxa_timeout': 0.0001,  # 0.01%
    'erros_4xx': 0.0005,  # 0.05%
    'erros_5xx': 0.0005  # 0.05%
}
```

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

## Planejamento de Capacidade

### Capacidade Atual

| Componente | Capacidade | Utilização | Margem |
|------------|------------|------------|--------|
| Servidores de API (15) | 15.000 req/seg | 12.760 (85%) | 15% |
| Cassandra (3) | 15.000 escritas/seg | 1.160 (8%) | 92% |
| Leituras Cassandra | 30.000 leituras/seg | 1.740 (6%) | 94% |
| Redis (3) | 300.000 ops/seg | 11.600 (4%) | 96% |

### Projeções de Crescimento

#### Crescimento de 2x
- **Escritas**: 2.320/seg (ainda dentro da capacidade)
- **Leituras**: 23.200/seg (cache lida com a maioria)
- **Ação**: Escalar servidores de API para 25-30 instâncias

#### Crescimento de 10x
- **Escritas**: 11.600/seg
- **Leituras**: 116.000/seg
- **Ação**: 
  - Escalar servidores de API para 150-200 instâncias
  - Escalar Cassandra para 5-7 nós
  - Escalar cluster Redis

#### Crescimento de 100x
- **Requer**: Implantação multi-região
- **Requer**: Sharding de banco de dados
- **Requer**: Estratégias de cache avançadas

## Oportunidades de Otimização

### 1. Cache Warming

**Pré-popular cache com URLs populares**:
```python
def warm_cache():
    """Pré-popular cache com top 10.000 URLs"""
    urls_populares = obter_top_urls(limit=10000)
    for url in urls_populares:
        redis.setex(f"url:{url.short_code}", 86400, url.long_url)
```

### 2. Réplicas de Leitura

**Usar réplicas de leitura Cassandra**:
- Rotear consultas de leitura para réplica mais próxima
- Reduz latência para usuários globais

### 3. Pool de Conexões

**Otimizar conexões de banco de dados**:
```python
# Reutilizar conexões
tamanho_pool_conexoes = min_instancias * 10
# Evitar overhead de conexão
```

### 4. Operações em Batch

**Agrupar escritas quando possível**:
```python
# Se agrupando múltiplas URLs
batch = []
for url in urls:
    batch.append(insert_statement)
session.execute_batch(batch)
```

## Testes de Performance

### Cenários de Teste de Carga

#### 1. Teste Baseline
- **Tráfego**: 12.760 req/seg
- **Duração**: 1 hora
- **Objetivo**: Verificar sistema lida com carga esperada

#### 2. Teste de Pico
- **Tráfego**: 25.520 req/seg (2x)
- **Duração**: 30 minutos
- **Objetivo**: Verificar sistema lida com picos de tráfego

#### 3. Teste de Estresse
- **Tráfego**: Aumentar gradualmente até falha
- **Objetivo**: Encontrar ponto de ruptura

#### 4. Teste de Resistência
- **Tráfego**: 12.760 req/seg
- **Duração**: 24 horas
- **Objetivo**: Verificar sem vazamentos de memória ou degradação

### Ferramentas

- **Apache JMeter**: Teste de carga
- **Gatling**: Teste de performance
- **wrk**: Benchmark HTTP
- **redis-benchmark**: Performance de cache

---

**Documentos Relacionados**:
- [Design de Arquitetura](architecture-design.pt-br.md)
- [Padrões de Escalabilidade](scalability-patterns.pt-br.md)

**Última Atualização**: Janeiro 2025
**Mantenedor**: Equipe Skynet

