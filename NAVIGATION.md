# 🗺️ Guia de Navegação - Skynet Docs

Este guia ajuda você a encontrar rapidamente a documentação que precisa.

## 🧠 **Documentos Centrais - Cérebro do Projeto**

### **Documentos de Referência Principal**
- [🧠 **Guia Central**](GUIA_CENTRAL.md) - **Cérebro do projeto** - Fonte única de verdade para IAs
- [📋 **Índice Organizacional**](INDICE_ORGANIZACIONAL.md) - Organização completa por assunto
- [🗺️ **Mapa de Navegação**](MAPA_NAVEGACAO.md) - Navegação visual e fluxos de decisão
- [📖 **Navegação**](NAVIGATION.md) - Este documento - Guia geral de navegação

### **Como Usar os Documentos Centrais**
1. **Para IAs**: Comece sempre com o [Guia Central](GUIA_CENTRAL.md)
2. **Para Navegação**: Use o [Índice Organizacional](INDICE_ORGANIZACIONAL.md)
3. **Para Fluxos**: Consulte o [Mapa de Navegação](MAPA_NAVEGACAO.md)
4. **Para Busca Rápida**: Use este documento (NAVIGATION.md)

## 🚀 Navegação Rápida

### Por Função
| Função | Seção Principal | Links Úteis |
|--------|----------------|-------------|
| **Desenvolvedor** | [Arquitetura](architecture/README.md) | [Escalabilidade](architecture/escalabilidade/README.md), [Design Patterns](architecture/design-patterns/README.md) |
| **Arquiteto** | [Arquitetura](architecture/README.md) | [System Design](templates/architecture/system-design-template.md), [C4 Model](templates/architecture/c4-model-template.md) |
| **QA Engineer** | [Testing](testing/README.md) | [Test Cases](templates/testing/test-case-template.md), [BDD](testing/bdd-example.md) |
| **Scrum Master** | [Processos](processes/README.md) | [Sprint Planning](templates/processes/sprint-planning-template.md), [Retrospectivas](templates/processes/retrospective-template.md) |
| **Product Owner** | [Templates](templates/README.md) | [PRD](templates/prd-template.md), [User Stories](templates/user-story-template.md) |
| **DevOps** | [Templates](templates/README.md) | [Deployment Guide](templates/deployment-guide-template.md), [Incident Report](templates/incident-report-template.md) |

### Por Tecnologia
| Tecnologia | Documentação | Templates |
|------------|---------------|-----------|
| **Frontend** | [Design Patterns](architecture/design-patterns/README.md) | [API Documentation](templates/api-documentation-template.md) |
| **Backend** | [Escalabilidade](architecture/escalabilidade/README.md) | [System Design](templates/architecture/system-design-template.md) |
| **Database** | [Database Replication](architecture/escalabilidade/04-database-replication.md) | [Database Schema](templates/database-schema-template.md) |
| **Cloud** | [Multi-Region](architecture/escalabilidade/07-multi-region.md) | [Deployment Guide](templates/deployment-guide-template.md) |

### Por Processo
| Processo | Documentação | Templates |
|----------|---------------|-----------|
| **Planejamento** | [Sprint Processos](processes/sprint-processos-burndown/README.md) | [Sprint Planning](templates/processes/sprint-planning-template.md) |
| **Desenvolvimento** | [Engineering Guidelines](templates/engineering-guidelines-template.md) | [Code Review](templates/code-review-template.md) |
| **Testes** | [Testing](testing/README.md) | [Test Plan](templates/testing/test-plan-template.md) |
| **Deploy** | [Deployment Guide](templates/deployment-guide-template.md) | [Incident Report](templates/incident-report-template.md) |

## 🔍 Busca por Assunto

### Arquitetura e Design
- **Escalabilidade**: [Guia Completo](architecture/escalabilidade/README.md)
- **Design Patterns**: [Padrões Estruturais](./architecture/design-patterns/estruturais/)
- **System Design**: [Template](templates/architecture/system-design-template.md)
- **C4 Model**: [Template](templates/architecture/c4-model-template.md)

### Desenvolvimento
- **Code Review**: [Template](templates/code-review-template.md)
- **Engineering Guidelines**: [Template](templates/engineering-guidelines-template.md)
- **API Documentation**: [Template](templates/api-documentation-template.md)
- **Database Schema**: [Template](templates/database-schema-template.md)

### Qualidade
- **Test Cases**: [Template](templates/testing/test-case-template.md)
- **Test Plan**: [Template](templates/testing/test-plan-template.md)
- **BDD**: [Examples](testing/bdd-example.md)
- **Quality Assurance**: [Template](templates/quality-assurance-plan-template.md)

### Processos Ágeis
- **Sprint Planning**: [Template](templates/processes/sprint-planning-template.md)
- **Retrospectivas**: [Template](templates/processes/retrospective-template.md)
- **User Stories**: [Template](templates/user-story-template.md)
- **Use Cases**: [Template](templates/use-case-template.md)

### Documentação
- **ADR**: [Template](templates/adr-template.md)
- **RFC**: [Template](templates/rfc-template.md)
- **PRD**: [Template](templates/prd-template.md)
- **TRD**: [Template](templates/trd-template.md)

## 📊 Níveis de Experiência

### Iniciante
- [Arquitetura Inicial](architecture/escalabilidade/01-arquitetura-inicial.md)
- [Design Patterns Básicos](architecture/design-patterns/estruturais/decorator/README.md)
- [Test Cases Simples](templates/testing/test-case-template.md)
- [Sprint Planning](templates/processes/sprint-planning-template.md)

### Intermediário
- [Load Balancing](architecture/escalabilidade/03-load-balancing.md)
- [Cache Layer](architecture/escalabilidade/05-cache-layer.md)
- [BDD Examples](testing/bdd-example.md)
- [Code Review](templates/code-review-template.md)

### Avançado
- [Multi-Region](architecture/escalabilidade/07-multi-region.md)
- [Message Queues](architecture/escalabilidade/08-message-queues.md)
- [Arquitetura Final](architecture/escalabilidade/09-arquitetura-final.md)
- [System Design](templates/architecture/system-design-template.md)

## 🎯 Fluxos de Trabalho

### Novo Projeto
1. **Requisitos**: [PRD](templates/prd-template.md) → [TRD](templates/trd-template.md)
2. **Arquitetura**: [System Design](templates/architecture/system-design-template.md) → [C4 Model](templates/architecture/c4-model-template.md)
3. **Desenvolvimento**: [Engineering Guidelines](templates/engineering-guidelines-template.md) → [Code Review](templates/code-review-template.md)
4. **Testes**: [Test Plan](templates/testing/test-plan-template.md) → [Test Cases](templates/testing/test-case-template.md)
5. **Deploy**: [Deployment Guide](templates/deployment-guide-template.md)

### Melhoria de Sistema
1. **Análise**: [Escalabilidade](architecture/escalabilidade/README.md) → [Arquitetura Final](architecture/escalabilidade/09-arquitetura-final.md)
2. **Decisão**: [ADR](templates/adr-template.md) → [RFC](templates/rfc-template.md)
3. **Implementação**: [Engineering Guidelines](templates/engineering-guidelines-template.md)
4. **Validação**: [Test Cases](templates/testing/test-case-template.md)

### Incidente de Produção
1. **Detecção**: [Incident Report](templates/incident-report-template.md)
2. **Análise**: [Troubleshooting Guide](templates/troubleshooting-guide-template.md)
3. **Resolução**: [Deployment Guide](templates/deployment-guide-template.md)
4. **Prevenção**: [ADR](templates/adr-template.md)

## 🔗 Links Úteis

### Documentação Externa
- [Scrum Guide](https://scrumguides.org/)
- [SAFe Framework](https://www.scaledagileframework.com/)
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)
- [Google SRE](https://sre.google/)

### Ferramentas
- [Mermaid](https://mermaid-js.github.io/) - Diagramas
- [Draw.io](https://app.diagrams.net/) - Diagramas
- [Jira](https://www.atlassian.com/software/jira) - Gestão de projetos
- [Confluence](https://www.atlassian.com/software/confluence) - Documentação

## 📞 Suporte

### Dúvidas sobre Documentação
1. Consulte este guia de navegação
2. Use a busca por assunto
3. Verifique os templates apropriados
4. Consulte os READMEs de cada seção

### Sugestões de Melhoria
1. Identifique a seção apropriada
2. Use os templates existentes
3. Siga as convenções estabelecidas
4. Atualize este guia se necessário

---

**Última atualização**: $(date)
**Mantenedor**: Equipe de Documentação Skynet
