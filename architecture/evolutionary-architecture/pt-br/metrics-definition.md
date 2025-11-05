# Guia de Definição de Métricas

## 📋 Visão Geral

Este guia explica como definir e usar métricas para decisões arquiteturais em arquitetura evolutiva. Métricas fornecem medidas objetivas e quantificáveis da saúde arquitetural e guiam decisões de evolução.

**Princípio Fundamental**: Decisões arquiteturais devem ser baseadas em métricas e dados reais, não em especulação.

---

## 🎯 Por que Métricas Importam

### Decisões Baseadas em Dados

Métricas permitem:
- **Avaliação Objetiva**: Medir saúde arquitetural objetivamente
- **Análise de Tendências**: Rastrear evolução ao longo do tempo
- **Detecção Precoce**: Identificar problemas antes que se tornem críticos
- **Decisões Informadas**: Baseadas em dados reais, não em suposições

### Tipos de Métricas Arquiteturais

1. **Métricas Estruturais**: Medem estrutura e organização do código
2. **Métricas de Qualidade**: Medem qualidade e manutenibilidade do código
3. **Métricas de Performance**: Medem performance do sistema
4. **Métricas de Evolução**: Medem quão facilmente a arquitetura pode evoluir
5. **Métricas de Negócio**: Medem entrega de valor de negócio

---

## 📊 Categorias Principais de Métricas

### 1. Métricas de Acoplamento

Acoplamento mede a interdependência entre módulos ou componentes.

#### Acoplamento Aferente (Ca)
**Definição**: Número de módulos que dependem de um módulo dado.

**Medição**:
```typescript
// Exemplo: Contar dependências de entrada
function calcularAcoplamentoAferente(nomeModulo: string): number {
  const todosArquivos = obterTodosArquivosFonte();
  return todosArquivos.filter(arquivo => 
    arquivo.imports.includes(nomeModulo)
  ).length;
}
```

**Meta**: Menor é melhor, mas alguns módulos (como core domain) devem ter Ca maior.

#### Acoplamento Eferente (Ce)
**Definição**: Número de módulos dos quais um módulo dado depende.

**Medição**:
```typescript
// Exemplo: Contar dependências de saída
function calcularAcoplamentoEferente(caminhoModulo: string): number {
  const modulo = parsearModulo(caminhoModulo);
  return modulo.imports.length;
}
```

**Meta**: Menor é melhor. Módulos com Ce alto são fortemente acoplados.

#### Instabilidade (I)
**Definição**: Razão de acoplamento eferente para acoplamento total.

**Fórmula**: `I = Ce / (Ca + Ce)`

**Intervalo**: 0 (estável) a 1 (instável)

**Meta**: 
- Módulos estáveis (I ≈ 0): Core domain, utilitários compartilhados
- Módulos instáveis (I ≈ 1): Componentes UI, adaptadores de infraestrutura

---

## 🎯 Métricas de Qualidade

### Cobertura de Testes

**Definição**: Porcentagem de código coberto por testes.

**Meta**: > 80% para código crítico, > 60% para código geral.

### Complexidade Ciclomática

**Definição**: Medida da complexidade de um módulo baseada em caminhos de execução.

**Meta**: < 10 para funções, < 20 para módulos.

### Dívida Técnica

**Definição**: Esforço estimado para corrigir problemas de qualidade.

**Medição**: Tempo estimado para corrigir todos os problemas identificados.

---

## 📈 Métricas de Performance

### Tempo de Resposta

**Definição**: Tempo para processar uma requisição.

**Meta**: < 200ms para operações críticas, < 1s para operações gerais.

### Throughput

**Definição**: Número de requisições processadas por unidade de tempo.

**Meta**: Definido com base em requisitos de negócio.

---

## 🔄 Métricas de Evolução

### Facilidade de Mudança

**Definição**: Quão fácil é modificar um módulo sem quebrar outros.

**Indicadores**:
- Baixo acoplamento
- Alta coesão
- Boa cobertura de testes
- Documentação clara

### Facilidade de Extensão

**Definição**: Quão fácil é adicionar novas funcionalidades.

**Indicadores**:
- Abstrações bem definidas
- Interfaces claras
- Baixo acoplamento

---

## 🛠️ Implementação de Métricas

### Configuração de Ferramentas

**TypeScript/JavaScript**:
- ESLint para análise estática
- SonarQube para métricas de qualidade
- Jest para cobertura de testes

**Go**:
- `golangci-lint` para análise estática
- `go test -cover` para cobertura
- Custom tools para métricas de acoplamento

**Python**:
- `pylint` ou `ruff` para análise estática
- `pytest-cov` para cobertura
- `radon` para complexidade ciclomática

---

## 📊 Dashboard de Métricas

### Métricas Recomendadas

**Estruturais**:
- Acoplamento (Ca, Ce, I)
- Coesão
- Complexidade ciclomática

**Qualidade**:
- Cobertura de testes
- Violações de linting
- Dívida técnica

**Performance**:
- Tempo de resposta
- Throughput
- Uso de recursos

---

## 🔗 Documentação Relacionada

- [Guia de Arquitetura Evolutiva](./README.md) - Visão geral
- [Estratégias de Automação](./automation-strategies.md) - Automação de validações
- [Template de Diretrizes](../../../templates/evolutionary-architecture/guidelines-template.md) - Template para diretrizes

**Versão em Inglês**: [Metrics Definition Guide (EN)](../metrics-definition.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

