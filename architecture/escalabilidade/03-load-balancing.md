# Load Balancing - Escalabilidade Horizontal

## Visão Geral

O Load Balancing é a técnica fundamental para escalabilidade horizontal, permitindo distribuir carga entre múltiplas instâncias da aplicação.

## Arquitetura com Load Balancer

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Mobile App   │
│   (React/Angular)│    │   (iOS/Android)│
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌─────────────────┐
         │      DNS       │
         │  api.meuapp.com│
         └─────────────────┘
                     │
         ┌─────────────────┐
         │ Load Balancer   │
         │   (HAProxy/      │
         │   Nginx/        │
         │   AWS ALB)      │
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
         │ Servidor Database│
         │ ┌─────────────┐ │
         │ │   Database  │ │
         │ │  (MySQL/    │ │
         │ │  PostgreSQL)│ │
         │ └─────────────┘ │
         └─────────────────┘
```

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

### 4. IP Hash
- Usa hash do IP do cliente
- Garante que mesmo cliente vá para mesmo servidor
- Útil para sessões stateful

## Implementação com HAProxy

### Configuração Básica
```haproxy
global
    daemon
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend web_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/app.pem
    redirect scheme https if !{ ssl_fc }
    default_backend api_servers

backend api_servers
    balance roundrobin
    option httpchk GET /health
    server api1 192.168.1.10:3000 check
    server api2 192.168.1.11:3000 check
    server api3 192.168.1.12:3000 check
```

### Health Checks
```haproxy
backend api_servers
    option httpchk GET /health
    http-check expect status 200
    server api1 192.168.1.10:3000 check inter 5s rise 2 fall 3
    server api2 192.168.1.11:3000 check inter 5s rise 2 fall 3
    server api3 192.168.1.12:3000 check inter 5s rise 2 fall 3
```

## Implementação com Nginx

### Configuração Básica
```nginx
upstream api_backend {
    least_conn;
    server 192.168.1.10:3000 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:3000 max_fails=3 fail_timeout=30s;
    server 192.168.1.12:3000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name api.meuapp.com;
    
    location / {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Configuração com SSL
```nginx
server {
    listen 443 ssl http2;
    server_name api.meuapp.com;
    
    ssl_certificate /etc/ssl/certs/app.crt;
    ssl_certificate_key /etc/ssl/private/app.key;
    
    location / {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## AWS Application Load Balancer

### Configuração Terraform
```hcl
resource "aws_lb" "api_lb" {
  name               = "api-load-balancer"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = aws_subnet.public[*].id
}

resource "aws_lb_target_group" "api_tg" {
  name     = "api-target-group"
  port     = 3000
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "api_listener" {
  load_balancer_arn = aws_lb.api_lb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = aws_acm_certificate.api_cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api_tg.arn
  }
}
```

## Health Check Endpoint

### Node.js/Express
```javascript
app.get('/health', (req, res) => {
  const healthcheck = {
    uptime: process.uptime(),
    message: 'OK',
    timestamp: Date.now(),
    checks: {
      database: 'OK',
      redis: 'OK',
      memory: process.memoryUsage()
    }
  };
  
  try {
    res.status(200).json(healthcheck);
  } catch (error) {
    healthcheck.message = error;
    res.status(503).json(healthcheck);
  }
});
```

### Python/Flask
```python
from flask import Flask, jsonify
import psutil
import time

app = Flask(__name__)

@app.route('/health')
def health_check():
    health = {
        'status': 'OK',
        'timestamp': time.time(),
        'uptime': time.time() - start_time,
        'memory': psutil.virtual_memory().percent,
        'cpu': psutil.cpu_percent()
    }
    
    return jsonify(health), 200
```

## Benefícios Alcançados

### ✅ Melhorias
- **Alta disponibilidade**: Falha de um servidor não derruba o sistema
- **Escalabilidade horizontal**: Pode adicionar mais servidores conforme necessário
- **Distribuição de carga**: Requisições distribuídas uniformemente
- **Failover automático**: Servidores com falha são removidos automaticamente

### 📊 Métricas Melhoradas
| Métrica | Antes | Depois |
|---------|-------|--------|
| Usuários simultâneos | 1.000-5.000 | 5.000-15.000 |
| Requisições/segundo | 100-500 | 500-1.500 |
| Tempo de resposta | 150-300ms | 100-200ms |
| Uptime | 98-99% | 99.5-99.9% |
| Capacidade de crescimento | Moderada | Alta |

## Considerações Importantes

### 1. Session Affinity
```javascript
// Para aplicações stateful, use sticky sessions
app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: { secure: true, maxAge: 24 * 60 * 60 * 1000 }
}));
```

### 2. Database Connection Pooling
```javascript
// Configure pool de conexões adequado
const pool = mysql.createPool({
  connectionLimit: 10, // Por servidor
  host: 'db-server',
  user: 'app_user',
  password: 'password',
  database: 'myapp'
});
```

### 3. Logging Centralizado
```javascript
// Use logs estruturados
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'app.log' }),
    new winston.transports.Console()
  ]
});
```

## Próximos Passos

Para continuar a evolução:

1. **Implementar Auto Scaling** para adicionar/remover servidores automaticamente
2. **Adicionar Cache Layer** para reduzir carga no banco
3. **Implementar Database Replication** para alta disponibilidade dos dados
4. **Configurar Multi-Region** para disaster recovery

## Checklist de Implementação

- [ ] Configurar Load Balancer (HAProxy/Nginx/AWS ALB)
- [ ] Implementar Health Checks
- [ ] Configurar SSL/TLS
- [ ] Testar failover automático
- [ ] Configurar monitoramento
- [ ] Implementar logging centralizado
- [ ] Configurar backup automático
- [ ] Testar distribuição de carga
- [ ] Documentar configurações
- [ ] Treinar equipe em troubleshooting
