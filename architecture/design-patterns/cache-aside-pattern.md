# Cache Aside Pattern

## Visão Geral

O **Cache Aside Pattern** é um padrão arquitetural simples e poderoso para resolver gargalos de performance em aplicações web, especialmente quando o banco de dados se torna o principal gargalo do sistema devido ao alto volume de consultas repetidas.

## Problema que Resolve

### Cenário Típico
- Sistema recebe volume muito alto de acessos simultâneos
- Aplicação fica lenta conforme número de usuários aumenta
- Banco de dados é bombardeado com consultas repetidas para os mesmos dados
- Banco de dados se torna o principal gargalo do sistema

### Exemplo Prático: E-commerce
- Frontend exibe categorias em destaque
- Toda requisição ao frontend gera consulta ao banco de dados
- Durante picos de tráfego (Black Friday), banco não consegue atender todas as consultas
- Sistema fica fora do ar devido a timeouts

## Como Funciona

### Fluxo Tradicional (Problemático)
```
Frontend → API → Banco de Dados
```

**Problemas:**
- Banco de dados é o elo mais fraco
- Operações consomem recursos (atomicidade, consistência, isolamento, durabilidade)
- Número limitado de conexões simultâneas
- Criação de fila de atendimento
- Timeouts e falhas do sistema

### Fluxo com Cache Aside
```
Frontend → API → Cache (Redis) → Banco de Dados (quando necessário)
```

**Benefícios:**
- Cache opera em memória RAM (100 nanosegundos vs 1 milissegundo do banco)
- Reduz drasticamente consultas ao banco
- Melhora performance e experiência do usuário

## Implementação

### Estratégia de Cache
1. **Primeira requisição:**
   - API consulta cache
   - Cache retorna vazio (dados não existem)
   - API busca dados no banco de dados
   - API armazena dados no cache
   - API retorna dados para o frontend

2. **Requisições subsequentes:**
   - API consulta cache
   - Cache retorna dados armazenados
   - API retorna dados para o frontend
   - **Não há consulta ao banco de dados**

### Exemplo de Código (Node.js/Express)

```javascript
// Configuração do Redis
const redis = require('redis');
const client = redis.createClient({
  host: 'redis', // nome do container Docker
  port: 6379
});

// Endpoint com Cache Aside
app.get('/categories/featured', async (req, res) => {
  const cacheKey = 'featured_categories';
  
  try {
    // 1. Consultar cache primeiro
    const cachedData = await client.get(cacheKey);
    
    if (cachedData) {
      // Dados encontrados no cache
      return res.json(JSON.parse(cachedData));
    }
    
    // 2. Cache miss - buscar no banco de dados
    const categories = await db.query(`
      SELECT id, name, image_url 
      FROM categories 
      WHERE is_featured = true
    `);
    
    // 3. Armazenar no cache com TTL
    await client.setex(cacheKey, 20, JSON.stringify(categories));
    
    // 4. Retornar dados
    res.json(categories);
    
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

## Invalidação de Cache

### Problema de Consistência
- Dados atualizados no banco não refletem imediatamente no cache
- Necessidade de estratégias de invalidação

### Estratégias de Invalidação

#### 1. TTL (Time To Live)
```javascript
// Cache expira automaticamente após 20 segundos
await client.setex(cacheKey, 20, JSON.stringify(data));
```

**Características:**
- Simples de implementar
- Garante atualização eventual dos dados
- Adequado para dados não críticos

#### 2. Invalidação Manual
- Invalidar cache quando dados são atualizados
- Mais complexo, mas garante consistência imediata

#### 3. Outras Estratégias
- LRU (Least Recently Used)
- LFU (Least Frequently Used)
- Write Through
- Write Behind

## Critérios para Usar Cache

### Dados Adequados para Cache
1. **Muito requisitados** - Alto volume de consultas
2. **Consistência eventual aceitável** - Não precisam ser 100% atualizados em tempo real
3. **Baixa frequência de mudança** - Dados que não mudam constantemente

### Dados Inadequados para Cache
- **Dados financeiros** (saldo bancário, transações)
- **Dados críticos de segurança**
- **Dados que mudam constantemente**
- **Dados que precisam de consistência forte**

## Considerações Importantes

### Recursos de Memória
- Cache consome memória RAM (recurso escasso)
- Não cachear tudo indiscriminadamente
- Monitorar uso de memória
- Balancear performance vs recursos

### Escalabilidade
- Redis pode ser distribuído
- Protocolo RESP (Redis Serialization Protocol) é mais rápido que HTTP
- Possibilidade de arquitetura distribuída para microsserviços

### Monitoramento
- Acompanhar hit rate do cache
- Monitorar tempo de resposta
- Verificar uso de memória
- Alertas para falhas de cache

## Vantagens

1. **Performance** - Reduz drasticamente tempo de resposta
2. **Escalabilidade** - Permite lidar com mais usuários simultâneos
3. **Simplicidade** - Fácil de implementar
4. **Flexibilidade** - Funciona com qualquer linguagem/framework
5. **Custo-benefício** - Solução eficaz sem upgrade de infraestrutura

## Desvantagens

1. **Consistência** - Dados podem estar desatualizados temporariamente
2. **Complexidade** - Necessidade de estratégias de invalidação
3. **Recursos** - Consumo de memória RAM
4. **Debugging** - Mais difícil de debugar problemas de cache

## Casos de Uso Ideais

- **Categorias de produtos** em e-commerce
- **Configurações de sistema** que mudam raramente
- **Dados de referência** (países, estados, moedas)
- **Conteúdo estático** ou semi-estático
- **Resultados de consultas complexas** que são executadas frequentemente

## Conclusão

O Cache Aside Pattern é uma solução arquitetural madura e eficaz para resolver problemas de performance causados por gargalos no banco de dados. É especialmente útil em cenários de alto tráfego onde dados são consultados repetidamente e podem tolerar pequenos atrasos na atualização.

A implementação correta requer análise cuidadosa dos dados a serem cacheados, escolha adequada de estratégias de invalidação e monitoramento contínuo para garantir que os benefícios superem os custos de complexidade e recursos.

---

**Referências:**
- Transcrição de aula sobre Cache Aside Pattern
- Padrões arquiteturais para sistemas de alta performance
- Boas práticas de cache em aplicações web
