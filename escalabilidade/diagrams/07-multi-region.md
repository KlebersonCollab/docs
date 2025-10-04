# Diagrama - Multi-Region

## Arquitetura Multi-Region

```mermaid
graph TB
    subgraph "Global Load Balancer"
        GLB[Route 53 + CloudFront<br/>Global DNS + CDN]
    end
    
    subgraph "US East (N. Virginia)"
        subgraph "Load Balancer"
            LB1[Application Load Balancer]
        end
        
        subgraph "Auto Scaling Group"
            API1[API Server 1]
            API2[API Server 2]
            API3[API Server 3]
        end
        
        subgraph "Cache Layer"
            CACHE1[Redis Cluster]
        end
        
        subgraph "Database"
            DB1[(Database Master)]
            DBS1[(Database Slave)]
        end
    end
    
    subgraph "US West (Oregon)"
        subgraph "Load Balancer"
            LB2[Application Load Balancer]
        end
        
        subgraph "Auto Scaling Group"
            API4[API Server 1]
            API5[API Server 2]
            API6[API Server 3]
        end
        
        subgraph "Cache Layer"
            CACHE2[Redis Cluster]
        end
        
        subgraph "Database"
            DB2[(Database Read Replica)]
        end
    end
    
    subgraph "EU West (Ireland)"
        subgraph "Load Balancer"
            LB3[Application Load Balancer]
        end
        
        subgraph "Auto Scaling Group"
            API7[API Server 1]
            API8[API Server 2]
            API9[API Server 3]
        end
        
        subgraph "Cache Layer"
            CACHE3[Redis Cluster]
        end
        
        subgraph "Database"
            DB3[(Database Read Replica)]
        end
    end
    
    GLB --> LB1
    GLB --> LB2
    GLB --> LB3
    
    LB1 --> API1
    LB1 --> API2
    LB1 --> API3
    
    LB2 --> API4
    LB2 --> API5
    LB2 --> API6
    
    LB3 --> API7
    LB3 --> API8
    LB3 --> API9
    
    API1 --> CACHE1
    API2 --> CACHE1
    API3 --> CACHE1
    
    API4 --> CACHE2
    API5 --> CACHE2
    API6 --> CACHE2
    
    API7 --> CACHE3
    API8 --> CACHE3
    API9 --> CACHE3
    
    CACHE1 --> DB1
    CACHE1 --> DBS1
    
    CACHE2 --> DB2
    CACHE3 --> DB3
    
    DB1 -.->|Cross-Region Replication| DB2
    DB1 -.->|Cross-Region Replication| DB3
    
    CACHE1 -.->|Cross-Region Replication| CACHE2
    CACHE1 -.->|Cross-Region Replication| CACHE3
    
    classDef global fill:#e3f2fd
    classDef region fill:#f3e5f5
    classDef loadbalancer fill:#ffebee
    classDef server fill:#e8f5e8
    classDef cache fill:#e8eaf6
    classDef database fill:#fff3e0
    classDef replication fill:#f1f8e9
    
    class GLB global
    class LB1,LB2,LB3 loadbalancer
    class API1,API2,API3,API4,API5,API6,API7,API8,API9 server
    class CACHE1,CACHE2,CACHE3 cache
    class DB1,DB2,DB3,DBS1 database
```

## Estratégias de Multi-Region

### 1. Active-Passive (Hot Standby)
- Uma região ativa, outras em standby
- Failover manual ou automático
- Menor custo, maior RTO

### 2. Active-Active
- Múltiplas regiões ativas simultaneamente
- Distribuição de carga global
- Maior custo, menor RTO

### 3. Active-Active com Read Replicas
- Escrita em uma região, leitura em todas
- Balanceamento de leitura global
- Compromisso entre custo e performance

## Benefícios do Multi-Region

- **Disaster Recovery**: Continuidade mesmo com falhas regionais
- **Latência Global**: Usuários atendidos pela região mais próxima
- **Alta Disponibilidade**: 99.99%+ de uptime
- **Compliance**: Dados armazenados em regiões específicas

## Métricas Melhoradas

| Métrica | Antes | Depois |
|---------|-------|--------|
| Usuários simultâneos | 200.000-1.000.000+ | 1.000.000+ (global) |
| Latência média | 100-200ms | 50-100ms (por região) |
| Uptime | 99.99% | 99.999% |
| RTO (Recovery Time Objective) | 4-8 horas | 15-30 minutos |
| RPO (Recovery Point Objective) | 1-4 horas | 5-15 minutos |
