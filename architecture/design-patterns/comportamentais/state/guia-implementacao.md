# Guia de Implementação - Padrão State

## 🎯 Visão Geral

Este guia fornece um roteiro completo para implementar o padrão State em seus projetos, desde a identificação da necessidade até a implementação e testes.

## 📋 Checklist de Implementação

### ✅ Fase 1: Análise e Planejamento

#### 1.1 Identificar a Necessidade
- [ ] Objeto com múltiplos estados
- [ ] Comportamento que muda baseado no estado
- [ ] Regras de transição complexas
- [ ] Necessidade de controle rigoroso

#### 1.2 Mapear Estados e Transições
- [ ] Listar todos os estados possíveis
- [ ] Definir transições permitidas
- [ ] Identificar regras de negócio
- [ ] Documentar exceções e casos especiais

#### 1.3 Avaliar Complexidade
- [ ] Quantos estados existem?
- [ ] Quantas transições são possíveis?
- [ ] Qual a frequência de mudanças?
- [ ] Vale a pena a complexidade adicional?

### ✅ Fase 2: Design da Arquitetura

#### 2.1 Definir Interface State
```php
interface EstadoPedido {
    public function preparar(Pedido $pedido): void;
    public function iniciarEntrega(Pedido $pedido): void;
    public function finalizarEntrega(Pedido $pedido): void;
}
```

#### 2.2 Criar Estados Concretos
```php
class Realizado implements EstadoPedido {
    // Implementação específica
}

class Preparando implements EstadoPedido {
    // Implementação específica
}
```

#### 2.3 Implementar Context
```php
class Pedido {
    private EstadoPedido $estado;
    
    public function __construct() {
        $this->estado = new Realizado();
    }
    
    public function preparar(): void {
        $this->estado->preparar($this);
    }
}
```

### ✅ Fase 3: Implementação

#### 3.1 Estrutura de Arquivos
```
src/
├── State/
│   ├── EstadoPedido.php
│   ├── Realizado.php
│   ├── Preparando.php
│   ├── EntregaIniciada.php
│   └── EntregaFinalizada.php
├── Pedido.php
└── index.php
```

#### 3.2 Implementação Passo a Passo

**Passo 1: Criar Interface**
```php
<?php

interface EstadoPedido {
    public function preparar(Pedido $pedido): void;
    public function iniciarEntrega(Pedido $pedido): void;
    public function finalizarEntrega(Pedido $pedido): void;
}
```

**Passo 2: Implementar Estados**
```php
<?php

class Realizado implements EstadoPedido {
    public function preparar(Pedido $pedido): void {
        $pedido->setEstado(new Preparando());
    }
    
    public function iniciarEntrega(Pedido $pedido): void {
        throw new DomainException("Pedido ainda não foi preparado");
    }
    
    public function finalizarEntrega(Pedido $pedido): void {
        throw new DomainException("Pedido ainda não foi preparado");
    }
}
```

**Passo 3: Implementar Context**
```php
<?php

class Pedido {
    private EstadoPedido $estado;
    
    public function __construct() {
        $this->estado = new Realizado();
    }
    
    public function preparar(): void {
        $this->estado->preparar($this);
    }
    
    public function setEstado(EstadoPedido $estado): void {
        $this->estado = $estado;
    }
}
```

### ✅ Fase 4: Testes

#### 4.1 Testes Unitários
```php
<?php

class PedidoTest extends PHPUnit\Framework\TestCase {
    public function testPedidoIniciaComoRealizado() {
        $pedido = new Pedido();
        $this->assertInstanceOf(Realizado::class, $pedido->getEstado());
    }
    
    public function testPedidoPodeSerPreparado() {
        $pedido = new Pedido();
        $pedido->preparar();
        $this->assertInstanceOf(Preparando::class, $pedido->getEstado());
    }
    
    public function testPedidoNaoPodeSerFinalizadoSemPreparar() {
        $pedido = new Pedido();
        $this->expectException(DomainException::class);
        $pedido->finalizarEntrega();
    }
}
```

#### 4.2 Testes de Integração
```php
<?php

class PedidoIntegrationTest extends PHPUnit\Framework\TestCase {
    public function testFluxoCompletoPedido() {
        $pedido = new Pedido();
        
        // Realizado -> Preparando
        $pedido->preparar();
        $this->assertInstanceOf(Preparando::class, $pedido->getEstado());
        
        // Preparando -> EntregaIniciada
        $pedido->iniciarEntrega();
        $this->assertInstanceOf(EntregaIniciada::class, $pedido->getEstado());
        
        // EntregaIniciada -> EntregaFinalizada
        $pedido->finalizarEntrega();
        $this->assertInstanceOf(EntregaFinalizada::class, $pedido->getEstado());
    }
}
```

## 🎯 Boas Práticas

### 1. **Nomenclatura Clara**

#### ✅ BOM
```php
class PedidoRealizado implements EstadoPedido
class PedidoEmPreparacao implements EstadoPedido
class PedidoEmEntrega implements EstadoPedido
```

#### ❌ RUIM
```php
class Estado1 implements EstadoPedido
class Estado2 implements EstadoPedido
class Estado3 implements EstadoPedido
```

### 2. **Tratamento de Exceções**

#### ✅ BOM
```php
public function iniciarEntrega(Pedido $pedido): void {
    throw new DomainException("Pedido ainda não foi preparado");
}
```

#### ❌ RUIM
```php
public function iniciarEntrega(Pedido $pedido): void {
    throw new Exception("Erro");
}
```

### 3. **Imutabilidade dos Estados**

#### ✅ BOM
```php
class Realizado implements EstadoPedido {
    // Sem propriedades mutáveis
    public function preparar(Pedido $pedido): void {
        $pedido->setEstado(new Preparando());
    }
}
```

#### ❌ RUIM
```php
class Realizado implements EstadoPedido {
    private bool $processado = false; // Evitar estado interno
    
    public function preparar(Pedido $pedido): void {
        $this->processado = true; // Evitar
    }
}
```

### 4. **Documentação Clara**

#### ✅ BOM
```php
/**
 * Estado inicial de um pedido
 * 
 * Transições permitidas:
 * - preparar() → Preparando
 * 
 * Transições bloqueadas:
 * - iniciarEntrega() → DomainException
 * - finalizarEntrega() → DomainException
 */
class Realizado implements EstadoPedido {
    // Implementação...
}
```

### 5. **Validação de Estados**

#### ✅ BOM
```php
class Pedido {
    public function podePreparar(): bool {
        return $this->estado instanceof Realizado;
    }
    
    public function podeFinalizar(): bool {
        return $this->estado instanceof EntregaIniciada;
    }
}
```

## 🚀 Extensões Avançadas

### 1. **Estados com Dados**

```php
interface EstadoPedido {
    public function preparar(Pedido $pedido, array $dados = []): void;
    public function iniciarEntrega(Pedido $pedido, array $dados = []): void;
    public function finalizarEntrega(Pedido $pedido, array $dados = []): void;
}

class Preparando implements EstadoPedido {
    public function preparar(Pedido $pedido, array $dados = []): void {
        // Usar dados para lógica específica
        $tempoPreparacao = $dados['tempo_preparacao'] ?? 30;
        $pedido->setTempoPreparacao($tempoPreparacao);
        $pedido->setEstado(new EntregaIniciada());
    }
}
```

### 2. **Histórico de Estados**

```php
class Pedido {
    private array $historicoEstados = [];
    
    public function setEstado(EstadoPedido $estado): void {
        $this->historicoEstados[] = [
            'estado' => get_class($estado),
            'timestamp' => new DateTime(),
            'dados' => $this->getDadosEstado()
        ];
        $this->estado = $estado;
    }
    
    public function getHistoricoEstados(): array {
        return $this->historicoEstados;
    }
}
```

### 3. **Estados com Timeout**

```php
class Preparando implements EstadoPedido {
    private DateTime $inicioPreparacao;
    
    public function __construct() {
        $this->inicioPreparacao = new DateTime();
    }
    
    public function iniciarEntrega(Pedido $pedido): void {
        $tempoDecorrido = (new DateTime())->diff($this->inicioPreparacao);
        
        if ($tempoDecorrido->i < 5) { // Menos de 5 minutos
            throw new DomainException("Pedido ainda não pode sair para entrega");
        }
        
        $pedido->setEstado(new EntregaIniciada());
    }
}
```

### 4. **Estados com Validação**

```php
class EntregaIniciada implements EstadoPedido {
    public function finalizarEntrega(Pedido $pedido): void {
        // Validar se o pedido pode ser finalizado
        if (!$this->podeFinalizar($pedido)) {
            throw new DomainException("Pedido não pode ser finalizado");
        }
        
        $pedido->setEstado(new EntregaFinalizada());
    }
    
    private function podeFinalizar(Pedido $pedido): bool {
        // Lógica de validação específica
        return $pedido->getTempoEntrega() > 10; // Mínimo 10 minutos
    }
}
```

## 🔧 Ferramentas e Bibliotecas

### 1. **PHP**
- **Symfony Workflow**: Componente oficial para máquinas de estado
- **State Machine**: Biblioteca específica para padrão State
- **PHPUnit**: Para testes unitários

### 2. **Python**
- **transitions**: Biblioteca para máquinas de estado
- **state_machine**: Implementação do padrão State
- **pytest**: Para testes

### 3. **TypeScript/JavaScript**
- **xstate**: Biblioteca para máquinas de estado
- **state-machine**: Implementação simples
- **Jest**: Para testes

### 4. **Java**
- **Spring State Machine**: Framework para máquinas de estado
- **JUnit**: Para testes
- **Mockito**: Para mocks

## 📊 Métricas e Monitoramento

### 1. **Métricas Importantes**

```php
class PedidoMetrics {
    private array $metricas = [];
    
    public function registrarTransicao(string $de, string $para): void {
        $chave = "{$de}->{$para}";
        $this->metricas[$chave] = ($this->metricas[$chave] ?? 0) + 1;
    }
    
    public function registrarFalha(string $estado, string $acao): void {
        $chave = "falha_{$estado}_{$acao}";
        $this->metricas[$chave] = ($this->metricas[$chave] ?? 0) + 1;
    }
    
    public function getMetricas(): array {
        return $this->metricas;
    }
}
```

### 2. **Logging de Transições**

```php
class Pedido {
    private Logger $logger;
    
    public function setEstado(EstadoPedido $estado): void {
        $estadoAnterior = get_class($this->estado);
        $novoEstado = get_class($estado);
        
        $this->logger->info("Transição de estado", [
            'de' => $estadoAnterior,
            'para' => $novoEstado,
            'pedido_id' => $this->id,
            'timestamp' => new DateTime()
        ]);
        
        $this->estado = $estado;
    }
}
```

## ⚠️ Armadilhas Comuns

### 1. **Over-engineering**
- Não use o padrão State para casos simples
- Avalie se a complexidade vale a pena

### 2. **Estados com Lógica Complexa**
- Mantenha os estados simples
- Evite lógica de negócio complexa nos estados

### 3. **Falta de Testes**
- Sempre teste as transições
- Teste casos de falha
- Teste validações

### 4. **Estados Mutáveis**
- Evite estado interno nos objetos State
- Mantenha os estados imutáveis

### 5. **Falta de Documentação**
- Documente as transições permitidas
- Documente as regras de negócio
- Mantenha exemplos atualizados

## 🎯 Checklist de Qualidade

### ✅ Implementação
- [ ] Interface State bem definida
- [ ] Estados concretos implementados
- [ ] Context implementado
- [ ] Transições controladas
- [ ] Exceções apropriadas

### ✅ Testes
- [ ] Testes unitários para cada estado
- [ ] Testes de integração para fluxos
- [ ] Testes de casos de falha
- [ ] Cobertura de código adequada

### ✅ Documentação
- [ ] Documentação da arquitetura
- [ ] Exemplos de uso
- [ ] Guia de implementação
- [ ] Troubleshooting

### ✅ Monitoramento
- [ ] Logs de transições
- [ ] Métricas de performance
- [ ] Alertas de falhas
- [ ] Dashboard de monitoramento

## 🚀 Conclusão

O padrão State é uma ferramenta poderosa para gerenciar estados complexos, mas deve ser usado com cuidado. Siga este guia para implementações bem-sucedidas e mantenha sempre a qualidade do código.

---

**Última atualização**: $(date)
**Mantenedor**: Equipe Skynet
**Versão**: 1.0








