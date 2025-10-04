# Auto Scaling - Elasticidade Automática

## Visão Geral

O Auto Scaling permite que a arquitetura se adapte automaticamente à demanda, adicionando ou removendo recursos conforme necessário.

## Arquitetura com Auto Scaling

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
         │   (AWS ALB)     │
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
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐        ┌───▼───┐        ┌───▼───┐
│Redis-1│        │Redis-2│        │Redis-3│
│Cache │        │Cache │        │Cache │
└───────┘        └───────┘        └───────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐        ┌───▼───┐        ┌───▼───┐
│ DB    │        │ DB    │        │ DB    │
│Master │        │Slave-1│        │Slave-2│
└───────┘        └───────┘        └───────┘

┌─────────────────────────────────────────┐
│           Auto Scaling Group            │
│  ┌─────────────────────────────────────┐│
│  │ Min: 2 instances                    ││
│  │ Max: 10 instances                   ││
│  │ Desired: 3 instances                ││
│  │ Scale-out: CPU > 70% for 5min      ││
│  │ Scale-in: CPU < 30% for 10min      ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
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

## Implementação AWS Auto Scaling

### Launch Template
```json
{
  "LaunchTemplateName": "api-server-template",
  "LaunchTemplateData": {
    "ImageId": "ami-0c02fb55956c7d316",
    "InstanceType": "t3.medium",
    "KeyName": "my-key-pair",
    "SecurityGroupIds": ["sg-12345678"],
    "UserData": "IyEvYmluL2Jhc2gKeXVtIHVwZGF0ZSAteQp5dW0gaW5zdGFsbCAteSBub2RlanMKc3lzdGVtY3RsIGVuYWJsZSBub2RlanMKc3lzdGVtY3RsIHN0YXJ0IG5vZGVqcw==",
    "TagSpecifications": [
      {
        "ResourceType": "instance",
        "Tags": [
          {
            "Key": "Name",
            "Value": "api-server"
          },
          {
            "Key": "Environment",
            "Value": "production"
          }
        ]
      }
    ]
  }
}
```

### Auto Scaling Group
```json
{
  "AutoScalingGroupName": "api-asg",
  "LaunchTemplate": {
    "LaunchTemplateName": "api-server-template",
    "Version": "$Latest"
  },
  "MinSize": 2,
  "MaxSize": 10,
  "DesiredCapacity": 3,
  "VPCZoneIdentifier": "subnet-12345678,subnet-87654321",
  "TargetGroupARNs": ["arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/api-tg/1234567890123456"],
  "HealthCheckType": "ELB",
  "HealthCheckGracePeriod": 300,
  "Tags": [
    {
      "Key": "Name",
      "Value": "api-asg",
      "PropagateAtLaunch": true
    }
  ]
}
```

### Scaling Policies
```json
{
  "PolicyName": "scale-out-policy",
  "AutoScalingGroupName": "api-asg",
  "PolicyType": "TargetTrackingScaling",
  "TargetTrackingConfiguration": {
    "TargetValue": 70.0,
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ASGAverageCPUUtilization"
    },
    "ScaleOutCooldown": 300,
    "ScaleInCooldown": 300
  }
}
```

## Implementação com Terraform

### Auto Scaling Group
```hcl
resource "aws_launch_template" "api_template" {
  name_prefix   = "api-template-"
  image_id      = "ami-0c02fb55956c7d316"
  instance_type = "t3.medium"
  
  vpc_security_group_ids = [aws_security_group.api_sg.id]
  
  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    db_host = aws_db_instance.main.endpoint
    redis_host = aws_elasticache_cluster.main.cache_nodes[0].address
  }))
  
  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "api-server"
    }
  }
}

resource "aws_autoscaling_group" "api_asg" {
  name                = "api-asg"
  vpc_zone_identifier = aws_subnet.private[*].id
  target_group_arns   = [aws_lb_target_group.api.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300
  
  min_size         = 2
  max_size         = 10
  desired_capacity = 3
  
  launch_template {
    id      = aws_launch_template.api_template.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Name"
    value               = "api-asg"
    propagate_at_launch = true
  }
}
```

### Scaling Policies
```hcl
resource "aws_autoscaling_policy" "scale_out" {
  name                   = "scale-out"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.api_asg.name
}

resource "aws_autoscaling_policy" "scale_in" {
  name                   = "scale-in"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.api_asg.name
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "70"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = [aws_autoscaling_policy.scale_out.arn]
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.api_asg.name
  }
}

resource "aws_cloudwatch_metric_alarm" "cpu_low" {
  alarm_name          = "cpu-low"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "30"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = [aws_autoscaling_policy.scale_in.arn]
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.api_asg.name
  }
}
```

## Implementação com Kubernetes

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
```

### Deployment com Resource Limits
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: myapp:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Métricas Personalizadas

### Custom Metrics com Prometheus
```javascript
const prometheus = require('prom-client');

// Contador de requisições
const httpRequestsTotal = new prometheus.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});

// Histograma de duração
const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10]
});

// Gauge de conexões ativas
const activeConnections = new prometheus.Gauge({
  name: 'active_connections',
  help: 'Number of active connections'
});

// Middleware para métricas
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    
    httpRequestsTotal
      .labels(req.method, req.route?.path || req.path, res.statusCode)
      .inc();
    
    httpRequestDuration
      .labels(req.method, req.route?.path || req.path)
      .observe(duration);
  });
  
  next();
});
```

### Scaling Baseado em Métricas Customizadas
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa-custom
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Pods
    pods:
      metric:
        name: active_connections
      target:
        type: AverageValue
        averageValue: "100"
```

## Implementação com Docker Swarm

### Docker Compose com Scaling
```yaml
version: '3.8'
services:
  api:
    image: myapp:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
      placement:
        constraints:
          - node.role == worker
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - REDIS_HOST=redis
```

### Scaling com Docker Swarm
```bash
# Escalar serviço
docker service scale api=5

# Verificar status
docker service ps api

# Atualizar serviço
docker service update --replicas 8 api
```

## Monitoramento e Alertas

### CloudWatch Alarms
```json
{
  "AlarmName": "High-CPU-Utilization",
  "ComparisonOperator": "GreaterThanThreshold",
  "EvaluationPeriods": 2,
  "MetricName": "CPUUtilization",
  "Namespace": "AWS/EC2",
  "Period": 300,
  "Statistic": "Average",
  "Threshold": 80.0,
  "ActionsEnabled": true,
  "AlarmActions": [
    "arn:aws:sns:us-east-1:123456789012:alerts"
  ],
  "AlarmDescription": "Alarm when CPU exceeds 80%"
}
```

### Prometheus Alerting Rules
```yaml
groups:
- name: scaling.rules
  rules:
  - alert: HighCPUUsage
    expr: cpu_usage_percent > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage detected"
      description: "CPU usage is above 80% for more than 5 minutes"
  
  - alert: HighMemoryUsage
    expr: memory_usage_percent > 85
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High memory usage detected"
      description: "Memory usage is above 85% for more than 5 minutes"
```

## Benefícios Alcançados

### ✅ Melhorias
- **Elasticidade**: Adaptação automática à demanda
- **Economia**: Paga apenas pelos recursos utilizados
- **Alta disponibilidade**: Redundância automática
- **Performance**: Mantém performance mesmo com picos de tráfego

### 📊 Métricas Melhoradas
| Métrica | Antes | Depois |
|---------|-------|--------|
| Usuários simultâneos | 50.000-200.000 | 200.000-1.000.000+ |
| Requisições/segundo | 5.000-20.000 | 20.000-100.000+ |
| Tempo de resposta | 10-50ms | 10-50ms (consistente) |
| Uptime | 99.9-99.99% | 99.99-99.999% |
| Custo | Fixo | Variável (paga pelo uso) |

## Considerações Importantes

### 1. Warm-up Time
```javascript
// Implementar warm-up para novas instâncias
app.get('/warmup', (req, res) => {
  // Pré-carregar dados críticos
  Promise.all([
    cache.get('system:config'),
    db.query('SELECT COUNT(*) FROM users'),
    // Outras operações de warm-up
  ]).then(() => {
    res.json({ status: 'warmed up' });
  });
});
```

### 2. Graceful Shutdown
```javascript
// Implementar shutdown graceful
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  
  // Parar aceitar novas conexões
  server.close(() => {
    console.log('Process terminated');
    process.exit(0);
  });
  
  // Aguardar conexões existentes terminarem
  setTimeout(() => {
    console.log('Force shutdown');
    process.exit(1);
  }, 10000);
});
```

### 3. Health Checks
```javascript
// Health check para load balancer
app.get('/health', (req, res) => {
  const health = {
    status: 'OK',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    checks: {
      database: 'OK',
      redis: 'OK'
    }
  };
  
  res.json(health);
});

// Readiness check
app.get('/ready', (req, res) => {
  // Verificar se a aplicação está pronta para receber tráfego
  const isReady = checkDatabaseConnection() && checkRedisConnection();
  
  if (isReady) {
    res.json({ status: 'ready' });
  } else {
    res.status(503).json({ status: 'not ready' });
  }
});
```

## Próximos Passos

Para continuar a evolução:

1. **Implementar Multi-Region** para disaster recovery
2. **Adicionar Message Queues** para processamento assíncrono
3. **Implementar CDN** para conteúdo estático
4. **Configurar Database Sharding** para bancos muito grandes

## Checklist de Implementação

- [ ] Configurar Auto Scaling Group
- [ ] Implementar Launch Template/Configuration
- [ ] Configurar Scaling Policies
- [ ] Implementar Health Checks
- [ ] Configurar CloudWatch Alarms
- [ ] Implementar Graceful Shutdown
- [ ] Configurar Warm-up das instâncias
- [ ] Testar scaling automático
- [ ] Configurar alertas de scaling
- [ ] Documentar procedimentos de scaling
