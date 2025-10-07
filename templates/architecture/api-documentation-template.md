# Template: Documentação de APIs

## 📋 **Informações do Documento**
- **Tipo**: Template de Documentação
- **Categoria**: APIs
- **Versão**: 1.0
- **Data**: [DATA_ATUAL]
- **Autor**: [AUTOR]
- **Revisado por**: [REVISOR]

## 🎯 **Visão Geral**

Este template fornece uma estrutura completa para documentar APIs, incluindo especificações técnicas, exemplos de uso, e guias de integração.

## 📐 **Estrutura do Template**

### **1. Informações Gerais**
```markdown
# [Nome da API]

## Informações Gerais
- **Versão**: [v1.0.0]
- **Base URL**: [https://api.exemplo.com/v1]
- **Formato**: [JSON]
- **Autenticação**: [Bearer Token, API Key, OAuth 2.0]
- **Rate Limiting**: [1000 requests/hour]
- **Suporte**: [support@exemplo.com]

## Changelog
| Versão | Data | Mudanças |
|--------|------|----------|
| v1.0.0 | 2024-01-01 | Versão inicial |
```

### **2. Autenticação**
```markdown
## Autenticação

### Métodos Suportados
- **Bearer Token**: Para autenticação de usuários
- **API Key**: Para autenticação de aplicações
- **OAuth 2.0**: Para autenticação de terceiros

### Exemplo de Uso
```bash
# Bearer Token
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.exemplo.com/v1/users

# API Key
curl -H "X-API-Key: YOUR_API_KEY" \
     https://api.exemplo.com/v1/users
```

### OAuth 2.0 Flow
1. **Authorization Code Flow**
2. **Client Credentials Flow**
3. **Refresh Token Flow**
```

### **3. Endpoints**
```markdown
## Endpoints

### [GET] /users
**Descrição**: Lista todos os usuários

**Parâmetros de Query**:
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| page | integer | Não | Número da página (padrão: 1) |
| limit | integer | Não | Itens por página (padrão: 20) |
| search | string | Não | Termo de busca |

**Resposta de Sucesso** (200):
```json
{
  "data": [
    {
      "id": 1,
      "name": "João Silva",
      "email": "joao@exemplo.com",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

**Resposta de Erro** (400):
```json
{
  "error": {
    "code": "INVALID_PARAMETERS",
    "message": "Parâmetros inválidos",
    "details": {
      "page": "Deve ser um número inteiro positivo"
    }
  }
}
```

### [POST] /users
**Descrição**: Cria um novo usuário

**Body**:
```json
{
  "name": "João Silva",
  "email": "joao@exemplo.com",
  "password": "senha123"
}
```

**Resposta de Sucesso** (201):
```json
{
  "data": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@exemplo.com",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### [GET] /users/{id}
**Descrição**: Obtém um usuário específico

**Parâmetros de Path**:
| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| id | integer | Sim | ID do usuário |

**Resposta de Sucesso** (200):
```json
{
  "data": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@exemplo.com",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### [PUT] /users/{id}
**Descrição**: Atualiza um usuário

**Body**:
```json
{
  "name": "João Silva Atualizado",
  "email": "joao.novo@exemplo.com"
}
```

### [DELETE] /users/{id}
**Descrição**: Remove um usuário

**Resposta de Sucesso** (204):
```
(No content)
```
```

### **4. Modelos de Dados**
```markdown
## Modelos de Dados

### User
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@exemplo.com",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Error
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Descrição do erro",
    "details": {}
  }
}
```

### Pagination
```json
{
  "page": 1,
  "limit": 20,
  "total": 100,
  "pages": 5
}
```
```

### **5. Códigos de Status**
```markdown
## Códigos de Status HTTP

### Sucesso
- **200 OK**: Requisição bem-sucedida
- **201 Created**: Recurso criado com sucesso
- **204 No Content**: Requisição bem-sucedida sem conteúdo

### Erro do Cliente
- **400 Bad Request**: Parâmetros inválidos
- **401 Unauthorized**: Não autenticado
- **403 Forbidden**: Sem permissão
- **404 Not Found**: Recurso não encontrado
- **422 Unprocessable Entity**: Dados inválidos

### Erro do Servidor
- **500 Internal Server Error**: Erro interno
- **502 Bad Gateway**: Erro de gateway
- **503 Service Unavailable**: Serviço indisponível
```

### **6. Rate Limiting**
```markdown
## Rate Limiting

### Limites
- **Geral**: 1000 requests/hour
- **Autenticação**: 10 requests/minute
- **Upload**: 100 requests/hour

### Headers de Resposta
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

### Exemplo de Resposta (429)
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "retry_after": 3600
  }
}
```
```

### **7. Exemplos de Uso**
```markdown
## Exemplos de Uso

### JavaScript/Node.js
```javascript
const axios = require('axios');

const api = axios.create({
  baseURL: 'https://api.exemplo.com/v1',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  }
});

// Listar usuários
const users = await api.get('/users', {
  params: { page: 1, limit: 10 }
});

// Criar usuário
const newUser = await api.post('/users', {
  name: 'João Silva',
  email: 'joao@exemplo.com',
  password: 'senha123'
});
```

### Python
```python
import requests

headers = {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
}

# Listar usuários
response = requests.get(
    'https://api.exemplo.com/v1/users',
    headers=headers,
    params={'page': 1, 'limit': 10}
)

# Criar usuário
response = requests.post(
    'https://api.exemplo.com/v1/users',
    headers=headers,
    json={
        'name': 'João Silva',
        'email': 'joao@exemplo.com',
        'password': 'senha123'
    }
)
```

### cURL
```bash
# Listar usuários
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://api.exemplo.com/v1/users?page=1&limit=10"

# Criar usuário
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name":"João Silva","email":"joao@exemplo.com","password":"senha123"}' \
     "https://api.exemplo.com/v1/users"
```
```

### **8. Webhooks**
```markdown
## Webhooks

### Eventos Suportados
- **user.created**: Usuário criado
- **user.updated**: Usuário atualizado
- **user.deleted**: Usuário removido

### Configuração
```json
{
  "url": "https://seu-site.com/webhook",
  "events": ["user.created", "user.updated"],
  "secret": "webhook_secret"
}
```

### Payload do Webhook
```json
{
  "event": "user.created",
  "data": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@exemplo.com"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Verificação de Assinatura
```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signature, secret) {
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  
  return signature === expectedSignature;
}
```
```

### **9. SDKs e Bibliotecas**
```markdown
## SDKs e Bibliotecas

### JavaScript/Node.js
```bash
npm install @exemplo/api-client
```

```javascript
const { ExemploAPI } = require('@exemplo/api-client');

const api = new ExemploAPI({
  apiKey: 'YOUR_API_KEY',
  baseURL: 'https://api.exemplo.com/v1'
});

const users = await api.users.list();
const user = await api.users.create({
  name: 'João Silva',
  email: 'joao@exemplo.com'
});
```

### Python
```bash
pip install exemplo-api-client
```

```python
from exemplo_api import ExemploAPI

api = ExemploAPI(api_key='YOUR_API_KEY')

users = api.users.list()
user = api.users.create(
    name='João Silva',
    email='joao@exemplo.com'
)
```
```

### **10. Troubleshooting**
```markdown
## Troubleshooting

### Problemas Comuns

#### 401 Unauthorized
- Verificar se o token está correto
- Verificar se o token não expirou
- Verificar se o token tem as permissões necessárias

#### 429 Rate Limit Exceeded
- Verificar os headers de rate limit
- Implementar retry com backoff exponencial
- Considerar upgrade do plano

#### 500 Internal Server Error
- Verificar se o serviço está funcionando
- Verificar os logs do servidor
- Contatar o suporte se persistir

### Debugging
```bash
# Verificar conectividade
curl -I https://api.exemplo.com/v1/health

# Verificar headers de resposta
curl -v https://api.exemplo.com/v1/users

# Verificar rate limit
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.exemplo.com/v1/users \
     -D headers.txt
```
```

### **11. Changelog**
```markdown
## Changelog

### v1.1.0 - 2024-02-01
- Adicionado endpoint `/users/{id}/avatar`
- Adicionado suporte a webhooks
- Melhorado rate limiting

### v1.0.0 - 2024-01-01
- Versão inicial da API
- Endpoints básicos de usuários
- Autenticação por Bearer Token
```

## 📊 **Checklist de Documentação**

### **Conteúdo Obrigatório**
- [ ] Informações gerais da API
- [ ] Métodos de autenticação
- [ ] Documentação de todos os endpoints
- [ ] Modelos de dados
- [ ] Códigos de status HTTP
- [ ] Exemplos de uso
- [ ] Rate limiting
- [ ] Changelog

### **Conteúdo Opcional**
- [ ] Webhooks
- [ ] SDKs e bibliotecas
- [ ] Troubleshooting
- [ ] Testes de integração
- [ ] Postman collection
- [ ] OpenAPI/Swagger spec

## 🔗 **Recursos Adicionais**

### **Ferramentas Recomendadas**
- [Swagger/OpenAPI](https://swagger.io/)
- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- [API Blueprint](https://apiblueprint.org/)

### **Referências**
- [REST API Design Guide](https://restfulapi.net/)
- [API Design Best Practices](https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design)
- [OpenAPI Specification](https://swagger.io/specification/)

---

**Última atualização**: [DATA]
**Mantenedor**: [EQUIPE]
**Próxima revisão**: [DATA]
