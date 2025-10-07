/**
 * Exemplo do Padrão Template Method - Sistema de Autenticação
 * 
 * Este exemplo demonstra como implementar o padrão Template Method para
 * eliminar duplicação de código em um sistema de autenticação que
 * suporta diferentes provedores de login (Google, Facebook, GitHub, etc.).
 */

// Interfaces para tipos de dados
interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
}

interface AuthResult {
  success: boolean;
  user?: User;
  token?: string;
  error?: string;
}

interface AuthProvider {
  name: string;
  clientId: string;
  redirectUri: string;
}

// Classe abstrata que define o template method
abstract class AuthenticationService {
  /**
   * Template Method - define o esqueleto do algoritmo de autenticação
   * Este método não pode ser sobrescrito pelas subclasses
   */
  public async authenticate(credentials: any): Promise<AuthResult> {
    console.log("🚀 Iniciando processo de autenticação...");
    
    try {
      // 1. Validar credenciais
      const validatedCredentials = await this.validateCredentials(credentials);
      console.log("✅ Credenciais validadas");
      
      // 2. Autenticar com provedor
      const authResult = await this.authenticateWithProvider(validatedCredentials);
      console.log("🔐 Autenticação com provedor realizada");
      
      // 3. Processar dados do usuário
      const processedUser = await this.processUserData(authResult);
      console.log("👤 Dados do usuário processados");
      
      // 4. Gerar token (implementação comum)
      const token = await this.generateToken(processedUser);
      console.log("🎫 Token gerado");
      
      // 5. Salvar sessão (implementação comum)
      await this.saveSession(processedUser, token);
      console.log("💾 Sessão salva");
      
      // 6. Enviar notificações (implementação comum)
      await this.sendNotifications(processedUser);
      console.log("📧 Notificações enviadas");
      
      console.log("✅ Autenticação concluída com sucesso!");
      
      return {
        success: true,
        user: processedUser,
        token: token
      };
      
    } catch (error) {
      console.error("❌ Erro durante autenticação:", error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Erro desconhecido'
      };
    }
  }
  
  /**
   * Método abstrato para validar credenciais
   * Cada subclasse implementa sua própria lógica
   */
  protected abstract validateCredentials(credentials: any): Promise<any>;
  
  /**
   * Método abstrato para autenticar com provedor
   * Cada subclasse implementa sua própria lógica
   */
  protected abstract authenticateWithProvider(credentials: any): Promise<any>;
  
  /**
   * Método abstrato para processar dados do usuário
   * Cada subclasse implementa sua própria lógica
   */
  protected abstract processUserData(authResult: any): Promise<User>;
  
  /**
   * Método abstrato para obter nome do provedor
   * Cada subclasse retorna seu nome específico
   */
  protected abstract getProviderName(): string;
  
  /**
   * Método comum para gerar token
   * Implementação compartilhada entre todas as subclasses
   */
  protected async generateToken(user: User): Promise<string> {
    console.log("🔐 Gerando token de autenticação...");
    
    // Simular geração de token JWT
    const payload = {
      userId: user.id,
      email: user.email,
      name: user.name,
      provider: this.getProviderName(),
      iat: Math.floor(Date.now() / 1000),
      exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24 horas
    };
    
    // Simular assinatura do token
    const token = `jwt.${btoa(JSON.stringify(payload))}.signature`;
    
    console.log(`   🎫 Token gerado para usuário: ${user.email}`);
    return token;
  }
  
  /**
   * Método comum para salvar sessão
   * Implementação compartilhada entre todas as subclasses
   */
  protected async saveSession(user: User, token: string): Promise<void> {
    console.log("💾 Salvando sessão do usuário...");
    
    // Simular salvamento da sessão
    const session = {
      userId: user.id,
      token: token,
      provider: this.getProviderName(),
      createdAt: new Date().toISOString(),
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
    };
    
    console.log(`   💾 Sessão salva para usuário: ${user.email}`);
    console.log(`   💾 Provedor: ${this.getProviderName()}`);
    console.log(`   💾 Expira em: ${session.expiresAt}`);
  }
  
  /**
   * Método comum para enviar notificações
   * Implementação compartilhada entre todas as subclasses
   */
  protected async sendNotifications(user: User): Promise<void> {
    console.log("📧 Enviando notificações...");
    
    // Enviar email de boas-vindas
    await this.sendWelcomeEmail(user);
    
    // Enviar notificação interna
    await this.sendInternalNotification(user);
    
    // Notificar administradores
    await this.notifyAdministrators(user);
  }
  
  /**
   * Enviar email de boas-vindas
   * Método comum para todas as subclasses
   */
  private async sendWelcomeEmail(user: User): Promise<void> {
    console.log(`   📧 Email de boas-vindas enviado para: ${user.email}`);
    console.log(`   📧 Assunto: Bem-vindo ao sistema!`);
  }
  
  /**
   * Enviar notificação interna
   * Método comum para todas as subclasses
   */
  private async sendInternalNotification(user: User): Promise<void> {
    console.log(`   🔔 Notificação interna enviada`);
    console.log(`   🔔 Usuário: ${user.name} (${user.email})`);
  }
  
  /**
   * Notificar administradores
   * Método comum para todas as subclasses
   */
  private async notifyAdministrators(user: User): Promise<void> {
    console.log(`   👥 Administradores notificados`);
    console.log(`   👥 Novo usuário: ${user.name} via ${this.getProviderName()}`);
  }
}

// Implementação concreta para autenticação via Google
class GoogleAuthenticationService extends AuthenticationService {
  private clientId: string;
  private redirectUri: string;
  
  constructor(clientId: string, redirectUri: string) {
    super();
    this.clientId = clientId;
    this.redirectUri = redirectUri;
  }
  
  protected async validateCredentials(credentials: any): Promise<any> {
    console.log("🔍 Validando credenciais do Google...");
    
    if (!credentials.code) {
      throw new Error("Código de autorização do Google não fornecido");
    }
    
    if (!credentials.state) {
      throw new Error("Estado de autorização do Google não fornecido");
    }
    
    console.log("✅ Credenciais do Google validadas");
    return credentials;
  }
  
  protected async authenticateWithProvider(credentials: any): Promise<any> {
    console.log("🔐 Autenticando com Google...");
    
    // Simular troca de código por token
    const tokenResponse = await this.exchangeCodeForToken(credentials.code);
    
    // Simular obtenção de dados do usuário
    const userInfo = await this.getUserInfo(tokenResponse.access_token);
    
    console.log("✅ Autenticação com Google realizada");
    return { tokenResponse, userInfo };
  }
  
  protected async processUserData(authResult: any): Promise<User> {
    console.log("👤 Processando dados do usuário do Google...");
    
    const userInfo = authResult.userInfo;
    
    return {
      id: userInfo.id,
      email: userInfo.email,
      name: userInfo.name,
      avatar: userInfo.picture
    };
  }
  
  protected getProviderName(): string {
    return "Google";
  }
  
  private async exchangeCodeForToken(code: string): Promise<any> {
    console.log("🔄 Trocando código por token do Google...");
    
    // Simular chamada para API do Google
    return {
      access_token: `google_access_token_${code}`,
      token_type: "Bearer",
      expires_in: 3600
    };
  }
  
  private async getUserInfo(accessToken: string): Promise<any> {
    console.log("👤 Obtendo informações do usuário do Google...");
    
    // Simular chamada para API do Google
    return {
      id: "google_user_123",
      email: "usuario@gmail.com",
      name: "Usuário Google",
      picture: "https://example.com/avatar.jpg"
    };
  }
}

// Implementação concreta para autenticação via Facebook
class FacebookAuthenticationService extends AuthenticationService {
  private appId: string;
  private appSecret: string;
  
  constructor(appId: string, appSecret: string) {
    super();
    this.appId = appId;
    this.appSecret = appSecret;
  }
  
  protected async validateCredentials(credentials: any): Promise<any> {
    console.log("🔍 Validando credenciais do Facebook...");
    
    if (!credentials.accessToken) {
      throw new Error("Token de acesso do Facebook não fornecido");
    }
    
    console.log("✅ Credenciais do Facebook validadas");
    return credentials;
  }
  
  protected async authenticateWithProvider(credentials: any): Promise<any> {
    console.log("🔐 Autenticando com Facebook...");
    
    // Simular validação do token
    const tokenInfo = await this.validateAccessToken(credentials.accessToken);
    
    // Simular obtenção de dados do usuário
    const userInfo = await this.getUserInfo(credentials.accessToken);
    
    console.log("✅ Autenticação com Facebook realizada");
    return { tokenInfo, userInfo };
  }
  
  protected async processUserData(authResult: any): Promise<User> {
    console.log("👤 Processando dados do usuário do Facebook...");
    
    const userInfo = authResult.userInfo;
    
    return {
      id: userInfo.id,
      email: userInfo.email,
      name: userInfo.name,
      avatar: userInfo.picture?.data?.url
    };
  }
  
  protected getProviderName(): string {
    return "Facebook";
  }
  
  private async validateAccessToken(accessToken: string): Promise<any> {
    console.log("🔄 Validando token de acesso do Facebook...");
    
    // Simular validação do token
    return {
      app_id: this.appId,
      user_id: "facebook_user_456",
      is_valid: true
    };
  }
  
  private async getUserInfo(accessToken: string): Promise<any> {
    console.log("👤 Obtendo informações do usuário do Facebook...");
    
    // Simular chamada para API do Facebook
    return {
      id: "facebook_user_456",
      email: "usuario@facebook.com",
      name: "Usuário Facebook",
      picture: {
        data: {
          url: "https://example.com/facebook_avatar.jpg"
        }
      }
    };
  }
}

// Implementação concreta para autenticação via GitHub
class GitHubAuthenticationService extends AuthenticationService {
  private clientId: string;
  private clientSecret: string;
  
  constructor(clientId: string, clientSecret: string) {
    super();
    this.clientId = clientId;
    this.clientSecret = clientSecret;
  }
  
  protected async validateCredentials(credentials: any): Promise<any> {
    console.log("🔍 Validando credenciais do GitHub...");
    
    if (!credentials.code) {
      throw new Error("Código de autorização do GitHub não fornecido");
    }
    
    console.log("✅ Credenciais do GitHub validadas");
    return credentials;
  }
  
  protected async authenticateWithProvider(credentials: any): Promise<any> {
    console.log("🔐 Autenticando com GitHub...");
    
    // Simular troca de código por token
    const tokenResponse = await this.exchangeCodeForToken(credentials.code);
    
    // Simular obtenção de dados do usuário
    const userInfo = await this.getUserInfo(tokenResponse.access_token);
    
    console.log("✅ Autenticação com GitHub realizada");
    return { tokenResponse, userInfo };
  }
  
  protected async processUserData(authResult: any): Promise<User> {
    console.log("👤 Processando dados do usuário do GitHub...");
    
    const userInfo = authResult.userInfo;
    
    return {
      id: userInfo.id.toString(),
      email: userInfo.email || userInfo.login + "@github.com",
      name: userInfo.name || userInfo.login,
      avatar: userInfo.avatar_url
    };
  }
  
  protected getProviderName(): string {
    return "GitHub";
  }
  
  private async exchangeCodeForToken(code: string): Promise<any> {
    console.log("🔄 Trocando código por token do GitHub...");
    
    // Simular chamada para API do GitHub
    return {
      access_token: `github_access_token_${code}`,
      token_type: "bearer",
      scope: "user:email"
    };
  }
  
  private async getUserInfo(accessToken: string): Promise<any> {
    console.log("👤 Obtendo informações do usuário do GitHub...");
    
    // Simular chamada para API do GitHub
    return {
      id: 789,
      login: "usuario-github",
      name: "Usuário GitHub",
      email: "usuario@github.com",
      avatar_url: "https://example.com/github_avatar.jpg"
    };
  }
}

// Implementação concreta para autenticação via LinkedIn
class LinkedInAuthenticationService extends AuthenticationService {
  private clientId: string;
  private clientSecret: string;
  
  constructor(clientId: string, clientSecret: string) {
    super();
    this.clientId = clientId;
    this.clientSecret = clientSecret;
  }
  
  protected async validateCredentials(credentials: any): Promise<any> {
    console.log("🔍 Validando credenciais do LinkedIn...");
    
    if (!credentials.code) {
      throw new Error("Código de autorização do LinkedIn não fornecido");
    }
    
    console.log("✅ Credenciais do LinkedIn validadas");
    return credentials;
  }
  
  protected async authenticateWithProvider(credentials: any): Promise<any> {
    console.log("🔐 Autenticando com LinkedIn...");
    
    // Simular troca de código por token
    const tokenResponse = await this.exchangeCodeForToken(credentials.code);
    
    // Simular obtenção de dados do usuário
    const userInfo = await this.getUserInfo(tokenResponse.access_token);
    
    console.log("✅ Autenticação com LinkedIn realizada");
    return { tokenResponse, userInfo };
  }
  
  protected async processUserData(authResult: any): Promise<User> {
    console.log("👤 Processando dados do usuário do LinkedIn...");
    
    const userInfo = authResult.userInfo;
    
    return {
      id: userInfo.id,
      email: userInfo.emailAddress,
      name: `${userInfo.firstName} ${userInfo.lastName}`,
      avatar: userInfo.profilePicture?.displayImage
    };
  }
  
  protected getProviderName(): string {
    return "LinkedIn";
  }
  
  private async exchangeCodeForToken(code: string): Promise<any> {
    console.log("🔄 Trocando código por token do LinkedIn...");
    
    // Simular chamada para API do LinkedIn
    return {
      access_token: `linkedin_access_token_${code}`,
      expires_in: 5184000
    };
  }
  
  private async getUserInfo(accessToken: string): Promise<any> {
    console.log("👤 Obtendo informações do usuário do LinkedIn...");
    
    // Simular chamada para API do LinkedIn
    return {
      id: "linkedin_user_101",
      firstName: "Usuário",
      lastName: "LinkedIn",
      emailAddress: "usuario@linkedin.com",
      profilePicture: {
        displayImage: "https://example.com/linkedin_avatar.jpg"
      }
    };
  }
}

// Exemplo de uso
function demonstrateTemplateMethod(): void {
  console.log("=== Demonstração do Padrão Template Method - Sistema de Autenticação ===\n");
  
  // Criar instâncias dos diferentes serviços de autenticação
  const googleAuth = new GoogleAuthenticationService("google_client_id", "http://localhost:3000/callback");
  const facebookAuth = new FacebookAuthenticationService("facebook_app_id", "facebook_app_secret");
  const githubAuth = new GitHubAuthenticationService("github_client_id", "github_client_secret");
  const linkedinAuth = new LinkedInAuthenticationService("linkedin_client_id", "linkedin_client_secret");
  
  // Simular autenticação com diferentes provedores
  const authServices = [
    { service: googleAuth, credentials: { code: "google_auth_code", state: "random_state" }, name: "Google" },
    { service: facebookAuth, credentials: { accessToken: "facebook_access_token" }, name: "Facebook" },
    { service: githubAuth, credentials: { code: "github_auth_code" }, name: "GitHub" },
    { service: linkedinAuth, credentials: { code: "linkedin_auth_code" }, name: "LinkedIn" }
  ];
  
  // Executar autenticação para cada provedor
  authServices.forEach(async ({ service, credentials, name }) => {
    console.log(`--- Autenticação via ${name} ---`);
    try {
      const result = await service.authenticate(credentials);
      if (result.success) {
        console.log(`✅ Autenticação ${name} bem-sucedida!`);
        console.log(`   👤 Usuário: ${result.user?.name} (${result.user?.email})`);
        console.log(`   🎫 Token: ${result.token?.substring(0, 20)}...`);
      } else {
        console.log(`❌ Falha na autenticação ${name}: ${result.error}`);
      }
    } catch (error) {
      console.log(`❌ Erro na autenticação ${name}:`, error);
    }
    console.log();
  });
}

// Demonstração de extensibilidade
function demonstrateExtensibility(): void {
  console.log("\n=== Demonstração de Extensibilidade ===\n");
  
  // Criar um novo serviço de autenticação para Twitter
  class TwitterAuthenticationService extends AuthenticationService {
    private apiKey: string;
    private apiSecret: string;
    
    constructor(apiKey: string, apiSecret: string) {
      super();
      this.apiKey = apiKey;
      this.apiSecret = apiSecret;
    }
    
    protected async validateCredentials(credentials: any): Promise<any> {
      console.log("🔍 Validando credenciais do Twitter...");
      
      if (!credentials.oauthToken) {
        throw new Error("Token OAuth do Twitter não fornecido");
      }
      
      console.log("✅ Credenciais do Twitter validadas");
      return credentials;
    }
    
    protected async authenticateWithProvider(credentials: any): Promise<any> {
      console.log("🔐 Autenticando com Twitter...");
      
      // Simular validação do token OAuth
      const tokenInfo = await this.validateOAuthToken(credentials.oauthToken);
      
      // Simular obtenção de dados do usuário
      const userInfo = await this.getUserInfo(credentials.oauthToken);
      
      console.log("✅ Autenticação com Twitter realizada");
      return { tokenInfo, userInfo };
    }
    
    protected async processUserData(authResult: any): Promise<User> {
      console.log("👤 Processando dados do usuário do Twitter...");
      
      const userInfo = authResult.userInfo;
      
      return {
        id: userInfo.id_str,
        email: userInfo.email || userInfo.screen_name + "@twitter.com",
        name: userInfo.name,
        avatar: userInfo.profile_image_url_https
      };
    }
    
    protected getProviderName(): string {
      return "Twitter";
    }
    
    private async validateOAuthToken(oauthToken: string): Promise<any> {
      console.log("🔄 Validando token OAuth do Twitter...");
      
      return {
        oauth_token: oauthToken,
        oauth_token_secret: "twitter_token_secret",
        user_id: "twitter_user_202"
      };
    }
    
    private async getUserInfo(oauthToken: string): Promise<any> {
      console.log("👤 Obtendo informações do usuário do Twitter...");
      
      return {
        id_str: "twitter_user_202",
        screen_name: "usuario_twitter",
        name: "Usuário Twitter",
        email: "usuario@twitter.com",
        profile_image_url_https: "https://example.com/twitter_avatar.jpg"
      };
    }
  }
  
  // Usar o novo serviço de autenticação
  const twitterAuth = new TwitterAuthenticationService("twitter_api_key", "twitter_api_secret");
  
  console.log("--- Autenticação via Twitter ---");
  twitterAuth.authenticate({ oauthToken: "twitter_oauth_token" });
}

// Demonstração de personalização
function demonstrateCustomization(): void {
  console.log("\n=== Demonstração de Personalização ===\n");
  
  // Serviço de autenticação personalizado que sobrescreve métodos comuns
  class CustomAuthenticationService extends AuthenticationService {
    protected async validateCredentials(credentials: any): Promise<any> {
      console.log("🔍 Validando credenciais com lógica personalizada...");
      return credentials;
    }
    
    protected async authenticateWithProvider(credentials: any): Promise<any> {
      console.log("🔐 Autenticando com provedor personalizado...");
      return { userInfo: { id: "custom_user", email: "custom@example.com", name: "Usuário Custom" } };
    }
    
    protected async processUserData(authResult: any): Promise<User> {
      console.log("👤 Processando dados com lógica personalizada...");
      
      const userInfo = authResult.userInfo;
      return {
        id: userInfo.id,
        email: userInfo.email,
        name: userInfo.name,
        avatar: "https://example.com/custom_avatar.jpg"
      };
    }
    
    protected getProviderName(): string {
      return "Custom";
    }
    
    // Sobrescrever método comum para personalização
    protected async sendNotifications(user: User): Promise<void> {
      console.log("📧 Enviando notificações personalizadas...");
      console.log(`   📧 Email personalizado enviado para: ${user.email}`);
      console.log(`   📧 Assunto personalizado: Bem-vindo ao sistema customizado!`);
      console.log(`   🔔 Notificação personalizada enviada`);
      console.log("✅ Notificações personalizadas enviadas com sucesso");
    }
  }
  
  // Usar o serviço personalizado
  const customAuth = new CustomAuthenticationService();
  
  console.log("--- Autenticação Personalizada ---");
  customAuth.authenticate({ customCredentials: "custom_auth_data" });
}

// Executar demonstrações
if (require.main === module) {
  demonstrateTemplateMethod();
  demonstrateExtensibility();
  demonstrateCustomization();
}

export {
  AuthenticationService,
  GoogleAuthenticationService,
  FacebookAuthenticationService,
  GitHubAuthenticationService,
  LinkedInAuthenticationService,
  User,
  AuthResult
};




