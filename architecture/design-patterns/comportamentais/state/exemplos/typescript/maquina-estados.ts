/**
 * Exemplo prático do Padrão State em TypeScript
 * Máquina de estados para controle de pedidos
 * 
 * Este exemplo demonstra como implementar o padrão State
 * para controlar os estados de uma máquina de estados
 */

// Interface que define o contrato para todos os estados
interface EstadoMaquina {
    processar(pedido: Pedido): void;
    cancelar(pedido: Pedido): void;
    finalizar(pedido: Pedido): void;
    getNome(): string;
}

/**
 * Estado inicial - Pedido criado
 */
class EstadoCriado implements EstadoMaquina {
    processar(pedido: Pedido): void {
        console.log("🔄 Processando pedido...");
        pedido.setEstado(new EstadoProcessando());
    }
    
    cancelar(pedido: Pedido): void {
        console.log("❌ Cancelando pedido...");
        pedido.setEstado(new EstadoCancelado());
    }
    
    finalizar(pedido: Pedido): void {
        throw new Error("❌ Pedido não pode ser finalizado sem ser processado");
    }
    
    getNome(): string {
        return "Criado";
    }
}

/**
 * Estado de processamento - Pedido sendo processado
 */
class EstadoProcessando implements EstadoMaquina {
    processar(pedido: Pedido): void {
        throw new Error("❌ Pedido já está sendo processado");
    }
    
    cancelar(pedido: Pedido): void {
        console.log("❌ Cancelando pedido em processamento...");
        pedido.setEstado(new EstadoCancelado());
    }
    
    finalizar(pedido: Pedido): void {
        console.log("✅ Finalizando pedido...");
        pedido.setEstado(new EstadoFinalizado());
    }
    
    getNome(): string {
        return "Processando";
    }
}

/**
 * Estado finalizado - Pedido concluído
 */
class EstadoFinalizado implements EstadoMaquina {
    processar(pedido: Pedido): void {
        throw new Error("❌ Pedido já foi finalizado");
    }
    
    cancelar(pedido: Pedido): void {
        throw new Error("❌ Pedido finalizado não pode ser cancelado");
    }
    
    finalizar(pedido: Pedido): void {
        throw new Error("❌ Pedido já foi finalizado");
    }
    
    getNome(): string {
        return "Finalizado";
    }
}

/**
 * Estado cancelado - Pedido cancelado
 */
class EstadoCancelado implements EstadoMaquina {
    processar(pedido: Pedido): void {
        throw new Error("❌ Pedido cancelado não pode ser processado");
    }
    
    cancelar(pedido: Pedido): void {
        throw new Error("❌ Pedido já foi cancelado");
    }
    
    finalizar(pedido: Pedido): void {
        throw new Error("❌ Pedido cancelado não pode ser finalizado");
    }
    
    getNome(): string {
        return "Cancelado";
    }
}

/**
 * Classe Pedido - Contexto do padrão State
 */
class Pedido {
    private estado: EstadoMaquina;
    private id: string;
    private cliente: string;
    private itens: string[];
    private dataCriacao: Date;
    private historicoEstados: string[];
    
    constructor(id: string, cliente: string, itens: string[] = []) {
        this.id = id;
        this.cliente = cliente;
        this.itens = itens;
        this.dataCriacao = new Date();
        this.historicoEstados = [];
        
        // Sempre inicia como criado
        this.estado = new EstadoCriado();
        this.historicoEstados.push(this.estado.getNome());
        
        console.log(`📝 Pedido #${id} criado para ${cliente}`);
        console.log(`🛒 Itens: ${itens.join(', ')}`);
        console.log(`⏰ Criado em: ${this.dataCriacao.toLocaleString()}`);
        console.log(`📊 Estado atual: ${this.getEstadoAtual()}\n`);
    }
    
    /**
     * Delega a operação para o estado atual
     */
    processar(): void {
        try {
            this.estado.processar(this);
            this.historicoEstados.push(this.getEstadoAtual());
        } catch (error) {
            console.error(`❌ Erro: ${error.message}`);
        }
    }
    
    /**
     * Delega a operação para o estado atual
     */
    cancelar(): void {
        try {
            this.estado.cancelar(this);
            this.historicoEstados.push(this.getEstadoAtual());
        } catch (error) {
            console.error(`❌ Erro: ${error.message}`);
        }
    }
    
    /**
     * Delega a operação para o estado atual
     */
    finalizar(): void {
        try {
            this.estado.finalizar(this);
            this.historicoEstados.push(this.getEstadoAtual());
        } catch (error) {
            console.error(`❌ Erro: ${error.message}`);
        }
    }
    
    /**
     * Permite que os estados alterem o estado do pedido
     */
    setEstado(estado: EstadoMaquina): void {
        this.estado = estado;
        console.log(`🔄 Estado alterado para: ${this.getEstadoAtual()}\n`);
    }
    
    /**
     * Retorna o nome do estado atual
     */
    getEstadoAtual(): string {
        return this.estado.getNome();
    }
    
    /**
     * Verifica se o pedido pode ser processado
     */
    podeProcessar(): boolean {
        return this.estado instanceof EstadoCriado;
    }
    
    /**
     * Verifica se o pedido pode ser cancelado
     */
    podeCancelar(): boolean {
        return this.estado instanceof EstadoCriado || 
               this.estado instanceof EstadoProcessando;
    }
    
    /**
     * Verifica se o pedido pode ser finalizado
     */
    podeFinalizar(): boolean {
        return this.estado instanceof EstadoProcessando;
    }
    
    /**
     * Retorna informações do pedido
     */
    getInfo(): object {
        return {
            id: this.id,
            cliente: this.cliente,
            estado: this.getEstadoAtual(),
            itens: this.itens,
            dataCriacao: this.dataCriacao.toLocaleString(),
            historico: this.historicoEstados
        };
    }
}

/**
 * Demonstração do uso do padrão State
 */
function demonstrarPadraoState(): void {
    console.log("=== DEMONSTRAÇÃO DO PADRÃO STATE ===\n");
    
    // Criar um pedido
    const pedido = new Pedido("12345", "João Silva", ["Hambúrguer", "Batata Frita", "Refrigerante"]);
    
    // Fluxo normal de um pedido
    console.log("=== FLUXO NORMAL ===");
    pedido.processar();
    pedido.finalizar();
    
    console.log("✅ Pedido processado com sucesso!");
    console.log(`📊 Informações finais: ${JSON.stringify(pedido.getInfo(), null, 2)}\n`);
    
    // Tentativas de violar as regras
    console.log("=== TENTATIVAS DE VIOLAR REGRAS ===");
    const pedido2 = new Pedido("67890", "Maria Santos", ["Pizza", "Coca-Cola"]);
    
    // Tentativa de finalizar sem processar
    pedido2.finalizar();
    
    // Fluxo correto
    console.log("=== FLUXO CORRETO ===");
    pedido2.processar();
    pedido2.finalizar();
    
    // Tentativa de processar pedido já finalizado
    pedido2.processar();
    
    // Demonstração de cancelamento
    console.log("=== CANCELAMENTO DE PEDIDO ===");
    const pedido3 = new Pedido("11111", "Pedro Costa", ["Salada", "Suco"]);
    pedido3.cancelar();
    
    // Tentativa de processar pedido cancelado
    pedido3.processar();
    
    console.log("=== DEMONSTRAÇÃO CONCLUÍDA ===");
}

/**
 * Demonstração de validações de estado
 */
function demonstrarValidacoes(): void {
    console.log("=== VALIDAÇÕES DE ESTADO ===\n");
    
    const pedido = new Pedido("99999", "Ana Lima", ["Café", "Pão de Açúcar"]);
    
    console.log(`Pode processar: ${pedido.podeProcessar()}`);
    console.log(`Pode cancelar: ${pedido.podeCancelar()}`);
    console.log(`Pode finalizar: ${pedido.podeFinalizar()}\n`);
    
    pedido.processar();
    
    console.log(`Pode processar: ${pedido.podeProcessar()}`);
    console.log(`Pode cancelar: ${pedido.podeCancelar()}`);
    console.log(`Pode finalizar: ${pedido.podeFinalizar()}\n`);
    
    pedido.finalizar();
    
    console.log(`Pode processar: ${pedido.podeProcessar()}`);
    console.log(`Pode cancelar: ${pedido.podeCancelar()}`);
    console.log(`Pode finalizar: ${pedido.podeFinalizar()}\n`);
}

// Executar demonstrações
demonstrarPadraoState();
demonstrarValidacoes();





