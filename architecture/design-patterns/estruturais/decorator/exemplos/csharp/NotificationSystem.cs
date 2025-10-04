using System;
using System.Collections.Generic;
using System.Text;

namespace DesignPatterns.Decorator
{
    /// <summary>
    /// Exemplo prático do padrão Decorator em C#
    /// Sistema de notificações com diferentes canais e funcionalidades
    /// </summary>

    // Interface base para notificações
    public interface INotificationService
    {
        string Send(string message, string recipient);
        string GetServiceName();
    }

    // Implementação concreta - Serviço básico de email
    public class EmailNotificationService : INotificationService
    {
        public string Send(string message, string recipient)
        {
            Console.WriteLine($"📧 Enviando email para: {recipient}");
            Console.WriteLine($"   📝 Assunto: {message.Substring(0, Math.Min(50, message.Length))}...");
            
            // Simulação de envio de email
            System.Threading.Thread.Sleep(100);
            
            return $"Email enviado para {recipient}";
        }

        public string GetServiceName()
        {
            return "Email Service";
        }
    }

    // Decorator abstrato
    public abstract class NotificationDecorator : INotificationService
    {
        protected INotificationService notificationService;

        public NotificationDecorator(INotificationService notificationService)
        {
            this.notificationService = notificationService;
        }

        public virtual string Send(string message, string recipient)
        {
            return notificationService.Send(message, recipient);
        }

        public virtual string GetServiceName()
        {
            return notificationService.GetServiceName();
        }
    }

    // Decorador concreto - SMS
    public class SmsNotificationDecorator : NotificationDecorator
    {
        public SmsNotificationDecorator(INotificationService notificationService) 
            : base(notificationService)
        {
        }

        public override string Send(string message, string recipient)
        {
            Console.WriteLine($"📱 Enviando SMS para: {recipient}");
            
            // Primeiro envia via serviço base
            string emailResult = notificationService.Send(message, recipient);
            
            // Depois envia SMS
            Console.WriteLine($"   📝 SMS: {message.Substring(0, Math.Min(160, message.Length))}...");
            System.Threading.Thread.Sleep(50);
            
            return $"{emailResult} + SMS enviado para {recipient}";
        }

        public override string GetServiceName()
        {
            return $"{notificationService.GetServiceName()} + SMS";
        }
    }

    // Decorador concreto - Push Notification
    public class PushNotificationDecorator : NotificationDecorator
    {
        public PushNotificationDecorator(INotificationService notificationService) 
            : base(notificationService)
        {
        }

        public override string Send(string message, string recipient)
        {
            Console.WriteLine($"🔔 Enviando Push Notification para: {recipient}");
            
            // Primeiro envia via serviço base
            string baseResult = notificationService.Send(message, recipient);
            
            // Depois envia Push Notification
            Console.WriteLine($"   📱 Push: {message.Substring(0, Math.Min(100, message.Length))}...");
            System.Threading.Thread.Sleep(30);
            
            return $"{baseResult} + Push enviado para {recipient}";
        }

        public override string GetServiceName()
        {
            return $"{notificationService.GetServiceName()} + Push";
        }
    }

    // Decorador concreto - Logging
    public class LoggingDecorator : NotificationDecorator
    {
        private List<string> logs;

        public LoggingDecorator(INotificationService notificationService) 
            : base(notificationService)
        {
            logs = new List<string>();
        }

        public override string Send(string message, string recipient)
        {
            Console.WriteLine($"📝 Logging notificação");
            
            // Log de entrada
            string logEntry = $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] Enviando para {recipient}: {message.Substring(0, Math.Min(30, message.Length))}...";
            logs.Add(logEntry);
            Console.WriteLine($"   📥 {logEntry}");
            
            // Envia notificação
            string result = notificationService.Send(message, recipient);
            
            // Log de saída
            string logExit = $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] Resultado: {result}";
            logs.Add(logExit);
            Console.WriteLine($"   📤 {logExit}");
            
            return result;
        }

        public List<string> GetLogs()
        {
            return new List<string>(logs);
        }

        public override string GetServiceName()
        {
            return $"{notificationService.GetServiceName()} + Logging";
        }
    }

    // Decorador concreto - Retry
    public class RetryDecorator : NotificationDecorator
    {
        private int maxRetries;
        private int retryDelay;

        public RetryDecorator(INotificationService notificationService, int maxRetries = 3, int retryDelay = 1000) 
            : base(notificationService)
        {
            this.maxRetries = maxRetries;
            this.retryDelay = retryDelay;
        }

        public override string Send(string message, string recipient)
        {
            Console.WriteLine($"🔄 Tentando enviar notificação (máx. {maxRetries} tentativas)");
            
            for (int attempt = 1; attempt <= maxRetries; attempt++)
            {
                try
                {
                    Console.WriteLine($"   🎯 Tentativa {attempt}/{maxRetries}");
                    string result = notificationService.Send(message, recipient);
                    
                    if (attempt > 1)
                    {
                        Console.WriteLine($"   ✅ Sucesso na tentativa {attempt}");
                    }
                    
                    return result;
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"   ❌ Falha na tentativa {attempt}: {ex.Message}");
                    
                    if (attempt < maxRetries)
                    {
                        Console.WriteLine($"   ⏳ Aguardando {retryDelay}ms antes da próxima tentativa...");
                        System.Threading.Thread.Sleep(retryDelay);
                    }
                    else
                    {
                        Console.WriteLine($"   💥 Todas as tentativas falharam");
                        throw new Exception($"Falha após {maxRetries} tentativas: {ex.Message}");
                    }
                }
            }
            
            return "Falha no envio";
        }

        public override string GetServiceName()
        {
            return $"{notificationService.GetServiceName()} + Retry({maxRetries})";
        }
    }

    // Decorador concreto - Rate Limiting
    public class RateLimitDecorator : NotificationDecorator
    {
        private int maxRequests;
        private TimeSpan timeWindow;
        private Queue<DateTime> requestTimes;

        public RateLimitDecorator(INotificationService notificationService, int maxRequests = 10, int timeWindowSeconds = 60) 
            : base(notificationService)
        {
            this.maxRequests = maxRequests;
            this.timeWindow = TimeSpan.FromSeconds(timeWindowSeconds);
            this.requestTimes = new Queue<DateTime>();
        }

        public override string Send(string message, string recipient)
        {
            Console.WriteLine($"🚦 Verificando rate limit: {maxRequests} requisições por {timeWindow.TotalSeconds}s");
            
            DateTime now = DateTime.Now;
            
            // Remove requisições antigas
            while (requestTimes.Count > 0 && now - requestTimes.Peek() > timeWindow)
            {
                requestTimes.Dequeue();
            }
            
            // Verifica se excedeu o limite
            if (requestTimes.Count >= maxRequests)
            {
                Console.WriteLine($"   ⏰ Rate limit excedido: {requestTimes.Count}/{maxRequests} requisições");
                throw new Exception("Rate limit excedido");
            }
            
            // Adiciona a requisição atual
            requestTimes.Enqueue(now);
            Console.WriteLine($"   ✅ Rate limit OK: {requestTimes.Count}/{maxRequests} requisições");
            
            // Envia notificação
            return notificationService.Send(message, recipient);
        }

        public override string GetServiceName()
        {
            return $"{notificationService.GetServiceName()} + RateLimit({maxRequests}/{timeWindow.TotalSeconds}s)";
        }
    }

    // Decorador concreto - Criptografia
    public class EncryptionDecorator : NotificationDecorator
    {
        private string encryptionKey;

        public EncryptionDecorator(INotificationService notificationService, string encryptionKey = "default_key") 
            : base(notificationService)
        {
            this.encryptionKey = encryptionKey;
        }

        public override string Send(string message, string recipient)
        {
            Console.WriteLine($"🔐 Criptografando mensagem");
            
            // Criptografa a mensagem
            string encryptedMessage = EncryptMessage(message);
            Console.WriteLine($"   🔑 Mensagem criptografada: {encryptedMessage.Substring(0, Math.Min(20, encryptedMessage.Length))}...");
            
            // Envia notificação com mensagem criptografada
            return notificationService.Send(encryptedMessage, recipient);
        }

        private string EncryptMessage(string message)
        {
            // Simulação simples de criptografia (Base64 + chave)
            string combined = message + "|" + encryptionKey;
            byte[] bytes = Encoding.UTF8.GetBytes(combined);
            return Convert.ToBase64String(bytes);
        }

        public override string GetServiceName()
        {
            return $"{notificationService.GetServiceName()} + Encryption";
        }
    }

    // Classe principal para demonstração
    public class NotificationSystemDemo
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("🚀 Demonstração do Padrão Decorator - Sistema de Notificações\n");
            
            string message = "Sua conta foi criada com sucesso! Bem-vindo ao nosso sistema.";
            string recipient = "usuario@exemplo.com";
            
            // Cenário 1: Notificação básica por email
            Console.WriteLine("📧 Cenário 1: Notificação básica por email");
            INotificationService service1 = new EmailNotificationService();
            string result1 = service1.Send(message, recipient);
            Console.WriteLine($"Resultado: {result1}\n");
            
            // Cenário 2: Email + SMS
            Console.WriteLine("📧📱 Cenário 2: Email + SMS");
            INotificationService service2 = new SmsNotificationDecorator(
                new EmailNotificationService()
            );
            string result2 = service2.Send(message, recipient);
            Console.WriteLine($"Resultado: {result2}\n");
            
            // Cenário 3: Email + SMS + Push
            Console.WriteLine("📧📱🔔 Cenário 3: Email + SMS + Push");
            INotificationService service3 = new PushNotificationDecorator(
                new SmsNotificationDecorator(
                    new EmailNotificationService()
                )
            );
            string result3 = service3.Send(message, recipient);
            Console.WriteLine($"Resultado: {result3}\n");
            
            // Cenário 4: Com logging
            Console.WriteLine("📝 Cenário 4: Com logging");
            INotificationService service4 = new LoggingDecorator(
                new EmailNotificationService()
            );
            string result4 = service4.Send(message, recipient);
            Console.WriteLine($"Resultado: {result4}\n");
            
            // Cenário 5: Com retry
            Console.WriteLine("🔄 Cenário 5: Com retry");
            INotificationService service5 = new RetryDecorator(
                new EmailNotificationService(),
                maxRetries: 3,
                retryDelay: 500
            );
            string result5 = service5.Send(message, recipient);
            Console.WriteLine($"Resultado: {result5}\n");
            
            // Cenário 6: Pipeline completo
            Console.WriteLine("🔧 Cenário 6: Pipeline completo");
            INotificationService service6 = new RateLimitDecorator(
                new LoggingDecorator(
                    new RetryDecorator(
                        new EncryptionDecorator(
                            new PushNotificationDecorator(
                                new SmsNotificationDecorator(
                                    new EmailNotificationService()
                                )
                            ),
                            "chave_super_secreta"
                        ),
                        maxRetries: 2,
                        retryDelay: 1000
                    )
                ),
                maxRequests: 5,
                timeWindowSeconds: 30
            );
            
            try
            {
                string result6 = service6.Send(message, recipient);
                Console.WriteLine($"Resultado: {result6}\n");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erro: {ex.Message}\n");
            }
            
            // Cenário 7: Teste de rate limiting
            Console.WriteLine("🚦 Cenário 7: Teste de rate limiting");
            INotificationService service7 = new RateLimitDecorator(
                new EmailNotificationService(),
                maxRequests: 2,
                timeWindowSeconds: 10
            );
            
            for (int i = 1; i <= 4; i++)
            {
                try
                {
                    Console.WriteLine($"Tentativa {i}:");
                    string result7 = service7.Send(message, recipient);
                    Console.WriteLine($"   Resultado: {result7}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"   Erro: {ex.Message}");
                }
                Console.WriteLine();
            }
            
            Console.WriteLine("✅ Demonstração concluída!");
        }
    }
}

