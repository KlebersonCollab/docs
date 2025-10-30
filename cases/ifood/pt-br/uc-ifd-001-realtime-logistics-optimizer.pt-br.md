# Caso de Uso: Otimizador de Logística em Tempo Real (PT-BR)

## Informações Básicas
- **ID**: UC-IFD-001
- **Nome**: Orquestração de frota em tempo real (telemetria → clusterização → roteirização)
- **Versão**: 1.0
- **Criação**: 2025-10-30
- **Atualização**: 2025-10-30

## Descrição
Atribuir contínua e dinamicamente entregadores a coletas/entregas consumindo telemetria ao vivo, agrupando pedidos em pico e calculando rotas multi-paradas (heurísticas tipo TSP) para minimizar atrasos e ociosidade.

## Atores
- **Aplicativo do Entregador** (Primário): envia localização/status via MQTT.
- **Orquestrador de Logística** (Primário): consome telemetria, clusteriza e roteiriza.
- **Despachante/Operador** (Secundário): monitora painéis e aciona controles regionais em incidentes.
- **Cliente** (Secundário): recebe ETAs.

## Pré-condições
- Ingestão de telemetria operacional (broker, autenticação ok).
- Restaurantes publicando prontidão; pedidos na fila.
- Entregadores suficientes online por região.

## Pós-condições
- Pedidos atribuídos; ETAs atualizadas; métricas/logs registrados.
- Em picos, batching aplicado e backlog reduzido gradualmente.

## Fluxo Principal
1. Telemetria chega (MQTT → barramento) com coordenadas/status.
2. Orquestrador atualiza estado do entregador e cruza com fila regional.
3. Engine de clusterização agrupa pedidos por espaço/tempo.
4. Engine de roteirização calcula sequências candidatas; escolhe menor custo.
5. Atribuições publicadas ao app; clientes notificados.

## Fluxos Alternativos
- **FA1 – Sobrecarga Regional**: backlog > limiar → habilitar batching; degradar políticas; rate-limit em novas regiões.
- **FA2 – Entregadores Escassos**: ampliar raio de busca; relaxar restrições; priorizar pedidos com SLA crítico.

## Exceções
- **EX1 – Queda de Telemetria**: queda para última posição conhecida; reduzir horizonte de atribuição; alertar SRE.
- **EX2 – Timeout de Roteirização**: devolver melhor rota até o tempo; registrar para melhoria offline.

## Regras de Negócio
- Priorizar risco de SLA e prontidão do preparo.
- Limitar tempo de computação por região (ex.: < 500ms mediano).
- Limitar tamanho de batch para evitar desvios excessivos.

## Requisitos Não Funcionais
- **Performance**: ciclo de atribuição P95 < 2s por região.
- **Escalabilidade**: suportar 100k+ pedidos concorrentes via particionamento.
- **Confiabilidade**: degradação graciosa; retries com jitter em falhas de publicação.

## Dependências
- Broker MQTT, barramento de eventos, app do entregador, feed de prontidão, API de atribuição.

## Cenários de Teste
1. Pico sintético: validar decaimento de backlog e SLA com batching ativo.
2. Perda de telemetria: validar fallback e alertas.
3. Estresse de roteirização: garantir retorno dentro do orçamento de tempo.

## Notas de Implementação
- Particionar por cidade → região → bairro para viabilidade computacional.
- Se LLM for usado para insights operacionais, anonimizar; não usar LLM no laço de atribuição.
- Kill-switch regional; pré-aquecer workers antes de picos previstos.

---
Status: Rascunho

