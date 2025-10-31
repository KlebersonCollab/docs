"""
Exemplo do Padrão Observer - Sistema de Notificação

Este exemplo demonstra como implementar o padrão Observer para um sistema
de notificações que monitora eventos e notifica automaticamente múltiplos
observadores com diferentes regras de negócio.
"""

import time
import random
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class EventType(Enum):
    """Tipos de eventos no sistema"""
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    ORDER_CREATED = "order_created"
    ORDER_CANCELLED = "order_cancelled"
    PAYMENT_PROCESSED = "payment_processed"
    PRODUCT_UPDATED = "product_updated"
    SYSTEM_ERROR = "system_error"


@dataclass
class Event:
    """Representa um evento no sistema"""
    event_type: EventType
    data: Dict[str, Any]
    timestamp: datetime
    user_id: Optional[str] = None
    
    def __str__(self) -> str:
        return f"{self.event_type.value} at {self.timestamp.strftime('%H:%M:%S')}"


# Interface para observadores
class EventObserver(ABC):
    """Interface para observadores de eventos"""
    
    @abstractmethod
    def update(self, event: Event) -> None:
        """Atualiza o observador com um novo evento"""
        pass


# Classe observável - Event Manager
class EventManager:
    """Gerenciador de eventos que notifica observadores"""
    
    def __init__(self):
        self._observers: List[EventObserver] = []
        self._event_history: List[Event] = []
    
    def add_observer(self, observer: EventObserver) -> None:
        """Adiciona um observador"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"👁️ Observador adicionado: {observer.__class__.__name__}")
    
    def remove_observer(self, observer: EventObserver) -> None:
        """Remove um observador"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"❌ Observador removido: {observer.__class__.__name__}")
    
    def notify_observers(self, event: Event) -> None:
        """Notifica todos os observadores sobre um evento"""
        print(f"🔔 Notificando {len(self._observers)} observadores sobre: {event}")
        
        for observer in self._observers:
            try:
                observer.update(event)
            except Exception as e:
                print(f"❌ Erro ao notificar {observer.__class__.__name__}: {e}")
    
    def publish_event(self, event_type: EventType, data: Dict[str, Any], user_id: Optional[str] = None) -> None:
        """Publica um evento e notifica observadores"""
        event = Event(
            event_type=event_type,
            data=data,
            timestamp=datetime.now(),
            user_id=user_id
        )
        
        self._event_history.append(event)
        self.notify_observers(event)
    
    def get_event_history(self) -> List[Event]:
        """Retorna o histórico de eventos"""
        return self._event_history.copy()


# Observador 1: Logger de Eventos
class EventLogger(EventObserver):
    """Observador que registra todos os eventos em log"""
    
    def __init__(self):
        self.logs: List[str] = []
    
    def update(self, event: Event) -> None:
        """Registra o evento no log"""
        log_entry = f"[{event.timestamp.strftime('%H:%M:%S')}] {event.event_type.value}: {event.data}"
        self.logs.append(log_entry)
        print(f"📝 [LOGGER] {log_entry}")
    
    def get_logs(self) -> List[str]:
        """Retorna todos os logs"""
        return self.logs.copy()
    
    def get_logs_by_type(self, event_type: EventType) -> List[str]:
        """Retorna logs de um tipo específico"""
        return [log for log in self.logs if event_type.value in log]


# Observador 2: Notificador de Usuários
class UserNotifier(EventObserver):
    """Observador que notifica usuários sobre eventos importantes"""
    
    def __init__(self):
        self.notifications_sent = 0
        self.user_preferences = {
            "user_1": [EventType.ORDER_CREATED, EventType.PAYMENT_PROCESSED],
            "user_2": [EventType.PRODUCT_UPDATED, EventType.SYSTEM_ERROR],
            "user_3": [EventType.USER_LOGIN, EventType.USER_LOGOUT]
        }
    
    def update(self, event: Event) -> None:
        """Notifica usuários baseado em suas preferências"""
        if not event.user_id:
            return
        
        user_prefs = self.user_preferences.get(event.user_id, [])
        
        if event.event_type in user_prefs:
            self._send_notification(event)
            self.notifications_sent += 1
    
    def _send_notification(self, event: Event) -> None:
        """Envia notificação para o usuário"""
        print(f"📱 [NOTIFIER] Notificação enviada para {event.user_id}: {event.event_type.value}")
        
        # Simular diferentes tipos de notificação
        if event.event_type == EventType.ORDER_CREATED:
            self._send_order_notification(event)
        elif event.event_type == EventType.PAYMENT_PROCESSED:
            self._send_payment_notification(event)
        elif event.event_type == EventType.SYSTEM_ERROR:
            self._send_error_notification(event)
    
    def _send_order_notification(self, event: Event) -> None:
        """Envia notificação sobre pedido"""
        order_id = event.data.get('order_id', 'N/A')
        print(f"    📦 Pedido #{order_id} criado com sucesso!")
    
    def _send_payment_notification(self, event: Event) -> None:
        """Envia notificação sobre pagamento"""
        amount = event.data.get('amount', 0)
        print(f"    💳 Pagamento de R$ {amount:.2f} processado!")
    
    def _send_error_notification(self, event: Event) -> None:
        """Envia notificação sobre erro"""
        error_message = event.data.get('error', 'Erro desconhecido')
        print(f"    ⚠️ Erro no sistema: {error_message}")


# Observador 3: Analisador de Métricas
class MetricsAnalyzer(EventObserver):
    """Observador que analisa métricas dos eventos"""
    
    def __init__(self):
        self.event_counts: Dict[EventType, int] = {}
        self.user_activity: Dict[str, int] = {}
        self.hourly_activity: Dict[int, int] = {}
    
    def update(self, event: Event) -> None:
        """Atualiza métricas baseado no evento"""
        # Contar eventos por tipo
        self.event_counts[event.event_type] = self.event_counts.get(event.event_type, 0) + 1
        
        # Contar atividade por usuário
        if event.user_id:
            self.user_activity[event.user_id] = self.user_activity.get(event.user_id, 0) + 1
        
        # Contar atividade por hora
        hour = event.timestamp.hour
        self.hourly_activity[hour] = self.hourly_activity.get(hour, 0) + 1
        
        # Mostrar análise em tempo real
        self._show_realtime_analysis(event)
    
    def _show_realtime_analysis(self, event: Event) -> None:
        """Mostra análise em tempo real"""
        print(f"📊 [METRICS] Evento {event.event_type.value} processado")
        print(f"    📈 Total de eventos: {sum(self.event_counts.values())}")
        print(f"    👤 Usuários ativos: {len(self.user_activity)}")
    
    def get_event_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas dos eventos"""
        total_events = sum(self.event_counts.values())
        
        return {
            "total_events": total_events,
            "event_distribution": self.event_counts,
            "most_active_user": max(self.user_activity.items(), key=lambda x: x[1]) if self.user_activity else None,
            "peak_hour": max(self.hourly_activity.items(), key=lambda x: x[1]) if self.hourly_activity else None
        }


# Observador 4: Sistema de Alertas
class AlertSystem(EventObserver):
    """Observador que gera alertas baseado em eventos"""
    
    def __init__(self):
        self.alerts_generated = 0
        self.alert_rules = {
            EventType.SYSTEM_ERROR: self._generate_error_alert,
            EventType.PAYMENT_PROCESSED: self._generate_payment_alert,
            EventType.USER_LOGIN: self._generate_login_alert
        }
    
    def update(self, event: Event) -> None:
        """Verifica se deve gerar alerta para o evento"""
        if event.event_type in self.alert_rules:
            self.alert_rules[event.event_type](event)
    
    def _generate_error_alert(self, event: Event) -> None:
        """Gera alerta para erro do sistema"""
        error_level = event.data.get('level', 'INFO')
        if error_level in ['ERROR', 'CRITICAL']:
            print(f"🚨 [ALERT] Erro crítico detectado: {event.data.get('error', 'N/A')}")
            self.alerts_generated += 1
    
    def _generate_payment_alert(self, event: Event) -> None:
        """Gera alerta para pagamento"""
        amount = event.data.get('amount', 0)
        if amount > 10000:  # Pagamentos acima de R$ 10.000
            print(f"💰 [ALERT] Pagamento alto processado: R$ {amount:.2f}")
            self.alerts_generated += 1
    
    def _generate_login_alert(self, event: Event) -> None:
        """Gera alerta para login suspeito"""
        ip_address = event.data.get('ip_address', 'N/A')
        if ip_address.startswith('192.168.') or ip_address.startswith('10.'):
            print(f"🔒 [ALERT] Login de IP interno: {ip_address}")
            self.alerts_generated += 1


# Observador 5: Cache Invalidation
class CacheInvalidator(EventObserver):
    """Observador que invalida cache baseado em eventos"""
    
    def __init__(self):
        self.cache_invalidations = 0
        self.cache_keys = {
            EventType.USER_LOGIN: ['user_session', 'user_profile'],
            EventType.ORDER_CREATED: ['user_orders', 'order_history'],
            EventType.PRODUCT_UPDATED: ['product_list', 'product_details'],
            EventType.PAYMENT_PROCESSED: ['payment_history', 'user_balance']
        }
    
    def update(self, event: Event) -> None:
        """Invalida cache baseado no tipo de evento"""
        if event.event_type in self.cache_keys:
            keys_to_invalidate = self.cache_keys[event.event_type]
            self._invalidate_cache(keys_to_invalidate, event)
    
    def _invalidate_cache(self, keys: List[str], event: Event) -> None:
        """Invalida chaves específicas do cache"""
        print(f"🗑️ [CACHE] Invalidando cache para evento {event.event_type.value}")
        for key in keys:
            print(f"    ❌ Cache key '{key}' invalidada")
            self.cache_invalidations += 1


# Simulador de eventos
class EventSimulator:
    """Simula eventos do sistema"""
    
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.users = ['user_1', 'user_2', 'user_3', 'user_4', 'user_5']
        self.products = ['product_a', 'product_b', 'product_c']
    
    def simulate_user_activity(self, duration_minutes: int = 5) -> None:
        """Simula atividade de usuários por um período"""
        print(f"🎭 Simulando atividade de usuários por {duration_minutes} minutos...\n")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        while time.time() < end_time:
            # Simular diferentes tipos de eventos
            event_type = random.choice(list(EventType))
            user_id = random.choice(self.users)
            
            if event_type == EventType.USER_LOGIN:
                self._simulate_login(user_id)
            elif event_type == EventType.ORDER_CREATED:
                self._simulate_order_creation(user_id)
            elif event_type == EventType.PAYMENT_PROCESSED:
                self._simulate_payment(user_id)
            elif event_type == EventType.PRODUCT_UPDATED:
                self._simulate_product_update()
            elif event_type == EventType.SYSTEM_ERROR:
                self._simulate_system_error()
            
            # Pausa entre eventos
            time.sleep(random.uniform(0.5, 2.0))
    
    def _simulate_login(self, user_id: str) -> None:
        """Simula login de usuário"""
        self.event_manager.publish_event(
            EventType.USER_LOGIN,
            {
                'ip_address': f"192.168.1.{random.randint(1, 255)}",
                'user_agent': 'Mozilla/5.0...',
                'login_method': 'email'
            },
            user_id
        )
    
    def _simulate_order_creation(self, user_id: str) -> None:
        """Simula criação de pedido"""
        self.event_manager.publish_event(
            EventType.ORDER_CREATED,
            {
                'order_id': f"ORD-{random.randint(1000, 9999)}",
                'total_amount': random.uniform(50, 500),
                'items_count': random.randint(1, 5)
            },
            user_id
        )
    
    def _simulate_payment(self, user_id: str) -> None:
        """Simula processamento de pagamento"""
        self.event_manager.publish_event(
            EventType.PAYMENT_PROCESSED,
            {
                'amount': random.uniform(100, 2000),
                'payment_method': random.choice(['credit_card', 'pix', 'boleto']),
                'transaction_id': f"TXN-{random.randint(10000, 99999)}"
            },
            user_id
        )
    
    def _simulate_product_update(self) -> None:
        """Simula atualização de produto"""
        self.event_manager.publish_event(
            EventType.PRODUCT_UPDATED,
            {
                'product_id': random.choice(self.products),
                'price_change': random.uniform(-0.1, 0.1),
                'stock_change': random.randint(-10, 10)
            }
        )
    
    def _simulate_system_error(self) -> None:
        """Simula erro do sistema"""
        self.event_manager.publish_event(
            EventType.SYSTEM_ERROR,
            {
                'error': random.choice([
                    'Database connection timeout',
                    'Memory allocation failed',
                    'API rate limit exceeded',
                    'File system error'
                ]),
                'level': random.choice(['ERROR', 'WARNING', 'INFO']),
                'component': random.choice(['database', 'api', 'cache', 'storage'])
            }
        )


# Exemplo de uso
def demonstrate_observer_pattern():
    """Demonstra o padrão Observer com sistema de notificações"""
    print("=== Demonstração do Padrão Observer - Sistema de Notificação ===\n")
    
    # Criar gerenciador de eventos
    event_manager = EventManager()
    
    # Criar observadores
    event_logger = EventLogger()
    user_notifier = UserNotifier()
    metrics_analyzer = MetricsAnalyzer()
    alert_system = AlertSystem()
    cache_invalidator = CacheInvalidator()
    
    # Adicionar observadores
    event_manager.add_observer(event_logger)
    event_manager.add_observer(user_notifier)
    event_manager.add_observer(metrics_analyzer)
    event_manager.add_observer(alert_system)
    event_manager.add_observer(cache_invalidator)
    
    print("\n✅ Todos os observadores adicionados!\n")
    
    # Criar simulador
    simulator = EventSimulator(event_manager)
    
    # Simular eventos
    simulator.simulate_user_activity(2)  # 2 minutos de simulação
    
    # Mostrar estatísticas finais
    print("\n=== Estatísticas Finais ===")
    print(f"📝 Logs gerados: {len(event_logger.get_logs())}")
    print(f"📱 Notificações enviadas: {user_notifier.notifications_sent}")
    print(f"🚨 Alertas gerados: {alert_system.alerts_generated}")
    print(f"🗑️ Cache invalidations: {cache_invalidator.cache_invalidations}")
    
    # Mostrar métricas
    stats = metrics_analyzer.get_event_statistics()
    print(f"📊 Total de eventos: {stats['total_events']}")
    print(f"👤 Usuário mais ativo: {stats['most_active_user']}")
    print(f"⏰ Hora de pico: {stats['peak_hour']}")


def demonstrate_observer_removal():
    """Demonstra remoção de observadores"""
    print("\n=== Demonstração de Remoção de Observadores ===\n")
    
    event_manager = EventManager()
    event_logger = EventLogger()
    user_notifier = UserNotifier()
    
    # Adicionar observadores
    event_manager.add_observer(event_logger)
    event_manager.add_observer(user_notifier)
    
    # Publicar evento com todos os observadores
    print("--- Com todos os observadores ---")
    event_manager.publish_event(
        EventType.USER_LOGIN,
        {'ip_address': '192.168.1.100'},
        'user_1'
    )
    
    # Remover um observador
    event_manager.remove_observer(user_notifier)
    
    # Publicar evento sem o observador removido
    print("\n--- Após remover UserNotifier ---")
    event_manager.publish_event(
        EventType.USER_LOGIN,
        {'ip_address': '192.168.1.101'},
        'user_2'
    )


def demonstrate_error_handling():
    """Demonstra tratamento de erros em observadores"""
    print("\n=== Demonstração de Tratamento de Erros ===\n")
    
    # Observador que gera erro
    class ErrorObserver(EventObserver):
        def update(self, event: Event) -> None:
            raise Exception("Erro simulado no observador")
    
    event_manager = EventManager()
    event_logger = EventLogger()
    error_observer = ErrorObserver()
    
    # Adicionar observadores (um normal, um com erro)
    event_manager.add_observer(event_logger)
    event_manager.add_observer(error_observer)
    
    # Publicar evento (deve continuar funcionando mesmo com erro)
    event_manager.publish_event(
        EventType.USER_LOGIN,
        {'ip_address': '192.168.1.102'},
        'user_3'
    )


if __name__ == "__main__":
    demonstrate_observer_pattern()
    demonstrate_observer_removal()
    demonstrate_error_handling()





