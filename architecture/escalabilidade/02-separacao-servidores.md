# Separação de Servidores - Primeira Evolução

## Visão Geral

A primeira evolução consiste em separar a aplicação do banco de dados em servidores distintos, eliminando a competição por recursos.

## Arquitetura

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
         │   Servidor API  │
         │ ┌─────────────┐ │
         │ │    API      │ │
         │ │  (Backend)  │ │
         │ └─────────────┘ │
         └─────────────────┘
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

## Benefícios Alcançados

### ✅ Melhorias
- **Recursos dedicados**: API e DB têm recursos próprios
- **Dimensionamento independente**: Pode escalar cada componente separadamente
- **Manutenção isolada**: Pode reiniciar um sem afetar o outro
- **Performance melhorada**: Sem competição por recursos

### ⚠️ Limitações Mantidas
- **Ponto único de falha**: Ainda existe SPOF
- **Escalabilidade limitada**: Não resolve problemas de alta disponibilidade
- **Sem redundância**: Falha de qualquer servidor derruba o sistema

## Configuração de Rede

### Servidor API
```bash
# Configuração típica
CPU: 2-4 cores
RAM: 4-8 GB
Storage: 50-100 GB SSD
Network: 1 Gbps
```

### Servidor Database
```bash
# Configuração típica
CPU: 4-8 cores
RAM: 8-16 GB
Storage: 100-500 GB SSD
Network: 1 Gbps
```

## Configuração de Conexão

### Exemplo com Node.js + MySQL
```javascript
const mysql = require('mysql2');

const dbConfig = {
  host: '192.168.1.100', // IP do servidor DB
  user: 'app_user',
  password: 'secure_password',
  database: 'myapp_db',
  port: 3306,
  connectionLimit: 10,
  acquireTimeout: 60000,
  timeout: 60000
};

const pool = mysql.createPool(dbConfig);
```

### Exemplo com Python + PostgreSQL
```python
import psycopg2
from psycopg2 import pool

db_config = {
    'host': '192.168.1.100',
    'port': 5432,
    'database': 'myapp_db',
    'user': 'app_user',
    'password': 'secure_password',
    'minconn': 1,
    'maxconn': 20
}

connection_pool = psycopg2.pool.ThreadedConnectionPool(**db_config)
```

## Considerações de Segurança

### 1. Firewall
```bash
# Servidor API - Apenas portas necessárias
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw deny 3306   # MySQL (apenas interno)
ufw deny 5432   # PostgreSQL (apenas interno)
```

### 2. Rede Privada
- Use IPs privados para comunicação entre servidores
- Configure VPN se necessário
- Implemente autenticação forte

### 3. Criptografia
```bash
# SSL/TLS para comunicação
# Certificados para conexões seguras
# Criptografia de dados em trânsito
```

## Monitoramento Básico

### Métricas Importantes
- **CPU Usage**: < 70% em ambos servidores
- **Memory Usage**: < 80% em ambos servidores
- **Disk I/O**: Monitorar latência
- **Network**: Largura de banda entre servidores
- **Database Connections**: Pool de conexões

### Ferramentas Recomendadas
```bash
# Monitoramento básico
htop                    # CPU e RAM
iotop                   # I/O de disco
netstat -i              # Estatísticas de rede
mysqladmin status       # Status do MySQL
```

## Capacidade Estimada

| Métrica | Valor |
|---------|-------|
| Usuários simultâneos | 1.000-5.000 |
| Requisições/segundo | 100-500 |
| Tempo de resposta | 150-300ms |
| Uptime | 98-99% |
| Capacidade de crescimento | Moderada |

## Próximos Passos

Para continuar a evolução:

1. **Implementar Load Balancer** para múltiplas instâncias da API
2. **Adicionar redundância** com réplicas do banco
3. **Implementar cache** para reduzir carga no banco
4. **Configurar monitoramento** avançado

## Checklist de Implementação

- [ ] Configurar servidores separados
- [ ] Configurar rede privada
- [ ] Implementar firewall
- [ ] Configurar SSL/TLS
- [ ] Testar conectividade
- [ ] Configurar backup
- [ ] Implementar monitoramento básico
- [ ] Documentar configurações
- [ ] Testar failover manual
- [ ] Configurar logs centralizados
