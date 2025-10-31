/**
 * Exemplo do Padrão Strategy - Sistema de Notificação
 * 
 * Este exemplo demonstra como implementar o padrão Strategy para enviar
 * diferentes tipos de notificações (Email, SMS, Push, WhatsApp) de forma
 * flexível e respeitando os princípios SOLID.
 */

// Enums para tipos e status
enum NotificationType {
  EMAIL = 'email',
  SMS = 'sms',
  PUSH = 'push',
  WHATSAPP = 'whatsapp'
}

enum NotificationStatus {
  PENDING = 'pending',
  SENT = 'sent',
  FAILED = 'failed',
  DELIVERED = 'delivered'
}

// Interfaces
interface NotificationData {
  recipient: string;
  message: string;
  subject?: string;
  metadata?: Record<string, any>;
}

interface NotificationResult {
  status: NotificationStatus;
  message: string;
  notificationId?: string;
  deliveryTime?: Date;
  error?: string;
}

// Interface da estratégia
interface NotificationStrategy {
  send(data: NotificationData): Promise<NotificationResult>;
  getType(): NotificationType;
  getPriority(): number;
  validateData(data: NotificationData): boolean;
}

// Estratégia concreta: Email
class EmailNotificationStrategy implements NotificationStrategy {
  private readonly priority = 1;
  private readonly type = NotificationType.EMAIL;

  async send(data: NotificationData): Promise<NotificationResult> {
    if (!this.validateData(data)) {
      return {
        status: NotificationStatus.FAILED,
        message: 'Dados de email inválidos',
        error: 'Email ou assunto não fornecido'
      };
    }

    try {
      // Simular envio de email
      await this.simulateEmailSending(data);
      
      return {
        status: NotificationStatus.SENT,
        message: 'Email enviado com sucesso',
        notificationId: `EMAIL_${Date.now()}`,
        deliveryTime: new Date()
      };
    } catch (error) {
      return {
        status: NotificationStatus.FAILED,
        message: 'Falha ao enviar email',
        error: error instanceof Error ? error.message : 'Erro desconhecido'
      };
    }
  }

  getType(): NotificationType {
    return this.type;
  }

  getPriority(): number {
    return this.priority;
  }

  validateData(data: NotificationData): boolean {
    return !!(data.recipient && data.subject && this.isValidEmail(data.recipient));
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  private async simulateEmailSending(data: NotificationData): Promise<void> {
    // Simular delay de envio
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Simular falha ocasional (10% de chance)
    if (Math.random() < 0.1) {
      throw new Error('Servidor de email indisponível');
    }
  }
}

// Estratégia concreta: SMS
class SMSNotificationStrategy implements NotificationStrategy {
  private readonly priority = 2;
  private readonly type = NotificationType.SMS;

  async send(data: NotificationData): Promise<NotificationResult> {
    if (!this.validateData(data)) {
      return {
        status: NotificationStatus.FAILED,
        message: 'Dados de SMS inválidos',
        error: 'Número de telefone inválido'
      };
    }

    try {
      // Simular envio de SMS
      await this.simulateSMSSending(data);
      
      return {
        status: NotificationStatus.SENT,
        message: 'SMS enviado com sucesso',
        notificationId: `SMS_${Date.now()}`,
        deliveryTime: new Date()
      };
    } catch (error) {
      return {
        status: NotificationStatus.FAILED,
        message: 'Falha ao enviar SMS',
        error: error instanceof Error ? error.message : 'Erro desconhecido'
      };
    }
  }

  getType(): NotificationType {
    return this.type;
  }

  getPriority(): number {
    return this.priority;
  }

  validateData(data: NotificationData): boolean {
    return !!(data.recipient && this.isValidPhone(data.recipient));
  }

  private isValidPhone(phone: string): boolean {
    // Validação simples de telefone brasileiro
    const phoneRegex = /^\(\d{2}\)\s\d{4,5}-\d{4}$/;
    return phoneRegex.test(phone);
  }

  private async simulateSMSSending(data: NotificationData): Promise<void> {
    // Simular delay de envio
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Simular falha ocasional (5% de chance)
    if (Math.random() < 0.05) {
      throw new Error('Operadora de telefone indisponível');
    }
  }
}

// Estratégia concreta: Push
class PushNotificationStrategy implements NotificationStrategy {
  private readonly priority = 3;
  private readonly type = NotificationType.PUSH;

  async send(data: NotificationData): Promise<NotificationResult> {
    if (!this.validateData(data)) {
      return {
        status: NotificationStatus.FAILED,
        message: 'Dados de push inválidos',
        error: 'Token de dispositivo inválido'
      };
    }

    try {
      // Simular envio de push
      await this.simulatePushSending(data);
      
      return {
        status: NotificationStatus.DELIVERED,
        message: 'Push entregue com sucesso',
        notificationId: `PUSH_${Date.now()}`,
        deliveryTime: new Date()
      };
    } catch (error) {
      return {
        status: NotificationStatus.FAILED,
        message: 'Falha ao enviar push',
        error: error instanceof Error ? error.message : 'Erro desconhecido'
      };
    }
  }

  getType(): NotificationType {
    return this.type;
  }

  getPriority(): number {
    return this.priority;
  }

  validateData(data: NotificationData): boolean {
    return !!(data.recipient && this.isValidDeviceToken(data.recipient));
  }

  private isValidDeviceToken(token: string): boolean {
    // Validação simples de token de dispositivo
    return token.length >= 20 && /^[a-zA-Z0-9]+$/.test(token);
  }

  private async simulatePushSending(data: NotificationData): Promise<void> {
    // Simular delay de envio
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Simular falha ocasional (3% de chance)
    if (Math.random() < 0.03) {
      throw new Error('Serviço de push indisponível');
    }
  }
}

// Estratégia concreta: WhatsApp
class WhatsAppNotificationStrategy implements NotificationStrategy {
  private readonly priority = 4;
  private readonly type = NotificationType.WHATSAPP;

  async send(data: NotificationData): Promise<NotificationResult> {
    if (!this.validateData(data)) {
      return {
        status: NotificationStatus.FAILED,
        message: 'Dados do WhatsApp inválidos',
        error: 'Número do WhatsApp inválido'
      };
    }

    try {
      // Simular envio do WhatsApp
      await this.simulateWhatsAppSending(data);
      
      return {
        status: NotificationStatus.DELIVERED,
        message: 'WhatsApp enviado com sucesso',
        notificationId: `WA_${Date.now()}`,
        deliveryTime: new Date()
      };
    } catch (error) {
      return {
        status: NotificationStatus.FAILED,
        message: 'Falha ao enviar WhatsApp',
        error: error instanceof Error ? error.message : 'Erro desconhecido'
      };
    }
  }

  getType(): NotificationType {
    return this.type;
  }

  getPriority(): number {
    return this.priority;
  }

  validateData(data: NotificationData): boolean {
    return !!(data.recipient && this.isValidWhatsAppNumber(data.recipient));
  }

  private isValidWhatsAppNumber(phone: string): boolean {
    // Validação simples de número do WhatsApp
    const whatsappRegex = /^\+55\d{10,11}$/;
    return whatsappRegex.test(phone);
  }

  private async simulateWhatsAppSending(data: NotificationData): Promise<void> {
    // Simular delay de envio
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Simular falha ocasional (2% de chance)
    if (Math.random() < 0.02) {
      throw new Error('API do WhatsApp indisponível');
    }
  }
}

// Contexto - Gerenciador de Notificações
class NotificationManager {
  private strategy: NotificationStrategy | null = null;

  setStrategy(strategy: NotificationStrategy): NotificationManager {
    this.strategy = strategy;
    return this;
  }

  async sendNotification(data: NotificationData): Promise<NotificationResult> {
    if (!this.strategy) {
      throw new Error('Estratégia de notificação não definida');
    }

    return await this.strategy.send(data);
  }

  getStrategyInfo(): { type: NotificationType; priority: number } | null {
    if (!this.strategy) {
      return null;
    }

    return {
      type: this.strategy.getType(),
      priority: this.strategy.getPriority()
    };
  }
}

// Factory para criar estratégias
class NotificationStrategyFactory {
  static createStrategy(type: NotificationType): NotificationStrategy {
    const strategies = {
      [NotificationType.EMAIL]: EmailNotificationStrategy,
      [NotificationType.SMS]: SMSNotificationStrategy,
      [NotificationType.PUSH]: PushNotificationStrategy,
      [NotificationType.WHATSAPP]: WhatsAppNotificationStrategy
    };

    const StrategyClass = strategies[type];
    if (!StrategyClass) {
      throw new Error(`Tipo de notificação '${type}' não suportado`);
    }

    return new StrategyClass();
  }

  static getAvailableTypes(): NotificationType[] {
    return Object.values(NotificationType);
  }
}

// Exemplo de uso
async function demonstrateNotificationStrategy(): Promise<void> {
  console.log('=== Demonstração do Padrão Strategy para Notificações ===\n');

  const manager = new NotificationManager();

  // Casos de teste
  const testCases = [
    {
      type: NotificationType.EMAIL,
      data: {
        recipient: 'usuario@email.com',
        message: 'Bem-vindo ao nosso sistema!',
        subject: 'Bem-vindo'
      }
    },
    {
      type: NotificationType.SMS,
      data: {
        recipient: '(11) 99999-9999',
        message: 'Seu código de verificação é: 123456'
      }
    },
    {
      type: NotificationType.PUSH,
      data: {
        recipient: 'abc123def456ghi789jkl012mno345pqr678',
        message: 'Você tem uma nova mensagem!'
      }
    },
    {
      type: NotificationType.WHATSAPP,
      data: {
        recipient: '+5511999999999',
        message: 'Olá! Seu pedido foi confirmado.'
      }
    }
  ];

  for (const testCase of testCases) {
    console.log(`--- Enviando ${testCase.type.toUpperCase()} ---`);
    
    try {
      // Criar estratégia
      const strategy = NotificationStrategyFactory.createStrategy(testCase.type);
      
      // Configurar manager
      manager.setStrategy(strategy);
      
      // Enviar notificação
      const result = await manager.sendNotification(testCase.data);
      
      // Exibir resultado
      console.log(`✅ Status: ${result.status}`);
      console.log(`📝 Mensagem: ${result.message}`);
      if (result.notificationId) {
        console.log(`🆔 ID: ${result.notificationId}`);
      }
      if (result.deliveryTime) {
        console.log(`⏰ Entregue em: ${result.deliveryTime.toLocaleString()}`);
      }
      if (result.error) {
        console.log(`❌ Erro: ${result.error}`);
      }
      
    } catch (error) {
      console.log(`❌ Erro: ${error instanceof Error ? error.message : 'Erro desconhecido'}`);
    }
    
    console.log();
  }
}

// Demonstração de flexibilidade
function demonstrateFlexibility(): void {
  console.log('=== Demonstração de Flexibilidade ===\n');

  const manager = new NotificationManager();

  console.log('Tipos de notificação disponíveis:');
  for (const type of NotificationStrategyFactory.getAvailableTypes()) {
    const strategy = NotificationStrategyFactory.createStrategy(type);
    const info = {
      type: strategy.getType(),
      priority: strategy.getPriority()
    };
    
    console.log(`- ${type.toUpperCase()}: Prioridade ${info.priority}`);
  }
}

// Executar demonstrações
if (require.main === module) {
  demonstrateNotificationStrategy()
    .then(() => {
      console.log('\n' + '='.repeat(50) + '\n');
      demonstrateFlexibility();
    })
    .catch(console.error);
}

export {
  NotificationType,
  NotificationStatus,
  NotificationData,
  NotificationResult,
  NotificationStrategy,
  EmailNotificationStrategy,
  SMSNotificationStrategy,
  PushNotificationStrategy,
  WhatsAppNotificationStrategy,
  NotificationManager,
  NotificationStrategyFactory
};








