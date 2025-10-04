# Database Replication - Alta Disponibilidade de Dados

## Visão Geral

A replicação de banco de dados é essencial para eliminar o ponto único de falha na camada de dados, implementando arquitetura Master-Slave.

## Arquitetura com Database Replication

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
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐        ┌───▼───┐        ┌───▼───┐
│ DB    │        │ DB    │        │ DB    │
│Master │◄──────►│Slave-1│        │Slave-2│
│(Write)│        │(Read) │        │(Read) │
└───────┘        └───────┘        └───────┘
```

## Tipos de Replicação

### 1. Master-Slave (Read Replicas)
- **Master**: Apenas escritas (INSERT, UPDATE, DELETE)
- **Slaves**: Apenas leituras (SELECT)
- **Replicação**: Assíncrona do Master para Slaves

### 2. Master-Master
- Ambos servidores aceitam leitura e escrita
- Replicação bidirecional
- Maior complexidade de sincronização

### 3. Multi-Master
- Múltiplos masters
- Replicação em anel ou mesh
- Máxima disponibilidade

## Implementação MySQL

### Configuração Master
```sql
-- /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-format = ROW
sync_binlog = 1
innodb_flush_log_at_trx_commit = 1

# Criar usuário para replicação
CREATE USER 'replicator'@'%' IDENTIFIED BY 'replication_password';
GRANT REPLICATION SLAVE ON *.* TO 'replicator'@'%';
FLUSH PRIVILEGES;

# Verificar status
SHOW MASTER STATUS;
```

### Configuração Slave
```sql
-- /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
server-id = 2
relay-log = mysql-relay-bin
read-only = 1

-- Configurar replicação
CHANGE MASTER TO
  MASTER_HOST='192.168.1.100',
  MASTER_USER='replicator',
  MASTER_PASSWORD='replication_password',
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=154;

START SLAVE;
SHOW SLAVE STATUS\G;
```

## Implementação PostgreSQL

### Configuração Master
```sql
-- postgresql.conf
wal_level = replica
max_wal_senders = 3
max_replication_slots = 3
synchronous_commit = on

-- pg_hba.conf
host replication replicator 192.168.1.0/24 md5

-- Criar usuário
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replication_password';
```

### Configuração Slave
```bash
# Backup do master
pg_basebackup -h 192.168.1.100 -D /var/lib/postgresql/data -U replicator -v -P -W

# Configurar recovery.conf
standby_mode = 'on'
primary_conninfo = 'host=192.168.1.100 port=5432 user=replicator password=replication_password'
```

## Configuração da Aplicação

### Node.js com Separação Read/Write
```javascript
const mysql = require('mysql2');

// Pool de conexões para escrita (Master)
const writePool = mysql.createPool({
  host: '192.168.1.100', // Master
  user: 'app_user',
  password: 'password',
  database: 'myapp',
  connectionLimit: 5
});

// Pool de conexões para leitura (Slaves)
const readPool = mysql.createPool({
  host: '192.168.1.101', // Slave 1
  user: 'app_user',
  password: 'password',
  database: 'myapp',
  connectionLimit: 10
});

// Função para escolher pool baseado na operação
function getConnection(operation) {
  if (operation === 'SELECT' || operation === 'SHOW') {
    return readPool;
  }
  return writePool;
}

// Exemplo de uso
async function getUsers() {
  const pool = getConnection('SELECT');
  const [rows] = await pool.execute('SELECT * FROM users');
  return rows;
}

async function createUser(userData) {
  const pool = getConnection('INSERT');
  const [result] = await pool.execute(
    'INSERT INTO users (name, email) VALUES (?, ?)',
    [userData.name, userData.email]
  );
  return result;
}
```

### Python com SQLAlchemy
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Engine para escrita
write_engine = create_engine(
    'mysql+pymysql://user:password@192.168.1.100:3306/myapp',
    pool_size=5,
    max_overflow=10
)

# Engine para leitura
read_engine = create_engine(
    'mysql+pymysql://user:password@192.168.1.101:3306/myapp',
    pool_size=10,
    max_overflow=20
)

WriteSession = sessionmaker(bind=write_engine)
ReadSession = sessionmaker(bind=read_engine)

class DatabaseRouter:
    @staticmethod
    def get_session(operation):
        if operation in ['SELECT', 'SHOW']:
            return ReadSession()
        return WriteSession()

# Exemplo de uso
def get_users():
    session = DatabaseRouter.get_session('SELECT')
    users = session.execute("SELECT * FROM users").fetchall()
    session.close()
    return users

def create_user(name, email):
    session = DatabaseRouter.get_session('INSERT')
    session.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email)
    )
    session.commit()
    session.close()
```

## Consistência Eventual

### O Problema
```javascript
// Cenário: Usuário insere dados e imediatamente consulta
async function createAndReadUser() {
  // 1. Inserir usuário (vai para Master)
  await createUser({ name: 'João', email: 'joao@email.com' });
  
  // 2. Consultar usuário (pode ir para Slave que ainda não replicou)
  const users = await getUsers(); // Pode não encontrar o usuário recém-criado
}
```

### Soluções

#### 1. Read-Your-Writes Consistency
```javascript
// Sempre ler do Master após escrita
async function createAndReadUser() {
  await createUser({ name: 'João', email: 'joao@email.com' });
  
  // Ler do Master para garantir consistência
  const users = await getUsersFromMaster();
}
```

#### 2. Delayed Read
```javascript
// Aguardar um tempo antes de ler
async function createAndReadUser() {
  await createUser({ name: 'João', email: 'joao@email.com' });
  
  // Aguardar replicação (ajustar conforme latência)
  await new Promise(resolve => setTimeout(resolve, 100));
  
  const users = await getUsers();
}
```

#### 3. Version-based Consistency
```javascript
// Usar timestamps ou versões para detectar inconsistência
async function createUserWithVersion(userData) {
  const timestamp = Date.now();
  await createUser({ ...userData, created_at: timestamp });
  
  // Retornar dados do Master
  return await getUserByIdFromMaster(userData.id);
}
```

## Monitoramento de Replicação

### MySQL
```sql
-- Verificar status da replicação
SHOW SLAVE STATUS\G;

-- Verificar lag
SELECT 
  MASTER_POS_WAIT('mysql-bin.000001', 154) as lag_seconds;

-- Monitorar conexões
SHOW PROCESSLIST;
```

### PostgreSQL
```sql
-- Verificar status da replicação
SELECT * FROM pg_stat_replication;

-- Verificar lag
SELECT 
  client_addr,
  state,
  sent_lsn,
  write_lsn,
  flush_lsn,
  replay_lsn,
  pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) as lag_bytes
FROM pg_stat_replication;
```

## Failover Automático

### Script de Failover
```bash
#!/bin/bash
# failover.sh

MASTER_HOST="192.168.1.100"
SLAVE_HOST="192.168.1.101"
HEALTH_CHECK_URL="http://$MASTER_HOST:8080/health"

# Verificar saúde do Master
if ! curl -f $HEALTH_CHECK_URL > /dev/null 2>&1; then
    echo "Master is down, promoting slave..."
    
    # Promover Slave para Master
    ssh $SLAVE_HOST "mysql -e 'STOP SLAVE; RESET MASTER;'"
    
    # Atualizar configuração do Load Balancer
    # (implementar lógica específica do seu LB)
    
    # Notificar equipe
    echo "Database failover completed" | mail -s "DB Failover Alert" admin@company.com
fi
```

### Configuração com Keepalived
```bash
# /etc/keepalived/keepalived.conf
vrrp_script chk_mysql {
    script "/usr/local/bin/check_mysql.sh"
    interval 2
    weight -2
    fall 3
    rise 2
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1234
    }
    virtual_ipaddress {
        192.168.1.200
    }
    track_script {
        chk_mysql
    }
}
```

## Benefícios Alcançados

### ✅ Melhorias
- **Eliminação de SPOF**: Banco de dados não é mais ponto único de falha
- **Distribuição de carga**: Leituras distribuídas entre slaves
- **Alta disponibilidade**: Falha do Master não derruba o sistema
- **Performance**: Leituras mais rápidas com slaves dedicados

### 📊 Métricas Melhoradas
| Métrica | Antes | Depois |
|---------|-------|--------|
| Usuários simultâneos | 5.000-15.000 | 15.000-50.000 |
| Requisições/segundo | 500-1.500 | 1.500-5.000 |
| Tempo de resposta (Read) | 100-200ms | 50-100ms |
| Tempo de resposta (Write) | 100-200ms | 100-200ms |
| Uptime | 99.5-99.9% | 99.9-99.99% |

## Considerações Importantes

### 1. Backup Strategy
```bash
# Backup do Master
mysqldump --single-transaction --routines --triggers myapp > backup_$(date +%Y%m%d).sql

# Backup dos Slaves
mysqldump --single-transaction --routines --triggers myapp > slave_backup_$(date +%Y%m%d).sql
```

### 2. Monitoring
```bash
# Script de monitoramento
#!/bin/bash
mysql -e "SHOW SLAVE STATUS\G" | grep -E "(Slave_IO_Running|Slave_SQL_Running|Seconds_Behind_Master)"
```

### 3. Security
```sql
-- Configurar SSL para replicação
CHANGE MASTER TO
  MASTER_SSL=1,
  MASTER_SSL_CA='/path/to/ca-cert.pem',
  MASTER_SSL_CERT='/path/to/client-cert.pem',
  MASTER_SSL_KEY='/path/to/client-key.pem';
```

## Próximos Passos

Para continuar a evolução:

1. **Implementar Cache Layer** para reduzir ainda mais a carga no banco
2. **Adicionar Auto Scaling** para servidores de aplicação
3. **Implementar Sharding** para bancos muito grandes
4. **Configurar Multi-Region** para disaster recovery

## Checklist de Implementação

- [ ] Configurar Master-Slave replication
- [ ] Implementar separação Read/Write na aplicação
- [ ] Configurar monitoramento de replicação
- [ ] Implementar failover automático
- [ ] Configurar backup automático
- [ ] Testar consistência eventual
- [ ] Configurar SSL para replicação
- [ ] Documentar procedimentos de failover
- [ ] Treinar equipe em troubleshooting
- [ ] Implementar alertas de lag de replicação
