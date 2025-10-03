# Template: API Documentation

## 1. Informações Básicas
- **ID da API**: [API-XXX]
- **Nome da API**: [Nome da API]
- **Versão**: [1.0]
- **Data de Criação**: [DD/MM/AAAA]
- **Última Atualização**: [DD/MM/AAAA]
- **Autor**: [Nome do Desenvolvedor/Arquiteto]
- **Status**: [Rascunho/Em Revisão/Aprovado/Deprecated]

## 2. Visão Geral
[Breve descrição da API, seu propósito, funcionalidades principais e como ela se encaixa na arquitetura geral do sistema.]

## 3. Informações de Acesso
- **Base URL**: `https://api.exemplo.com/v1`
- **Protocolo**: HTTPS
- **Autenticação**: [Bearer Token, API Key, OAuth 2.0, etc.]
- **Rate Limiting**: [Limites de requisições por minuto/hora]
- **Formato de Dados**: JSON

## 4. Autenticação
[Descreva como autenticar com a API.]

### 4.1. Método de Autenticação
[Ex: Bearer Token, API Key, OAuth 2.0]

### 4.2. Como Obter Credenciais
[Passos para obter credenciais de acesso]

### 4.3. Exemplo de Uso
```bash
# Exemplo de autenticação
curl -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     https://api.exemplo.com/v1/endpoint
```

## 5. Endpoints da API

### 5.1. [Nome do Endpoint 1]
**URL**: `GET /v1/endpoint1`
**Descrição**: [Descrição do que este endpoint faz]

#### Parâmetros
| Nome | Tipo | Obrigatório | Descrição | Exemplo |
|------|------|-------------|-----------|---------|
| param1 | string | Sim | Descrição do parâmetro | "valor_exemplo" |
| param2 | integer | Não | Descrição do parâmetro | 123 |

#### Resposta de Sucesso (200)
```json
{
  "status": "success",
  "data": {
    "id": 123,
    "name": "Exemplo",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "message": "Operação realizada com sucesso"
}
```

#### Resposta de Erro (400)
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Parâmetro inválido",
    "details": "O parâmetro 'param1' é obrigatório"
  }
}
```

#### Exemplo de Uso
```bash
curl -X GET "https://api.exemplo.com/v1/endpoint1?param1=valor" \
     -H "Authorization: Bearer YOUR_TOKEN"
```

### 5.2. [Nome do Endpoint 2]
**URL**: `POST /v1/endpoint2`
**Descrição**: [Descrição do que este endpoint faz]

#### Parâmetros do Body
```json
{
  "field1": "string",
  "field2": 123,
  "field3": {
    "nested_field": "value"
  }
}
```

#### Resposta de Sucesso (201)
```json
{
  "status": "success",
  "data": {
    "id": 456,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "message": "Recurso criado com sucesso"
}
```

#### Exemplo de Uso
```bash
curl -X POST "https://api.exemplo.com/v1/endpoint2" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"field1": "valor", "field2": 123}'
```

## 6. Códigos de Status HTTP
| Código | Descrição | Quando Usar |
|--------|-----------|-------------|
| 200 | OK | Requisição bem-sucedida |
| 201 | Created | Recurso criado com sucesso |
| 400 | Bad Request | Parâmetros inválidos |
| 401 | Unauthorized | Token inválido ou ausente |
| 403 | Forbidden | Acesso negado |
| 404 | Not Found | Recurso não encontrado |
| 429 | Too Many Requests | Rate limit excedido |
| 500 | Internal Server Error | Erro interno do servidor |

## 7. Modelos de Dados

### 7.1. [Nome do Modelo 1]
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 7.2. [Nome do Modelo 2]
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "status": "enum",
  "user_id": "integer"
}
```

## 8. Tratamento de Erros

### 8.1. Formato de Erro
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Mensagem de erro legível",
    "details": "Detalhes adicionais do erro",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

### 8.2. Códigos de Erro Comuns
| Código | Descrição | Solução |
|--------|-----------|---------|
| INVALID_TOKEN | Token inválido | Verificar token de autenticação |
| MISSING_PARAMETER | Parâmetro obrigatório ausente | Incluir parâmetro na requisição |
| INVALID_FORMAT | Formato de dados inválido | Verificar formato JSON |
| RATE_LIMIT_EXCEEDED | Limite de requisições excedido | Aguardar ou reduzir frequência |

## 9. Rate Limiting
- **Limite**: 1000 requisições por hora
- **Headers de Resposta**:
  - `X-RateLimit-Limit`: Limite total
  - `X-RateLimit-Remaining`: Requisições restantes
  - `X-RateLimit-Reset`: Timestamp de reset

## 10. Versionamento
- **Estratégia**: URL versioning (`/v1/`, `/v2/`)
- **Deprecação**: 6 meses de aviso
- **Suporte**: 2 versões anteriores

## 11. SDKs e Bibliotecas
- **JavaScript**: `npm install api-client`
- **Python**: `pip install api-client`
- **Java**: `Maven/Gradle dependency`
- **PHP**: `composer require api-client`

## 12. Exemplos de Integração

### 12.1. JavaScript/Node.js
```javascript
const ApiClient = require('api-client');

const client = new ApiClient({
  baseURL: 'https://api.exemplo.com/v1',
  token: 'YOUR_TOKEN'
});

// Exemplo de uso
client.get('/endpoint1', { param1: 'valor' })
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

### 12.2. Python
```python
import requests

headers = {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.exemplo.com/v1/endpoint1',
    headers=headers,
    params={'param1': 'valor'}
)

print(response.json())
```

### 12.3. cURL
```bash
# GET request
curl -X GET "https://api.exemplo.com/v1/endpoint1" \
     -H "Authorization: Bearer YOUR_TOKEN"

# POST request
curl -X POST "https://api.exemplo.com/v1/endpoint2" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"field1": "valor"}'
```

## 13. Changelog
| Versão | Data | Mudanças |
|--------|------|----------|
| 1.0 | DD/MM/AAAA | Versão inicial |
| 1.1 | DD/MM/AAAA | Adicionado endpoint X |
| 1.2 | DD/MM/AAAA | Corrigido bug Y |

## 14. Suporte
- **Email**: api-support@exemplo.com
- **Documentação**: https://docs.exemplo.com
- **Status**: https://status.exemplo.com
- **Issues**: https://github.com/exemplo/api/issues

## 15. Aprovações
- **Desenvolvedor**: [Nome] - [Assinatura/Data]
- **Arquiteto**: [Nome] - [Assinatura/Data]
- **Product Owner**: [Nome] - [Assinatura/Data]

---

**Referências**:
- [Link para TRD relacionado]
- [Link para System Design]
- [Link para ADRs relevantes]

**Histórico de Revisões**:
| Versão | Data | Autor | Descrição da Mudança |
|--------|------|-------|----------------------|
| 1.0    | DD/MM/AAAA | [Autor] | Criação inicial da API Documentation |
