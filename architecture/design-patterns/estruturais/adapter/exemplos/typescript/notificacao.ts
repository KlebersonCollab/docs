/**
 * Exemplo prático do Padrão Adapter em TypeScript
 * Sistema de notificações com diferentes provedores
 * 
 * Este exemplo demonstra como implementar o padrão Adapter
 * para integrar diferentes serviços de notificação
 */

// Interface que define o contrato para provedores de notificação
interface NotificationAdapter {
    sendEmail(to: string, subject: string, body: string): Promise<NotificationResult>;
    sendSMS(to: string, message: string): Promise<NotificationResult>;
    sendPushNotification(userId: string, title: string, body: string): Promise<NotificationResult>;
}

// Interface para resultados de notificação
interface NotificationResult {
    success: boolean;
    messageId: string;
    provider: string;
    timestamp: Date;
    error?: string;
}

/**
 * Adapter para SendGrid
 */
class SendGridAdapter implements NotificationAdapter {
    private apiKey: string;
    
    constructor(apiKey: string) {
        this.apiKey = apiKey;
        console.log(`🔑 SendGrid inicializado com API key: ${apiKey.substring(0, 8)}...`);
    }
    
    async sendEmail(to: string, subject: string, body: string): Promise<NotificationResult> {
        console.log(`📧 Enviando email via SendGrid para: ${to}`);
        
        try {
            // Simulação da API do SendGrid
            const messageId = `sg_${Date.now()}`;
            
            // Validação específica do SendGrid
            if (!this.validateSendGridEmail(to)) {
                throw new Error('Email inválido para SendGrid');
            }
            
            // Processamento específico do SendGrid
            await this.simulateApiCall();
            
            const result: NotificationResult = {
                success: true,
                messageId,
                provider: 'sendgrid',
                timestamp: new Date()
            };
            
            console.log(`✅ Email enviado via SendGrid: ${messageId}`);
            return result;
            
        } catch (error) {
            return {
                success: false,
                messageId: '',
                provider: 'sendgrid',
                timestamp: new Date(),
                error: error instanceof Error ? error.message : 'Erro desconhecido'
            };
        }
    }
    
    async sendSMS(to: string, message: string): Promise<NotificationResult> {
        console.log(`📱 Enviando SMS via SendGrid para: ${to}`);
        
        try {
            const messageId = `sg_sms_${Date.now()}`;
            
            if (!this.validateSendGridSMS(to)) {
                throw new Error('Número inválido para SendGrid SMS');
            }
            
            await this.simulateApiCall();
            
            const result: NotificationResult = {
                success: true,
                messageId,
                provider: 'sendgrid',
                timestamp: new Date()
            };
            
            console.log(`✅ SMS enviado via SendGrid: ${messageId}`);
            return result;
            
        } catch (error) {
            return {
                success: false,
                messageId: '',
                provider: 'sendgrid',
                timestamp: new Date(),
                error: error instanceof Error ? error.message : 'Erro desconhecido'
            };
        }
    }
    
    async sendPushNotification(userId: string, title: string, body: string): Promise<NotificationResult> {
        console.log(`🔔 Enviando push via SendGrid para usuário: ${userId}`);
        
        try {
            const messageId = `sg_push_${Date.now()}`;
            
            await this.simulateApiCall();
            
            const result: NotificationResult = {
                success: true,
                messageId,
                provider: 'sendgrid',
                timestamp: new Date()
            };
            
            console.log(`✅ Push enviado via SendGrid: ${messageId}`);
            return result;
            
        } catch (error) {
            return {
                success: false,
                messageId: '',
                provider: 'sendgrid',
                timestamp: new Date(),
                error: error instanceof Error ? error.message : 'Erro desconhecido'
            };
        }
    }
    
    private validateSendGridEmail(email: string): boolean {
        return email.includes('@') && email.includes('.');
    }
    
    private validateSendGridSMS(phone: string): boolean {
        return phone.length >= 10;
    }
    
    private async simulateApiCall(): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, 100));
    }
}

/**
 * Adapter para AWS SES
 */
class AWSSESAdapter implements NotificationAdapter {
    private accessKey: string;
    private secretKey: string;
    private region: string;
    
    constructor(accessKey: string, secretKey: string, region: string) {
        this.accessKey = accessKey;
        this.secretKey = secretKey;
        this.region = region;
        console.log(`🔑 AWS SES inicializado na região: ${region}`);
    }
    
    async sendEmail(to: string, subject: string, body: string): Promise<NotificationResult> {
        console.log(`📧 Enviando email via AWS SES para: ${to}`);
        
        try {
            const messageId = `aws_${Date.now()}`;
            
            if (!this.validateAWSEmail(to)) {
                throw new Error('Email inválido para AWS SES');
            }
            
            await this.simulateApiCall();
            
            const result: NotificationResult = {
                success: true,
                messageId,
                provider: 'aws-ses',
                timestamp: new Date()
            };
            
            console.log(`✅ Email enviado via AWS SES: ${messageId}`);
            return result;
            
        } catch (error) {
            return {
                success: false,
                messageId: '',
                provider: 'aws-ses',
                timestamp: new Date(),
                error: error instanceof Error ? error.message : 'Erro desconhecido'
            };
        }
    }
    
    async sendSMS(to: string, message: string): Promise<NotificationResult> {
        console.log(`📱 Enviando SMS via AWS SES para: ${to}`);
        
        try {
            const messageId = `aws_sms_${Date.now()}`;
            
            if (!this.validateAWSSMS(to)) {
                throw new Error('Número inválido para AWS SES SMS');
            }
            
            await this.simulateApiCall();
            
            const result: NotificationResult = {
                success: true,
                messageId,
                provider: 'aws-ses',
                timestamp: new Date()
            };
            
            console.log(`✅ SMS enviado via AWS SES: ${messageId}`);
            return result;
            
        } catch (error) {
            return {
                success: false,
                messageId: '',
                provider: 'aws-ses',
                timestamp: new Date(),
                error: error instanceof Error ? error.message : 'Erro desconhecido'
            };
        }
    }
    
    async sendPushNotification(userId: string, title: string, body: string): Promise<NotificationResult> {
        console.log(`🔔 Enviando push via AWS SES para usuário: ${userId}`);
        
        try {
            const messageId = `aws_push_${Date.now()}`;
            
            await this.simulateApiCall();
            
            const result: NotificationResult = {
                success: true,
                messageId,
                provider: 'aws-ses',
                timestamp: new Date()
            };
            
            console.log(`✅ Push enviado via AWS SES: ${messageId}`);
            return result;
            
        } catch (error) {
            return {
                success: false,
                messageId: '',
                provider: 'aws-ses',
                timestamp: new Date(),
                error: error instanceof Error ? error.message : 'Erro desconhecido'
            };
        }
    }
    
    private validateAWSEmail(email: string): boolean {
        return email.includes('@') && email.includes('.') && email.length > 5;
    }
    
    private validateAWSSMS(phone: string): boolean {
        return phone.length >= 11;
    }
    
    private async simulateApiCall(): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, 150));
    }
}

/**
 * Adapter para Twilio
 */
class TwilioAdapter implements NotificationAdapter {
    private accountSid: string;
    private authToken: string;
    
    constructor(accountSid: string, authToken: string) {
        this.accountSid = accountSid;
        this.authToken = authToken;
        console.log(`🔑 Twilio inicializado com Account SID: ${accountSid.substring(0, 8)}...`);
    }
    
    async sendEmail(to: string, subject: string, body: string): Promise<NotificationResult> {
        console.log(`📧 Enviando email via Twilio para: ${to}`);
        
        try {
            const messageId = `tw_${Date.now()}`;
            
            if (!this.validateTwilioEmail(to)) {
                throw new Error('Email inválido para Twilio');
            }
            
            await this.simulateApiCall();
            
            const result: NotificationResult = {
                success: true,
                messageId,
                provider: 'twilio',
                timestamp: new Date()
            };
            
            console.log(`✅ Email enviado via Twilio: ${messageId}`);
            return result;
            
        } catch (error) {
            return {
                success: false,
                messageId: '',
                provider: 'twilio',
                timestamp: new Date(),
                error: error instanceof Error ? error.message : 'Erro desconhecido'
            };
        }
    }
    
    async sendSMS(to: string, message: string): Promise<NotificationResult> {
        console.log(`📱 Enviando SMS via Twilio para: ${to}`);
        
        try {
            const messageId = `tw_sms_${Date.now()}`;
            
            if (!this.validateTwilioSMS(to)) {
                throw new Error('Número inválido para Twilio SMS');
            }
            
            await this.simulateApiCall();
            
            const result: NotificationResult = {
                success: true,
                messageId,
                provider: 'twilio',
                timestamp: new Date()
            };
            
            console.log(`✅ SMS enviado via Twilio: ${messageId}`);
            return result;
            
        } catch (error) {
            return {
                success: false,
                messageId: '',
                provider: 'twilio',
                timestamp: new Date(),
                error: error instanceof Error ? error.message : 'Erro desconhecido'
            };
        }
    }
    
    async sendPushNotification(userId: string, title: string, body: string): Promise<NotificationResult> {
        console.log(`🔔 Enviando push via Twilio para usuário: ${userId}`);
        
        try {
            const messageId = `tw_push_${Date.now()}`;
            
            await this.simulateApiCall();
            
            const result: NotificationResult = {
                success: true,
                messageId,
                provider: 'twilio',
                timestamp: new Date()
            };
            
            console.log(`✅ Push enviado via Twilio: ${messageId}`);
            return result;
            
        } catch (error) {
            return {
                success: false,
                messageId: '',
                provider: 'twilio',
                timestamp: new Date(),
                error: error instanceof Error ? error.message : 'Erro desconhecido'
            };
        }
    }
    
    private validateTwilioEmail(email: string): boolean {
        return email.includes('@') && email.includes('.') && email.length > 3;
    }
    
    private validateTwilioSMS(phone: string): boolean {
        return phone.length >= 10 && phone.startsWith('+');
    }
    
    private async simulateApiCall(): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, 200));
    }
}

/**
 * Cliente do padrão Adapter - Sistema de notificações
 */
class NotificationService {
    private adapter: NotificationAdapter;
    private notifications: NotificationResult[] = [];
    
    constructor(adapter: NotificationAdapter) {
        this.adapter = adapter;
    }
    
    async sendEmail(to: string, subject: string, body: string): Promise<NotificationResult> {
        console.log(`🔄 Enviando notificação por email...`);
        
        const result = await this.adapter.sendEmail(to, subject, body);
        this.notifications.push(result);
        
        if (result.success) {
            console.log(`✅ Email enviado com sucesso!`);
        } else {
            console.log(`❌ Falha ao enviar email: ${result.error}`);
        }
        
        return result;
    }
    
    async sendSMS(to: string, message: string): Promise<NotificationResult> {
        console.log(`🔄 Enviando notificação por SMS...`);
        
        const result = await this.adapter.sendSMS(to, message);
        this.notifications.push(result);
        
        if (result.success) {
            console.log(`✅ SMS enviado com sucesso!`);
        } else {
            console.log(`❌ Falha ao enviar SMS: ${result.error}`);
        }
        
        return result;
    }
    
    async sendPushNotification(userId: string, title: string, body: string): Promise<NotificationResult> {
        console.log(`🔄 Enviando notificação push...`);
        
        const result = await this.adapter.sendPushNotification(userId, title, body);
        this.notifications.push(result);
        
        if (result.success) {
            console.log(`✅ Push enviado com sucesso!`);
        } else {
            console.log(`❌ Falha ao enviar push: ${result.error}`);
        }
        
        return result;
    }
    
    getNotifications(): NotificationResult[] {
        return this.notifications;
    }
    
    getSuccessRate(): number {
        const successful = this.notifications.filter(n => n.success).length;
        return this.notifications.length > 0 ? (successful / this.notifications.length) * 100 : 0;
    }
}

/**
 * Demonstração do uso do padrão Adapter
 */
async function demonstrarSendGrid(): Promise<void> {
    console.log("=== DEMONSTRAÇÃO COM SENDGRID ===");
    
    const sendGridAdapter = new SendGridAdapter("SG.1234567890abcdef");
    const notificationService = new NotificationService(sendGridAdapter);
    
    // Enviar email
    await notificationService.sendEmail(
        "usuario@exemplo.com",
        "Bem-vindo!",
        "Obrigado por se cadastrar em nosso serviço."
    );
    
    // Enviar SMS
    await notificationService.sendSMS(
        "+5511999999999",
        "Seu código de verificação é: 123456"
    );
    
    // Enviar push
    await notificationService.sendPushNotification(
        "user123",
        "Nova mensagem",
        "Você recebeu uma nova mensagem"
    );
    
    console.log(`📊 Taxa de sucesso: ${notificationService.getSuccessRate().toFixed(1)}%\n`);
}

async function demonstrarAWSSES(): Promise<void> {
    console.log("=== DEMONSTRAÇÃO COM AWS SES ===");
    
    const awsSESAdapter = new AWSSESAdapter("AKIA1234567890", "secret123", "us-east-1");
    const notificationService = new NotificationService(awsSESAdapter);
    
    // Enviar email
    await notificationService.sendEmail(
        "cliente@empresa.com",
        "Confirmação de Pedido",
        "Seu pedido foi confirmado e está sendo processado."
    );
    
    // Enviar SMS
    await notificationService.sendSMS(
        "+5511888888888",
        "Seu pedido foi confirmado!"
    );
    
    console.log(`📊 Taxa de sucesso: ${notificationService.getSuccessRate().toFixed(1)}%\n`);
}

async function demonstrarTwilio(): Promise<void> {
    console.log("=== DEMONSTRAÇÃO COM TWILIO ===");
    
    const twilioAdapter = new TwilioAdapter("AC1234567890", "auth_token_123");
    const notificationService = new NotificationService(twilioAdapter);
    
    // Enviar email
    await notificationService.sendEmail(
        "admin@sistema.com",
        "Relatório Diário",
        "Relatório de vendas do dia está disponível."
    );
    
    // Enviar SMS
    await notificationService.sendSMS(
        "+5511777777777",
        "Relatório diário enviado por email"
    );
    
    console.log(`📊 Taxa de sucesso: ${notificationService.getSuccessRate().toFixed(1)}%\n`);
}

async function demonstrarFlexibilidade(): Promise<void> {
    console.log("=== DEMONSTRAÇÃO DE FLEXIBILIDADE ===");
    
    // Configuração dinâmica de provedores
    const providers = {
        'sendgrid': new SendGridAdapter("SG.1234567890abcdef"),
        'aws-ses': new AWSSESAdapter("AKIA1234567890", "secret123", "us-east-1"),
        'twilio': new TwilioAdapter("AC1234567890", "auth_token_123")
    };
    
    // Selecionar provedor dinamicamente
    const selectedProvider = providers['sendgrid']; // Pode vir de configuração
    const notificationService = new NotificationService(selectedProvider);
    
    // Enviar notificação
    await notificationService.sendEmail(
        "teste@exemplo.com",
        "Teste de Flexibilidade",
        "Esta notificação foi enviada usando o provedor configurado dinamicamente."
    );
    
    console.log(`✅ Provedor configurado dinamicamente: ${selectedProvider.constructor.name}`);
    console.log(`✅ Fácil troca de provedor sem modificar código!\n`);
}

async function demonstrarComparacaoProvedores(): Promise<void> {
    console.log("=== COMPARAÇÃO DE PROVEDORES ===");
    
    const providers = [
        { name: 'SendGrid', adapter: new SendGridAdapter("SG.1234567890abcdef") },
        { name: 'AWS SES', adapter: new AWSSESAdapter("AKIA1234567890", "secret123", "us-east-1") },
        { name: 'Twilio', adapter: new TwilioAdapter("AC1234567890", "auth_token_123") }
    ];
    
    console.log("🔄 Testando envio de email com diferentes provedores:\n");
    
    for (const provider of providers) {
        const notificationService = new NotificationService(provider.adapter);
        
        try {
            const result = await notificationService.sendEmail(
                "teste@exemplo.com",
                `Teste com ${provider.name}`,
                `Este é um teste usando ${provider.name}`
            );
            
            console.log(`🔹 ${provider.name}:`);
            console.log(`   Status: ${result.success ? 'Sucesso' : 'Falha'}`);
            console.log(`   ID: ${result.messageId}`);
            console.log(`   Provedor: ${result.provider}\n`);
            
        } catch (error) {
            console.log(`❌ Erro com ${provider.name}: ${error}\n`);
        }
    }
}

async function main(): Promise<void> {
    console.log("🎯 DEMONSTRAÇÃO DO PADRÃO ADAPTER EM TYPESCRIPT");
    console.log("Sistema de Notificações com Múltiplos Provedores\n");
    
    // Demonstrações
    await demonstrarSendGrid();
    await demonstrarAWSSES();
    await demonstrarTwilio();
    await demonstrarFlexibilidade();
    await demonstrarComparacaoProvedores();
    
    console.log("=== DEMONSTRAÇÃO CONCLUÍDA ===");
    console.log("✅ O padrão Adapter permite integrar diferentes provedores!");
    console.log("✅ Cada provedor mantém sua interface específica!");
    console.log("✅ O código cliente permanece inalterado!");
    console.log("✅ Fácil troca de provedores via configuração!");
}

// Executar demonstração
main().catch(console.error);








