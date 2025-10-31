# Considerações de Segurança - Encurtador de URL (PT-BR)

> **Versão em Inglês**: [English Version](../security-considerations.md)

---

## Visão Geral

Segurança em encurtadores de URL envolve prevenir enumeração de URLs, proteger URLs privadas e garantir que o sistema não possa ser abusado.

## Principais Preocupações de Segurança

### 1. Códigos Curtos Previsíveis

#### Problema

Se códigos curtos são gerados sequencialmente a partir do ID 1, tornam-se previsíveis:
- Código curto para ID 1: "1" (ou "2TX" em base 62)
- Código curto para ID 2: "2" (ou próximo na sequência)
- Atacantes podem enumerar todas as URLs

#### Cenário de Ataque

```python
# Atacante pode adivinhar URLs
for i in range(1, 1000000):
    short_code = encode_base62(i)
    url = f"https://bit.ly/{short_code}"
    # Tentar acessar URL
```

#### Solução: Começar de Valor Inicial Alto

```python
ID_INICIAL = 14_000_000  # 62^4 = ~14.7M combinações

# Garante:
# - Mínimo 4 caracteres no código curto
# - Não pode enumerar desde o início
# - Requer testar 14M+ combinações
```

**Cálculo**:
- 62^4 = 14.776.336 combinações
- Começar em 14M garante mínimo de 4 caracteres
- Torna enumeração impraticável

### 2. Detecção de Padrão Sequencial

#### Problema

Mesmo com ID inicial alto, padrões sequenciais são detectáveis:

```
ID: 14.000.000 → Código: "abc1"
ID: 14.000.001 → Código: "abc2"
ID: 14.000.002 → Código: "abc3"
```

Padrão torna-se óbvio após alguns exemplos.

#### Solução: Ofuscação de ID (HashID)

Use biblioteca como `hashids` para embaralhar a codificação Base 62:

```python
from hashids import Hashids

hashids = Hashids(
    salt='chave-secreta-conhecida-apenas-pelo-servidor',
    min_length=4,
    alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
)

# IDs sequenciais produzem códigos não sequenciais
hashids.encode(14000000)  # Retorna: "CJ0"
hashids.encode(14000001)  # Retorna: "X9K"
hashids.encode(14000002)  # Retorna: "L2P"
```

#### Como Funciona

1. **Chave Secreta**: Servidor usa segredo para embaralhar alfabeto
2. **Determinístico**: Mesmo ID sempre produz mesmo código
3. **Não Reversível**: Sem segredo, não pode determinar padrão
4. **Quebra de Padrão**: IDs sequenciais → Códigos não sequenciais

### 3. Gerenciamento de Chave Secreta

#### Requisitos

- **Armazenamento**: Variáveis de ambiente ou serviço de gerenciamento de segredos
- **Rotação**: Planejar estratégia de rotação de chave
- **Backup**: Backup seguro (perder chave quebra URLs existentes)

```python
import os

CHAVE_SECRETA = os.environ.get('URL_SHORTENER_SECRET_KEY')
if not CHAVE_SECRETA:
    raise ValueError("Chave secreta deve ser definida")
```

#### Estratégia de Rotação de Chave

**Desafio**: Mudar segredo quebra todas as URLs existentes

**Soluções**:
1. **Suporte Multi-Segredo**: Suportar múltiplos segredos (antigo + novo)
2. **Período de Migração**: Transição gradual com ambos os segredos ativos
3. **Armazenamento no Banco**: Armazenar ID original, regenerar códigos se necessário

### 4. Validação e Filtragem de URL

#### URLs Maliciosas

Prevenir abuso validando URLs:

```python
from urllib.parse import urlparse

def validar_url(url: str) -> bool:
    """Validar URL antes de encurtar"""
    try:
        result = urlparse(url)
        
        # Deve ter scheme
        if not result.scheme:
            return False
        
        # Deve ser HTTP/HTTPS
        if result.scheme not in ['http', 'https']:
            return False
        
        # Deve ter netloc (domínio)
        if not result.netloc:
            return False
        
        # Bloquear URLs internas/localhost
        if result.netloc in ['localhost', '127.0.0.1', '0.0.0.0']:
            return False
        
        # Verificar padrões maliciosos
        patterns_maliciosos = [
            'javascript:',
            'data:',
            'vbscript:',
            'file:'
        ]
        
        if any(pattern in url.lower() for pattern in patterns_maliciosos):
            return False
        
        return True
    
    except Exception:
        return False
```

### 5. Rate Limiting

#### Proteção Contra Abuso

Implementar rate limiting para prevenir:
- Ataques DDoS
- Geração automatizada de URLs
- Esgotamento de recursos

```python
from redis import Redis
import time

redis_client = Redis()

def verificar_rate_limit(ip_usuario: str, limite: int = 100, janela: int = 3600) -> bool:
    """Verificar se usuário excedeu limite de taxa"""
    chave = f"rate_limit:{ip_usuario}"
    
    atual = redis_client.incr(chave)
    
    if atual == 1:
        redis_client.expire(chave, janela)
    
    return atual <= limite
```

**Configuração**:
- **Limite**: 100 URLs por hora por IP
- **Janela**: 1 hora de janela deslizante
- **Modo Estrito**: Bloquear após limite excedido
- **Modo Suave**: Retornar respostas mais lentas

### 6. Proteção de URL Privada

#### Requisito

Algumas URLs devem ser privadas e não descobríveis.

#### Soluções

##### Opção 1: Códigos Curtos Customizados
Permitir que usuários especifiquem seus próprios códigos (com validação):

```python
def criar_codigo_curto_customizado(codigo_usuario: str) -> bool:
    """Permitir usuário criar código curto customizado"""
    # Validar formato
    if not re.match(r'^[a-zA-Z0-9]{4,7}$', codigo_usuario):
        return False
    
    # Verificar disponibilidade
    if codigo_existe(codigo_usuario):
        return False
    
    return True
```

##### Opção 2: Autenticação Obrigatória
Requerer autenticação para criação de URL:

```python
def encurtar_url(url_longa: str, id_usuario: int) -> str:
    """Criar URL curta com associação de usuário"""
    url_id = obter_proximo_id()
    codigo_curto = codificar_com_ofuscacao(url_id)
    
    # Armazenar com associação de usuário
    armazenar_url(codigo_curto, url_longa, id_usuario)
    
    return codigo_curto
```

##### Opção 3: Expiração e Controle de Acesso
Adicionar expiração e controles de acesso:

```python
def encurtar_url_com_expiração(
    url_longa: str,
    expira_em_dias: int = None,
    senha: str = None
) -> str:
    """Criar URL com expiração opcional e senha"""
    codigo_curto = criar_codigo_curto()
    
    metadata = {
        'url_longa': url_longa,
        'criado_em': datetime.now(),
        'expira_em': datetime.now() + timedelta(days=expira_em_dias) if expira_em_dias else None,
        'senha': hash_senha(senha) if senha else None
    }
    
    armazenar_url(codigo_curto, metadata)
    return codigo_curto
```

### 7. Forçar HTTPS

#### Requisito

Todas as comunicações devem ser criptografadas.

**Configuração**:
- Forçar redirecionamentos HTTPS
- Headers HSTS
- Certificados SSL/TLS

```python
# Exemplo de middleware
@app.before_request
def force_https():
    if request.headers.get('X-Forwarded-Proto') == 'http':
        return redirect(request.url.replace('http://', 'https://'), 301)
```

### 8. Sanitização de Entrada

#### Prevenir Ataques de Injeção

```python
def sanitizar_url(url: str) -> str:
    """Sanitizar entrada de URL"""
    # Remover caracteres de controle
    url = ''.join(char for char in url if ord(char) >= 32)
    
    # Limitar comprimento
    if len(url) > 2048:
        raise ValueError("URL muito longa")
    
    # Validar encoding
    try:
        url.encode('utf-8')
    except UnicodeEncodeError:
        raise ValueError("Encoding de URL inválido")
    
    return url
```

## Checklist de Segurança

### Antes da Produção

- [ ] Chave secreta armazenada com segurança (não no código)
- [ ] HTTPS forçado
- [ ] Rate limiting implementado
- [ ] Validação de URL ativa
- [ ] Sanitização de entrada
- [ ] Monitoramento e alertas
- [ ] Logs de acesso habilitados
- [ ] Headers de segurança configurados
- [ ] Auditorias de segurança regulares
- [ ] Plano de resposta a incidentes

### Contínuo

- [ ] Monitorar padrões suspeitos
- [ ] Revisar logs de acesso regularmente
- [ ] Atualizar dependências
- [ ] Aplicar patches de segurança
- [ ] Testes de penetração
- [ ] Treinamento de segurança para equipe

## Resumo de Melhores Práticas de Segurança

1. **Começar Alto**: Iniciar sequência de ID a partir de 14M+ para prevenir enumeração
2. **Ofuscar**: Usar HashID com chave secreta para quebrar padrões sequenciais
3. **Validar**: Verificar todas as URLs antes de encurtar
4. **Limitar**: Implementar rate limiting para prevenir abuso
5. **Criptografar**: Forçar HTTPS em todo lugar
6. **Monitorar**: Rastrear e alertar sobre atividade suspeita
7. **Rotacionar**: Planejar rotação de chave secreta
8. **Sanitizar**: Limpar todas as entradas

---

**Documentos Relacionados**:
- [Detalhes de Implementação](implementation-details.pt-br.md)
- [Design de Arquitetura](architecture-design.pt-br.md)

**Última Atualização**: Janeiro 2025
**Mantenedor**: Equipe Skynet

