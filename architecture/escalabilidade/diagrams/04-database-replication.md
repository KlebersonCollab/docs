# Diagrama - Database Replication

## Arquitetura com Replicação de Banco de Dados

```mermaid
graph TB
    subgraph "Client Layer"
        FE[Frontend<br/>React/Angular]
        MA[Mobile App<br/>iOS/Android]
    end
    
    subgraph "Network Layer"
        DNS[DNS<br/>api.meuapp.com]
    end
    
    subgraph "Load Balancer"
        LB[Load Balancer<br/>HAProxy/Nginx/AWS ALB]
    end
    
    subgraph "Application Servers"
        API1[API Server 1<br/>Backend Code]
        API2[API Server 2<br/>Backend Code]
        API3[API Server 3<br/>Backend Code]
    end
    
    subgraph "Database Cluster"
        DBM[(Database Master<br/>MySQL/PostgreSQL<br/>Write Operations)]
        DBS1[(Database Slave 1<br/>MySQL/PostgreSQL<br/>Read Operations)]
        DBS2[(Database Slave 2<br/>MySQL/PostgreSQL<br/>Read Operations)]
    end
    
    FE --> DNS
    MA --> DNS
    DNS --> LB
    LB --> API1
    LB --> API2
    LB --> API3
    
    API1 --> DBM
    API1 --> DBS1
    API1 --> DBS2
    
    API2 --> DBM
    API2 --> DBS1
    API2 --> DBS2
    
    API3 --> DBM
    API3 --> DBS1
    API3 --> DBS2
    
    DBM -.->|Replication| DBS1
    DBM -.->|Replication| DBS2
    
    classDef client fill:#e1f5fe
    classDef network fill:#f3e5f5
    classDef loadbalancer fill:#ffebee
    classDef server fill:#e8f5e8
    classDef database fill:#fff3e0
    classDef replication fill:#f1f8e9
    
    class FE,MA client
    class DNS network
    class LB loadbalancer
    class API1,API2,API3 server
    class DBM,DBS1,DBS2 database
```

## Benefícios da Replicação

- **Eliminação de SPOF**: Banco de dados não é mais ponto único de falha
- **Distribuição de carga**: Leituras distribuídas entre slaves
- **Alta disponibilidade**: Falha do Master não derruba o sistema
- **Performance**: Leituras mais rápidas com slaves dedicados

## Tipos de Replicação

### 1. Master-Slave (Read Replicas)
- **Master**: Apenas escritas (INSERT, UPDATE, DELETE)
- **Slaves**: Apenas leituras (SELECT)
- **Replicação**: Assíncrona do Master para Slaves

### 2. Master-Master
- Ambos servidores aceitam leitura e escrita
- Replicação bidirecional
- Maior complexidade de sincronização

### 3. Multi-Master
- Múltiplos masters
- Replicação em anel ou mesh
- Máxima disponibilidade

## Consistência Eventual

### O Problema
```javascript
// Cenário: Usuário insere dados e imediatamente consulta
async function createAndReadUser() {
  // 1. Inserir usuário (vai para Master)
  await createUser({ name: 'João', email: 'joao@email.com' });
  
  // 2. Consultar usuário (pode ir para Slave que ainda não replicou)
  const users = await getUsers(); // Pode não encontrar o usuário recém-criado
}
```

### Soluções

#### 1. Read-Your-Writes Consistency
```javascript
// Sempre ler do Master após escrita
async function createAndReadUser() {
  await createUser({ name: 'João', email: 'joao@email.com' });
  
  // Ler do Master para garantir consistência
  const users = await getUsersFromMaster();
}
```

## Métricas Melhoradas

| Métrica | Antes | Depois |
|---------|-------|--------|
| Usuários simultâneos | 5.000-15.000 | 15.000-50.000 |
| Requisições/segundo | 500-1.500 | 1.500-5.000 |
| Tempo de resposta (Read) | 100-200ms | 50-100ms |
| Tempo de resposta (Write) | 100-200ms | 100-200ms |
| Uptime | 99.5-99.9% | 99.9-99.99% |
