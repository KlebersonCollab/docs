/**
 * Exemplo do Padrão Facade - Sistema de Autenticação
 * 
 * Este exemplo demonstra como implementar o padrão Facade para simplificar
 * o processo de autenticação em um sistema, ocultando a complexidade de
 * múltiplos subsistemas de segurança.
 */

// Enums para tipos e status
enum AuthStatus {
  SUCCESS = 'success',
  FAILED = 'failed',
  PENDING = 'pending',
  EXPIRED = 'expired'
}

enum UserRole {
  ADMIN = 'admin',
  USER = 'user',
  MODERATOR = 'moderator',
  GUEST = 'guest'
}

// Interfaces
interface User {
  id: string;
  email: string;
  password: string;
  role: UserRole;
  isActive: boolean;
  lastLogin?: Date;
}

interface AuthResult {
  success: boolean;
  user?: User;
  token?: string;
  error?: string;
  status: AuthStatus;
}

interface LoginCredentials {
  email: string;
  password: string;
  rememberMe?: boolean;
}

// Subsistema 1: Gerenciador de Usuários
class UserManager {
  private users: Map<string, User> = new Map();
  private sessions: Map<string, string> = new Map(); // sessionId -> userId

  constructor() {
    // Usuários de exemplo
    this.users.set('user1', {
      id: 'user1',
      email: 'admin@example.com',
      password: 'hashed_password_1',
      role: UserRole.ADMIN,
      isActive: true
    });

    this.users.set('user2', {
      id: 'user2',
      email: 'user@example.com',
      password: 'hashed_password_2',
      role: UserRole.USER,
      isActive: true
    });
  }

  async findUserByEmail(email: string): Promise<User | null> {
    // Simular busca no banco de dados
    await this.simulateDelay(100);
    
    for (const user of this.users.values()) {
      if (user.email === email) {
        return user;
      }
    }
    return null;
  }

  async findUserById(id: string): Promise<User | null> {
    // Simular busca no banco de dados
    await this.simulateDelay(50);
    
    return this.users.get(id) || null;
  }

  async updateLastLogin(userId: string): Promise<void> {
    const user = this.users.get(userId);
    if (user) {
      user.lastLogin = new Date();
      this.users.set(userId, user);
    }
  }

  async createSession(userId: string): Promise<string> {
    const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.sessions.set(sessionId, userId);
    return sessionId;
  }

  async getSession(sessionId: string): Promise<string | null> {
    return this.sessions.get(sessionId) || null;
  }

  async destroySession(sessionId: string): Promise<void> {
    this.sessions.delete(sessionId);
  }

  private async simulateDelay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Subsistema 2: Validador de Credenciais
class CredentialValidator {
  private readonly emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  private readonly passwordMinLength = 8;

  validateEmail(email: string): boolean {
    return this.emailRegex.test(email);
  }

  validatePassword(password: string): boolean {
    return password.length >= this.passwordMinLength;
  }

  validateCredentials(credentials: LoginCredentials): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!this.validateEmail(credentials.email)) {
      errors.push('Email inválido');
    }

    if (!this.validatePassword(credentials.password)) {
      errors.push('Senha deve ter pelo menos 8 caracteres');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}

// Subsistema 3: Gerenciador de Senhas
class PasswordManager {
  async hashPassword(password: string): Promise<string> {
    // Simular hash de senha
    await this.simulateDelay(200);
    return `hashed_${password}_${Date.now()}`;
  }

  async verifyPassword(password: string, hashedPassword: string): Promise<boolean> {
    // Simular verificação de senha
    await this.simulateDelay(150);
    
    // Para exemplo, vamos usar uma verificação simples
    return hashedPassword.includes(password);
  }

  async generatePasswordResetToken(): Promise<string> {
    // Simular geração de token
    await this.simulateDelay(100);
    return `reset_token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private async simulateDelay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Subsistema 4: Gerenciador de Tokens
class TokenManager {
  private tokens: Map<string, { userId: string; expiresAt: Date }> = new Map();

  async generateToken(userId: string, expiresInHours: number = 24): Promise<string> {
    const token = `token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const expiresAt = new Date(Date.now() + expiresInHours * 60 * 60 * 1000);
    
    this.tokens.set(token, { userId, expiresAt });
    
    console.log(`🔑 Token gerado para usuário ${userId}, expira em ${expiresInHours}h`);
    return token;
  }

  async validateToken(token: string): Promise<{ isValid: boolean; userId?: string; error?: string }> {
    const tokenData = this.tokens.get(token);
    
    if (!tokenData) {
      return { isValid: false, error: 'Token não encontrado' };
    }

    if (tokenData.expiresAt < new Date()) {
      this.tokens.delete(token);
      return { isValid: false, error: 'Token expirado' };
    }

    return { isValid: true, userId: tokenData.userId };
  }

  async revokeToken(token: string): Promise<void> {
    this.tokens.delete(token);
    console.log(`🔑 Token revogado: ${token}`);
  }

  async revokeAllUserTokens(userId: string): Promise<void> {
    for (const [token, data] of this.tokens.entries()) {
      if (data.userId === userId) {
        this.tokens.delete(token);
      }
    }
    console.log(`🔑 Todos os tokens do usuário ${userId} foram revogados`);
  }
}

// Subsistema 5: Sistema de Logs de Segurança
class SecurityLogger {
  private logs: Array<{
    timestamp: Date;
    userId?: string;
    action: string;
    status: AuthStatus;
    ipAddress?: string;
    userAgent?: string;
  }> = [];

  logAuthAttempt(userId: string | undefined, action: string, status: AuthStatus, ipAddress?: string, userAgent?: string): void {
    const logEntry = {
      timestamp: new Date(),
      userId,
      action,
      status,
      ipAddress,
      userAgent
    };
    
    this.logs.push(logEntry);
    
    console.log(`🔒 Log de Segurança: ${action} - ${status} - ${userId || 'N/A'}`);
  }

  logSecurityEvent(event: string, details: string): void {
    console.log(`🚨 Evento de Segurança: ${event} - ${details}`);
  }

  getAuthLogs(userId?: string): Array<any> {
    if (userId) {
      return this.logs.filter(log => log.userId === userId);
    }
    return this.logs;
  }
}

// Subsistema 6: Gerenciador de Permissões
class PermissionManager {
  private rolePermissions: Map<UserRole, string[]> = new Map();

  constructor() {
    // Definir permissões por role
    this.rolePermissions.set(UserRole.ADMIN, ['read', 'write', 'delete', 'admin']);
    this.rolePermissions.set(UserRole.MODERATOR, ['read', 'write', 'moderate']);
    this.rolePermissions.set(UserRole.USER, ['read', 'write']);
    this.rolePermissions.set(UserRole.GUEST, ['read']);
  }

  hasPermission(userRole: UserRole, permission: string): boolean {
    const permissions = this.rolePermissions.get(userRole) || [];
    return permissions.includes(permission);
  }

  getUserPermissions(userRole: UserRole): string[] {
    return this.rolePermissions.get(userRole) || [];
  }
}

// Facade: Interface simplificada para o subsistema complexo
class AuthenticationFacade {
  private userManager: UserManager;
  private credentialValidator: CredentialValidator;
  private passwordManager: PasswordManager;
  private tokenManager: TokenManager;
  private securityLogger: SecurityLogger;
  private permissionManager: PermissionManager;

  constructor() {
    this.userManager = new UserManager();
    this.credentialValidator = new CredentialValidator();
    this.passwordManager = new PasswordManager();
    this.tokenManager = new TokenManager();
    this.securityLogger = new SecurityLogger();
    this.permissionManager = new PermissionManager();
  }

  /**
   * Método principal para login
   */
  async login(credentials: LoginCredentials, ipAddress?: string, userAgent?: string): Promise<AuthResult> {
    try {
      console.log(`🔐 Iniciando processo de login para: ${credentials.email}`);

      // 1. Validar credenciais
      const validation = this.credentialValidator.validateCredentials(credentials);
      if (!validation.isValid) {
        this.securityLogger.logAuthAttempt(undefined, 'login', AuthStatus.FAILED, ipAddress, userAgent);
        return {
          success: false,
          status: AuthStatus.FAILED,
          error: validation.errors.join(', ')
        };
      }

      // 2. Buscar usuário
      const user = await this.userManager.findUserByEmail(credentials.email);
      if (!user) {
        this.securityLogger.logAuthAttempt(undefined, 'login', AuthStatus.FAILED, ipAddress, userAgent);
        return {
          success: false,
          status: AuthStatus.FAILED,
          error: 'Usuário não encontrado'
        };
      }

      // 3. Verificar se usuário está ativo
      if (!user.isActive) {
        this.securityLogger.logAuthAttempt(user.id, 'login', AuthStatus.FAILED, ipAddress, userAgent);
        return {
          success: false,
          status: AuthStatus.FAILED,
          error: 'Usuário inativo'
        };
      }

      // 4. Verificar senha
      const isPasswordValid = await this.passwordManager.verifyPassword(credentials.password, user.password);
      if (!isPasswordValid) {
        this.securityLogger.logAuthAttempt(user.id, 'login', AuthStatus.FAILED, ipAddress, userAgent);
        return {
          success: false,
          status: AuthStatus.FAILED,
          error: 'Senha incorreta'
        };
      }

      // 5. Atualizar último login
      await this.userManager.updateLastLogin(user.id);

      // 6. Gerar token
      const token = await this.tokenManager.generateToken(user.id, credentials.rememberMe ? 168 : 24); // 7 dias ou 1 dia

      // 7. Criar sessão
      const sessionId = await this.userManager.createSession(user.id);

      // 8. Log de sucesso
      this.securityLogger.logAuthAttempt(user.id, 'login', AuthStatus.SUCCESS, ipAddress, userAgent);

      console.log(`✅ Login realizado com sucesso para: ${user.email}`);

      return {
        success: true,
        user,
        token,
        status: AuthStatus.SUCCESS
      };

    } catch (error) {
      this.securityLogger.logSecurityEvent('login_error', error instanceof Error ? error.message : 'Erro desconhecido');
      return {
        success: false,
        status: AuthStatus.FAILED,
        error: 'Erro interno do servidor'
      };
    }
  }

  /**
   * Método para validar token
   */
  async validateToken(token: string): Promise<AuthResult> {
    try {
      const validation = await this.tokenManager.validateToken(token);
      
      if (!validation.isValid) {
        return {
          success: false,
          status: AuthStatus.FAILED,
          error: validation.error
        };
      }

      const user = await this.userManager.findUserById(validation.userId!);
      if (!user || !user.isActive) {
        return {
          success: false,
          status: AuthStatus.FAILED,
          error: 'Usuário não encontrado ou inativo'
        };
      }

      return {
        success: true,
        user,
        token,
        status: AuthStatus.SUCCESS
      };

    } catch (error) {
      return {
        success: false,
        status: AuthStatus.FAILED,
        error: 'Erro na validação do token'
      };
    }
  }

  /**
   * Método para logout
   */
  async logout(token: string): Promise<{ success: boolean; message: string }> {
    try {
      await this.tokenManager.revokeToken(token);
      this.securityLogger.logSecurityEvent('logout', `Token revogado: ${token}`);
      
      return {
        success: true,
        message: 'Logout realizado com sucesso'
      };
    } catch (error) {
      return {
        success: false,
        message: 'Erro ao realizar logout'
      };
    }
  }

  /**
   * Método para verificar permissões
   */
  async checkPermission(userId: string, permission: string): Promise<boolean> {
    try {
      const user = await this.userManager.findUserById(userId);
      if (!user) {
        return false;
      }

      return this.permissionManager.hasPermission(user.role, permission);
    } catch (error) {
      return false;
    }
  }

  /**
   * Método para obter permissões do usuário
   */
  async getUserPermissions(userId: string): Promise<string[]> {
    try {
      const user = await this.userManager.findUserById(userId);
      if (!user) {
        return [];
      }

      return this.permissionManager.getUserPermissions(user.role);
    } catch (error) {
      return [];
    }
  }
}

// Controller que usa a Facade
class AuthController {
  private authFacade: AuthenticationFacade;

  constructor(authFacade: AuthenticationFacade) {
    this.authFacade = authFacade;
  }

  async login(credentials: LoginCredentials, ipAddress?: string, userAgent?: string): Promise<AuthResult> {
    return await this.authFacade.login(credentials, ipAddress, userAgent);
  }

  async validateToken(token: string): Promise<AuthResult> {
    return await this.authFacade.validateToken(token);
  }

  async logout(token: string): Promise<{ success: boolean; message: string }> {
    return await this.authFacade.logout(token);
  }

  async checkPermission(userId: string, permission: string): Promise<boolean> {
    return await this.authFacade.checkPermission(userId, permission);
  }
}

// Exemplo de uso
async function demonstrateAuthFacade(): Promise<void> {
  console.log('=== Demonstração do Padrão Facade - Sistema de Autenticação ===\n');

  const authFacade = new AuthenticationFacade();
  const authController = new AuthController(authFacade);

  // Teste de login
  console.log('--- Teste de Login ---');
  const loginResult = await authController.login({
    email: 'admin@example.com',
    password: 'hashed_password_1',
    rememberMe: true
  }, '192.168.1.1', 'Mozilla/5.0...');

  if (loginResult.success) {
    console.log(`✅ Login bem-sucedido!`);
    console.log(`👤 Usuário: ${loginResult.user?.email}`);
    console.log(`🔑 Token: ${loginResult.token}`);

    // Teste de validação de token
    console.log('\n--- Teste de Validação de Token ---');
    const validationResult = await authController.validateToken(loginResult.token!);
    
    if (validationResult.success) {
      console.log(`✅ Token válido!`);
      console.log(`👤 Usuário: ${validationResult.user?.email}`);
      console.log(`🎭 Role: ${validationResult.user?.role}`);

      // Teste de permissões
      console.log('\n--- Teste de Permissões ---');
      const hasAdminPermission = await authController.checkPermission(validationResult.user!.id, 'admin');
      console.log(`🔐 Tem permissão de admin: ${hasAdminPermission ? 'Sim' : 'Não'}`);

      const hasWritePermission = await authController.checkPermission(validationResult.user!.id, 'write');
      console.log(`✍️ Tem permissão de escrita: ${hasWritePermission ? 'Sim' : 'Não'}`);

      // Teste de logout
      console.log('\n--- Teste de Logout ---');
      const logoutResult = await authController.logout(loginResult.token!);
      console.log(`🚪 Logout: ${logoutResult.message}`);
    }
  } else {
    console.log(`❌ Falha no login: ${loginResult.error}`);
  }

  console.log('\n' + '='.repeat(50) + '\n');
}

// Demonstração de casos de erro
async function demonstrateErrorCases(): Promise<void> {
  console.log('=== Demonstração de Casos de Erro ===\n');

  const authFacade = new AuthenticationFacade();
  const authController = new AuthController(authFacade);

  // Teste com credenciais inválidas
  console.log('--- Login com Email Inválido ---');
  const invalidEmailResult = await authController.login({
    email: 'email-invalido',
    password: 'senha123'
  });
  console.log(`Resultado: ${invalidEmailResult.success ? '✅ Sucesso' : '❌ Falha'}`);
  if (!invalidEmailResult.success) {
    console.log(`Erro: ${invalidEmailResult.error}`);
  }

  // Teste com usuário inexistente
  console.log('\n--- Login com Usuário Inexistente ---');
  const nonExistentUserResult = await authController.login({
    email: 'inexistente@example.com',
    password: 'senha123'
  });
  console.log(`Resultado: ${nonExistentUserResult.success ? '✅ Sucesso' : '❌ Falha'}`);
  if (!nonExistentUserResult.success) {
    console.log(`Erro: ${nonExistentUserResult.error}`);
  }

  // Teste com senha incorreta
  console.log('\n--- Login com Senha Incorreta ---');
  const wrongPasswordResult = await authController.login({
    email: 'admin@example.com',
    password: 'senha_errada'
  });
  console.log(`Resultado: ${wrongPasswordResult.success ? '✅ Sucesso' : '❌ Falha'}`);
  if (!wrongPasswordResult.success) {
    console.log(`Erro: ${wrongPasswordResult.error}`);
  }
}

// Executar demonstrações
if (require.main === module) {
  demonstrateAuthFacade()
    .then(() => demonstrateErrorCases())
    .catch(console.error);
}

export {
  AuthStatus,
  UserRole,
  User,
  AuthResult,
  LoginCredentials,
  AuthenticationFacade,
  AuthController
};




