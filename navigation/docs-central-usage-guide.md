# 📚 **Guia de Uso: Projeto Docs como Fonte Central**

## 🎯 **Visão Geral**

Este guia explica como utilizar o projeto docs como fonte única de verdade para toda documentação, seguindo a regra `docs-central-rule.mdc` estabelecida para o Cursor.

## 🏗️ **Estrutura do Projeto Docs**

### **Localização**
```
/home/kleberson/Projetos/Skynet/docs/
```

### **Coleções MCP Vectorizer**
- **`docs-architecture`**: Padrões arquiteturais, design patterns, C4 models
- **`docs-templates`**: Templates para documentação, FRD, ADRs, database schemas  
- **`docs-processes`**: Processos de desenvolvimento, Sprint de Processos, workflows
- **`docs-navigation`**: Estrutura de navegação e organização
- **`docs-governance`**: Governança, regras e padrões organizacionais
- **`docs-testing`**: Estratégias de teste e qualidade

## 🔍 **Como Consultar o Projeto Docs**

### **1. Busca Semântica (Recomendado)**
```typescript
// ✅ CORRETO: Consultar via MCP Vectorizer
mcp_hive-vectorizer_search_vectors(
  collection: "docs-architecture",
  query: "padrões arquiteturais Flutter",
  limit: 10
)
```

### **2. Análise de Projeto**
```typescript
// Para análise completa do projeto docs
mcp_hive-vectorizer_analyze_project(
  project_path: "/home/kleberson/Projetos/Skynet/docs"
)
```

### **3. Busca por Símbolos**
```typescript
// Para encontrar símbolos específicos
mcp_hive-vectorizer_find_symbols(
  file_path: "/home/kleberson/Projetos/Skynet/docs/architecture/design-patterns/",
  query: "decorator pattern"
)
```

## 📋 **Fluxo de Trabalho Recomendado**

### **Fase 1: Consulta Inicial**
1. **Identificar o contexto**: Que tipo de documentação/preocupação você tem?
2. **Escolher a coleção apropriada**: docs-architecture, docs-templates, docs-processes, etc.
3. **Fazer busca semântica**: Use o MCP Vectorizer para encontrar conteúdo relevante
4. **Analisar resultados**: Revise os resultados e identifique padrões/templates aplicáveis

### **Fase 2: Aplicação**
1. **Seguir templates encontrados**: Use os templates disponíveis como base
2. **Aplicar padrões arquiteturais**: Implemente seguindo os padrões estabelecidos
3. **Respeitar processos**: Siga os processos de desenvolvimento definidos
4. **Manter governança**: Mantenha conformidade com as regras organizacionais

### **Fase 3: Documentação**
1. **Documentar seguindo templates**: Use os templates encontrados para documentar
2. **Atualizar arquitetura se necessário**: Registre mudanças arquiteturais
3. **Registrar lições aprendidas**: Documente aprendizados e melhorias
4. **Manter governança atualizada**: Atualize regras e padrões conforme necessário

## 🎯 **Casos de Uso Específicos**

### **Caso 1: Implementação de Nova Feature Flutter**

#### **Passo 1: Consultar Padrões Arquiteturais**
```typescript
mcp_hive-vectorizer_search_vectors(
  collection: "docs-architecture",
  query: "padrão arquitetural Flutter feature",
  limit: 5
)
```

#### **Passo 2: Buscar Templates de Implementação**
```typescript
mcp_hive-vectorizer_search_vectors(
  collection: "docs-templates",
  query: "template implementação feature Flutter",
  limit: 5
)
```

#### **Passo 3: Verificar Processos de Desenvolvimento**
```typescript
mcp_hive-vectorizer_search_vectors(
  collection: "docs-processes",
  query: "processo desenvolvimento feature Flutter",
  limit: 5
)
```

#### **Passo 4: Implementar Seguindo Padrões**
- Use os padrões arquiteturais encontrados
- Siga os templates de implementação
- Respeite os processos de desenvolvimento
- Mantenha conformidade com governança

### **Caso 2: Refatoração de Código**

#### **Passo 1: Consultar Design Patterns**
```typescript
mcp_hive-vectorizer_search_vectors(
  collection: "docs-architecture",
  query: "design patterns refatoração",
  limit: 5
)
```

#### **Passo 2: Verificar Padrões de Qualidade**
```typescript
mcp_hive-vectorizer_search_vectors(
  collection: "docs-governance",
  query: "padrões qualidade código",
  limit: 5
)
```

#### **Passo 3: Aplicar Padrões Encontrados**
- Use os design patterns apropriados
- Mantenha os padrões de qualidade
- Documente as mudanças realizadas
- Valide com a governança estabelecida

### **Caso 3: Documentação de Projeto**

#### **Passo 1: Buscar Templates de Documentação**
```typescript
mcp_hive-vectorizer_search_vectors(
  collection: "docs-templates",
  query: "template documentação projeto",
  limit: 5
)
```

#### **Passo 2: Verificar Estrutura de Documentação**
```typescript
mcp_hive-vectorizer_search_vectors(
  collection: "docs-navigation",
  query: "estrutura documentação",
  limit: 5
)
```

#### **Passo 3: Usar Templates e Estrutura**
- Use os templates encontrados como base
- Siga a estrutura de documentação estabelecida
- Mantenha consistência com outros projetos
- Atualize a navegação se necessário

## 📊 **Templates Disponíveis**

### **Templates de Arquitetura**
- **C4 Model Template**: Documentação arquitetural em 4 níveis
- **Database Schema Template**: Esquemas de banco de dados
- **API Documentation Template**: Documentação de APIs
- **Microservices Template**: Arquitetura de microsserviços

### **Templates de Documentação**
- **FRD Template**: Functional Requirements Document
- **ADR Template**: Architecture Decision Records
- **Data Governance Template**: Governança de dados
- **Use Case Template**: Casos de uso

### **Templates de Processos**
- **Sprint Planning Template**: Planejamento de sprints
- **Daily Standup Template**: Reuniões diárias
- **Sprint Review Template**: Revisão de sprints
- **Retrospective Template**: Retrospectivas

## 🔧 **Integração com Outros Projetos**

### **Projeto Agronex-Web**
```typescript
// Consultar padrões específicos do Agronex
mcp_hive-vectorizer_search_vectors(
  collection: "agronex-web-docs",
  query: "padrões Flutter Agronex",
  limit: 5
)
```

### **Projeto Backend**
```typescript
// Consultar padrões do backend
mcp_hive-vectorizer_search_vectors(
  collection: "backend-docs",
  query: "padrões Django backend",
  limit: 5
)
```

### **Projeto Vectorizer**
```typescript
// Consultar documentação do Vectorizer
mcp_hive-vectorizer_search_vectors(
  collection: "vectorizer-docs",
  query: "documentação Vectorizer",
  limit: 5
)
```

## ⚠️ **Regras Críticas**

### **❌ NUNCA FAÇA**
- Leia arquivos do projeto docs diretamente
- Ignore os templates disponíveis
- Crie documentação sem consultar o projeto docs
- Implemente padrões sem verificar o projeto docs

### **✅ SEMPRE FAÇA**
- Consulte o MCP Vectorizer antes de implementar
- Use os templates disponíveis
- Siga os padrões estabelecidos
- Mantenha a governança atualizada

## 📈 **Métricas de Uso**

### **Verificações Regulares**
```typescript
// Verificar status do sistema
mcp_hive-vectorizer_health_check()

// Verificar métricas de análise
mcp_hive-vectorizer_get_code_analysis_metrics()

// Verificar estatísticas de memória
mcp_hive-vectorizer_get_memory_stats()
```

### **Alertas Importantes**
- Projeto docs não consultado antes de implementação
- Templates não utilizados para documentação
- Padrões arquiteturais ignorados
- Processos de desenvolvimento não seguidos

## 🎯 **Exemplos Práticos**

### **Exemplo 1: Implementação de Nova Feature Flutter**
```markdown
1. mcp_hive-vectorizer_search_vectors(collection: "docs-architecture", query: "padrão Flutter feature")
2. mcp_hive-vectorizer_search_vectors(collection: "docs-templates", query: "template implementação Flutter")
3. mcp_hive-vectorizer_search_vectors(collection: "docs-processes", query: "processo desenvolvimento Flutter")
4. Implementar seguindo padrões encontrados
5. Documentar usando templates encontrados
```

### **Exemplo 2: Refatoração de Código**
```markdown
1. mcp_hive-vectorizer_search_vectors(collection: "docs-architecture", query: "design patterns refatoração")
2. mcp_hive-vectorizer_search_vectors(collection: "docs-governance", query: "padrões qualidade")
3. Aplicar padrões encontrados
4. Validar com governança
5. Documentar mudanças
```

### **Exemplo 3: Documentação de Projeto**
```markdown
1. mcp_hive-vectorizer_search_vectors(collection: "docs-templates", query: "template documentação projeto")
2. mcp_hive-vectorizer_search_vectors(collection: "docs-navigation", query: "estrutura documentação")
3. Usar templates encontrados
4. Seguir estrutura estabelecida
5. Manter navegação consistente
```

## 🔗 **Links Relacionados**

- **Regra Central**: `.cursor/rules/docs-central-rule.mdc`
- **Projeto Docs**: `/home/kleberson/Projetos/Skynet/docs`
- **MCP Vectorizer**: Coleções docs-*
- **Templates**: `docs/templates/`
- **Processos**: `docs/processes/`
- **Arquitetura**: `docs/architecture/`

## 📚 **Recursos Adicionais**

### **Documentação Técnica**
- **Design Patterns**: Padrões de design implementados
- **Arquitetura**: Padrões arquiteturais estabelecidos
- **Processos**: Metodologias de desenvolvimento
- **Governança**: Regras e padrões organizacionais

### **Templates e Modelos**
- **Documentação**: Templates para todos os tipos de documentação
- **Arquitetura**: Modelos arquiteturais (C4, etc.)
- **Processos**: Templates para processos de desenvolvimento
- **Qualidade**: Padrões de qualidade e teste

## 🎯 **Conclusão**

O projeto docs é o **coração de toda documentação** e deve ser consultado **SEMPRE** antes de qualquer implementação, documentação ou decisão arquitetural. Use o MCP Vectorizer para acessar este conhecimento de forma eficiente e mantenha a consistência em todos os projetos.

**Lembre-se**: O projeto docs é a fonte única de verdade - consulte-o sempre via MCP Vectorizer para garantir qualidade, consistência e conformidade com os padrões estabelecidos.

---

**Última atualização**: $(date)
**Mantenedor**: Equipe Skynet
**Versão**: 1.0
