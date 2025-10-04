# Multi-Region - Disaster Recovery e Alta Disponibilidade

## Visão Geral

A implementação de arquitetura multi-região elimina o ponto único de falha a nível de data center, garantindo continuidade de negócio mesmo em caso de desastres naturais ou falhas regionais.

## Arquitetura Multi-Region

```
                    ┌─────────────────────────────────────┐
                    │           Global Load Balancer       │
                    │         (Route 53 + CloudFront)     │
                    └─────────────────────────────────────┘
                                      │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
         ┌─────────▼─────────┐ ┌───────▼───────┐ ┌────────▼────────┐
         │   US East (N. Virginia) │   US West (Oregon) │   EU West (Ireland) │
         │                        │                    │                    │
         │ ┌─────────────────────┐│┌─────────────────────┐│┌─────────────────────┐│
         │ │   Load Balancer     │││   Load Balancer     │││   Load Balancer     ││
         │ │   (ALB)             │││   (ALB)             │││   (ALB)             ││
         │ └─────────────────────┘│└─────────────────────┘│└─────────────────────┘│
         │           │           │           │           │           │           │
         │ ┌─────────▼─────────┐ │ ┌─────────▼─────────┐ │ ┌─────────▼─────────┐ │
         │ │   Auto Scaling    │ │ │   Auto Scaling    │ │ │   Auto Scaling    │ │
         │ │   Group (2-10)    │ │ │   Group (2-10)    │ │ │   Group (2-10)    │ │
         │ └───────────────────┘ │ └───────────────────┘ │ └───────────────────┘ │
         │           │           │           │           │           │           │
         │ ┌─────────▼─────────┐ │ ┌─────────▼─────────┐ │ ┌─────────▼─────────┐ │
         │ │   API Servers     │ │ │   API Servers     │ │ │   API Servers     │ │
         │ │   (3-10 instances)│ │ │   (3-10 instances)│ │ │   (3-10 instances)│ │
         │ └───────────────────┘ │ └───────────────────┘ │ └───────────────────┘ │
         │           │           │           │           │           │           │
         │ ┌─────────▼─────────┐ │ ┌─────────▼─────────┐ │ ┌─────────▼─────────┐ │
         │ │   Redis Cluster   │ │ │   Redis Cluster   │ │ │   Redis Cluster   │ │
         │ │   (3-6 nodes)     │ │ │   (3-6 nodes)     │ │ │   (3-6 nodes)     │ │
         │ └───────────────────┘ │ └───────────────────┘ │ └───────────────────┘ │
         │           │           │           │           │           │           │
         │ ┌─────────▼─────────┐ │ ┌─────────▼─────────┐ │ ┌─────────▼─────────┐ │
         │ │   Database        │ │ │   Database        │ │ │   Database        │ │
         │ │   Master-Slave    │ │ │   Master-Slave    │ │ │   Master-Slave    │ │
         │ └───────────────────┘ │ └───────────────────┘ │ └───────────────────┘ │
         └───────────────────────┘ └─────────────────────┘ └─────────────────────┘
                    │                        │                        │
                    └────────────────────────┼────────────────────────┘
                                             │
                    ┌────────────────────────▼────────────────────────┐
                    │           Cross-Region Replication              │
                    │         (Database + Cache + Storage)            │
                    └─────────────────────────────────────────────────┘
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

## Implementação AWS Multi-Region

### Route 53 Configuration
```yaml
# DNS Configuration
api.example.com:
  type: A
  alias: true
  target: d1234567890.cloudfront.net
  
# Health checks
health-check-us-east:
  type: HTTP
  resource_path: /health
  port: 443
  protocol: HTTPS
  failure_threshold: 3
  request_interval: 30
  
health-check-us-west:
  type: HTTP
  resource_path: /health
  port: 443
  protocol: HTTPS
  failure_threshold: 3
  request_interval: 30
```

### CloudFront Distribution
```yaml
CloudFrontDistribution:
  Type: AWS::CloudFront::Distribution
  Properties:
    DistributionConfig:
      Origins:
        - Id: us-east-origin
          DomainName: api-us-east.example.com
          CustomOriginConfig:
            HTTPPort: 443
            HTTPSPort: 443
            OriginProtocolPolicy: https-only
        - Id: us-west-origin
          DomainName: api-us-west.example.com
          CustomOriginConfig:
            HTTPPort: 443
            HTTPSPort: 443
            OriginProtocolPolicy: https-only
      DefaultCacheBehavior:
        TargetOriginId: us-east-origin
        ViewerProtocolPolicy: redirect-to-https
        CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad
      CacheBehaviors:
        - PathPattern: /api/*
          TargetOriginId: us-east-origin
          ViewerProtocolPolicy: redirect-to-https
          CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad
      PriceClass: PriceClass_All
      Enabled: true
```

## Database Cross-Region Replication

### RDS Cross-Region Read Replica
```yaml
# Primary Database (US East)
PrimaryDB:
  Type: AWS::RDS::DBInstance
  Properties:
    DBInstanceIdentifier: primary-db
    Engine: MySQL
    EngineVersion: '8.0'
    DBInstanceClass: db.r5.large
    AllocatedStorage: 100
    MasterUsername: admin
    MasterUserPassword: !Ref DatabasePassword
    MultiAZ: true
    BackupRetentionPeriod: 7
    PreferredBackupWindow: '03:00-04:00'
    PreferredMaintenanceWindow: 'sun:04:00-sun:05:00'

# Read Replica (US West)
ReadReplicaUSWest:
  Type: AWS::RDS::DBInstance
  Properties:
    DBInstanceIdentifier: read-replica-us-west
    SourceDBInstanceIdentifier: !Ref PrimaryDB
    DBInstanceClass: db.r5.large
    MultiAZ: false

# Read Replica (EU West)
ReadReplicaEUWest:
  Type: AWS::RDS::DBInstance
  Properties:
    DBInstanceIdentifier: read-replica-eu-west
    SourceDBInstanceIdentifier: !Ref PrimaryDB
    DBInstanceClass: db.r5.large
    MultiAZ: false
```

### DynamoDB Global Tables
```yaml
GlobalTable:
  Type: AWS::DynamoDB::GlobalTable
  Properties:
    TableName: myapp-table
    AttributeDefinitions:
      - AttributeName: id
        AttributeType: S
    KeySchema:
      - AttributeName: id
        KeyType: HASH
    BillingMode: PAY_PER_REQUEST
    Replicas:
      - Region: us-east-1
      - Region: us-west-2
      - Region: eu-west-1
```

## Cache Cross-Region Replication

### ElastiCache Global Datastore
```yaml
# Primary Cluster (US East)
PrimaryRedisCluster:
  Type: AWS::ElastiCache::ReplicationGroup
  Properties:
    ReplicationGroupId: primary-redis
    Description: Primary Redis cluster
    NodeType: cache.r5.large
    NumCacheClusters: 3
    Engine: redis
    EngineVersion: '6.x'
    Port: 6379
    GlobalReplicationGroupId: !Ref GlobalReplicationGroup

# Global Replication Group
GlobalReplicationGroup:
  Type: AWS::ElastiCache::GlobalReplicationGroup
  Properties:
    GlobalReplicationGroupId: myapp-global-redis
    Description: Global Redis replication group
    PrimaryReplicationGroupId: !Ref PrimaryRedisCluster
    GlobalReplicationGroupDescription: Global Redis for myapp
```

## Application Configuration

### Region-Aware Configuration
```javascript
const config = {
  regions: {
    'us-east-1': {
      database: {
        host: 'primary-db.us-east-1.rds.amazonaws.com',
        port: 3306,
        readReplicas: [
          'read-replica-1.us-east-1.rds.amazonaws.com'
        ]
      },
      redis: {
        host: 'primary-redis.us-east-1.cache.amazonaws.com',
        port: 6379
      },
      s3: {
        bucket: 'myapp-assets-us-east-1',
        region: 'us-east-1'
      }
    },
    'us-west-2': {
      database: {
        host: 'read-replica-us-west.us-west-2.rds.amazonaws.com',
        port: 3306,
        readOnly: true
      },
      redis: {
        host: 'global-redis.us-west-2.cache.amazonaws.com',
        port: 6379
      },
      s3: {
        bucket: 'myapp-assets-us-west-2',
        region: 'us-west-2'
      }
    },
    'eu-west-1': {
      database: {
        host: 'read-replica-eu-west.eu-west-1.rds.amazonaws.com',
        port: 3306,
        readOnly: true
      },
      redis: {
        host: 'global-redis.eu-west-1.cache.amazonaws.com',
        port: 6379
      },
      s3: {
        bucket: 'myapp-assets-eu-west-1',
        region: 'eu-west-1'
      }
    }
  }
};

// Detectar região atual
const currentRegion = process.env.AWS_REGION || 'us-east-1';
const regionConfig = config.regions[currentRegion];

// Configurar conexões baseadas na região
const dbConfig = regionConfig.database;
const redisConfig = regionConfig.redis;
const s3Config = regionConfig.s3;
```

### Database Connection with Region Awareness
```javascript
class DatabaseManager {
  constructor() {
    this.region = process.env.AWS_REGION || 'us-east-1';
    this.config = this.getRegionConfig();
    this.writeConnection = this.createWriteConnection();
    this.readConnections = this.createReadConnections();
  }

  getRegionConfig() {
    const configs = {
      'us-east-1': {
        write: 'primary-db.us-east-1.rds.amazonaws.com',
        reads: ['read-replica-1.us-east-1.rds.amazonaws.com']
      },
      'us-west-2': {
        write: 'primary-db.us-east-1.rds.amazonaws.com', // Cross-region write
        reads: ['read-replica-us-west.us-west-2.rds.amazonaws.com']
      },
      'eu-west-1': {
        write: 'primary-db.us-east-1.rds.amazonaws.com', // Cross-region write
        reads: ['read-replica-eu-west.eu-west-1.rds.amazonaws.com']
      }
    };
    
    return configs[this.region];
  }

  createWriteConnection() {
    // Sempre escrever na região primária
    return mysql.createConnection({
      host: 'primary-db.us-east-1.rds.amazonaws.com',
      user: 'app_user',
      password: process.env.DB_PASSWORD,
      database: 'myapp'
    });
  }

  createReadConnections() {
    return this.config.reads.map(host => 
      mysql.createConnection({
        host,
        user: 'app_user',
        password: process.env.DB_PASSWORD,
        database: 'myapp'
      })
    );
  }

  async write(query, params) {
    return this.writeConnection.execute(query, params);
  }

  async read(query, params) {
    // Round-robin entre read replicas
    const connection = this.readConnections[
      Math.floor(Math.random() * this.readConnections.length)
    ];
    return connection.execute(query, params);
  }
}
```

## Failover Automation

### Lambda Function for Failover
```javascript
const AWS = require('aws-sdk');
const route53 = new AWS.Route53();
const rds = new AWS.RDS();

exports.handler = async (event) => {
  const { region, healthCheckId } = event;
  
  try {
    // 1. Verificar saúde da região
    const healthCheck = await route53.getHealthCheck({
      HealthCheckId: healthCheckId
    }).promise();
    
    if (healthCheck.HealthCheck.Status === 'Healthy') {
      console.log(`Region ${region} is healthy`);
      return;
    }
    
    // 2. Promover read replica para master
    if (region === 'us-west-2') {
      await promoteReadReplica('read-replica-us-west');
    } else if (region === 'eu-west-1') {
      await promoteReadReplica('read-replica-eu-west');
    }
    
    // 3. Atualizar DNS
    await updateDNSRecords(region);
    
    // 4. Notificar equipe
    await sendNotification(`Failover completed for region ${region}`);
    
  } catch (error) {
    console.error('Failover error:', error);
    await sendAlert(`Failover failed for region ${region}: ${error.message}`);
  }
};

async function promoteReadReplica(replicaId) {
  await rds.promoteReadReplica({
    DBInstanceIdentifier: replicaId
  }).promise();
  
  console.log(`Promoted ${replicaId} to master`);
}

async function updateDNSRecords(region) {
  // Atualizar registros DNS para apontar para nova região
  const changeBatch = {
    Changes: [{
      Action: 'UPSERT',
      ResourceRecordSet: {
        Name: 'api.example.com',
        Type: 'A',
        AliasTarget: {
          DNSName: `api-${region}.example.com`,
          EvaluateTargetHealth: true,
          HostedZoneId: 'Z2FDTNDATAQYW2'
        }
      }
    }]
  };
  
  await route53.changeResourceRecordSets({
    HostedZoneId: 'Z1234567890',
    ChangeBatch: changeBatch
  }).promise();
}
```

## Monitoring Multi-Region

### CloudWatch Cross-Region Dashboard
```yaml
Dashboard:
  Type: AWS::CloudWatch::Dashboard
  Properties:
    DashboardName: MultiRegionDashboard
    DashboardBody: !Sub |
      {
        "widgets": [
          {
            "type": "metric",
            "x": 0,
            "y": 0,
            "width": 12,
            "height": 6,
            "properties": {
              "metrics": [
                ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", "api-us-east"],
                ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", "api-us-west"],
                ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", "api-eu-west"]
              ],
              "period": 300,
              "stat": "Sum",
              "region": "us-east-1",
              "title": "Request Count by Region"
            }
          },
          {
            "type": "metric",
            "x": 12,
            "y": 0,
            "width": 12,
            "height": 6,
            "properties": {
              "metrics": [
                ["AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", "api-us-east"],
                ["AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", "api-us-west"],
                ["AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", "api-eu-west"]
              ],
              "period": 300,
              "stat": "Average",
              "region": "us-east-1",
              "title": "Response Time by Region"
            }
          }
        ]
      }
```

### Custom Metrics for Cross-Region Monitoring
```javascript
const cloudwatch = new AWS.CloudWatch();

class MultiRegionMonitor {
  constructor() {
    this.region = process.env.AWS_REGION;
    this.namespace = 'MyApp/MultiRegion';
  }

  async recordLatency(operation, latency) {
    await cloudwatch.putMetricData({
      Namespace: this.namespace,
      MetricData: [{
        MetricName: 'OperationLatency',
        Dimensions: [
          { Name: 'Region', Value: this.region },
          { Name: 'Operation', Value: operation }
        ],
        Value: latency,
        Unit: 'Milliseconds',
        Timestamp: new Date()
      }]
    }).promise();
  }

  async recordError(operation, errorType) {
    await cloudwatch.putMetricData({
      Namespace: this.namespace,
      MetricData: [{
        MetricName: 'ErrorCount',
        Dimensions: [
          { Name: 'Region', Value: this.region },
          { Name: 'Operation', Value: operation },
          { Name: 'ErrorType', Value: errorType }
        ],
        Value: 1,
        Unit: 'Count',
        Timestamp: new Date()
      }]
    }).promise();
  }

  async recordReplicationLag(lag) {
    await cloudwatch.putMetricData({
      Namespace: this.namespace,
      MetricData: [{
        MetricName: 'ReplicationLag',
        Dimensions: [
          { Name: 'Region', Value: this.region }
        ],
        Value: lag,
        Unit: 'Seconds',
        Timestamp: new Date()
      }]
    }).promise();
  }
}
```

## Benefícios Alcançados

### ✅ Melhorias
- **Disaster Recovery**: Continuidade mesmo com falhas regionais
- **Latência Global**: Usuários atendidos pela região mais próxima
- **Alta Disponibilidade**: 99.99%+ de uptime
- **Compliance**: Dados armazenados em regiões específicas

### 📊 Métricas Melhoradas
| Métrica | Antes | Depois |
|---------|-------|--------|
| Usuários simultâneos | 200.000-1.000.000+ | 1.000.000+ (global) |
| Latência média | 100-200ms | 50-100ms (por região) |
| Uptime | 99.99% | 99.999% |
| RTO (Recovery Time Objective) | 4-8 horas | 15-30 minutos |
| RPO (Recovery Point Objective) | 1-4 horas | 5-15 minutos |

## Considerações Importantes

### 1. Data Consistency
```javascript
// Implementar consistência eventual
class DataConsistencyManager {
  async writeWithConsistency(data, options = {}) {
    const { requireConsistency = false, timeout = 5000 } = options;
    
    if (requireConsistency) {
      // Aguardar replicação para todas as regiões
      await this.waitForReplication(data.id, timeout);
    }
    
    return this.write(data);
  }

  async waitForReplication(id, timeout) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      const isConsistent = await this.checkConsistency(id);
      if (isConsistent) return true;
      
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    throw new Error('Replication timeout');
  }
}
```

### 2. Cost Optimization
```yaml
# Configurar Lifecycle Policies para S3
LifecycleConfiguration:
  Rules:
    - Id: ArchiveOldData
      Status: Enabled
      Transitions:
        - Days: 30
          StorageClass: STANDARD_IA
        - Days: 90
          StorageClass: GLACIER
        - Days: 365
          StorageClass: DEEP_ARCHIVE
```

### 3. Security
```yaml
# Configurar KMS para criptografia cross-region
KMSKey:
  Type: AWS::KMS::Key
  Properties:
    Description: Cross-region encryption key
    KeyPolicy:
      Statement:
        - Effect: Allow
          Principal:
            AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
          Action: 'kms:*'
          Resource: '*'
    MultiRegion: true
```

## Próximos Passos

Para continuar a evolução:

1. **Implementar Message Queues** para processamento assíncrono
2. **Adicionar CDN** para conteúdo estático global
3. **Implementar Database Sharding** para bancos muito grandes
4. **Configurar Microserviços** para maior modularidade

## Checklist de Implementação

- [ ] Configurar múltiplas regiões AWS
- [ ] Implementar cross-region replication
- [ ] Configurar Route 53 com health checks
- [ ] Implementar failover automático
- [ ] Configurar monitoramento cross-region
- [ ] Implementar backup cross-region
- [ ] Configurar criptografia cross-region
- [ ] Testar disaster recovery
- [ ] Documentar procedimentos de failover
- [ ] Treinar equipe em operações multi-region
