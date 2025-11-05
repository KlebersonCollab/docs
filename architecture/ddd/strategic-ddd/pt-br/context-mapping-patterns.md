# 🗺️ Padrões de Context Mapping

## 📋 Visão Geral

Context Mapping é o processo de identificar e documentar relacionamentos entre bounded contexts. Entender esses relacionamentos é crucial para projetar estratégias de integração e gerenciar dependências.

**Princípio Fundamental**: Cada relacionamento entre contextos requer uma estratégia de integração específica.

---

## 🎯 Padrões de Context Mapping

### 1. Shared Kernel

**Definição**: Duas equipes compartilham um pequeno subconjunto do modelo de domínio.

**Características**:
- Código compartilhado
- Requer coordenação entre equipes
- Mudanças requerem acordo de ambas equipes
- Alto risco de conflitos

**Use Quando**:
- Modelo compartilhado pequeno e estável
- Ambas equipes precisam do mesmo modelo
- Coordenação é viável

**Aviso**: Use com moderação. Shared kernels podem se tornar um gargalo.

---

### 2. Customer-Supplier

**Definição**: Equipe downstream depende da equipe upstream. Equipe upstream não tem dependência de downstream.

**Características**:
- Direção de dependência clara
- Equipe upstream controla o modelo
- Equipe downstream deve se adaptar
- Equipe upstream tem prioridade

**Estratégia de Integração**:
- Equipe upstream fornece API
- Equipe downstream consome API
- SLA para equipe upstream
- Estratégia de versionamento

---

### 3. Conformist

**Definição**: Equipe downstream deve se conformar ao modelo upstream sem influência.

**Características**:
- Downstream não tem influência
- Modelo upstream é fixo (legacy, third-party)
- Downstream deve se adaptar completamente
- Nenhuma negociação possível

**Use Quando**:
- Integrando com sistemas legados
- Integrando com sistemas third-party
- Equipe upstream é externa

---

### 4. Anti-Corruption Layer (ACL)

**Definição**: Equipe downstream cria uma camada de tradução para proteger seu modelo de corrupção upstream.

**Características**:
- Camada de tradução entre contextos
- Protege modelo downstream
- Isola modelo upstream
- Complexidade adicional

**Use Quando**:
- Modelo upstream não se encaixa nas necessidades downstream
- Precisa proteger modelo downstream
- Modelo upstream é legacy ou third-party

---

### 5. Separate Ways

**Definição**: Dois contextos não têm relacionamento e podem evoluir independentemente.

**Características**:
- Sem dependências
- Evolução independente
- Nenhuma integração necessária
- Isolamento completo

---

### 6. Partnership

**Definição**: Duas equipes trabalham juntas de perto, compartilhando desenvolvimento e integração.

**Características**:
- Relacionamento colaborativo
- Desenvolvimento compartilhado
- Dependências mútuas
- Requer coordenação

**Aviso**: Requer forte coordenação. Pode ser difícil de manter.

---

## 🗺️ Exemplo de Context Map

### Plataforma E-Commerce

```
Order Management (Core Domain)
    ↓ Customer-Supplier
Payment Processing (Generic - Stripe)
    ↓ Conformist
Shipping Service (Generic - Third-party)
    ↓ Anti-Corruption Layer
Inventory Management (Supporting)
    ↔ Partnership
Product Catalog (Core Domain)
```

**Legenda**:
- **Core Domain**: Order Management, Product Catalog
- **Supporting**: Inventory Management
- **Generic**: Payment Processing, Shipping Service

---

## 🔄 Estratégias de Integração

### Estratégia 1: Integração Síncrona

**Use Quando**:
- Consistência imediata necessária
- Baixa latência aceitável
- Baixo volume
- Chamadas de API diretas

**Padrões**:
- REST API
- gRPC
- GraphQL

### Estratégia 2: Integração Assíncrona

**Use Quando**:
- Consistência eventual aceitável
- Alto volume
- Desacoplamento desejado
- Arquitetura orientada a eventos

**Padrões**:
- Filas de mensagens (RabbitMQ, SQS)
- Event streaming (Kafka)
- Pub/Sub (Pub/Sub, SNS)

---

## 📊 Matriz de Seleção de Padrão

| Relacionamento | Padrão de Integração | Tecnologia | Quando Usar |
|----------------|---------------------|------------|-------------|
| Customer-Supplier | REST API | HTTP/REST | Upstream fornece API |
| Customer-Supplier | Eventos | Message Queue | Desacoplamento desejado |
| Conformist | Adapter | HTTP/REST | API third-party |
| Anti-Corruption Layer | Translator | Qualquer | Mismatch de modelo |
| Partnership | API Compartilhada | REST/gRPC | Desenvolvimento colaborativo |
| Shared Kernel | Biblioteca Compartilhada | Biblioteca | Modelo compartilhado pequeno |

---

## 🚫 Anti-Padrões

### ❌ Big Ball of Mud

**Problema**: Todos os contextos integrados sem limites claros.

**Solução**: Identificar bounded contexts e aplicar padrões apropriados.

### ❌ Banco de Dados Compartilhado

**Problema**: Múltiplos contextos compartilhando mesmo banco de dados.

**Solução**: Separar bancos de dados por contexto, usar padrões de integração.

---

## 🔗 Documentação Relacionada

- [Guia de DDD Estratégico](./README.md) - Visão geral do DDD Estratégico
- [Identificação de Bounded Context](./bounded-context-identification.md) - Como identificar contextos
- [Classificação de Subdomínios](./subdomain-classification.md) - Classificar subdomínios
- [Guia de Event-Driven Architecture](../../../event-driven-architecture/README.md) - Integração orientada a eventos

**Versão em Inglês**: [Context Mapping Patterns (EN)](../context-mapping-patterns.md)

---

**Versão**: 1.0  
**Última Atualização**: 2025  
**Mantenedor**: Equipe de Documentação Skynet

