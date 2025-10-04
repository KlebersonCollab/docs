# Cache Layer - Otimização de Performance

## Visão Geral

A implementação de uma camada de cache é fundamental para reduzir a carga no banco de dados e melhorar significativamente a performance da aplicação.

## Arquitetura com Cache

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
```

## Padrões de Cache

### 1. Cache-Aside (Lazy Loading)
```javascript
async function getUser(id) {
  // 1. Verificar cache primeiro
  let user = await redis.get(`user:${id}`);
  
  if (user) {
    return JSON.parse(user);
  }
  
  // 2. Se não estiver no cache, buscar no banco
  user = await db.query('SELECT * FROM users WHERE id = ?', [id]);
  
  // 3. Armazenar no cache para próximas consultas
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  
  return user;
}
```

### 2. Write-Through
```javascript
async function createUser(userData) {
  // 1. Escrever no banco
  const user = await db.query(
    'INSERT INTO users (name, email) VALUES (?, ?)',
    [userData.name, userData.email]
  );
  
  // 2. Escrever no cache imediatamente
  await redis.setex(
    `user:${user.id}`, 
    3600, 
    JSON.stringify(user)
  );
  
  return user;
}
```

### 3. Write-Behind (Write-Back)
```javascript
async function updateUser(id, userData) {
  // 1. Atualizar cache imediatamente
  await redis.setex(
    `user:${id}`, 
    3600, 
    JSON.stringify(userData)
  );
  
  // 2. Agendar escrita no banco (assíncrona)
  scheduleDatabaseUpdate(id, userData);
  
  return userData;
}
```

## Implementação com Redis

### Configuração Básica
```javascript
const redis = require('redis');
const client = redis.createClient({
  host: '192.168.1.200',
  port: 6379,
  password: 'redis_password',
  retry_strategy: (options) => {
    if (options.error && options.error.code === 'ECONNREFUSED') {
      return new Error('Redis server refused connection');
    }
    if (options.total_retry_time > 1000 * 60 * 60) {
      return new Error('Retry time exhausted');
    }
    if (options.attempt > 10) {
      return undefined;
    }
    return Math.min(options.attempt * 100, 3000);
  }
});

client.on('error', (err) => {
  console.error('Redis Client Error', err);
});
```

### Cache com TTL
```javascript
class CacheService {
  constructor() {
    this.redis = redis.createClient({
      host: '192.168.1.200',
      port: 6379
    });
  }

  async get(key) {
    try {
      const value = await this.redis.get(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Cache get error:', error);
      return null;
    }
  }

  async set(key, value, ttl = 3600) {
    try {
      await this.redis.setex(key, ttl, JSON.stringify(value));
    } catch (error) {
      console.error('Cache set error:', error);
    }
  }

  async del(key) {
    try {
      await this.redis.del(key);
    } catch (error) {
      console.error('Cache delete error:', error);
    }
  }

  async invalidatePattern(pattern) {
    try {
      const keys = await this.redis.keys(pattern);
      if (keys.length > 0) {
        await this.redis.del(...keys);
      }
    } catch (error) {
      console.error('Cache invalidate error:', error);
    }
  }
}
```

## Cache de Consultas Complexas

### Cache de Relatórios
```javascript
async function getSalesReport(startDate, endDate) {
  const cacheKey = `report:sales:${startDate}:${endDate}`;
  
  // Verificar cache
  let report = await cache.get(cacheKey);
  if (report) {
    return report;
  }
  
  // Gerar relatório (operação pesada)
  report = await generateSalesReport(startDate, endDate);
  
  // Cache por 1 hora
  await cache.set(cacheKey, report, 3600);
  
  return report;
}
```

### Cache de Listagens com Paginação
```javascript
async function getUsers(page = 1, limit = 10) {
  const cacheKey = `users:page:${page}:limit:${limit}`;
  
  let users = await cache.get(cacheKey);
  if (users) {
    return users;
  }
  
  const offset = (page - 1) * limit;
  users = await db.query(
    'SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?',
    [limit, offset]
  );
  
  // Cache por 5 minutos
  await cache.set(cacheKey, users, 300);
  
  return users;
}
```

## Cache de Sessões

### Implementação com Redis
```javascript
const session = require('express-session');
const RedisStore = require('connect-redis')(session);

app.use(session({
  store: new RedisStore({
    client: redis.createClient({
      host: '192.168.1.200',
      port: 6379
    })
  }),
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,
    maxAge: 24 * 60 * 60 * 1000 // 24 horas
  }
}));
```

## Cache de Dados Estáticos

### Cache de Configurações
```javascript
class ConfigCache {
  constructor() {
    this.cache = new Map();
    this.loadConfigurations();
  }

  async loadConfigurations() {
    const configs = await db.query('SELECT * FROM configurations');
    configs.forEach(config => {
      this.cache.set(config.key, config.value);
    });
  }

  get(key) {
    return this.cache.get(key);
  }

  async refresh() {
    this.cache.clear();
    await this.loadConfigurations();
  }
}
```

## Invalidação de Cache

### Invalidação por Tags
```javascript
class TaggedCache {
  async set(key, value, tags = [], ttl = 3600) {
    await redis.setex(key, ttl, JSON.stringify(value));
    
    // Armazenar tags
    for (const tag of tags) {
      await redis.sadd(`tag:${tag}`, key);
    }
  }

  async invalidateByTag(tag) {
    const keys = await redis.smembers(`tag:${tag}`);
    if (keys.length > 0) {
      await redis.del(...keys);
      await redis.del(`tag:${tag}`);
    }
  }
}

// Uso
const taggedCache = new TaggedCache();

// Armazenar com tags
await taggedCache.set('user:123', userData, ['user', 'profile']);

// Invalidar por tag
await taggedCache.invalidateByTag('user'); // Remove todos os caches de usuário
```

### Invalidação por Eventos
```javascript
// Event listener para invalidação automática
db.on('user:updated', async (userId) => {
  await cache.del(`user:${userId}`);
  await cache.invalidatePattern(`user:${userId}:*`);
});

db.on('user:deleted', async (userId) => {
  await cache.del(`user:${userId}`);
  await cache.invalidatePattern(`user:${userId}:*`);
});
```

## Cache Distribuído

### Redis Cluster
```javascript
const Redis = require('ioredis');

const cluster = new Redis.Cluster([
  { host: '192.168.1.200', port: 7000 },
  { host: '192.168.1.201', port: 7000 },
  { host: '192.168.1.202', port: 7000 }
], {
  redisOptions: {
    password: 'redis_password'
  }
});
```

### Memcached
```javascript
const memcached = require('memcached');

const client = new memcached('192.168.1.200:11211', {
  retries: 10,
  retry: 10000,
  remove: true
});

// Uso similar ao Redis
client.get('user:123', (err, data) => {
  if (data) {
    console.log('Cache hit:', data);
  } else {
    console.log('Cache miss');
  }
});
```

## Monitoramento de Cache

### Métricas Importantes
```javascript
class CacheMetrics {
  constructor() {
    this.hits = 0;
    this.misses = 0;
    this.errors = 0;
  }

  recordHit() {
    this.hits++;
  }

  recordMiss() {
    this.misses++;
  }

  recordError() {
    this.errors++;
  }

  getHitRate() {
    const total = this.hits + this.misses;
    return total > 0 ? (this.hits / total) * 100 : 0;
  }

  getStats() {
    return {
      hits: this.hits,
      misses: this.misses,
      errors: this.errors,
      hitRate: this.getHitRate()
    };
  }
}
```

### Health Check
```javascript
app.get('/health/cache', async (req, res) => {
  try {
    await redis.ping();
    res.json({ status: 'OK', cache: 'Connected' });
  } catch (error) {
    res.status(503).json({ status: 'Error', cache: 'Disconnected' });
  }
});
```

## Benefícios Alcançados

### ✅ Melhorias
- **Performance**: Redução drástica no tempo de resposta
- **Redução de carga**: Menos consultas ao banco de dados
- **Escalabilidade**: Suporte a mais usuários simultâneos
- **Economia**: Menos recursos de banco necessários

### 📊 Métricas Melhoradas
| Métrica | Antes | Depois |
|---------|-------|--------|
| Usuários simultâneos | 15.000-50.000 | 50.000-200.000 |
| Requisições/segundo | 1.500-5.000 | 5.000-20.000 |
| Tempo de resposta (Cache Hit) | 100-200ms | 10-50ms |
| Tempo de resposta (Cache Miss) | 100-200ms | 100-200ms |
| Hit Rate | 0% | 80-95% |
| Carga no banco | 100% | 20-50% |

## Estratégias de Cache

### 1. Cache de Dados Frequentes
```javascript
// Cache de produtos mais vendidos
async function getTopProducts() {
  const cacheKey = 'products:top';
  let products = await cache.get(cacheKey);
  
  if (!products) {
    products = await db.query(`
      SELECT p.*, COUNT(o.id) as sales_count 
      FROM products p 
      JOIN order_items oi ON p.id = oi.product_id 
      JOIN orders o ON oi.order_id = o.id 
      WHERE o.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
      GROUP BY p.id 
      ORDER BY sales_count DESC 
      LIMIT 10
    `);
    
    await cache.set(cacheKey, products, 1800); // 30 minutos
  }
  
  return products;
}
```

### 2. Cache de Dados Estáticos
```javascript
// Cache de configurações do sistema
async function getSystemConfig() {
  const cacheKey = 'system:config';
  let config = await cache.get(cacheKey);
  
  if (!config) {
    config = await db.query('SELECT * FROM system_config');
    await cache.set(cacheKey, config, 3600); // 1 hora
  }
  
  return config;
}
```

### 3. Cache de Resultados de Cálculos
```javascript
// Cache de estatísticas complexas
async function getDashboardStats() {
  const cacheKey = 'dashboard:stats';
  let stats = await cache.get(cacheKey);
  
  if (!stats) {
    stats = await calculateComplexStats();
    await cache.set(cacheKey, stats, 300); // 5 minutos
  }
  
  return stats;
}
```

## Próximos Passos

Para continuar a evolução:

1. **Implementar Auto Scaling** para servidores de aplicação
2. **Adicionar CDN** para conteúdo estático
3. **Implementar Message Queues** para processamento assíncrono
4. **Configurar Multi-Region** para disaster recovery

## Checklist de Implementação

- [ ] Configurar Redis/Memcached
- [ ] Implementar padrões de cache (Cache-Aside, Write-Through)
- [ ] Configurar TTL adequado para cada tipo de dado
- [ ] Implementar invalidação de cache
- [ ] Configurar monitoramento de hit rate
- [ ] Implementar fallback para falhas de cache
- [ ] Configurar backup do cache
- [ ] Testar performance com e sem cache
- [ ] Documentar estratégias de cache
- [ ] Treinar equipe em troubleshooting de cache
