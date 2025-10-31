# Detalhes de Implementação - Encurtador de URL (PT-BR)

> **Versão em Inglês**: [English Version](../implementation-details.md)

---

## Visão Geral

Este documento detalha a abordagem de implementação para gerar códigos curtos únicos, evitar colisões e garantir segurança.

## Geração de Código Curto

### Declaração do Problema

Precisamos gerar um código curto único para cada URL sem:
- Colisões de hash (mesmo código para URLs diferentes)
- Padrões previsíveis (risco de segurança)
- Consultas ao banco durante geração (performance)

### Abordagem 1: Funções Hash (❌ Não Recomendado)

#### Por que Funções Hash Falham

1. **Base Errada**
   - Funções hash (MD5, SHA1, CRC32) trabalham com Base 16 (0-9, A-F)
   - Viola nosso requisito para Base 62
   - Resulta em códigos curtos mais longos do que necessário

2. **Risco de Colisão**
   - URLs diferentes podem gerar o mesmo hash
   - Truncar hashes aumenta probabilidade de colisão
   - Requereria consultas ao banco para verificar unicidade

3. **Impacto na Performance**
   - Toda geração requer verificação no banco
   - Colisões aumentam exponencialmente com o tempo (Paradoxo do Aniversário)
   - Com 2.21 milhões de URLs, colisões tornam-se prováveis

4. **Paradoxo do Aniversário**
   - Mesmo com 3.5 trilhões de possibilidades
   - Colisões aparecem após ~2.21 milhões de URLs
   - Dado 100M URLs/dia, colisões ocorrem em minutos

#### Conclusão
Funções hash **não são adequadas** para encurtamento de URL devido a riscos de colisão e impacto na performance.

### Abordagem 2: Conversão Base 62 (✅ Recomendado)

#### Conceito

Converter um ID inteiro único para representação Base 62.

#### Conjunto de Caracteres Base 62

```
0-9  : 10 caracteres
a-z  : 26 caracteres
A-Z  : 26 caracteres
Total: 62 caracteres
```

**Mapeamento**:
- 0 → '0'
- 1 → '1'
- ...
- 9 → '9'
- 10 → 'A'
- 11 → 'B'
- ...
- 35 → 'Z'
- 36 → 'a'
- 37 → 'b'
- ...
- 61 → 'z'

#### Algoritmo de Conversão

**Exemplo**: Converter 11.157 para Base 62

```
Passo 1: 11.157 ÷ 62 = 179 resto 59
Passo 2: 179 ÷ 62 = 2 resto 55
Passo 3: 2 ÷ 62 = 0 resto 2

Restos (ordem reversa): 2, 55, 59

Mapeamento:
2  → '2'
55 → 'T'
59 → 'X'

Resultado: 11.157 em Base 62 = "2TX"
```

#### Implementação (Python)

```python
import base62

def encode_to_base62(numero_decimal):
    """Converter número decimal para Base 62"""
    return base62.encode(numero_decimal)

def decode_from_base62(string_base62):
    """Converter string Base 62 de volta para decimal"""
    return base62.decode(string_base62)

# Exemplo
short_code = encode_to_base62(11157)  # Retorna "2TX"
original_id = decode_from_base62("2TX")  # Retorna 11157
```

#### Vantagens

1. **Zero Colisões**: Cada ID mapeia para exatamente uma representação Base 62
2. **Sem Consulta ao Banco**: Conversão direta, sem verificação
3. **Determinístico**: Mesmo ID sempre produz mesmo código
4. **Reversível**: Pode decodificar código curto de volta para ID original

#### Valor ID Inicial

**Consideração de Segurança**: Começar do ID 1 torna códigos previsíveis.

**Solução**: Começar de um valor alto inicial (ex.: 14 milhões)
- 62^4 = ~14.7 milhões de combinações
- Começar em 14M garante códigos com pelo menos 4 caracteres
- Previne adivinhação fácil de URLs

**Configuração**:
```python
ID_INICIAL = 14_000_000  # Começar de 14 milhões
```

### Abordagem 3: Base 62 com Ofuscação de ID (✅ Recomendado para Produção)

#### Problema com IDs Sequenciais

Se IDs são sequenciais (1, 2, 3, 4...), o padrão torna-se óbvio:
- Fácil adivinhar próximas URLs
- Risco de segurança para URLs privadas
- Atacantes podem enumerar todas as URLs

#### Solução: HashID com Segredo

Use biblioteca como `hashids` para ofuscar a codificação Base 62.

**Implementação**:
```python
from hashids import Hashids

# Criar instância HashID com chave secreta
hashids = Hashids(
    salt='sua-chave-secreta-aqui',
    min_length=4,
    alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
)

def encode_id_com_ofuscacao(id_decimal):
    """Codificar ID com ofuscação"""
    return hashids.encode(id_decimal)

def decode_id_de_ofuscacao(codigo_ofuscado):
    """Decodificar código ofuscado de volta para ID"""
    decoded = hashids.decode(codigo_ofuscado)
    return decoded[0] if decoded else None

# Exemplo
ofuscado = encode_id_com_ofuscacao(11157)  # Retorna "CJ0" (não "2TX")
original_id = decode_id_de_ofuscacao("CJ0")  # Retorna 11157
```

#### Como Funciona

1. Usa chave secreta para embaralhar alfabeto Base 62
2. Mesmo ID sempre produz mesmo código ofuscado (determinístico)
3. Sem chave secreta, não pode fazer engenharia reversa do padrão
4. Mesma chave secreta = mesmo padrão de embaralhamento

#### Benefícios de Segurança

- **Quebra de Padrões**: IDs sequenciais produzem códigos não sequenciais
- **Dependente de Segredo**: Apenas com chave secreta códigos podem ser decodificados
- **Não Previsível**: Não pode adivinhar próxima URL sem segredo

## Esquema do Banco de Dados

### Estrutura da Tabela Cassandra

```cql
CREATE TABLE url_shortener (
    short_code TEXT PRIMARY KEY,
    long_url TEXT,
    created_at TIMESTAMP
) WITH CLUSTERING ORDER BY (created_at DESC);
```

**Por que Cassandra?**
- Escalabilidade horizontal
- Lida com bilhões de registros
- Alto throughput de escrita
- Replicação integrada para disponibilidade
- Leituras de baixa latência

### Redis para Geração de ID

**Comando**: `INCR counter`

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379)

def get_next_id():
    """Obter próximo ID único do Redis"""
    return redis_client.incr('url_counter')
```

**Configuração**:
```python
# Definir valor inicial
redis_client.set('url_counter', 14_000_000)
```

**Por que Redis?**
- Operação de incremento atômica (sem condições de corrida)
- Extremamente rápido (em memória)
- Suporta clustering para alta disponibilidade

**Configuração de Alta Disponibilidade**:
- Modo Redis Cluster
- Ou Redis Sentinel para failover automático
- Garante disponibilidade 24x7

## Fluxo Completo

### Fluxo de Encurtamento de URL

```
1. Cliente envia POST /api/v1/shorten com URL longa
2. Backend recebe requisição
3. Obter próximo ID do Redis (operação INCR)
4. Converter ID para Base 62 (com ofuscação se habilitada)
5. Armazenar no Cassandra: short_code → long_url
6. Retornar URL curta para cliente
```

### Fluxo de Redirecionamento de URL

```
1. Cliente solicita GET /{shortCode}
2. Backend recebe requisição
3. Verificar cache Redis primeiro (para URLs populares)
4. Se não estiver em cache, consultar Cassandra
5. Se encontrado, armazenar em cache e retornar redirecionamento
6. Retornar 301 ou 302 com header Location
```

## Principais Takeaways

1. **Evite Funções Hash**: Use conversão Base 62
2. **Começar Alto**: Iniciar sequência de ID a partir de 14M+ por segurança
3. **Ofuscar**: Usar HashID com chave secreta para prevenir detecção de padrão
4. **Sem Verificações no Banco**: Conversão direta elimina verificações de colisão
5. **Operações Atômicas**: Redis INCR garante IDs únicos entre instâncias

---

**Documentos Relacionados**:
- [Design de Arquitetura](architecture-design.pt-br.md)
- [Considerações de Segurança](security-considerations.pt-br.md)

**Última Atualização**: Janeiro 2025
**Mantenedor**: Equipe Skynet

