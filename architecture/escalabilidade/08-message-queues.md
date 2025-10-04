# Message Queues - Processamento Assíncrono

## Visão Geral

As Message Queues permitem processamento assíncrono de tarefas pesadas, melhorando a responsividade da aplicação e permitindo maior escalabilidade.

## Arquitetura com Message Queues

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Mobile App   │
│   (React/Angular)│    │   (iOS/Android)│
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
│Server │        │Server │        │Server │
└───────┘        └───────┘        └───────┘
    │                │                │
    └────────────────┼────────────────┘
                     │
         ┌─────────────────┐
         │ Message Queue   │
         │ (SQS/RabbitMQ/  │
         │  Apache Kafka)  │
         └─────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐        ┌───▼───┐        ┌───▼───┐
│Worker-1│        │Worker-2│        │Worker-3│
│Server │        │Server │        │Server │
└───────┘        └───────┘        └───────┘
    │                │                │
    └────────────────┼────────────────┘
                     │
         ┌─────────────────┐
         │   Database      │
         │   (Master-Slave)│
         └─────────────────┘
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

## Implementação com AWS SQS

### Configuração SQS
```yaml
# Dead Letter Queue
DeadLetterQueue:
  Type: AWS::SQS::Queue
  Properties:
    QueueName: myapp-dlq
    MessageRetentionPeriod: 1209600 # 14 days
    VisibilityTimeoutSeconds: 30

# Main Queue
MainQueue:
  Type: AWS::SQS::Queue
  Properties:
    QueueName: myapp-queue
    VisibilityTimeoutSeconds: 300
    MessageRetentionPeriod: 1209600
    RedrivePolicy:
      deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
      maxReceiveCount: 3
    DelaySeconds: 0
    ReceiveMessageWaitTimeSeconds: 20 # Long polling

# Priority Queue
PriorityQueue:
  Type: AWS::SQS::Queue
  Properties:
    QueueName: myapp-priority-queue
    VisibilityTimeoutSeconds: 300
    MessageRetentionPeriod: 1209600
    DelaySeconds: 0
```

### Enviando Mensagens
```javascript
const AWS = require('aws-sdk');
const sqs = new AWS.SQS({ region: 'us-east-1' });

class MessageProducer {
  constructor() {
    this.queueUrl = process.env.SQS_QUEUE_URL;
    this.priorityQueueUrl = process.env.SQS_PRIORITY_QUEUE_URL;
  }

  async sendMessage(message, options = {}) {
    const { priority = 'normal', delay = 0 } = options;
    
    const params = {
      QueueUrl: priority === 'high' ? this.priorityQueueUrl : this.queueUrl,
      MessageBody: JSON.stringify(message),
      DelaySeconds: delay,
      MessageAttributes: {
        Priority: {
          DataType: 'String',
          StringValue: priority
        },
        Timestamp: {
          DataType: 'Number',
          StringValue: Date.now().toString()
        }
      }
    };

    try {
      const result = await sqs.sendMessage(params).promise();
      console.log('Message sent:', result.MessageId);
      return result;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async sendBatch(messages, options = {}) {
    const { priority = 'normal' } = options;
    const queueUrl = priority === 'high' ? this.priorityQueueUrl : this.queueUrl;
    
    const entries = messages.map((message, index) => ({
      Id: index.toString(),
      MessageBody: JSON.stringify(message),
      MessageAttributes: {
        Priority: {
          DataType: 'String',
          StringValue: priority
        }
      }
    }));

    const params = {
      QueueUrl: queueUrl,
      Entries: entries
    };

    try {
      const result = await sqs.sendMessageBatch(params).promise();
      console.log('Batch sent:', result.Successful.length, 'messages');
      return result;
    } catch (error) {
      console.error('Error sending batch:', error);
      throw error;
    }
  }
}
```

### Consumindo Mensagens
```javascript
class MessageConsumer {
  constructor() {
    this.queueUrl = process.env.SQS_QUEUE_URL;
    this.isProcessing = false;
  }

  async start() {
    console.log('Starting message consumer...');
    this.isProcessing = true;
    
    while (this.isProcessing) {
      try {
        const messages = await this.receiveMessages();
        
        if (messages.length > 0) {
          await this.processMessages(messages);
        } else {
          // Long polling - aguardar mensagens
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
      } catch (error) {
        console.error('Consumer error:', error);
        await new Promise(resolve => setTimeout(resolve, 5000));
      }
    }
  }

  async receiveMessages() {
    const params = {
      QueueUrl: this.queueUrl,
      MaxNumberOfMessages: 10,
      WaitTimeSeconds: 20, // Long polling
      MessageAttributeNames: ['All']
    };

    const result = await sqs.receiveMessage(params).promise();
    return result.Messages || [];
  }

  async processMessages(messages) {
    const promises = messages.map(message => this.processMessage(message));
    await Promise.allSettled(promises);
  }

  async processMessage(message) {
    try {
      const body = JSON.parse(message.Body);
      console.log('Processing message:', body);

      // Processar mensagem baseada no tipo
      switch (body.type) {
        case 'email':
          await this.processEmail(body.data);
          break;
        case 'report':
          await this.processReport(body.data);
          break;
        case 'image':
          await this.processImage(body.data);
          break;
        default:
          console.log('Unknown message type:', body.type);
      }

      // Remover mensagem da fila após processamento
      await this.deleteMessage(message.ReceiptHandle);
      
    } catch (error) {
      console.error('Error processing message:', error);
      // Mensagem será reprocessada ou enviada para DLQ
    }
  }

  async deleteMessage(receiptHandle) {
    const params = {
      QueueUrl: this.queueUrl,
      ReceiptHandle: receiptHandle
    };

    await sqs.deleteMessage(params).promise();
  }

  async stop() {
    console.log('Stopping message consumer...');
    this.isProcessing = false;
  }
}
```

## Implementação com RabbitMQ

### Configuração RabbitMQ
```javascript
const amqp = require('amqplib');

class RabbitMQManager {
  constructor() {
    this.connection = null;
    this.channel = null;
  }

  async connect() {
    this.connection = await amqp.connect('amqp://localhost');
    this.channel = await this.connection.createChannel();
    
    // Configurar exchanges e queues
    await this.setupQueues();
  }

  async setupQueues() {
    // Exchange para emails
    await this.channel.assertExchange('email-exchange', 'direct', {
      durable: true
    });

    // Exchange para relatórios
    await this.channel.assertExchange('report-exchange', 'direct', {
      durable: true
    });

    // Queue para emails
    await this.channel.assertQueue('email-queue', {
      durable: true
    });

    // Queue para relatórios
    await this.channel.assertQueue('report-queue', {
      durable: true
    });

    // Bindings
    await this.channel.bindQueue('email-queue', 'email-exchange', 'email');
    await this.channel.bindQueue('report-queue', 'report-exchange', 'report');
  }

  async publish(exchange, routingKey, message) {
    const messageBuffer = Buffer.from(JSON.stringify(message));
    
    await this.channel.publish(exchange, routingKey, messageBuffer, {
      persistent: true,
      timestamp: Date.now()
    });
  }

  async consume(queue, callback) {
    await this.channel.consume(queue, async (msg) => {
      if (msg) {
        try {
          const message = JSON.parse(msg.content.toString());
          await callback(message);
          this.channel.ack(msg);
        } catch (error) {
          console.error('Error processing message:', error);
          this.channel.nack(msg, false, false); // Rejeitar e não reenviar
        }
      }
    });
  }
}
```

### Producer com RabbitMQ
```javascript
class EmailProducer {
  constructor(rabbitMQ) {
    this.rabbitMQ = rabbitMQ;
  }

  async sendEmail(emailData) {
    const message = {
      type: 'email',
      data: emailData,
      timestamp: Date.now(),
      retryCount: 0
    };

    await this.rabbitMQ.publish('email-exchange', 'email', message);
    console.log('Email message sent:', emailData.to);
  }

  async sendBulkEmails(emails) {
    const promises = emails.map(email => this.sendEmail(email));
    await Promise.all(promises);
  }
}
```

### Consumer com RabbitMQ
```javascript
class EmailConsumer {
  constructor(rabbitMQ) {
    this.rabbitMQ = rabbitMQ;
  }

  async start() {
    await this.rabbitMQ.consume('email-queue', async (message) => {
      await this.processEmail(message);
    });
  }

  async processEmail(message) {
    const { data } = message;
    
    try {
      // Simular envio de email
      await this.sendEmail(data);
      console.log('Email sent successfully:', data.to);
    } catch (error) {
      console.error('Error sending email:', error);
      throw error;
    }
  }

  async sendEmail(emailData) {
    // Implementar envio real de email
    const { to, subject, body } = emailData;
    
    // Simular delay de envio
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    console.log(`Email sent to ${to}: ${subject}`);
  }
}
```

## Implementação com Apache Kafka

### Configuração Kafka
```javascript
const kafka = require('kafkajs');

const kafkaClient = kafka({
  clientId: 'myapp-producer',
  brokers: ['localhost:9092']
});

const producer = kafkaClient.producer();
const consumer = kafkaClient.consumer({ groupId: 'myapp-group' });

class KafkaManager {
  async connect() {
    await producer.connect();
    await consumer.connect();
    
    // Subscrever tópicos
    await consumer.subscribe({ topic: 'emails', fromBeginning: false });
    await consumer.subscribe({ topic: 'reports', fromBeginning: false });
  }

  async produce(topic, message) {
    await producer.send({
      topic,
      messages: [{
        key: message.id || Date.now().toString(),
        value: JSON.stringify(message),
        timestamp: Date.now().toString()
      }]
    });
  }

  async consume(callback) {
    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const messageData = JSON.parse(message.value.toString());
        await callback(topic, messageData);
      }
    });
  }
}
```

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

## Monitoramento de Message Queues

### Métricas SQS
```javascript
const cloudwatch = new AWS.CloudWatch();

class SQSMonitor {
  async getQueueMetrics(queueName) {
    const params = {
      Namespace: 'AWS/SQS',
      MetricName: 'ApproximateNumberOfMessages',
      Dimensions: [
        { Name: 'QueueName', Value: queueName }
      ],
      StartTime: new Date(Date.now() - 3600000), // 1 hora atrás
      EndTime: new Date(),
      Period: 300,
      Statistics: ['Average']
    };

    const result = await cloudwatch.getMetricStatistics(params).promise();
    return result.Datapoints;
  }

  async getDLQMetrics() {
    const params = {
      Namespace: 'AWS/SQS',
      MetricName: 'ApproximateNumberOfMessagesVisible',
      Dimensions: [
        { Name: 'QueueName', Value: 'myapp-dlq' }
      ],
      StartTime: new Date(Date.now() - 3600000),
      EndTime: new Date(),
      Period: 300,
      Statistics: ['Average']
    };

    return await cloudwatch.getMetricStatistics(params).promise();
  }
}
```

### Health Check
```javascript
app.get('/health/queue', async (req, res) => {
  try {
    const queueAttributes = await sqs.getQueueAttributes({
      QueueUrl: process.env.SQS_QUEUE_URL,
      AttributeNames: ['ApproximateNumberOfMessages']
    }).promise();

    const messageCount = parseInt(
      queueAttributes.Attributes.ApproximateNumberOfMessages
    );

    if (messageCount > 1000) {
      res.status(503).json({
        status: 'Warning',
        message: 'Queue backlog is high',
        messageCount
      });
    } else {
      res.json({
        status: 'OK',
        messageCount
      });
    }
  } catch (error) {
    res.status(503).json({
      status: 'Error',
      message: 'Queue health check failed'
    });
  }
});
```

## Benefícios Alcançados

### ✅ Melhorias
- **Responsividade**: API responde imediatamente
- **Escalabilidade**: Processamento distribuído
- **Resiliência**: Falhas não afetam a API
- **Throughput**: Maior capacidade de processamento

### 📊 Métricas Melhoradas
| Métrica | Antes | Depois |
|---------|-------|--------|
| Tempo de resposta da API | 200-500ms | 50-100ms |
| Throughput | 1.000-5.000 req/s | 5.000-20.000 req/s |
| Processamento assíncrono | 0% | 80-90% |
| Disponibilidade | 99.9% | 99.99% |
| Capacidade de picos | Limitada | Ilimitada |

## Considerações Importantes

### 1. Message Ordering
```javascript
// Garantir ordem das mensagens
class OrderedMessageProcessor {
  async processOrderedMessages(messages) {
    // Ordenar por timestamp
    const sortedMessages = messages.sort((a, b) => 
      a.timestamp - b.timestamp
    );
    
    for (const message of sortedMessages) {
      await this.processMessage(message);
    }
  }
}
```

### 2. Dead Letter Queue
```javascript
// Configurar DLQ para mensagens com falha
const dlqConfig = {
  deadLetterTargetArn: 'arn:aws:sqs:us-east-1:123456789012:myapp-dlq',
  maxReceiveCount: 3
};
```

### 3. Message Deduplication
```javascript
// Evitar processamento duplicado
class DeduplicationManager {
  constructor() {
    this.processedMessages = new Set();
  }

  async processMessage(message) {
    const messageId = message.id || this.generateMessageId(message);
    
    if (this.processedMessages.has(messageId)) {
      console.log('Duplicate message ignored:', messageId);
      return;
    }
    
    this.processedMessages.add(messageId);
    await this.processMessageContent(message);
  }
}
```

## Próximos Passos

Para continuar a evolução:

1. **Implementar CDN** para conteúdo estático
2. **Adicionar Database Sharding** para bancos muito grandes
3. **Configurar Microserviços** para maior modularidade
4. **Implementar Event Sourcing** para auditoria completa

## Checklist de Implementação

- [ ] Configurar Message Queue (SQS/RabbitMQ/Kafka)
- [ ] Implementar producers e consumers
- [ ] Configurar Dead Letter Queue
- [ ] Implementar retry logic
- [ ] Configurar monitoramento de filas
- [ ] Implementar health checks
- [ ] Configurar alertas de backlog
- [ ] Testar processamento assíncrono
- [ ] Documentar padrões de mensageria
- [ ] Treinar equipe em troubleshooting de filas
