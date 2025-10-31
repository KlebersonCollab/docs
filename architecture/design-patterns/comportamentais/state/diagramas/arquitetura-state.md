# Diagramas do Padrão State

## 📊 Arquitetura Geral

### Diagrama de Classes

```mermaid
classDiagram
    class Context {
        -State state
        +request()
        +setState(State state)
    }
    
    class State {
        <<interface>>
        +handle(Context context)
    }
    
    class ConcreteStateA {
        +handle(Context context)
    }
    
    class ConcreteStateB {
        +handle(Context context)
    }
    
    class ConcreteStateC {
        +handle(Context context)
    }
    
    Context --> State
    State <|-- ConcreteStateA
    State <|-- ConcreteStateB
    State <|-- ConcreteStateC
```

### Componentes do Padrão

| Componente | Responsabilidade | Exemplo |
|------------|------------------|---------|
| **Context** | Mantém referência para o estado atual | Classe `Pedido` |
| **State** | Interface que define operações | Interface `EstadoPedido` |
| **ConcreteState** | Implementa comportamento específico | Classes `Realizado`, `Preparando`, etc. |

## 🔄 Fluxo de Estados

### Diagrama de Estados - Pedido iFood

```mermaid
stateDiagram-v2
    [*] --> Realizado : Pedido criado
    Realizado --> Preparando : preparar()
    Preparando --> EntregaIniciada : iniciarEntrega()
    EntregaIniciada --> EntregaFinalizada : finalizarEntrega()
    EntregaFinalizada --> [*] : Pedido concluído
    
    note right of Realizado
        Estado inicial
        Apenas pode transitar
        para Preparando
    end note
    
    note right of Preparando
        Pedido sendo preparado
        Apenas pode transitar
        para EntregaIniciada
    end note
    
    note right of EntregaIniciada
        Pedido saiu para entrega
        Apenas pode transitar
        para EntregaFinalizada
    end note
    
    note right of EntregaFinalizada
        Estado final
        Não pode transitar
        para nenhum outro estado
    end note
```

### Tabela de Transições

| Estado Atual | Ação | Próximo Estado | Condição |
|---------------|------|----------------|----------|
| Realizado | `preparar()` | Preparando | ✅ Sempre permitido |
| Realizado | `iniciarEntrega()` | - | ❌ Bloqueado |
| Realizado | `finalizarEntrega()` | - | ❌ Bloqueado |
| Preparando | `preparar()` | - | ❌ Bloqueado |
| Preparando | `iniciarEntrega()` | EntregaIniciada | ✅ Sempre permitido |
| Preparando | `finalizarEntrega()` | - | ❌ Bloqueado |
| EntregaIniciada | `preparar()` | - | ❌ Bloqueado |
| EntregaIniciada | `iniciarEntrega()` | - | ❌ Bloqueado |
| EntregaIniciada | `finalizarEntrega()` | EntregaFinalizada | ✅ Sempre permitido |
| EntregaFinalizada | Qualquer ação | - | ❌ Todas bloqueadas |

## 🏗️ Arquitetura Detalhada

### Estrutura de Arquivos

```
src/
├── State/
│   ├── EstadoPedido.php          # Interface
│   ├── Realizado.php            # Estado inicial
│   ├── Preparando.php            # Estado de preparação
│   ├── EntregaIniciada.php       # Estado de entrega
│   └── EntregaFinalizada.php     # Estado final
├── Pedido.php                    # Contexto
└── index.php                     # Código cliente
```

### Diagrama de Sequência - Fluxo Normal

```mermaid
sequenceDiagram
    participant Cliente
    participant Pedido
    participant Realizado
    participant Preparando
    participant EntregaIniciada
    participant EntregaFinalizada
    
    Cliente->>Pedido: new Pedido()
    Pedido->>Realizado: setEstado(new Realizado())
    
    Cliente->>Pedido: preparar()
    Pedido->>Realizado: preparar(pedido)
    Realizado->>Pedido: setEstado(new Preparando())
    
    Cliente->>Pedido: iniciarEntrega()
    Pedido->>Preparando: iniciarEntrega(pedido)
    Preparando->>Pedido: setEstado(new EntregaIniciada())
    
    Cliente->>Pedido: finalizarEntrega()
    Pedido->>EntregaIniciada: finalizarEntrega(pedido)
    EntregaIniciada->>Pedido: setEstado(new EntregaFinalizada())
```

### Diagrama de Sequência - Tentativa de Violação

```mermaid
sequenceDiagram
    participant Cliente
    participant Pedido
    participant Realizado
    participant EntregaIniciada
    
    Cliente->>Pedido: new Pedido()
    Pedido->>Realizado: setEstado(new Realizado())
    
    Cliente->>Pedido: iniciarEntrega()
    Pedido->>Realizado: iniciarEntrega(pedido)
    Realizado-->>Cliente: DomainException: "Pedido ainda não foi preparado"
```

## 🎯 Padrões de Implementação

### 1. Interface State

```mermaid
graph TD
    A[Interface State] --> B[Método 1]
    A --> C[Método 2]
    A --> D[Método 3]
    
    B --> E[Implementação A]
    B --> F[Implementação B]
    B --> G[Implementação C]
    
    C --> E
    C --> F
    C --> G
    
    D --> E
    D --> F
    D --> G
```

### 2. Context com Estados

```mermaid
graph TD
    A[Context] --> B[Estado Atual]
    A --> C[Operação 1]
    A --> D[Operação 2]
    A --> E[Operação 3]
    
    B --> F[Estado A]
    B --> G[Estado B]
    B --> H[Estado C]
    
    C --> I[Delega para Estado]
    D --> I
    E --> I
    
    I --> F
    I --> G
    I --> H
```

## 🔧 Variações do Padrão

### 1. State com Dados

```mermaid
classDiagram
    class Context {
        -State state
        -Map data
        +request(data)
        +setState(State state)
    }
    
    class State {
        <<interface>>
        +handle(Context context, Map data)
    }
    
    class ConcreteStateA {
        +handle(Context context, Map data)
    }
    
    Context --> State
    State <|-- ConcreteStateA
```

### 2. State com Histórico

```mermaid
classDiagram
    class Context {
        -State state
        -List history
        +request()
        +setState(State state)
        +getHistory()
    }
    
    class State {
        <<interface>>
        +handle(Context context)
    }
    
    Context --> State
```

### 3. State com Timeout

```mermaid
classDiagram
    class Context {
        -State state
        -DateTime lastChange
        +request()
        +setState(State state)
        +checkTimeout()
    }
    
    class State {
        <<interface>>
        +handle(Context context)
        +canTransition()
    }
    
    Context --> State
```

## 📈 Métricas e Monitoramento

### Diagrama de Métricas

```mermaid
graph TD
    A[Estado Atual] --> B[Contador de Transições]
    A --> C[Tempo no Estado]
    A --> D[Falhas de Transição]
    
    B --> E[Métricas de Performance]
    C --> E
    D --> E
    
    E --> F[Dashboard]
    E --> G[Alertas]
    E --> H[Relatórios]
```

### Tabela de Métricas

| Métrica | Descrição | Valor Ideal |
|---------|------------|--------------|
| **Transições por minuto** | Número de mudanças de estado | < 100 |
| **Tempo médio no estado** | Duração média em cada estado | Variável |
| **Taxa de falhas** | % de transições que falharam | < 1% |
| **Estados órfãos** | Estados que não podem transitar | 0 |

## 🚀 Extensões Avançadas

### 1. State Machine

```mermaid
stateDiagram-v2
    [*] --> Estado1
    Estado1 --> Estado2 : Evento1
    Estado2 --> Estado3 : Evento2
    Estado3 --> Estado1 : Evento3
    Estado3 --> [*] : Evento4
    
    note right of Estado1
        Pode receber Evento1
        ou Evento3
    end note
    
    note right of Estado2
        Pode receber Evento2
        ou Evento1
    end note
    
    note right of Estado3
        Pode receber Evento3
        ou Evento4
    end note
```

### 2. Hierarchical State

```mermaid
stateDiagram-v2
    [*] --> EstadoPai
    EstadoPai --> EstadoFilho1
    EstadoPai --> EstadoFilho2
    EstadoFilho1 --> EstadoNeto1
    EstadoFilho1 --> EstadoNeto2
    EstadoFilho2 --> EstadoNeto3
    EstadoNeto1 --> EstadoPai
    EstadoNeto2 --> EstadoPai
    EstadoNeto3 --> EstadoPai
```

### 3. Parallel State

```mermaid
stateDiagram-v2
    [*] --> EstadoParalelo
    EstadoParalelo --> EstadoA
    EstadoParalelo --> EstadoB
    EstadoA --> EstadoA1
    EstadoA --> EstadoA2
    EstadoB --> EstadoB1
    EstadoB --> EstadoB2
    EstadoA1 --> EstadoA
    EstadoA2 --> EstadoA
    EstadoB1 --> EstadoB
    EstadoB2 --> EstadoB
```

## 🎯 Conclusão

Os diagramas apresentados mostram:

1. **Arquitetura clara** do padrão State
2. **Fluxos de transição** bem definidos
3. **Prevenção de violações** de regras
4. **Extensibilidade** para casos complexos
5. **Monitoramento** e métricas de qualidade

O padrão State oferece uma solução robusta e escalável para gerenciar estados complexos em aplicações, garantindo que as regras de negócio sejam sempre respeitadas.

---

**Última atualização**: $(date)
**Mantenedor**: Equipe Skynet
**Versão**: 1.0





