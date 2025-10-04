# Diagrama - Auto Scaling

## Arquitetura com Auto Scaling

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
    
    subgraph "Auto Scaling Group"
        subgraph "Application Servers"
            API1[API Server 1<br/>Backend Code]
            API2[API Server 2<br/>Backend Code]
            API3[API Server 3<br/>Backend Code]
            API4[API Server 4<br/>Backend Code]
            API5[API Server 5<br/>Backend Code]
        end
        
        subgraph "Scaling Policies"
            SP1[Scale Out<br/>CPU > 70%]
            SP2[Scale In<br/>CPU < 30%]
            SP3[Min: 2 instances]
            SP4[Max: 10 instances]
        end
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
    LB --> API4
    LB --> API5
    
    API1 --> CACHE1
    API1 --> CACHE2
    API1 --> CACHE3
    
    API2 --> CACHE1
    API2 --> CACHE2
    API2 --> CACHE3
    
    API3 --> CACHE1
    API3 --> CACHE2
    API3 --> CACHE3
    
    API4 --> CACHE1
    API4 --> CACHE2
    API4 --> CACHE3
    
    API5 --> CACHE1
    API5 --> CACHE2
    API5 --> CACHE3
    
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
    classDef scaling fill:#fce4ec
    classDef cache fill:#e8eaf6
    classDef database fill:#fff3e0
    
    class FE,MA client
    class DNS network
    class LB loadbalancer
    class API1,API2,API3,API4,API5 server
    class SP1,SP2,SP3,SP4 scaling
    class CACHE1,CACHE2,CACHE3 cache
    class DBM,DBS1,DBS2 database
```

## Tipos de Auto Scaling

### 1. Horizontal Scaling (Scale-Out/Scale-In)
- Adiciona/remove instâncias da aplicação
- Mais comum e eficaz
- Mantém performance individual

### 2. Vertical Scaling (Scale-Up/Scale-Down)
- Aumenta/diminui recursos da instância
- Menos comum em produção
- Pode causar downtime

## Configuração Auto Scaling

### Launch Template
```yaml
LaunchTemplate:
  ImageId: ami-0c02fb55956c7d316
  InstanceType: t3.medium
  SecurityGroupIds: [sg-12345678]
  UserData: |
    #!/bin/bash
    yum update -y
    yum install -y nodejs
    systemctl enable nodejs
    systemctl start nodejs
```

### Scaling Policies
```yaml
ScalingPolicies:
  ScaleOut:
    MetricName: CPUUtilization
    Threshold: 70
    ComparisonOperator: GreaterThanThreshold
    EvaluationPeriods: 2
    ScalingAdjustment: 1
    AdjustmentType: ChangeInCapacity
  
  ScaleIn:
    MetricName: CPUUtilization
    Threshold: 30
    ComparisonOperator: LessThanThreshold
    EvaluationPeriods: 2
    ScalingAdjustment: -1
    AdjustmentType: ChangeInCapacity
```

## Benefícios do Auto Scaling

- **Elasticidade**: Adaptação automática à demanda
- **Economia**: Paga apenas pelos recursos utilizados
- **Alta disponibilidade**: Redundância automática
- **Performance**: Mantém performance mesmo com picos de tráfego

## Métricas Melhoradas

| Métrica | Antes | Depois |
|---------|-------|--------|
| Usuários simultâneos | 50.000-200.000 | 200.000-1.000.000+ |
| Requisições/segundo | 5.000-20.000 | 20.000-100.000+ |
| Tempo de resposta | 10-50ms | 10-50ms (consistente) |
| Uptime | 99.9-99.99% | 99.99-99.999% |
| Custo | Fixo | Variável (paga pelo uso) |
