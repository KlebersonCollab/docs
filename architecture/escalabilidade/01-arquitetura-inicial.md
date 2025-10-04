# Arquitetura Inicial - Monolítica Básica

## Visão Geral

A arquitetura inicial representa o ponto de partida mais simples: uma aplicação monolítica com banco de dados no mesmo servidor.

## Componentes

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Mobile App   │
│   (React/Angular)│    │   (iOS/Android)│
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌─────────────────┐
         │      DNS       │
         │  api.meuapp.com│
         └─────────────────┘
                     │
         ┌─────────────────┐
         │   Servidor      │
         │ ┌─────────────┐ │
         │ │    API      │ │
         │ │  (Backend)  │ │
         │ └─────────────┘ │
         │ ┌─────────────┐ │
         │ │   Database  │ │
         │ │  (MySQL/    │ │
         │ │  PostgreSQL)│ │
         │ └─────────────┘ │
         └─────────────────┘
```

## Características

### ✅ Vantagens
- **Simplicidade**: Fácil de desenvolver e deployar
- **Custo baixo**: Apenas um servidor necessário
- **Debugging simples**: Tudo em um lugar
- **Desenvolvimento rápido**: Sem complexidade de rede

### ❌ Desvantagens
- **Ponto único de falha**: Se o servidor falha, tudo para
- **Competição por recursos**: API e DB competem por CPU/RAM
- **Escalabilidade limitada**: Não consegue crescer horizontalmente
- **Manutenção complexa**: Mudanças afetam todo o sistema

## Problemas Identificados

### 1. Ponto Único de Falha (SPOF)
- Servidor único = risco total
- Sem redundância
- Tempo de inatividade alto

### 2. Limitações de Recursos
- CPU compartilhada entre API e DB
- Memória limitada
- I/O do disco compartilhado

### 3. Escalabilidade Vertical Limitada
- Limite físico de hardware
- Custo exponencial
- Não resolve problemas de disponibilidade

## Métricas Típicas

| Métrica | Valor Típico |
|---------|--------------|
| Usuários simultâneos | 100-1.000 |
| Requisições/segundo | 10-100 |
| Tempo de resposta | 200-500ms |
| Uptime | 95-99% |
| Capacidade de crescimento | Muito limitada |

## Próximos Passos

Para evoluir desta arquitetura, precisamos:

1. **Separar responsabilidades** (API e DB em servidores diferentes)
2. **Implementar redundância** (múltiplas instâncias)
3. **Adicionar load balancing**
4. **Otimizar performance** (cache, CDN)

Esta arquitetura é adequada para:
- Protótipos
- MVPs
- Aplicações com baixo tráfego
- Projetos de aprendizado

**Não é adequada para:**
- Produção com alta disponibilidade
- Aplicações que precisam escalar
- Sistemas críticos de negócio
