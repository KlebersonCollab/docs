# Diagrama - Separação de Servidores

## Arquitetura com Servidores Separados

```mermaid
graph TB
    subgraph "Client Layer"
        FE[Frontend<br/>React/Angular]
        MA[Mobile App<br/>iOS/Android]
    end
    
    subgraph "Network Layer"
        DNS[DNS<br/>api.meuapp.com]
    end
    
    subgraph "Application Server"
        API[API Server<br/>Backend Code]
    end
    
    subgraph "Database Server"
        DB[(Database<br/>MySQL/PostgreSQL)]
    end
    
    FE --> DNS
    MA --> DNS
    DNS --> API
    API --> DB
    
    classDef client fill:#e1f5fe
    classDef network fill:#f3e5f5
    classDef server fill:#e8f5e8
    classDef database fill:#fff3e0
    
    class FE,MA client
    class DNS network
    class API server
    class DB database
```

## Benefícios Alcançados

- **Recursos dedicados**: API e DB têm recursos próprios
- **Dimensionamento independente**: Pode escalar cada componente separadamente
- **Manutenção isolada**: Pode reiniciar um sem afetar o outro
- **Performance melhorada**: Sem competição por recursos

## Limitações Mantidas

- **Ponto único de falha**: Ainda existe SPOF
- **Escalabilidade limitada**: Não resolve problemas de alta disponibilidade
- **Sem redundância**: Falha de qualquer servidor derruba o sistema

## Métricas Melhoradas

| Métrica | Antes | Depois |
|---------|-------|--------|
| Usuários simultâneos | 100-1.000 | 1.000-5.000 |
| Requisições/segundo | 10-100 | 100-500 |
| Tempo de resposta | 200-500ms | 150-300ms |
| Uptime | 95-99% | 98-99% |
| Capacidade de crescimento | Muito limitada | Moderada |
