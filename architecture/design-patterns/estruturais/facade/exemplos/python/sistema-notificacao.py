"""
Exemplo do Padrão Facade - Sistema de Notificação

Este exemplo demonstra como implementar o padrão Facade para simplificar
o envio de notificações em um sistema, ocultando a complexidade de múltiplos
subsistemas de comunicação.
"""

import time
import random
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from enum import Enum


class NotificationStatus(Enum):
    """Status possíveis de uma notificação"""
    PENDING = "pending"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"


class NotificationType(Enum):
    """Tipos de notificação disponíveis"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WHATSAPP = "whatsapp"


# Subsistema 1: Gerenciador de Templates
class TemplateManager:
    """Gerencia templates de notificação"""
    
    def __init__(self):
        self.templates = {
            'welcome': {
                'subject': 'Bem-vindo ao nosso sistema!',
                'body': 'Olá {name}, seja bem-vindo!'
            },
            'order_confirmation': {
                'subject': 'Pedido confirmado',
                'body': 'Seu pedido #{order_id} foi confirmado com sucesso!'
            },
            'password_reset': {
                'subject': 'Redefinição de senha',
                'body': 'Clique no link para redefinir sua senha: {reset_link}'
            }
        }
    
    def get_template(self, template_name: str) -> Dict[str, str]:
        """Retorna template por nome"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' não encontrado")
        
        return self.templates[template_name]
    
    def render_template(self, template_name: str, variables: Dict[str, str]) -> Dict[str, str]:
        """Renderiza template com variáveis"""
        template = self.get_template(template_name)
        
        rendered = {}
        for key, value in template.items():
            rendered[key] = value.format(**variables)
        
        return rendered


# Subsistema 2: Validador de Dados
class DataValidator:
    """Valida dados de notificação"""
    
    def validate_email(self, email: str) -> bool:
        """Valida formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_phone(self, phone: str) -> bool:
        """Valida formato de telefone"""
        import re
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))
    
    def validate_notification_data(self, data: Dict[str, Any]) -> bool:
        """Valida dados completos da notificação"""
        required_fields = ['recipient', 'type', 'template']
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Validação específica por tipo
        if data['type'] == NotificationType.EMAIL:
            return self.validate_email(data['recipient'])
        elif data['type'] == NotificationType.SMS:
            return self.validate_phone(data['recipient'])
        
        return True


# Subsistema 3: Gerenciador de Preferências
class PreferenceManager:
    """Gerencia preferências de notificação do usuário"""
    
    def __init__(self):
        self.user_preferences = {}
    
    def get_user_preferences(self, user_id: str) -> Dict[str, bool]:
        """Retorna preferências do usuário"""
        return self.user_preferences.get(user_id, {
            'email_enabled': True,
            'sms_enabled': True,
            'push_enabled': True,
            'whatsapp_enabled': False
        })
    
    def update_preferences(self, user_id: str, preferences: Dict[str, bool]) -> None:
        """Atualiza preferências do usuário"""
        self.user_preferences[user_id] = preferences
    
    def is_notification_allowed(self, user_id: str, notification_type: NotificationType) -> bool:
        """Verifica se notificação é permitida para o usuário"""
        prefs = self.get_user_preferences(user_id)
        
        type_mapping = {
            NotificationType.EMAIL: 'email_enabled',
            NotificationType.SMS: 'sms_enabled',
            NotificationType.PUSH: 'push_enabled',
            NotificationType.WHATSAPP: 'whatsapp_enabled'
        }
        
        return prefs.get(type_mapping[notification_type], False)


# Subsistema 4: Sistema de Logs
class NotificationLogger:
    """Sistema de logs para notificações"""
    
    def __init__(self):
        self.logs = []
    
    def log_notification(self, notification_id: str, status: NotificationStatus, details: str = "") -> None:
        """Registra log de notificação"""
        log_entry = {
            'id': notification_id,
            'status': status.value,
            'timestamp': time.time(),
            'details': details
        }
        self.logs.append(log_entry)
        print(f"📝 Log: {notification_id} - {status.value} - {details}")
    
    def get_notification_logs(self, notification_id: str) -> List[Dict[str, Any]]:
        """Retorna logs de uma notificação específica"""
        return [log for log in self.logs if log['id'] == notification_id]


# Subsistema 5: Provedores de Notificação
class NotificationProvider(ABC):
    """Interface para provedores de notificação"""
    
    @abstractmethod
    def send(self, recipient: str, subject: str, body: str) -> bool:
        pass


class EmailProvider(NotificationProvider):
    """Provedor de email"""
    
    def send(self, recipient: str, subject: str, body: str) -> bool:
        print(f"📧 Enviando email para: {recipient}")
        print(f"📝 Assunto: {subject}")
        print(f"📄 Conteúdo: {body}")
        
        # Simular envio
        time.sleep(1)
        
        # Simular falha ocasional (3% de chance)
        if random.random() < 0.03:
            return False
        
        print("✅ Email enviado com sucesso!")
        return True


class SMSProvider(NotificationProvider):
    """Provedor de SMS"""
    
    def send(self, recipient: str, subject: str, body: str) -> bool:
        print(f"📱 Enviando SMS para: {recipient}")
        print(f"📄 Mensagem: {body}")
        
        # Simular envio
        time.sleep(0.5)
        
        # Simular falha ocasional (2% de chance)
        if random.random() < 0.02:
            return False
        
        print("✅ SMS enviado com sucesso!")
        return True


class PushProvider(NotificationProvider):
    """Provedor de notificação push"""
    
    def send(self, recipient: str, subject: str, body: str) -> bool:
        print(f"🔔 Enviando push para: {recipient}")
        print(f"📝 Título: {subject}")
        print(f"📄 Conteúdo: {body}")
        
        # Simular envio
        time.sleep(0.3)
        
        # Simular falha ocasional (1% de chance)
        if random.random() < 0.01:
            return False
        
        print("✅ Push enviado com sucesso!")
        return True


class WhatsAppProvider(NotificationProvider):
    """Provedor de WhatsApp"""
    
    def send(self, recipient: str, subject: str, body: str) -> bool:
        print(f"💬 Enviando WhatsApp para: {recipient}")
        print(f"📄 Mensagem: {body}")
        
        # Simular envio
        time.sleep(1.5)
        
        # Simular falha ocasional (4% de chance)
        if random.random() < 0.04:
            return False
        
        print("✅ WhatsApp enviado com sucesso!")
        return True


# Facade: Interface simplificada para o subsistema complexo
class NotificationFacade:
    """Facade para simplificar o envio de notificações"""
    
    def __init__(self):
        self.template_manager = TemplateManager()
        self.validator = DataValidator()
        self.preference_manager = PreferenceManager()
        self.logger = NotificationLogger()
        
        # Provedores de notificação
        self.providers = {
            NotificationType.EMAIL: EmailProvider(),
            NotificationType.SMS: SMSProvider(),
            NotificationType.PUSH: PushProvider(),
            NotificationType.WHATSAPP: WhatsAppProvider()
        }
    
    def send_notification(self, user_id: str, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Método principal para enviar notificação"""
        notification_id = f"notif_{int(time.time())}"
        
        try:
            print(f"🔔 Iniciando envio de notificação {notification_id}")
            
            # 1. Validar dados
            if not self.validator.validate_notification_data(notification_data):
                raise ValueError("Dados de notificação inválidos")
            
            # 2. Verificar preferências do usuário
            notification_type = notification_data['type']
            if not self.preference_manager.is_notification_allowed(user_id, notification_type):
                raise ValueError(f"Notificação {notification_type.value} não permitida para o usuário")
            
            # 3. Renderizar template
            template_name = notification_data['template']
            variables = notification_data.get('variables', {})
            rendered_template = self.template_manager.render_template(template_name, variables)
            
            # 4. Enviar notificação
            provider = self.providers[notification_type]
            success = provider.send(
                notification_data['recipient'],
                rendered_template['subject'],
                rendered_template['body']
            )
            
            if success:
                self.logger.log_notification(notification_id, NotificationStatus.SENT, "Enviado com sucesso")
                return {
                    'success': True,
                    'notification_id': notification_id,
                    'status': 'sent'
                }
            else:
                self.logger.log_notification(notification_id, NotificationStatus.FAILED, "Falha no envio")
                return {
                    'success': False,
                    'notification_id': notification_id,
                    'status': 'failed',
                    'error': 'Falha no envio da notificação'
                }
                
        except Exception as e:
            self.logger.log_notification(notification_id, NotificationStatus.FAILED, str(e))
            return {
                'success': False,
                'notification_id': notification_id,
                'status': 'failed',
                'error': str(e)
            }
    
    def send_welcome_notification(self, user_id: str, user_email: str, user_name: str) -> Dict[str, Any]:
        """Método específico para notificação de boas-vindas"""
        notification_data = {
            'recipient': user_email,
            'type': NotificationType.EMAIL,
            'template': 'welcome',
            'variables': {'name': user_name}
        }
        
        return self.send_notification(user_id, notification_data)
    
    def send_order_confirmation(self, user_id: str, user_email: str, order_id: str) -> Dict[str, Any]:
        """Método específico para confirmação de pedido"""
        notification_data = {
            'recipient': user_email,
            'type': NotificationType.EMAIL,
            'template': 'order_confirmation',
            'variables': {'order_id': order_id}
        }
        
        return self.send_notification(user_id, notification_data)
    
    def send_password_reset(self, user_id: str, user_email: str, reset_link: str) -> Dict[str, Any]:
        """Método específico para redefinição de senha"""
        notification_data = {
            'recipient': user_email,
            'type': NotificationType.EMAIL,
            'template': 'password_reset',
            'variables': {'reset_link': reset_link}
        }
        
        return self.send_notification(user_id, notification_data)
    
    def get_notification_logs(self, notification_id: str) -> List[Dict[str, Any]]:
        """Retorna logs de uma notificação"""
        return self.logger.get_notification_logs(notification_id)


# Controller que usa a Facade
class NotificationController:
    """Controller que usa a Facade para envio de notificações"""
    
    def __init__(self, notification_facade: NotificationFacade):
        self.notification_facade = notification_facade
    
    def send_welcome_email(self, user_id: str, user_email: str, user_name: str) -> Dict[str, Any]:
        """Endpoint para envio de email de boas-vindas"""
        return self.notification_facade.send_welcome_notification(user_id, user_email, user_name)
    
    def send_order_confirmation(self, user_id: str, user_email: str, order_id: str) -> Dict[str, Any]:
        """Endpoint para confirmação de pedido"""
        return self.notification_facade.send_order_confirmation(user_id, user_email, order_id)
    
    def send_password_reset(self, user_id: str, user_email: str, reset_link: str) -> Dict[str, Any]:
        """Endpoint para redefinição de senha"""
        return self.notification_facade.send_password_reset(user_id, user_email, reset_link)


# Exemplo de uso
def demonstrate_notification_facade():
    """Demonstra o uso do padrão Facade para notificações"""
    print("=== Demonstração do Padrão Facade - Sistema de Notificação ===\n")
    
    # Criar facade
    notification_facade = NotificationFacade()
    
    # Criar controller
    controller = NotificationController(notification_facade)
    
    # Configurar preferências do usuário
    notification_facade.preference_manager.update_preferences('user123', {
        'email_enabled': True,
        'sms_enabled': True,
        'push_enabled': True,
        'whatsapp_enabled': False
    })
    
    print("--- Enviando Email de Boas-vindas ---")
    result1 = controller.send_welcome_email('user123', 'usuario@email.com', 'João Silva')
    print(f"Resultado: {'✅ Sucesso' if result1['success'] else '❌ Falha'}")
    if not result1['success']:
        print(f"Erro: {result1['error']}")
    
    print("\n--- Enviando Confirmação de Pedido ---")
    result2 = controller.send_order_confirmation('user123', 'usuario@email.com', 'PED-001')
    print(f"Resultado: {'✅ Sucesso' if result2['success'] else '❌ Falha'}")
    if not result2['success']:
        print(f"Erro: {result2['error']}")
    
    print("\n--- Enviando Redefinição de Senha ---")
    result3 = controller.send_password_reset('user123', 'usuario@email.com', 'https://app.com/reset?token=abc123')
    print(f"Resultado: {'✅ Sucesso' if result3['success'] else '❌ Falha'}")
    if not result3['success']:
        print(f"Erro: {result3['error']}")
    
    print("\n" + "="*50 + "\n")


def demonstrate_reusability():
    """Demonstra reutilização da Facade"""
    print("=== Demonstração de Reutilização ===\n")
    
    notification_facade = NotificationFacade()
    
    # Configurar preferências para diferentes usuários
    notification_facade.preference_manager.update_preferences('user1', {
        'email_enabled': True,
        'sms_enabled': False,
        'push_enabled': True,
        'whatsapp_enabled': False
    })
    
    notification_facade.preference_manager.update_preferences('user2', {
        'email_enabled': True,
        'sms_enabled': True,
        'push_enabled': False,
        'whatsapp_enabled': True
    })
    
    # Enviar notificações para diferentes usuários
    users = [
        {'id': 'user1', 'email': 'user1@email.com', 'name': 'Maria'},
        {'id': 'user2', 'email': 'user2@email.com', 'name': 'Pedro'}
    ]
    
    for user in users:
        print(f"--- Enviando para {user['name']} ---")
        result = notification_facade.send_welcome_notification(user['id'], user['email'], user['name'])
        print(f"Resultado: {'✅ Sucesso' if result['success'] else '❌ Falha'}")
        if not result['success']:
            print(f"Erro: {result['error']}")
        print()


def demonstrate_logging():
    """Demonstra sistema de logs"""
    print("=== Demonstração de Logs ===\n")
    
    notification_facade = NotificationFacade()
    
    # Enviar algumas notificações
    result1 = notification_facade.send_welcome_notification('user123', 'test@email.com', 'Test User')
    result2 = notification_facade.send_order_confirmation('user123', 'test@email.com', 'PED-002')
    
    # Verificar logs
    if result1['success']:
        logs1 = notification_facade.get_notification_logs(result1['notification_id'])
        print(f"Logs da notificação {result1['notification_id']}:")
        for log in logs1:
            print(f"  - {log['status']}: {log['details']}")
    
    if result2['success']:
        logs2 = notification_facade.get_notification_logs(result2['notification_id'])
        print(f"\nLogs da notificação {result2['notification_id']}:")
        for log in logs2:
            print(f"  - {log['status']}: {log['details']}")


if __name__ == "__main__":
    demonstrate_notification_facade()
    demonstrate_reusability()
    demonstrate_logging()








