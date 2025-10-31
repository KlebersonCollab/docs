<?php

/**
 * Exemplo do Padrão Facade - Sistema de E-commerce
 * 
 * Este exemplo demonstra como implementar o padrão Facade para simplificar
 * o processamento de pedidos em um sistema de e-commerce, ocultando a
 * complexidade de múltiplos subsistemas.
 */

// Subsistema 1: Processamento de Pagamento
class PaymentProcessor 
{
    public function processPayment(array $orderDetails): bool 
    {
        $amount = $orderDetails['amount'];
        $paymentMethod = $orderDetails['payment_method'];
        
        echo "💳 Processando pagamento de R$ {$amount} via {$paymentMethod}\n";
        
        // Simular processamento
        sleep(1);
        
        // Simular falha ocasional (5% de chance)
        if (rand(1, 100) <= 5) {
            throw new Exception('Falha no processamento do pagamento');
        }
        
        echo "✅ Pagamento processado com sucesso!\n";
        return true;
    }
    
    public function validatePaymentMethod(string $method): bool 
    {
        $validMethods = ['credit_card', 'debit_card', 'pix', 'boleto'];
        return in_array($method, $validMethods);
    }
}

// Subsistema 2: Sistema de Notificações
class Notifier 
{
    public function sendConfirmation(array $orderDetails): void 
    {
        $customerEmail = $orderDetails['customer_email'];
        $orderId = $orderDetails['order_id'];
        
        echo "📧 Enviando confirmação para: {$customerEmail}\n";
        echo "📝 Pedido #{$orderId} confirmado com sucesso!\n";
        
        // Simular envio de email
        sleep(1);
        
        echo "✅ Email de confirmação enviado!\n";
    }
    
    public function sendInventoryAlert(array $orderDetails): void 
    {
        $productId = $orderDetails['product_id'];
        $quantity = $orderDetails['quantity'];
        
        echo "📊 Enviando alerta de estoque para comercial\n";
        echo "📦 Produto #{$productId} - Quantidade: {$quantity}\n";
        
        // Simular envio de alerta
        sleep(1);
        
        echo "✅ Alerta de estoque enviado!\n";
    }
}

// Subsistema 3: Gerenciamento de Estoque
class InventoryManager 
{
    public function updateStock(array $orderDetails): void 
    {
        $productId = $orderDetails['product_id'];
        $quantity = $orderDetails['quantity'];
        
        echo "📦 Atualizando estoque do produto #{$productId}\n";
        echo "📊 Reduzindo {$quantity} unidades do estoque\n";
        
        // Simular atualização de estoque
        sleep(1);
        
        echo "✅ Estoque atualizado com sucesso!\n";
    }
    
    public function checkStock(int $productId, int $quantity): bool 
    {
        // Simular verificação de estoque
        $availableStock = rand(0, 100);
        
        echo "🔍 Verificando estoque disponível: {$availableStock} unidades\n";
        
        return $availableStock >= $quantity;
    }
}

// Subsistema 4: Serviço de Entrega
class DeliveryService 
{
    public function initializeDelivery(array $orderDetails): void 
    {
        $customerAddress = $orderDetails['customer_address'];
        $orderId = $orderDetails['order_id'];
        
        echo "🚚 Inicializando entrega para pedido #{$orderId}\n";
        echo "📍 Endereço: {$customerAddress}\n";
        
        // Simular inicialização da entrega
        sleep(1);
        
        echo "✅ Entrega inicializada com sucesso!\n";
    }
    
    public function calculateDeliveryTime(string $address): int 
    {
        // Simular cálculo de tempo de entrega
        $baseTime = 24; // horas
        $randomFactor = rand(0, 48);
        
        return $baseTime + $randomFactor;
    }
}

// Facade: Interface simplificada para o subsistema complexo
class OrderFacade 
{
    private PaymentProcessor $paymentProcessor;
    private Notifier $notifier;
    private InventoryManager $inventoryManager;
    private DeliveryService $deliveryService;
    
    public function __construct() 
    {
        $this->paymentProcessor = new PaymentProcessor();
        $this->notifier = new Notifier();
        $this->inventoryManager = new InventoryManager();
        $this->deliveryService = new DeliveryService();
    }
    
    /**
     * Processa um pedido completo - método principal da facade
     */
    public function processOrder(array $orderDetails): array 
    {
        echo "🛒 Iniciando processamento do pedido #{$orderDetails['order_id']}\n\n";
        
        try {
            // 1. Verificar estoque
            if (!$this->inventoryManager->checkStock($orderDetails['product_id'], $orderDetails['quantity'])) {
                throw new Exception('Estoque insuficiente');
            }
            
            // 2. Processar pagamento
            $this->paymentProcessor->processPayment($orderDetails);
            
            // 3. Enviar confirmação
            $this->notifier->sendConfirmation($orderDetails);
            
            // 4. Atualizar estoque
            $this->inventoryManager->updateStock($orderDetails);
            
            // 5. Inicializar entrega
            $this->deliveryService->initializeDelivery($orderDetails);
            
            // 6. Enviar alerta de estoque para comercial
            $this->notifier->sendInventoryAlert($orderDetails);
            
            echo "\n🎉 Pedido processado com sucesso!\n";
            
            return [
                'success' => true,
                'order_id' => $orderDetails['order_id'],
                'message' => 'Pedido processado com sucesso'
            ];
            
        } catch (Exception $e) {
            echo "\n❌ Erro no processamento: {$e->getMessage()}\n";
            
            return [
                'success' => false,
                'order_id' => $orderDetails['order_id'],
                'error' => $e->getMessage()
            ];
        }
    }
    
    /**
     * Processa apenas o pagamento (método específico)
     */
    public function processPaymentOnly(array $orderDetails): bool 
    {
        try {
            $this->paymentProcessor->processPayment($orderDetails);
            return true;
        } catch (Exception $e) {
            echo "❌ Erro no pagamento: {$e->getMessage()}\n";
            return false;
        }
    }
    
    /**
     * Verifica estoque sem processar pedido
     */
    public function checkStock(int $productId, int $quantity): bool 
    {
        return $this->inventoryManager->checkStock($productId, $quantity);
    }
}

// Controller que usa a Facade
class OrderController 
{
    private OrderFacade $orderFacade;
    
    public function __construct(OrderFacade $orderFacade) 
    {
        $this->orderFacade = $orderFacade;
    }
    
    /**
     * Endpoint para criar pedido
     */
    public function createOrder(array $requestData): array 
    {
        $orderDetails = [
            'order_id' => $requestData['order_id'],
            'customer_email' => $requestData['customer_email'],
            'customer_address' => $requestData['customer_address'],
            'product_id' => $requestData['product_id'],
            'quantity' => $requestData['quantity'],
            'amount' => $requestData['amount'],
            'payment_method' => $requestData['payment_method']
        ];
        
        // Apenas chama a facade - não conhece a complexidade
        return $this->orderFacade->processOrder($orderDetails);
    }
}

// Serviço de pedidos que demonstra reutilização
class OrderService 
{
    private OrderFacade $orderFacade;
    
    public function __construct(OrderFacade $orderFacade) 
    {
        $this->orderFacade = $orderFacade;
    }
    
    /**
     * Processa pedido de cliente
     */
    public function processCustomerOrder(array $orderData): array 
    {
        return $this->orderFacade->processOrder($orderData);
    }
    
    /**
     * Processa pedido de revenda
     */
    public function processResellerOrder(array $orderData): array 
    {
        // Lógica específica para revenda
        $orderData['payment_method'] = 'credit_card';
        return $this->orderFacade->processOrder($orderData);
    }
    
    /**
     * Verifica disponibilidade de produto
     */
    public function checkProductAvailability(int $productId, int $quantity): bool 
    {
        return $this->orderFacade->checkStock($productId, $quantity);
    }
}

// Exemplo de uso
function demonstrateFacadePattern(): void 
{
    echo "=== Demonstração do Padrão Facade - E-commerce ===\n\n";
    
    // Criar facade
    $orderFacade = new OrderFacade();
    
    // Criar controller
    $controller = new OrderController($orderFacade);
    
    // Dados de exemplo
    $orderData = [
        'order_id' => 'ORD-001',
        'customer_email' => 'cliente@email.com',
        'customer_address' => 'Rua das Flores, 123',
        'product_id' => 101,
        'quantity' => 2,
        'amount' => 199.90,
        'payment_method' => 'credit_card'
    ];
    
    echo "--- Processando Pedido Completo ---\n";
    $result = $controller->createOrder($orderData);
    
    if ($result['success']) {
        echo "✅ Pedido criado com sucesso!\n";
    } else {
        echo "❌ Falha ao criar pedido: {$result['error']}\n";
    }
    
    echo "\n" . str_repeat("=", 50) . "\n\n";
}

// Demonstração de reutilização
function demonstrateReusability(): void 
{
    echo "=== Demonstração de Reutilização ===\n\n";
    
    $orderFacade = new OrderFacade();
    $orderService = new OrderService($orderFacade);
    
    // Dados para diferentes tipos de pedido
    $customerOrder = [
        'order_id' => 'CUST-001',
        'customer_email' => 'cliente@email.com',
        'customer_address' => 'Rua A, 123',
        'product_id' => 201,
        'quantity' => 1,
        'amount' => 99.90,
        'payment_method' => 'pix'
    ];
    
    $resellerOrder = [
        'order_id' => 'RESELLER-001',
        'customer_email' => 'revenda@empresa.com',
        'customer_address' => 'Rua B, 456',
        'product_id' => 301,
        'quantity' => 10,
        'amount' => 999.00,
        'payment_method' => 'credit_card'
    ];
    
    echo "--- Pedido de Cliente ---\n";
    $result1 = $orderService->processCustomerOrder($customerOrder);
    echo ($result1['success'] ? "✅ Sucesso" : "❌ Falha") . "\n\n";
    
    echo "--- Pedido de Revenda ---\n";
    $result2 = $orderService->processResellerOrder($resellerOrder);
    echo ($result2['success'] ? "✅ Sucesso" : "❌ Falha") . "\n\n";
}

// Demonstração de métodos específicos
function demonstrateSpecificMethods(): void 
{
    echo "=== Demonstração de Métodos Específicos ===\n\n";
    
    $orderFacade = new OrderFacade();
    
    // Verificar estoque
    echo "--- Verificando Estoque ---\n";
    $hasStock = $orderFacade->checkStock(101, 5);
    echo ($hasStock ? "✅ Estoque disponível" : "❌ Estoque insuficiente") . "\n\n";
    
    // Processar apenas pagamento
    echo "--- Processando Apenas Pagamento ---\n";
    $paymentData = [
        'amount' => 150.00,
        'payment_method' => 'credit_card'
    ];
    
    $paymentSuccess = $orderFacade->processPaymentOnly($paymentData);
    echo ($paymentSuccess ? "✅ Pagamento processado" : "❌ Falha no pagamento") . "\n\n";
}

// Executar demonstrações
if (php_sapi_name() === 'cli') {
    demonstrateFacadePattern();
    demonstrateReusability();
    demonstrateSpecificMethods();
}








