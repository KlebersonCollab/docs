# ADR-001: Modernização de Banco – Oracle para Postgres em Microsserviços (PT-BR)

> **Versão em Inglês**: [ADR-001](../adr-001-database-modernization.md)

---

## Status
Aceita

## Contexto
A operação inicial dependia de um único Oracle on-prem. Com o aumento de volume: pressão de custo (licença por core), risco operacional (gargalo único) e barreiras de escala. O crescimento do monólito agravou hotspots no DB.

## Decisão
Aplicar Strangler para extrair hotspots do monólito em microsserviços por domínio com Postgres. Cada serviço é dono do seu esquema; shared-nothing por padrão. Cache em leituras intensas.

## Consequências
- **Positivas**: Menor raio de explosão, maior agilidade, redução de custos, esquemas orientados a domínio.
- **Negativas**: Maior complexidade operacional, transações distribuídas, consistência eventual.

## Alternativas Consideradas
- Escalar cluster Oracle: pouca agilidade; custo; gargalo central permanece.
- Sharding Oracle: complexo e caro; lock-in do fornecedor.

## Notas de Implementação
- Priorizar domínios de alta carga/mutação nas primeiras extrações.
- Introduzir eventos para evitar acoplamento rígido.
- Dual-write apenas sob janelas curtas e controladas na migração.

---
Atualização: 2025-10-30


