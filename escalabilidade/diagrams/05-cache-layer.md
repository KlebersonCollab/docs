# Diagrama - Cache Layer

## Arquitetura com Cache Layer

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
    
    subgraph "Cache Layer"
        CACHE1[Redis Cache 1<br/>In-Memory Storage]
        CACHE2[Redis Cache 2<br/>In-Memory Storage]
        CACHE3[Redis Cache 3<br/>In-Memory Storage]
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
    
    API1 --> CACHE1
    API1 --> CACHE2
    API1 --> CACHE3
    
    API2 --> CACHE1
    API2 --> CACHE2
    API2 --> CACHE3
    
    API3 --> CACHE1
    API3 --> CACHE2
    API3 --> CACHE3
    
    CACHE1 --> DBM
    CACHE1 --> DBS1
    CACHE1 --> DBS2
    
    CACHE2 --> DBM
    CACHE2 --> DBS1
    CACHE2 --> DBS2
    
    CACHE3 --> DBM
    CACHE3 --> DBS1
    CACHE3 --> DBS2
    
    DBM -.->|Replication| DBS1
    DBM -.->|Replication| DBS2
    
    classDef client fill:#e1f5fe
    classDef network fill:#f3e5f5
    classDef loadbalancer fill:#ffebee
    classDef server fill:#e8f5e8
    classDef cache fill:#e8eaf6
    classDef database fill:#fff3e0
    
    class FE,MA client
    class DNS network
    class LB loadbalancer
    class API1,API2,API3 server
    class CACHE1,CACHE2,CACHE3 cache
    class DBM,DBS1,DBS2 database
```

## Padrões de Cache

### 1. Cache-Aside (Lazy Loading)
```javascript
async function getUser(id) {
  // 1. Verificar cache primeiro
  let user = await redis.get(`user:${id}`);
  
  if (user) {
    return JSON.parse(user);
  }
  
  // 2. Se não estiver no cache, buscar no banco
  user = await db.query('SELECT * FROM users WHERE id = ?', [id]);
  
  // 3. Armazenar no cache para próximas consultas
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  
  return user;
}
```

### 2. Write-Through
```javascript
async function createUser(userData) {
  // 1. Escrever no banco
  const user = await db.query(
    'INSERT INTO users (name, email) VALUES (?, ?)',
    [userData.name, userData.email]
  );
  
  // 2. Escrever no cache imediatamente
  await redis.setex(
    `user:${user.id}`, 
    3600, 
    JSON.stringify(user)
  );
  
  return user;
}
```

### 3. Write-Behind (Write-Back)
```javascript
async function updateUser(id, userData) {
  // 1. Atualizar cache imediatamente
  await redis.setex(
    `user:${id}`, 
    3600, 
    JSON.stringify(userData)
  );
  
  // 2. Agendar escrita no banco (assíncrona)
  scheduleDatabaseUpdate(id, userData);
  
  return userData;
}
```

## Benefícios do Cache

- **Performance**: Redução drástica no tempo de resposta
- **Redução de carga**: Menos consultas ao banco de dados
- **Escalabilidade**: Suporte a mais usuários simultâneos
- **Economia**: Menos recursos de banco necessários

## Métricas Melhoradas

| Métrica | Antes | Depois |
|---------|-------|--------|
| Usuários simultâneos | 15.000-50.000 | 50.000-200.000 |
| Requisições/segundo | 1.500-5.000 | 5.000-20.000 |
| Tempo de resposta (Cache Hit) | 100-200ms | 10-50ms |
| Tempo de resposta (Cache Miss) | 100-200ms | 100-200ms |
| Hit Rate | 0% | 80-95% |
| Carga no banco | 100% | 20-50% |
