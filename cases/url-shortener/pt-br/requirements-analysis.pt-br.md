# Análise de Requisitos - Encurtador de URL (PT-BR)

> **Versão em Inglês**: [English Version](../requirements-analysis.md)

---

## Visão Geral

Antes de projetar qualquer arquitetura, é crítico entender e estabelecer requisitos. Este documento descreve os requisitos funcionais e não funcionais para um sistema encurtador de URL.

## Requisitos Funcionais

### 1. Encurtamento de URL
**Descrição**: O sistema deve ser capaz de encurtar uma URL longa em uma URL curta.

**Endpoint**: `POST /api/v1/shorten`

**Requisição**:
```json
{
  "url": "https://example.com/url/muito/longa/com/muitos/parametros"
}
```

**Resposta**: `201 Created`
```json
{
  "shortUrl": "https://bit.ly/2tx"
}
```

### 2. Redirecionamento de URL
**Descrição**: Quando uma URL curta é acessada, o sistema deve redirecionar o usuário para a URL original.

**Endpoint**: `GET /{shortCode}`

**Resposta**: `301 Moved Permanently` ou `302 Found`
```
Location: https://example.com/url/muito/longa/com/muitos/parametros
```

## Requisitos Não Funcionais

### 1. Capacidade de Volume
- **Requisito**: Sistema deve suportar 100 milhões de URLs geradas por dia
- **Detalhamento**:
  - 100.000.000 URLs / 24 horas / 60 minutos / 60 segundos
  - **Operações de Escrita**: ~1.160 requisições por segundo
  - **Operações de Leitura**: ~11.600 requisições por segundo (proporção 10:1)

### 2. Comprimento do Código Curto
- **Requisito**: Código curto deve ser o mais curto possível
- **Restrição**: Apenas números 0-9, letras minúsculas a-z e letras maiúsculas A-Z são permitidos (Base 62)
- **Resultado do Cálculo**: 7 caracteres mínimos para 365 bilhões de combinações únicas

### 3. Restrição de Conjunto de Caracteres
- **Permitido**: 0-9, a-z, A-Z (62 caracteres no total - Base 62)
- **Não Permitido**: Caracteres especiais que podem causar problemas em URLs

### 4. Proporção Leitura-Escrita
- **Requisito**: Para cada operação de escrita, haverão 10 operações de leitura
- **Racionalização**: Esta é a média para a maioria das aplicações do mundo real
- **Impacto**: Arquitetura deve ser otimizada para cargas de trabalho com muitas leituras

### 5. Tamanho de Armazenamento de URL
- **Comprimento Médio**: 100 bytes por URL armazenada no banco de dados
- **Propósito**: Usado para cálculos de capacidade

### 6. Retenção de Dados
- **Requisito**: URLs devem ser armazenadas por 10 anos
- **Cálculo de Armazenamento Total**:
  - 100 milhões de URLs/dia × 365 dias × 10 anos = 365 bilhões de registros
  - 365 bilhões × 100 bytes = 36.5 TB de armazenamento

### 7. Alta Disponibilidade
- **Requisito**: Sistema deve operar em modo de alta disponibilidade 24x7
- **Impacto**: Nenhum ponto único de falha, redundância necessária em todas as camadas

## Resumo de Cálculos

### Throughput
| Métrica | Valor |
|---------|-------|
| URLs por dia | 100.000.000 |
| Operações de escrita/seg | ~1.160 |
| Operações de leitura/seg | ~11.600 |
| Proporção Leitura:Escrita | 10:1 |

### Armazenamento
| Métrica | Valor |
|---------|-------|
| Registros em 10 anos | 365 bilhões |
| Tamanho médio de URL | 100 bytes |
| Armazenamento total necessário | 36.5 TB |

### Especificações do Código Curto
| Métrica | Valor |
|---------|-------|
| Conjunto de caracteres | Base 62 (0-9, a-z, A-Z) |
| Comprimento mínimo | 7 caracteres |
| Total de combinações | 3.5 trilhões |

## Perguntas-Chave para Cenários de Entrevista

Ao se deparar com uma entrevista de system design, faça estas perguntas:

1. **Volume de Tráfego**
   - Qual é o volume diário de tráfego?
   - Quais são os padrões de tráfego de pico?

2. **Proporção de Operações**
   - Qual é a proporção leitura:escrita?
   - Como as operações variam ao longo do dia?

3. **Requisitos de Armazenamento**
   - Por quanto tempo os dados devem ser retidos?
   - Qual é o tamanho médio dos dados armazenados?

4. **Requisitos de Disponibilidade**
   - Qual é o tempo de inatividade aceitável?
   - Quais são os SLAs?

5. **Requisitos de Segurança**
   - Existem preocupações de privacidade?
   - Os códigos curtos devem ser previsíveis ou ofuscados?

## Arquitetura Orientada por Requisitos

> **Princípio Crítico**: Todas as decisões arquiteturais devem ser baseadas em requisitos. Sem requisitos claros, qualquer arquitetura será baseada em chute.

### Árvore de Decisão

1. **Alto Volume** → Requer escalamento horizontal, não vertical
2. **Muitas Leituras** → Camada de cache é essencial
3. **Armazenamento Grande** → Escolha do banco de dados crítica (Cassandra para escalamento horizontal)
4. **Alta Disponibilidade** → Redundância em todas as camadas
5. **Códigos Curtos Únicos** → Requer seleção cuidadosa de algoritmo

## Próximos Passos

Após estabelecer requisitos:
1. Calcular todas as métricas necessárias (throughput, armazenamento, etc.)
2. Escolher tecnologias apropriadas baseadas nos requisitos
3. Projetar padrões arquiteturais (cache, load balancing, etc.)
4. Planejar escalabilidade e alta disponibilidade

---

**Documentos Relacionados**:
- [Design de Arquitetura](architecture-design.pt-br.md)
- [Detalhes de Implementação](implementation-details.pt-br.md)

**Última Atualização**: Janeiro 2025
**Mantenedor**: Equipe Skynet
