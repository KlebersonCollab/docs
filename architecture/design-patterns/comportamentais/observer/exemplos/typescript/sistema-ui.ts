/**
 * Exemplo do Padrão Observer - Sistema de UI Reativa
 * 
 * Este exemplo demonstra como implementar o padrão Observer para criar
 * um sistema de UI reativa que atualiza automaticamente múltiplos
 * componentes quando o estado da aplicação muda.
 */

// Enums para tipos de eventos e estados
enum EventType {
  USER_LOGIN = 'user_login',
  USER_LOGOUT = 'user_logout',
  CART_UPDATED = 'cart_updated',
  PRODUCT_VIEWED = 'product_viewed',
  SEARCH_PERFORMED = 'search_performed',
  THEME_CHANGED = 'theme_changed',
  LANGUAGE_CHANGED = 'language_changed'
}

enum Theme {
  LIGHT = 'light',
  DARK = 'dark',
  AUTO = 'auto'
}

enum Language {
  PT = 'pt',
  EN = 'en',
  ES = 'es'
}

// Interfaces
interface Event {
  type: EventType;
  data: any;
  timestamp: Date;
  userId?: string;
}

interface Observer {
  update(event: Event): void;
}

interface UserState {
  isLoggedIn: boolean;
  userId?: string;
  username?: string;
  email?: string;
}

interface CartState {
  items: CartItem[];
  total: number;
  itemCount: number;
}

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface AppState {
  user: UserState;
  cart: CartState;
  theme: Theme;
  language: Language;
  isLoading: boolean;
}

// Classe observável - State Manager
class StateManager {
  private observers: Observer[] = [];
  private state: AppState;
  private eventHistory: Event[] = [];

  constructor() {
    this.state = {
      user: { isLoggedIn: false },
      cart: { items: [], total: 0, itemCount: 0 },
      theme: Theme.LIGHT,
      language: Language.PT,
      isLoading: false
    };
  }

  public addObserver(observer: Observer): void {
    if (!this.observers.includes(observer)) {
      this.observers.push(observer);
      console.log(`👁️ Observador adicionado: ${observer.constructor.name}`);
    }
  }

  public removeObserver(observer: Observer): void {
    const index = this.observers.indexOf(observer);
    if (index > -1) {
      this.observers.splice(index, 1);
      console.log(`❌ Observador removido: ${observer.constructor.name}`);
    }
  }

  public getState(): AppState {
    return { ...this.state };
  }

  public setState(newState: Partial<AppState>): void {
    const oldState = { ...this.state };
    this.state = { ...this.state, ...newState };
    
    // Notificar observadores sobre mudanças
    this.notifyObservers({
      type: EventType.USER_LOGIN, // Seria um tipo mais específico
      data: { oldState, newState: this.state },
      timestamp: new Date()
    });
  }

  public login(userId: string, username: string, email: string): void {
    this.state.user = {
      isLoggedIn: true,
      userId,
      username,
      email
    };

    this.publishEvent(EventType.USER_LOGIN, {
      userId,
      username,
      email
    }, userId);
  }

  public logout(): void {
    const userId = this.state.user.userId;
    this.state.user = { isLoggedIn: false };

    this.publishEvent(EventType.USER_LOGOUT, {
      userId
    }, userId);
  }

  public addToCart(item: Omit<CartItem, 'quantity'>): void {
    const existingItem = this.state.cart.items.find(i => i.id === item.id);
    
    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      this.state.cart.items.push({ ...item, quantity: 1 });
    }

    this.updateCartTotals();
    this.publishEvent(EventType.CART_UPDATED, {
      item,
      cartState: this.state.cart
    });
  }

  public removeFromCart(itemId: string): void {
    this.state.cart.items = this.state.cart.items.filter(item => item.id !== itemId);
    this.updateCartTotals();
    
    this.publishEvent(EventType.CART_UPDATED, {
      itemId,
      cartState: this.state.cart
    });
  }

  public changeTheme(theme: Theme): void {
    this.state.theme = theme;
    this.publishEvent(EventType.THEME_CHANGED, { theme });
  }

  public changeLanguage(language: Language): void {
    this.state.language = language;
    this.publishEvent(EventType.LANGUAGE_CHANGED, { language });
  }

  private updateCartTotals(): void {
    this.state.cart.total = this.state.cart.items.reduce(
      (sum, item) => sum + (item.price * item.quantity), 
      0
    );
    this.state.cart.itemCount = this.state.cart.items.reduce(
      (sum, item) => sum + item.quantity, 
      0
    );
  }

  private publishEvent(type: EventType, data: any, userId?: string): void {
    const event: Event = {
      type,
      data,
      timestamp: new Date(),
      userId
    };

    this.eventHistory.push(event);
    this.notifyObservers(event);
  }

  private notifyObservers(event: Event): void {
    console.log(`🔔 Notificando ${this.observers.length} observadores sobre: ${event.type}`);
    
    this.observers.forEach(observer => {
      try {
        observer.update(event);
      } catch (error) {
        console.error(`❌ Erro ao notificar ${observer.constructor.name}:`, error);
      }
    });
  }
}

// Observador 1: Header Component
class HeaderComponent implements Observer {
  private userInfo: HTMLElement | null = null;
  private cartIcon: HTMLElement | null = null;

  constructor() {
    this.initializeDOM();
  }

  private initializeDOM(): void {
    // Simular elementos DOM
    this.userInfo = document.createElement('div');
    this.cartIcon = document.createElement('div');
  }

  public update(event: Event): void {
    switch (event.type) {
      case EventType.USER_LOGIN:
        this.updateUserInfo(event.data);
        break;
      case EventType.USER_LOGOUT:
        this.clearUserInfo();
        break;
      case EventType.CART_UPDATED:
        this.updateCartIcon(event.data.cartState);
        break;
    }
  }

  private updateUserInfo(data: any): void {
    console.log(`👤 [HEADER] Usuário logado: ${data.username} (${data.email})`);
    // Simular atualização do DOM
    if (this.userInfo) {
      this.userInfo.textContent = `Olá, ${data.username}!`;
    }
  }

  private clearUserInfo(): void {
    console.log(`👤 [HEADER] Usuário deslogado`);
    if (this.userInfo) {
      this.userInfo.textContent = 'Login';
    }
  }

  private updateCartIcon(cartState: CartState): void {
    console.log(`🛒 [HEADER] Carrinho atualizado: ${cartState.itemCount} itens (R$ ${cartState.total.toFixed(2)})`);
    if (this.cartIcon) {
      this.cartIcon.textContent = `Carrinho (${cartState.itemCount})`;
    }
  }
}

// Observador 2: Sidebar Component
class SidebarComponent implements Observer {
  private userMenu: HTMLElement | null = null;
  private cartSummary: HTMLElement | null = null;

  constructor() {
    this.initializeDOM();
  }

  private initializeDOM(): void {
    this.userMenu = document.createElement('div');
    this.cartSummary = document.createElement('div');
  }

  public update(event: Event): void {
    switch (event.type) {
      case EventType.USER_LOGIN:
        this.showUserMenu(event.data);
        break;
      case EventType.USER_LOGOUT:
        this.hideUserMenu();
        break;
      case EventType.CART_UPDATED:
        this.updateCartSummary(event.data.cartState);
        break;
    }
  }

  private showUserMenu(data: any): void {
    console.log(`📋 [SIDEBAR] Menu do usuário exibido para: ${data.username}`);
    if (this.userMenu) {
      this.userMenu.innerHTML = `
        <div>Perfil: ${data.username}</div>
        <div>Email: ${data.email}</div>
        <button>Configurações</button>
        <button>Logout</button>
      `;
    }
  }

  private hideUserMenu(): void {
    console.log(`📋 [SIDEBAR] Menu do usuário ocultado`);
    if (this.userMenu) {
      this.userMenu.innerHTML = '';
    }
  }

  private updateCartSummary(cartState: CartState): void {
    console.log(`📋 [SIDEBAR] Resumo do carrinho atualizado`);
    if (this.cartSummary) {
      this.cartSummary.innerHTML = `
        <h3>Carrinho (${cartState.itemCount})</h3>
        <div>Total: R$ ${cartState.total.toFixed(2)}</div>
        <ul>
          ${cartState.items.map(item => 
            `<li>${item.name} x${item.quantity} - R$ ${(item.price * item.quantity).toFixed(2)}</li>`
          ).join('')}
        </ul>
      `;
    }
  }
}

// Observador 3: Theme Manager
class ThemeManager implements Observer {
  private currentTheme: Theme = Theme.LIGHT;

  public update(event: Event): void {
    if (event.type === EventType.THEME_CHANGED) {
      this.changeTheme(event.data.theme);
    }
  }

  private changeTheme(theme: Theme): void {
    this.currentTheme = theme;
    console.log(`🎨 [THEME] Tema alterado para: ${theme}`);
    
    // Simular aplicação do tema
    this.applyTheme(theme);
  }

  private applyTheme(theme: Theme): void {
    const body = document.body;
    
    switch (theme) {
      case Theme.LIGHT:
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        break;
      case Theme.DARK:
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        break;
      case Theme.AUTO:
        // Simular detecção automática
        const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        this.applyTheme(isDark ? Theme.DARK : Theme.LIGHT);
        break;
    }
  }
}

// Observador 4: Language Manager
class LanguageManager implements Observer {
  private currentLanguage: Language = Language.PT;
  private translations: Record<Language, Record<string, string>> = {
    [Language.PT]: {
      'welcome': 'Bem-vindo',
      'cart': 'Carrinho',
      'login': 'Login',
      'logout': 'Sair'
    },
    [Language.EN]: {
      'welcome': 'Welcome',
      'cart': 'Cart',
      'login': 'Login',
      'logout': 'Logout'
    },
    [Language.ES]: {
      'welcome': 'Bienvenido',
      'cart': 'Carrito',
      'login': 'Iniciar sesión',
      'logout': 'Cerrar sesión'
    }
  };

  public update(event: Event): void {
    if (event.type === EventType.LANGUAGE_CHANGED) {
      this.changeLanguage(event.data.language);
    }
  }

  private changeLanguage(language: Language): void {
    this.currentLanguage = language;
    console.log(`🌐 [LANGUAGE] Idioma alterado para: ${language}`);
    
    // Simular atualização de textos
    this.updateTexts();
  }

  private updateTexts(): void {
    const texts = this.translations[this.currentLanguage];
    console.log(`🌐 [LANGUAGE] Textos atualizados:`, texts);
    
    // Simular atualização de elementos DOM
    Object.entries(texts).forEach(([key, value]) => {
      const element = document.querySelector(`[data-translate="${key}"]`);
      if (element) {
        element.textContent = value;
      }
    });
  }
}

// Observador 5: Analytics Tracker
class AnalyticsTracker implements Observer {
  private events: Event[] = [];
  private userSessions: Map<string, number> = new Map();

  public update(event: Event): void {
    this.events.push(event);
    this.trackEvent(event);
  }

  private trackEvent(event: Event): void {
    console.log(`📊 [ANALYTICS] Evento rastreado: ${event.type}`);
    
    switch (event.type) {
      case EventType.USER_LOGIN:
        this.trackUserLogin(event);
        break;
      case EventType.CART_UPDATED:
        this.trackCartUpdate(event);
        break;
      case EventType.PRODUCT_VIEWED:
        this.trackProductView(event);
        break;
    }
  }

  private trackUserLogin(event: Event): void {
    const userId = event.data.userId;
    const sessionCount = this.userSessions.get(userId) || 0;
    this.userSessions.set(userId, sessionCount + 1);
    
    console.log(`📊 [ANALYTICS] Login do usuário ${userId} (sessão #${sessionCount + 1})`);
  }

  private trackCartUpdate(event: Event): void {
    const cartState = event.data.cartState;
    console.log(`📊 [ANALYTICS] Carrinho atualizado: ${cartState.itemCount} itens, R$ ${cartState.total.toFixed(2)}`);
  }

  private trackProductView(event: Event): void {
    console.log(`📊 [ANALYTICS] Produto visualizado: ${event.data.productId}`);
  }

  public getAnalytics(): any {
    return {
      totalEvents: this.events.length,
      userSessions: Object.fromEntries(this.userSessions),
      eventTypes: this.events.reduce((acc, event) => {
        acc[event.type] = (acc[event.type] || 0) + 1;
        return acc;
      }, {} as Record<string, number>)
    };
  }
}

// Observador 6: Notification System
class NotificationSystem implements Observer {
  private notifications: string[] = [];

  public update(event: Event): void {
    switch (event.type) {
      case EventType.USER_LOGIN:
        this.showWelcomeNotification(event.data);
        break;
      case EventType.CART_UPDATED:
        this.showCartNotification(event.data);
        break;
      case EventType.THEME_CHANGED:
        this.showThemeNotification(event.data);
        break;
    }
  }

  private showWelcomeNotification(data: any): void {
    const message = `Bem-vindo, ${data.username}!`;
    this.notifications.push(message);
    console.log(`🔔 [NOTIFICATION] ${message}`);
  }

  private showCartNotification(data: any): void {
    const message = `Item adicionado ao carrinho! Total: R$ ${data.cartState.total.toFixed(2)}`;
    this.notifications.push(message);
    console.log(`🔔 [NOTIFICATION] ${message}`);
  }

  private showThemeNotification(data: any): void {
    const message = `Tema alterado para: ${data.theme}`;
    this.notifications.push(message);
    console.log(`🔔 [NOTIFICATION] ${message}`);
  }

  public getNotifications(): string[] {
    return [...this.notifications];
  }
}

// Exemplo de uso
function demonstrateObserverPattern(): void {
  console.log('=== Demonstração do Padrão Observer - Sistema de UI Reativa ===\n');

  // Criar gerenciador de estado
  const stateManager = new StateManager();

  // Criar observadores
  const headerComponent = new HeaderComponent();
  const sidebarComponent = new SidebarComponent();
  const themeManager = new ThemeManager();
  const languageManager = new LanguageManager();
  const analyticsTracker = new AnalyticsTracker();
  const notificationSystem = new NotificationSystem();

  // Adicionar observadores
  stateManager.addObserver(headerComponent);
  stateManager.addObserver(sidebarComponent);
  stateManager.addObserver(themeManager);
  stateManager.addObserver(languageManager);
  stateManager.addObserver(analyticsTracker);
  stateManager.addObserver(notificationSystem);

  console.log('✅ Todos os observadores adicionados!\n');

  // Simular interações do usuário
  console.log('--- Simulando Login ---');
  stateManager.login('user123', 'João Silva', 'joao@email.com');

  console.log('\n--- Simulando Adição ao Carrinho ---');
  stateManager.addToCart({
    id: 'prod1',
    name: 'Produto A',
    price: 99.90
  });

  stateManager.addToCart({
    id: 'prod2',
    name: 'Produto B',
    price: 149.90
  });

  console.log('\n--- Simulando Mudança de Tema ---');
  stateManager.changeTheme(Theme.DARK);

  console.log('\n--- Simulando Mudança de Idioma ---');
  stateManager.changeLanguage(Language.EN);

  console.log('\n--- Simulando Logout ---');
  stateManager.logout();

  // Mostrar estatísticas
  console.log('\n=== Estatísticas Finais ===');
  const analytics = analyticsTracker.getAnalytics();
  console.log('📊 Analytics:', analytics);
  
  const notifications = notificationSystem.getNotifications();
  console.log('🔔 Notificações:', notifications);
}

// Demonstração de remoção de observadores
function demonstrateObserverRemoval(): void {
  console.log('\n=== Demonstração de Remoção de Observadores ===\n');

  const stateManager = new StateManager();
  const headerComponent = new HeaderComponent();
  const sidebarComponent = new SidebarComponent();

  // Adicionar observadores
  stateManager.addObserver(headerComponent);
  stateManager.addObserver(sidebarComponent);

  // Simular evento com todos os observadores
  console.log('--- Com todos os observadores ---');
  stateManager.login('user456', 'Maria Santos', 'maria@email.com');

  // Remover um observador
  stateManager.removeObserver(sidebarComponent);

  // Simular evento sem o observador removido
  console.log('\n--- Após remover SidebarComponent ---');
  stateManager.addToCart({
    id: 'prod3',
    name: 'Produto C',
    price: 199.90
  });
}

// Demonstração de tratamento de erros
function demonstrateErrorHandling(): void {
  console.log('\n=== Demonstração de Tratamento de Erros ===\n');

  // Observador que gera erro
  class ErrorObserver implements Observer {
    public update(event: Event): void {
      throw new Error('Erro simulado no observador');
    }
  }

  const stateManager = new StateManager();
  const headerComponent = new HeaderComponent();
  const errorObserver = new ErrorObserver();

  // Adicionar observadores (um normal, um com erro)
  stateManager.addObserver(headerComponent);
  stateManager.addObserver(errorObserver);

  // Simular evento (deve continuar funcionando mesmo com erro)
  stateManager.login('user789', 'Pedro Costa', 'pedro@email.com');
}

// Executar demonstrações
if (require.main === module) {
  demonstrateObserverPattern();
  demonstrateObserverRemoval();
  demonstrateErrorHandling();
}

export {
  EventType,
  Theme,
  Language,
  StateManager,
  HeaderComponent,
  SidebarComponent,
  ThemeManager,
  LanguageManager,
  AnalyticsTracker,
  NotificationSystem
};




