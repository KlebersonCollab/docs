# Encurtador de URL - Estudo de Caso de System Design (PT-BR)

> **Versão em Inglês**: [English Version](../README.md)

---

## Visão Geral

O Encurtador de URL é um desafio clássico de system design que demonstra os mesmos princípios arquiteturais utilizados em grandes aplicações como YouTube, Instagram, Uber e Netflix. Apesar de parecer simples, este sistema requer cuidadosa consideração de escalabilidade, performance e conceitos de sistemas distribuídos.

## Índice

1. [Análise de Requisitos](requirements-analysis.pt-br.md)
2. [Design de Arquitetura](architecture-design.pt-br.md)
3. [Detalhes de Implementação](implementation-details.pt-br.md)
4. [Padrões de Escalabilidade](scalability-patterns.pt-br.md)
5. [Considerações de Segurança](security-considerations.pt-br.md)
6. [Métricas de Performance](performance-metrics.pt-br.md)

## Insights Principais

### Princípio Crítico
> "Toda arquitetura é feita para atender requisitos muito bem definidos. Sem requisito, você não consegue arquitetar nada porque qualquer coisa que você tentar arquitetar será baseada no chute."

### Conceitos Fundamentais

1. **Requisitos Primeiro**: Requisitos funcionais e não funcionais devem ser claramente definidos antes de qualquer decisão arquitetural
2. **Fundamento Matemático**: Todas as escolhas arquiteturais são baseadas em cálculos, estimativas e aproximações
3. **Sem Solução Perfeita**: Trade-offs são inerentes a toda decisão arquitetural
4. **Impacto do Status Code**: Até mesmo códigos HTTP (301 vs 302) afetam toda a arquitetura do sistema

## Referência Rápida

### Declaração do Problema
Dada uma URL longa, criar uma URL curta. Quando a URL curta é solicitada, redirecionar o usuário para a URL original.

### Requisitos Principais
- **Funcional**: Encurtamento e redirecionamento de URL
- **Não Funcional**: Alto volume, baixa latência, alta disponibilidade

### Stack Tecnológico
- **Banco de Dados**: Cassandra (para escalabilidade horizontal e alta disponibilidade)
- **Cache**: Redis (para URLs frequentemente acessadas e geração de ID)
- **Load Balancer**: Para escalamento horizontal
- **Backend**: Múltiplas instâncias para alta disponibilidade

## Documentação Relacionada

- [Guia de Seleção de Banco de Dados](../../architecture/database-selection-guide.md)
- [Padrões de Camada de Cache](../../architecture/escalabilidade/05-cache-layer.md)
- [Load Balancing](../../architecture/escalabilidade/03-load-balancing.md)

---

**Fonte**: Transcrição de vídeo - Entrevista de System Design
**Última Atualização**: Janeiro 2025
**Mantenedor**: Equipe Skynet

