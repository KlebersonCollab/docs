# Diagrama - Arquitetura Inicial

## Arquitetura Monolítica Básica

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

## Características da Arquitetura Inicial

- **Simplicidade**: Fácil de desenvolver e deployar
- **Custo baixo**: Apenas um servidor necessário
- **Ponto único de falha**: Se o servidor falha, tudo para
- **Competição por recursos**: API e DB competem por CPU/RAM
- **Escalabilidade limitada**: Não consegue crescer horizontalmente

## Limitações

| Aspecto | Limitação |
|---------|-----------|
| Usuários simultâneos | 100-1.000 |
| Requisições/segundo | 10-100 |
| Tempo de resposta | 200-500ms |
| Uptime | 95-99% |
| Capacidade de crescimento | Muito limitada |
