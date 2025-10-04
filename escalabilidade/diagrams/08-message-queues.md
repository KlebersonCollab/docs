# Diagrama - Message Queues

## Arquitetura com Message Queues

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
    
    subgraph "Message Queue Layer"
        MQ1[Message Queue 1<br/>SQS/RabbitMQ/Kafka]
        MQ2[Message Queue 2<br/>SQS/RabbitMQ/Kafka]
        MQ3[Message Queue 3<br/>SQS/RabbitMQ/Kafka]
    end
    
    subgraph "Worker Servers"
        W1[Worker Server 1<br/>Background Processing]
        W2[Worker Server 2<br/>Background Processing]
        W3[Worker Server 3<br/>Background Processing]
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
    
    API1 --> MQ1
    API1 --> MQ2
    API1 --> MQ3
    
    API2 --> MQ1
    API2 --> MQ2
    API2 --> MQ3
    
    API3 --> MQ1
    API3 --> MQ2
    API3 --> MQ3
    
    MQ1 --> W1
    MQ2 --> W2
    MQ3 --> W3
    
    W1 --> CACHE1
    W1 --> CACHE2
    W1 --> CACHE3
    
    W2 --> CACHE1
    W2 --> CACHE2
    W2 --> CACHE3
    
    W3 --> CACHE1
    W3 --> CACHE2
    W3 --> CACHE3
    
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
    classDef queue fill:#e0f2f1
    classDef worker fill:#fff8e1
    classDef cache fill:#e8eaf6
    classDef database fill:#fff3e0
    
    class FE,MA client
    class DNS network
    class LB loadbalancer
    class API1,API2,API3 server
    class MQ1,MQ2,MQ3 queue
    class W1,W2,W3 worker
    class CACHE1,CACHE2,CACHE3 cache
    class DBM,DBS1,DBS2 database
```

## Tipos de Message Queues

### 1. Point-to-Point (Fila)
- Uma mensagem para um consumidor
- Ordem garantida
- Exemplo: SQS, RabbitMQ

### 2. Publish-Subscribe (Tópico)
- Uma mensagem para múltiplos consumidores
- Broadcasting
- Exemplo: SNS, Apache Kafka

### 3. Request-Reply
- Padrão síncrono com queue
- RPC over message queue
- Exemplo: RabbitMQ RPC

## Padrões de Processamento

### 1. Fan-Out Pattern
```javascript
// Um produtor, múltiplos consumidores
class FanOutProducer {
  async publishToMultipleQueues(message) {
    const queues = ['email-queue', 'sms-queue', 'push-queue'];
    
    const promises = queues.map(queue => 
      this.publishToQueue(queue, message)
    );
    
    await Promise.all(promises);
  }
}
```

### 2. Work Queue Pattern
```javascript
// Distribuição de trabalho entre workers
class WorkQueue {
  async distributeWork(tasks) {
    for (const task of tasks) {
      await this.publishToQueue('work-queue', task);
    }
  }
}
```

### 3. Request-Reply Pattern
```javascript
class RequestReply {
  async sendRequest(request) {
    const correlationId = this.generateCorrelationId();
    const replyQueue = `reply-${correlationId}`;
    
    // Criar queue temporária para resposta
    await this.createTempQueue(replyQueue);
    
    // Enviar requisição
    await this.publishToQueue('request-queue', {
      ...request,
      correlationId,
      replyTo: replyQueue
    });
    
    // Aguardar resposta
    return this.waitForReply(replyQueue, correlationId);
  }
}
```

## Benefícios das Message Queues

- **Responsividade**: API responde imediatamente
- **Escalabilidade**: Processamento distribuído
- **Resiliência**: Falhas não afetam a API
- **Throughput**: Maior capacidade de processamento

## Métricas Melhoradas

| Métrica | Antes | Depois |
|---------|-------|--------|
| Tempo de resposta da API | 200-500ms | 50-100ms |
| Throughput | 1.000-5.000 req/s | 5.000-20.000 req/s |
| Processamento assíncrono | 0% | 80-90% |
| Disponibilidade | 99.9% | 99.99% |
| Capacidade de picos | Limitada | Ilimitada |
