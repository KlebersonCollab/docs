# Diagrama - Load Balancing

## Arquitetura com Load Balancer

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
    
    subgraph "Database Server"
        DB[(Database<br/>MySQL/PostgreSQL)]
    end
    
    FE --> DNS
    MA --> DNS
    DNS --> LB
    LB --> API1
    LB --> API2
    LB --> API3
    API1 --> DB
    API2 --> DB
    API3 --> DB
    
    classDef client fill:#e1f5fe
    classDef network fill:#f3e5f5
    classDef loadbalancer fill:#ffebee
    classDef server fill:#e8f5e8
    classDef database fill:#fff3e0
    
    class FE,MA client
    class DNS network
    class LB loadbalancer
    class API1,API2,API3 server
    class DB database
```

## Benefícios do Load Balancing

- **Alta disponibilidade**: Falha de um servidor não derruba o sistema
- **Escalabilidade horizontal**: Pode adicionar mais servidores conforme necessário
- **Distribuição de carga**: Requisições distribuídas uniformemente
- **Failover automático**: Servidores com falha são removidos automaticamente

## Tipos de Load Balancing

### 1. Round Robin
- Distribui requisições sequencialmente
- Mais simples de implementar
- Não considera carga dos servidores

### 2. Least Connections
- Direciona para servidor com menos conexões ativas
- Melhor para conexões de longa duração
- Considera estado atual dos servidores

### 3. Weighted Round Robin
- Permite pesos diferentes para servidores
- Útil para servidores com capacidades diferentes
- Flexibilidade na distribuição

## Métricas Melhoradas

| Métrica | Antes | Depois |
|---------|-------|--------|
| Usuários simultâneos | 1.000-5.000 | 5.000-15.000 |
| Requisições/segundo | 100-500 | 500-1.500 |
| Tempo de resposta | 150-300ms | 100-200ms |
| Uptime | 98-99% | 99.5-99.9% |
| Capacidade de crescimento | Moderada | Alta |
