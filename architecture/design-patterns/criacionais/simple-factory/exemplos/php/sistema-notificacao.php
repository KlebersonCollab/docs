<?php

/**
 * Exemplo do Padrão Simple Factory - Sistema de Notificações
 * 
 * Este exemplo demonstra como implementar o padrão Simple Factory para criar
 * diferentes tipos de notificações (Email, SMS, Slack) de forma centralizada
 * e reutilizável.
 */

// Interface para notificações
interface NotificationInterface 
{
    public function send(string $message, string $recipient): bool;
    public function getType(): string;
    public function getPriority(): int;
}

// Implementação concreta: Email
class EmailNotification implements NotificationInterface 
{
    public function send(string $message, string $recipient): bool 
    {
        // Simular envio de email
        echo "📧 Enviando email para: {$recipient}\n";
        echo "📝 Mensagem: {$message}\n";
        echo "✅ Email enviado com sucesso!\n\n";
        
        return true;
    }
    
    public function getType(): string 
    {
        return 'email';
    }
    
    public function getPriority(): int 
    {
        return 1; // Alta prioridade
    }
}

// Implementação concreta: SMS
class SMSNotification implements NotificationInterface 
{
    public function send(string $message, string $recipient): bool 
    {
        // Simular envio de SMS
        echo "📱 Enviando SMS para: {$recipient}\n";
        echo "📝 Mensagem: {$message}\n";
        echo "✅ SMS enviado com sucesso!\n\n";
        
        return true;
    }
    
    public function getType(): string 
    {
        return 'sms';
    }
    
    public function getPriority(): int 
    {
        return 2; // Média prioridade
    }
}

// Implementação concreta: Slack
class SlackNotification implements NotificationInterface 
{
    public function send(string $message, string $recipient): bool 
    {
        // Simular envio para Slack
        echo "💬 Enviando mensagem no Slack para: {$recipient}\n";
        echo "📝 Mensagem: {$message}\n";
        echo "✅ Mensagem enviada no Slack com sucesso!\n\n";
        
        return true;
    }
    
    public function getType(): string 
    {
        return 'slack';
    }
    
    public function getPriority(): int 
    {
        return 3; // Baixa prioridade
    }
}

// Implementação concreta: WhatsApp
class WhatsAppNotification implements NotificationInterface 
{
    public function send(string $message, string $recipient): bool 
    {
        // Simular envio via WhatsApp
        echo "📲 Enviando WhatsApp para: {$recipient}\n";
        echo "📝 Mensagem: {$message}\n";
        echo "✅ WhatsApp enviado com sucesso!\n\n";
        
        return true;
    }
    
    public function getType(): string 
    {
        return 'whatsapp';
    }
    
    public function getPriority(): int 
    {
        return 1; // Alta prioridade
    }
}

// Simple Factory para criar notificações
class NotificationFactory 
{
    /**
     * Cria uma instância de notificação baseada no tipo
     */
    public static function create(string $type): NotificationInterface 
    {
        return match($type) {
            'email' => new EmailNotification(),
            'sms' => new SMSNotification(),
            'slack' => new SlackNotification(),
            'whatsapp' => new WhatsAppNotification(),
            default => throw new InvalidArgumentException("Tipo de notificação '{$type}' não suportado")
        };
    }
    
    /**
     * Retorna lista de tipos suportados
     */
    public static function getSupportedTypes(): array 
    {
        return ['email', 'sms', 'slack', 'whatsapp'];
    }
    
    /**
     * Verifica se um tipo é suportado
     */
    public static function isSupported(string $type): bool 
    {
        return in_array($type, self::getSupportedTypes());
    }
}

// Controller que usa a Factory
class NotificationController 
{
    /**
     * Envia notificação usando a Factory
     */
    public function sendNotification(string $type, string $message, string $recipient): array 
    {
        try {
            // Validar tipo antes de criar
            if (!NotificationFactory::isSupported($type)) {
                return [
                    'success' => false,
                    'error' => "Tipo '{$type}' não suportado",
                    'supported_types' => NotificationFactory::getSupportedTypes()
                ];
            }
            
            // Criar notificação usando Factory
            $notification = NotificationFactory::create($type);
            
            // Enviar notificação
            $result = $notification->send($message, $recipient);
            
            return [
                'success' => $result,
                'type' => $notification->getType(),
                'priority' => $notification->getPriority(),
                'message' => 'Notificação enviada com sucesso'
            ];
            
        } catch (InvalidArgumentException $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => 'Erro interno: ' . $e->getMessage()
            ];
        }
    }
}

// Serviço de notificação que demonstra reutilização
class NotificationService 
{
    private NotificationController $controller;
    
    public function __construct(NotificationController $controller) 
    {
        $this->controller = $controller;
    }
    
    /**
     * Envia notificação de boas-vindas
     */
    public function sendWelcomeNotification(string $userEmail, string $userName): array 
    {
        $message = "Bem-vindo ao nosso sistema, {$userName}!";
        return $this->controller->sendNotification('email', $message, $userEmail);
    }
    
    /**
     * Envia notificação de alerta
     */
    public function sendAlertNotification(string $phoneNumber, string $alertMessage): array 
    {
        return $this->controller->sendNotification('sms', $alertMessage, $phoneNumber);
    }
    
    /**
     * Envia notificação para equipe
     */
    public function sendTeamNotification(string $slackChannel, string $teamMessage): array 
    {
        return $this->controller->sendNotification('slack', $teamMessage, $slackChannel);
    }
    
    /**
     * Envia notificação urgente via WhatsApp
     */
    public function sendUrgentNotification(string $whatsappNumber, string $urgentMessage): array 
    {
        return $this->controller->sendNotification('whatsapp', $urgentMessage, $whatsappNumber);
    }
}

// Exemplo de uso
function demonstrateSimpleFactory(): void 
{
    echo "=== Demonstração do Padrão Simple Factory ===\n\n";
    
    // Criar instâncias
    $controller = new NotificationController();
    $service = new NotificationService($controller);
    
    // Casos de teste
    $testCases = [
        [
            'type' => 'email',
            'message' => 'Sua conta foi criada com sucesso!',
            'recipient' => 'usuario@email.com'
        ],
        [
            'type' => 'sms',
            'message' => 'Código de verificação: 123456',
            'recipient' => '(11) 99999-9999'
        ],
        [
            'type' => 'slack',
            'message' => 'Nova tarefa atribuída a você',
            'recipient' => '#geral'
        ],
        [
            'type' => 'whatsapp',
            'message' => 'Lembrete: Reunião em 30 minutos',
            'recipient' => '+5511999999999'
        ],
        [
            'type' => 'telegram', // Tipo não suportado
            'message' => 'Mensagem de teste',
            'recipient' => '@usuario'
        ]
    ];
    
    foreach ($testCases as $index => $testCase) {
        echo "--- Teste " . ($index + 1) . ": {$testCase['type']} ---\n";
        
        $result = $controller->sendNotification(
            $testCase['type'],
            $testCase['message'],
            $testCase['recipient']
        );
        
        if ($result['success']) {
            echo "✅ Sucesso: {$result['message']}\n";
            echo "📊 Tipo: {$result['type']}\n";
            echo "⚡ Prioridade: {$result['priority']}\n";
        } else {
            echo "❌ Erro: {$result['error']}\n";
            if (isset($result['supported_types'])) {
                echo "📋 Tipos suportados: " . implode(', ', $result['supported_types']) . "\n";
            }
        }
        
        echo "\n";
    }
}

// Demonstração de reutilização
function demonstrateReusability(): void 
{
    echo "=== Demonstração de Reutilização ===\n\n";
    
    $controller = new NotificationController();
    $service = new NotificationService($controller);
    
    // Diferentes cenários usando o mesmo serviço
    $scenarios = [
        [
            'name' => 'Boas-vindas',
            'action' => fn() => $service->sendWelcomeNotification('novo@usuario.com', 'João Silva')
        ],
        [
            'name' => 'Alerta',
            'action' => fn() => $service->sendAlertNotification('(11) 99999-9999', 'Sistema em manutenção')
        ],
        [
            'name' => 'Equipe',
            'action' => fn() => $service->sendTeamNotification('#dev', 'Deploy realizado com sucesso')
        ],
        [
            'name' => 'Urgente',
            'action' => fn() => $service->sendUrgentNotification('+5511999999999', 'Ação imediata necessária')
        ]
    ];
    
    foreach ($scenarios as $scenario) {
        echo "--- Cenário: {$scenario['name']} ---\n";
        $result = $scenario['action']();
        
        if ($result['success']) {
            echo "✅ {$result['message']}\n";
        } else {
            echo "❌ {$result['error']}\n";
        }
        
        echo "\n";
    }
}

// Demonstração de flexibilidade
function demonstrateFlexibility(): void 
{
    echo "=== Demonstração de Flexibilidade ===\n\n";
    
    echo "Tipos de notificação suportados:\n";
    foreach (NotificationFactory::getSupportedTypes() as $type) {
        $notification = NotificationFactory::create($type);
        echo "- {$type}: Prioridade {$notification->getPriority()}\n";
    }
    
    echo "\nVerificações de suporte:\n";
    $testTypes = ['email', 'sms', 'telegram', 'whatsapp'];
    
    foreach ($testTypes as $type) {
        $supported = NotificationFactory::isSupported($type);
        $status = $supported ? '✅' : '❌';
        echo "{$status} {$type}: " . ($supported ? 'Suportado' : 'Não suportado') . "\n";
    }
}

// Executar demonstrações
if (php_sapi_name() === 'cli') {
    demonstrateSimpleFactory();
    echo "\n" . str_repeat("=", 50) . "\n\n";
    demonstrateReusability();
    echo "\n" . str_repeat("=", 50) . "\n\n";
    demonstrateFlexibility();
}








