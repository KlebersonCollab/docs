# Design de Arquitetura - Encurtador de URL (PT-BR)

> **Versão em Inglês**: [English Version](../architecture-design.md)

---

## Visão Geral

Este documento descreve a arquitetura completa do sistema para um encurtador de URL escalável, desde o design inicial simples até sistema distribuído pronto para produção.

## Evolução da Arquitetura

### Estágio 1: Arquitetura Básica (❌ Insuficiente)

```
┌──────────┐
│ Frontend │
└────┬─────┘
     │
┌────▼─────┐
│ Backend  │
│ Server   │
└────┬─────┘
     │
┌────▼─────┐
│Database  │
└──────────┘
```

**Problemas**:
- Servidor único não pode lidar com 1.160 escritas/seg e 11.600 leituras/seg
- Banco de dados único é ponto único de falha
- Sem redundância (viola requisito de disponibilidade 24x7)

### Estágio 2: Escalamento Horizontal (✅ Melhor)

```
┌──────────┐
│ Frontend │
└────┬─────┘
     │
┌────▼─────────────┐
│ Load Balancer    │
└────┬─────────────┘
     │
┌────┼────┬────┬────┐
│    │    │    │    │
┌───▼──┐┌───▼──┐┌───▼──┐
│API-1 ││API-2 ││API-3 │
└───┬──┘└───┬──┘└───┬──┘
    │      │      │
    └──────┼──────┘
           │
    ┌──────▼──────┐
    │  Database   │
    │ (Cassandra) │
    └─────────────┘
```

**Melhorias**:
- Múltiplas instâncias de API para escalamento horizontal
- Load balancer distribui tráfego
- Ainda tem banco como possível gargalo

### Estágio 3: Arquitetura Completa (✅ Pronto para Produção)

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Mobile App   │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌─────────────────┐
         │ Load Balancer   │
         └─────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐        ┌───▼───┐        ┌───▼───┐
│ API-1 │        │ API-2 │        │ API-3 │
└───┬───┘        └───┬───┘        └───┬───┘
    │                │                │
    └────────────────┼────────────────┘
                     │
         ┌───────────┼───────────┐
         │          │           │
    ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
    │ Redis   │ │ Redis   │ │ Redis   │
    │ Cluster │ │ Cluster │ │ Cluster │
    │(Cache + │ │(Cache + │ │(Cache + │
    │ Counter)│ │ Counter)│ │ Counter)│
    └────┬────┘ └────┬────┘ └────┬────┘
         │          │           │
         └──────────┼───────────┘
                    │
         ┌──────────▼───────────┐
         │    Cassandra        │
         │    Cluster          │
         │  (Multiple Nodes)   │
         └─────────────────────┘
```

## Detalhes dos Componentes

### 1. Load Balancer

**Propósito**: Distribuir requisições recebidas entre múltiplas instâncias do backend

**Benefícios**:
- Alta disponibilidade (se uma instância falha, outras continuam)
- Throughput aumentado (processamento paralelo)
- Health checks e failover automático

**Configuração**:
- Algoritmo round-robin ou least-connections
- Health checks a cada 30 segundos
- Sessões sticky não necessárias (API stateless)

### 2. Servidores de API

**Estratégia de Escalamento**: Horizontal (múltiplas instâncias)

**Requisitos por Instância**:
- Design stateless (sem armazenamento de sessão)
- Arquitetura share-nothing
- Comportamento consistente entre todas as instâncias

**Cálculo do Número de Instâncias**:
```
Capacidade necessária: 1.160 escritas/seg + 11.600 leituras/seg = 12.760 req/seg
Capacidade de instância única: ~1.000 req/seg
Mínimo de instâncias: 13 instâncias
Recomendado: 15-20 instâncias (com 50% de margem)
```

### 3. Cluster Redis

**Propósito Duplo**:
1. **Geração de ID**: Contador atômico para IDs únicos
2. **Camada de Cache**: Armazenar URLs frequentemente acessadas

#### Redis para Geração de ID

```python
# Incremento atômico - sem condições de corrida
next_id = redis_client.incr('url_counter')
```

**Alta Disponibilidade**:
- Redis Cluster (mínimo 3-6 nós)
- Ou Redis Sentinel para failover automático
- Crítico para operação do sistema (sem ele, não pode criar novas URLs)

#### Redis para Cache

**Estratégia**: Cache de URLs Mais Frequentemente Acessadas (MFU)

```python
# Cache URLs populares por 1 hora
redis_client.setex(f"url:{short_code}", 3600, long_url)
```

**Benefícios**:
- Reduz carga no banco de dados
- Tempos de resposta mais rápidos (memória vs disco)
- Lida com 11.600 leituras/seg eficientemente

**Taxa de Cache Hit Alvo**: 80-90%

### 4. Cluster Cassandra

**Por que Cassandra?**

1. **Escalabilidade Horizontal**
   - Pode escalar para centenas de nós
   - Lida com bilhões de registros facilmente
   - Suporta requisito de 36.5 TB de armazenamento

2. **Alto Throughput de Escrita**
   - Otimizado para cargas de trabalho com muitas escritas
   - Lida com 1.160 escritas/seg por nó facilmente
   - Escalamento linear com mais nós

3. **Alta Disponibilidade**
   - Replicação integrada
   - Sem ponto único de falha
   - Distribuição automática de dados

4. **Leituras de Baixa Latência**
   - Armazenamento colunar otimizado para leituras
   - Partition key (short_code) permite lookups rápidos

**Esquema**:
```cql
CREATE TABLE url_shortener (
    short_code TEXT PRIMARY KEY,
    long_url TEXT,
    created_at TIMESTAMP
);
```

**Replicação**:
- Fator de replicação: 3 (3 cópias de cada registro)
- Permite 1-2 falhas de nó sem perda de dados

## Fluxo de Dados

### Fluxo de Encurtamento de URL

```
1. Cliente → Load Balancer
2. Load Balancer → Servidor de API (selecionado)
3. Servidor de API → Redis (INCR counter) → Obter ID único
4. Servidor de API → Converter ID para Base 62 com ofuscação
5. Servidor de API → Cassandra (Armazenar: short_code → long_url)
6. Servidor de API → Cliente (Retornar URL curta)
```

**Performance**:
- Latência média: < 50ms
- Escritas no banco: Apenas para Cassandra (sem leituras necessárias)
- Operações Redis: Único INCR (atômico, rápido)

### Fluxo de Redirecionamento de URL

```
1. Cliente → Load Balancer
2. Load Balancer → Servidor de API
3. Servidor de API → Cache Redis (Verificar primeiro)
   ├─ Cache Hit: Retornar URL imediatamente
   └─ Cache Miss: Continuar para passo 4
4. Servidor de API → Cassandra (Consultar por short_code)
5. Servidor de API → Cache Redis (Armazenar para futuro)
6. Servidor de API → Cliente (301/302 redirect)
```

**Performance**:
- Cache Hit: < 5ms
- Cache Miss: < 20ms (consulta Cassandra)

## Impacto dos Códigos de Status HTTP

### 301 vs 302 - Decisão Arquitetural Crítica

#### 301 Moved Permanently

**Comportamento**:
- Navegador faz cache do redirecionamento localmente
- Requisições subsequentes vão diretamente ao destino (sem requisição ao servidor)
- Reduz carga no servidor significativamente

**Prós**:
- Carga mínima no servidor
- Mais rápido para usuários finais

**Contras**:
- Não pode rastrear analytics (requisições não chegam ao servidor)
- Não pode identificar URLs populares para cache
- Não pode implementar dashboard de analytics

#### 302 Found (Redirect Temporário)

**Comportamento**:
- Navegador verifica servidor em toda requisição
- Servidor trata cada redirecionamento
- Caminho completo da requisição disponível

**Prós**:
- Pode rastrear todos os cliques
- Pode identificar URLs populares
- Habilita analytics e estratégia de cache
- Pode implementar dashboards

**Contras**:
- Maior carga no servidor
- Toda requisição atinge backend

### Recomendação

**Usar 302** para encurtador de URL porque:
1. Habilita analytics (funcionalidade crítica)
2. Permite otimização de cache (identificar URLs populares)
3. Suporta funcionalidade de dashboard
4. Camada de cache ainda pode reduzir carga no banco

**Nota**: Escolha do código de status muda fundamentalmente a arquitetura. 301 torna camada de cache desnecessária, mas elimina capacidade de analytics.

## Planejamento de Capacidade

### Operações de Escrita
- **Alvo**: 1.160 escritas/seg
- **Pico**: Assumir 2x = 2.320 escritas/seg
- **Cassandra**: Pode lidar com ~5.000 escritas/seg por nó
- **Nós Necessários**: 1 nó (com 100% de margem) ou 2 nós (para redundância)

### Operações de Leitura
- **Alvo**: 11.600 leituras/seg
- **Pico**: Assumir 2x = 23.200 leituras/seg
- **Taxa de Cache Hit**: 85% = 19.720 em cache, 3.480 consultas DB/seg
- **Cassandra**: Pode lidar com ~10.000 leituras/seg por nó
- **Nós Necessários**: 1-2 nós

### Total de Nós Necessários
- **Mínimo**: 3 nós (para fator de replicação 3)
- **Recomendado**: 5-7 nós (para performance e redundância)

## Configuração de Alta Disponibilidade

### Implantação Multi-Região

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

**Benefícios**:
- Redundância geográfica
- Latência menor (rotear para região mais próxima)
- Recuperação de desastres

## Monitoramento e Métricas

### Métricas-Chave

1. **Throughput**
   - Escritas/seg
   - Leituras/seg
   - Taxa de cache hit

2. **Latência**
   - P50, P95, P99 de tempos de resposta
   - Latência de cache vs latência de banco

3. **Disponibilidade**
   - Percentual de uptime
   - Taxa de erro
   - Requisições falhadas

4. **Capacidade**
   - Tamanho do banco de dados
   - Uso de memória do cache
   - Largura de banda de rede

## Próximos Passos

1. Implementar estratégia de cache (identificar URLs populares)
2. Configurar monitoramento e alertas
3. Planejar implantação multi-região
4. Projetar dashboard de analytics
5. Implementar rate limiting e medidas de segurança

---

**Documentos Relacionados**:
- [Padrões de Escalabilidade](scalability-patterns.pt-br.md)
- [Métricas de Performance](performance-metrics.pt-br.md)

**Última Atualização**: Janeiro 2025
**Mantenedor**: Equipe Skynet

