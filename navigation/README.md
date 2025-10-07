# 📚 **Navegação do Projeto Docs**

## 🎯 **Visão Geral**

Este diretório contém a documentação de navegação e uso do projeto docs como fonte central de documentação para todos os projetos.

## 📋 **Documentos Disponíveis**

### **1. Regra Central**
- **Arquivo**: `.cursor/rules/docs-central-rule.mdc`
- **Propósito**: Regra principal para o Cursor sobre uso do projeto docs
- **Status**: ✅ Ativa e implementada
- **Aplicação**: Todos os projetos no workspace

### **2. Guia de Uso**
- **Arquivo**: `docs/navigation/docs-central-usage-guide.md`
- **Propósito**: Guia detalhado de como utilizar o projeto docs
- **Conteúdo**: Fluxos de trabalho, casos de uso, exemplos práticos
- **Status**: ✅ Disponível

### **3. Resumo Executivo**
- **Arquivo**: `docs/navigation/docs-central-summary.md`
- **Propósito**: Resumo executivo da implementação
- **Conteúdo**: Benefícios, métricas, status da implementação
- **Status**: ✅ Disponível

## 🏗️ **Estrutura do Projeto Docs**

### **Coleções MCP Vectorizer**
- **`docs-architecture`**: Padrões arquiteturais, design patterns, C4 models
- **`docs-templates`**: Templates para documentação, FRD, ADRs, database schemas
- **`docs-processes`**: Processos de desenvolvimento, Sprint de Processos, workflows
- **`docs-navigation`**: Estrutura de navegação e organização
- **`docs-governance`**: Governança, regras e padrões organizacionais
- **`docs-testing`**: Estratégias de teste e qualidade

### **Diretórios Principais**
```
docs/
├── architecture/          # Padrões arquiteturais e design patterns
├── templates/            # Templates para documentação
├── processes/            # Processos de desenvolvimento
├── governance/           # Governança e regras
├── testing/              # Estratégias de teste
└── navigation/           # Estrutura de navegação
```

## 🔍 **Como Consultar o Projeto Docs**

### **1. Busca Semântica (Recomendado)**
```typescript
// Consultar padrões arquiteturais
mcp_hive-vectorizer_search_vectors(
  collection: "docs-architecture",
  query: "padrões arquiteturais Flutter",
  limit: 10
)
```

### **2. Análise de Projeto**
```typescript
// Análise completa do projeto docs
mcp_hive-vectorizer_analyze_project(
  project_path: "/home/kleberson/Projetos/Skynet/docs"
)
```

### **3. Busca por Símbolos**
```typescript
// Encontrar símbolos específicos
mcp_hive-vectorizer_find_symbols(
  file_path: "/home/kleberson/Projetos/Skynet/docs/architecture/",
  query: "design patterns"
)
```

## 📋 **Fluxo de Trabalho Recomendado**

### **Fase 1: Consulta Inicial**
1. **Identificar contexto**: Que tipo de documentação/preocupação você tem?
2. **Escolher coleção**: docs-architecture, docs-templates, docs-processes, etc.
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

### **Caso 1: Implementação de Nova Feature**
```markdown
1. Consultar docs-architecture para padrões existentes
2. Verificar docs-templates para templates relevantes
3. Revisar docs-processes para processos aplicáveis
4. Validar com docs-governance para regras e padrões
```

### **Caso 2: Refatoração de Código**
```markdown
1. Consultar docs-architecture para design patterns
2. Verificar docs-governance para padrões de qualidade
3. Aplicar padrões encontrados
4. Validar com governança
5. Documentar mudanças
```

### **Caso 3: Documentação de Projeto**
```markdown
1. Consultar docs-templates para templates de documentação
2. Verificar docs-navigation para estrutura de documentação
3. Usar templates encontrados
4. Seguir estrutura estabelecida
5. Manter navegação consistente
```

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

## 🔗 **Links Relacionados**

- **Regra Central**: `.cursor/rules/docs-central-rule.mdc`
- **Guia de Uso**: `docs/navigation/docs-central-usage-guide.md`
- **Resumo Executivo**: `docs/navigation/docs-central-summary.md`
- **Projeto Docs**: `/home/kleberson/Projetos/Skynet/docs`
- **MCP Vectorizer**: Coleções docs-*

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
