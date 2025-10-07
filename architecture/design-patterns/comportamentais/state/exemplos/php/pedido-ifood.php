<?php

/**
 * Exemplo prático do Padrão State em PHP
 * Sistema de pedidos do iFood com controle de estados
 * 
 * Este exemplo demonstra como implementar o padrão State
 * para controlar os estados de um pedido de delivery
 */

// Interface que define o contrato para todos os estados
interface EstadoPedido {
    public function preparar(Pedido $pedido): void;
    public function iniciarEntrega(Pedido $pedido): void;
    public function finalizarEntrega(Pedido $pedido): void;
}

/**
 * Estado inicial - Pedido recém criado
 * Pode apenas transitar para Preparando
 */
class Realizado implements EstadoPedido {
    public function preparar(Pedido $pedido): void {
        echo "🍳 Preparando pedido...\n";
        $pedido->setEstado(new Preparando());
    }
    
    public function iniciarEntrega(Pedido $pedido): void {
        throw new DomainException("❌ Pedido ainda não foi preparado");
    }
    
    public function finalizarEntrega(Pedido $pedido): void {
        throw new DomainException("❌ Pedido ainda não foi preparado");
    }
}

/**
 * Estado de preparação - Pedido sendo preparado
 * Pode apenas transitar para EntregaIniciada
 */
class Preparando implements EstadoPedido {
    public function preparar(Pedido $pedido): void {
        throw new DomainException("❌ Pedido já está sendo preparado");
    }
    
    public function iniciarEntrega(Pedido $pedido): void {
        echo "🚚 Iniciando entrega...\n";
        $pedido->setEstado(new EntregaIniciada());
    }
    
    public function finalizarEntrega(Pedido $pedido): void {
        throw new DomainException("❌ Pedido não pode ser finalizado pois ainda está sendo preparado");
    }
}

/**
 * Estado de entrega iniciada - Pedido saiu para entrega
 * Pode apenas transitar para EntregaFinalizada
 */
class EntregaIniciada implements EstadoPedido {
    public function preparar(Pedido $pedido): void {
        throw new DomainException("❌ Pedido já foi preparado");
    }
    
    public function iniciarEntrega(Pedido $pedido): void {
        throw new DomainException("❌ Pedido já saiu para o cliente");
    }
    
    public function finalizarEntrega(Pedido $pedido): void {
        echo "✅ Entrega finalizada!\n";
        $pedido->setEstado(new EntregaFinalizada());
    }
}

/**
 * Estado final - Pedido entregue
 * Não pode transitar para nenhum outro estado
 */
class EntregaFinalizada implements EstadoPedido {
    public function preparar(Pedido $pedido): void {
        throw new DomainException("❌ Pedido já foi entregue ao cliente");
    }
    
    public function iniciarEntrega(Pedido $pedido): void {
        throw new DomainException("❌ Pedido já foi entregue ao cliente");
    }
    
    public function finalizarEntrega(Pedido $pedido): void {
        throw new DomainException("❌ Pedido já foi entregue ao cliente");
    }
}

/**
 * Classe Pedido - Contexto do padrão State
 * Representa um pedido que pode estar em diferentes estados
 */
class Pedido {
    private EstadoPedido $estado;
    private string $id;
    private string $cliente;
    private array $itens;
    private DateTime $criadoEm;
    
    public function __construct(string $id, string $cliente, array $itens = []) {
        $this->id = $id;
        $this->cliente = $cliente;
        $this->itens = $itens;
        $this->criadoEm = new DateTime();
        
        // Sempre inicia como realizado
        $this->estado = new Realizado();
        
        echo "📝 Pedido #{$id} criado para {$cliente}\n";
        echo "🛒 Itens: " . implode(', ', $itens) . "\n";
        echo "⏰ Criado em: " . $this->criadoEm->format('d/m/Y H:i:s') . "\n\n";
    }
    
    /**
     * Delega a operação para o estado atual
     */
    public function preparar(): void {
        $this->estado->preparar($this);
    }
    
    /**
     * Delega a operação para o estado atual
     */
    public function iniciarEntrega(): void {
        $this->estado->iniciarEntrega($this);
    }
    
    /**
     * Delega a operação para o estado atual
     */
    public function finalizarEntrega(): void {
        $this->estado->finalizarEntrega($this);
    }
    
    /**
     * Permite que os estados alterem o estado do pedido
     */
    public function setEstado(EstadoPedido $estado): void {
        $this->estado = $estado;
        echo "🔄 Estado alterado para: " . get_class($estado) . "\n\n";
    }
    
    /**
     * Retorna informações do pedido
     */
    public function getInfo(): array {
        return [
            'id' => $this->id,
            'cliente' => $this->cliente,
            'estado' => get_class($this->estado),
            'itens' => $this->itens,
            'criado_em' => $this->criadoEm->format('d/m/Y H:i:s')
        ];
    }
    
    /**
     * Verifica se o pedido pode ser cancelado
     */
    public function podeCancelar(): bool {
        return $this->estado instanceof Realizado || 
               $this->estado instanceof Preparando;
    }
    
    /**
     * Cancela o pedido (apenas se possível)
     */
    public function cancelar(): void {
        if (!$this->podeCancelar()) {
            throw new DomainException("❌ Pedido não pode ser cancelado no estado atual");
        }
        
        echo "❌ Pedido #{$this->id} cancelado\n";
        $this->estado = new Cancelado();
    }
}

/**
 * Estado especial para pedidos cancelados
 */
class Cancelado implements EstadoPedido {
    public function preparar(Pedido $pedido): void {
        throw new DomainException("❌ Pedido cancelado não pode ser preparado");
    }
    
    public function iniciarEntrega(Pedido $pedido): void {
        throw new DomainException("❌ Pedido cancelado não pode ser entregue");
    }
    
    public function finalizarEntrega(Pedido $pedido): void {
        throw new DomainException("❌ Pedido cancelado não pode ser finalizado");
    }
}

/**
 * Demonstração do uso do padrão State
 */
function demonstrarPadraoState(): void {
    echo "=== DEMONSTRAÇÃO DO PADRÃO STATE ===\n\n";
    
    // Criar um pedido
    $pedido = new Pedido("12345", "João Silva", ["Hambúrguer", "Batata Frita", "Refrigerante"]);
    
    // Fluxo normal de um pedido
    echo "=== FLUXO NORMAL ===\n";
    
    try {
        $pedido->preparar();
        $pedido->iniciarEntrega();
        $pedido->finalizarEntrega();
        
        echo "✅ Pedido processado com sucesso!\n\n";
    } catch (DomainException $e) {
        echo "Erro: " . $e->getMessage() . "\n\n";
    }
    
    // Tentativas de violar as regras
    echo "=== TENTATIVAS DE VIOLAR REGRAS ===\n";
    
    $pedido2 = new Pedido("67890", "Maria Santos", ["Pizza", "Coca-Cola"]);
    
    try {
        $pedido2->iniciarEntrega(); // Deveria falhar
    } catch (DomainException $e) {
        echo "✅ Regra respeitada: " . $e->getMessage() . "\n";
    }
    
    try {
        $pedido2->finalizarEntrega(); // Deveria falhar
    } catch (DomainException $e) {
        echo "✅ Regra respeitada: " . $e->getMessage() . "\n";
    }
    
    // Fluxo correto
    echo "\n=== FLUXO CORRETO ===\n";
    $pedido2->preparar();
    $pedido2->iniciarEntrega();
    $pedido2->finalizarEntrega();
    
    // Tentativa de cancelar pedido já entregue
    echo "\n=== TENTATIVA DE CANCELAR PEDIDO ENTREGUE ===\n";
    try {
        $pedido->cancelar();
    } catch (DomainException $e) {
        echo "✅ Regra respeitada: " . $e->getMessage() . "\n";
    }
    
    // Cancelamento de pedido em preparação
    echo "\n=== CANCELAMENTO DE PEDIDO EM PREPARAÇÃO ===\n";
    $pedido3 = new Pedido("11111", "Pedro Costa", ["Salada", "Suco"]);
    $pedido3->preparar();
    $pedido3->cancelar();
    
    echo "\n=== DEMONSTRAÇÃO CONCLUÍDA ===\n";
}

// Executar demonstração
demonstrarPadraoState();

