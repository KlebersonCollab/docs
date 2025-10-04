# Violações Comuns do Princípio da Responsabilidade Única

## Informações Básicas
- **ID do Documento**: SRP-002
- **Nome**: Violações Comuns do SRP
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

Este documento apresenta as violações mais comuns do Princípio da Responsabilidade Única (SRP), seus impactos e como identificá-las. As violações do SRP são frequentemente causadas por mal-entendimento sobre o que constitui uma "responsabilidade única".

## 1. Classe com Múltiplas Responsabilidades

### Definição
Classes que executam diferentes tipos de operações não relacionadas, violando o princípio de coesão.

### Exemplo Problemático
```typescript
// ❌ Classe com múltiplas responsabilidades
class UserService {
  // Responsabilidade 1: Gerenciamento de usuários
  createUser(user: User): void {
    // Lógica de criação
  }
  
  updateUser(user: User): void {
    // Lógica de atualização
  }
  
  deleteUser(userId: string): void {
    // Lógica de exclusão
  }
  
  // Responsabilidade 2: Envio de emails
  sendWelcomeEmail(user: User): void {
    // Lógica de email
  }
  
  sendPasswordResetEmail(user: User): void {
    // Lógica de email
  }
  
  // Responsabilidade 3: Geração de relatórios
  generateUserReport(): void {
    // Lógica de relatório
  }
  
  exportUserData(): void {
    // Lógica de exportação
  }
  
  // Responsabilidade 4: Logging
  logUserActivity(user: User, activity: string): void {
    // Lógica de log
  }
}
```

### Problemas Identificados

#### 1. Múltiplos Motivos para Mudança
- **Se a lógica de usuário mudar**: Classe precisa ser alterada
- **Se a lógica de email mudar**: Classe precisa ser alterada
- **Se a lógica de relatório mudar**: Classe precisa ser alterada
- **Se a lógica de log mudar**: Classe precisa ser alterada

#### 2. Violação do SRP
- **Responsabilidades misturadas**: Usuário, email, relatório e log
- **Dificulta manutenção**: Mudanças em uma área afetam outras
- **Código duplicado**: Lógica não pode ser reutilizada

#### 3. Problemas de Teste
- **Testes complexos**: Muitas dependências para testar
- **Mocks complexos**: Muitas interfaces para mockar
- **Testes frágeis**: Mudanças quebram testes não relacionados

## 2. Classe com Responsabilidades Técnicas Misturadas

### Exemplo Problemático
```typescript
// ❌ Classe com responsabilidades técnicas misturadas
class OrderProcessor {
  // Responsabilidade 1: Lógica de negócio
  processOrder(order: Order): void {
    this.validateOrder(order);
    this.calculateTotal(order);
    this.processPayment(order);
  }
  
  private validateOrder(order: Order): void {
    // Lógica de validação
  }
  
  private calculateTotal(order: Order): void {
    // Lógica de cálculo
  }
  
  private processPayment(order: Order): void {
    // Lógica de pagamento
  }
  
  // Responsabilidade 2: Persistência
  saveOrder(order: Order): void {
    // Conexão com banco
    // Query SQL
    // Tratamento de erro
  }
  
  loadOrder(orderId: string): Order {
    // Conexão com banco
    // Query SQL
    // Mapeamento de dados
  }
  
  // Responsabilidade 3: Logging
  logOrderActivity(order: Order, activity: string): void {
    // Formatação de log
    // Escrita em arquivo
    // Tratamento de erro
  }
  
  // Responsabilidade 4: Notificação
  sendOrderNotification(order: Order): void {
    // Configuração de email
    // Envio de email
    // Tratamento de erro
  }
}
```

### Problemas Identificados

#### 1. Violação de Separação de Responsabilidades
- **Lógica de negócio**: Misturada com persistência
- **Persistência**: Misturada com logging
- **Logging**: Misturado com notificação

#### 2. Dificuldade de Teste
- **Testes de integração**: Necessários para testar persistência
- **Mocks complexos**: Muitas dependências externas
- **Testes frágeis**: Dependem de infraestrutura

#### 3. Problemas de Manutenção
- **Mudanças em cascata**: Alterações afetam múltiplas áreas
- **Código duplicado**: Lógica similar em diferentes métodos
- **Acoplamento alto**: Dependências entre responsabilidades

## 3. Classe com Responsabilidades de Diferentes Níveis

### Exemplo Problemático
```typescript
// ❌ Classe com responsabilidades de diferentes níveis
class ProductService {
  // Responsabilidade 1: Gerenciamento de produtos
  createProduct(product: Product): void {
    // Lógica de criação
  }
  
  updateProduct(product: Product): void {
    // Lógica de atualização
  }
  
  deleteProduct(productId: string): void {
    // Lógica de exclusão
  }
  
  // Responsabilidade 2: Validação de dados
  validateProductData(product: Product): boolean {
    // Validação de campos
    // Validação de regras de negócio
    // Validação de integridade
  }
  
  // Responsabilidade 3: Transformação de dados
  transformProductForAPI(product: Product): any {
    // Mapeamento de campos
    // Formatação de dados
    // Serialização
  }
  
  transformProductFromAPI(data: any): Product {
    // Deserialização
    // Mapeamento de campos
    // Validação de entrada
  }
  
  // Responsabilidade 4: Cache
  getProductFromCache(productId: string): Product {
    // Verificação de cache
    // Retorno de dados
  }
  
  setProductInCache(product: Product): void {
    // Armazenamento em cache
    // Configuração de TTL
  }
  
  // Responsabilidade 5: Auditoria
  auditProductChange(product: Product, change: string): void {
    // Registro de auditoria
    // Timestamp
    // Usuário responsável
  }
}
```

### Problemas Identificados

#### 1. Responsabilidades de Diferentes Níveis
- **Nível de domínio**: Gerenciamento de produtos
- **Nível de aplicação**: Validação e transformação
- **Nível de infraestrutura**: Cache e auditoria

#### 2. Violação de Arquitetura
- **Separação de camadas**: Responsabilidades misturadas
- **Dependências incorretas**: Camadas superiores dependem de inferiores
- **Testabilidade**: Dificulta testes unitários

#### 3. Problemas de Evolução
- **Mudanças em cascata**: Alterações afetam múltiplas camadas
- **Acoplamento alto**: Dependências entre níveis
- **Reutilização**: Lógica não pode ser reutilizada

## 4. Classe com Responsabilidades de Diferentes Contextos

### Exemplo Problemático
```typescript
// ❌ Classe com responsabilidades de diferentes contextos
class OrderService {
  // Responsabilidade 1: Gerenciamento de pedidos
  createOrder(order: Order): void {
    // Lógica de criação
  }
  
  updateOrder(order: Order): void {
    // Lógica de atualização
  }
  
  cancelOrder(orderId: string): void {
    // Lógica de cancelamento
  }
  
  // Responsabilidade 2: Gerenciamento de estoque
  checkInventory(productId: string, quantity: number): boolean {
    // Verificação de estoque
    // Consulta ao banco
    // Validação de disponibilidade
  }
  
  updateInventory(productId: string, quantity: number): void {
    // Atualização de estoque
    // Transação de banco
    // Validação de integridade
  }
  
  // Responsabilidade 3: Gerenciamento de pagamentos
  processPayment(order: Order, paymentMethod: string): void {
    // Processamento de pagamento
    // Integração com gateway
    // Validação de transação
  }
  
  refundPayment(orderId: string): void {
    // Processamento de reembolso
    // Integração com gateway
    // Validação de reembolso
  }
  
  // Responsabilidade 4: Gerenciamento de usuários
  getUserOrders(userId: string): Order[] {
    // Consulta de pedidos do usuário
    // Filtros e paginação
    // Formatação de dados
  }
  
  updateUserProfile(userId: string, profile: UserProfile): void {
    // Atualização de perfil
    // Validação de dados
    // Persistência
  }
}
```

### Problemas Identificados

#### 1. Responsabilidades de Diferentes Contextos
- **Contexto de pedidos**: Gerenciamento de pedidos
- **Contexto de estoque**: Gerenciamento de estoque
- **Contexto de pagamentos**: Gerenciamento de pagamentos
- **Contexto de usuários**: Gerenciamento de usuários

#### 2. Violação de Bounded Contexts
- **Contextos misturados**: Diferentes domínios em uma classe
- **Dependências incorretas**: Contextos acoplados
- **Evolução independente**: Contextos não podem evoluir separadamente

#### 3. Problemas de Manutenção
- **Mudanças em cascata**: Alterações afetam múltiplos contextos
- **Código duplicado**: Lógica similar em diferentes contextos
- **Testabilidade**: Dificulta testes de contexto específico

## 5. Classe com Responsabilidades de Diferentes Abstrações

### Exemplo Problemático
```typescript
// ❌ Classe com responsabilidades de diferentes abstrações
class DataProcessor {
  // Responsabilidade 1: Processamento de dados
  processData(data: any): any {
    // Lógica de processamento
  }
  
  transformData(data: any): any {
    // Lógica de transformação
  }
  
  validateData(data: any): boolean {
    // Lógica de validação
  }
  
  // Responsabilidade 2: Persistência
  saveData(data: any): void {
    // Conexão com banco
    // Query SQL
    // Tratamento de erro
  }
  
  loadData(id: string): any {
    // Conexão com banco
    // Query SQL
    // Mapeamento de dados
  }
  
  // Responsabilidade 3: Serialização
  serializeData(data: any): string {
    // Conversão para JSON
    // Formatação
    // Tratamento de erro
  }
  
  deserializeData(json: string): any {
    // Parsing de JSON
    // Validação
    // Tratamento de erro
  }
  
  // Responsabilidade 4: Cache
  getDataFromCache(key: string): any {
    // Verificação de cache
    // Retorno de dados
  }
  
  setDataInCache(key: string, data: any): void {
    // Armazenamento em cache
    // Configuração de TTL
  }
}
```

### Problemas Identificados

#### 1. Responsabilidades de Diferentes Abstrações
- **Abstração de domínio**: Processamento de dados
- **Abstração de persistência**: Persistência de dados
- **Abstração de serialização**: Serialização de dados
- **Abstração de cache**: Cache de dados

#### 2. Violação de Separação de Responsabilidades
- **Responsabilidades misturadas**: Diferentes abstrações em uma classe
- **Dependências incorretas**: Abstrações acopladas
- **Testabilidade**: Dificulta testes de abstração específica

#### 3. Problemas de Evolução
- **Mudanças em cascata**: Alterações afetam múltiplas abstrações
- **Código duplicado**: Lógica similar em diferentes abstrações
- **Reutilização**: Lógica não pode ser reutilizada

## 6. Detecção de Violações

### 1. Análise de Motivos para Mudança
```typescript
// ❌ Múltiplos motivos para mudança
class UserService {
  // Motivo 1: Lógica de usuário mudou
  createUser(): void { }
  
  // Motivo 2: Lógica de email mudou
  sendEmail(): void { }
  
  // Motivo 3: Lógica de log mudou
  logActivity(): void { }
  
  // Motivo 4: Lógica de relatório mudou
  generateReport(): void { }
}
```

### 2. Análise de Coesão
```typescript
// ❌ Baixa coesão - métodos não relacionados
class OrderService {
  createOrder(): void { }
  sendEmail(): void { }
  logActivity(): void { }
  generateReport(): void { }
}
```

### 3. Análise de Acoplamento
```typescript
// ❌ Alto acoplamento - muitas dependências
class OrderService {
  constructor(
    private userRepo: UserRepository,
    private productRepo: ProductRepository,
    private paymentService: PaymentService,
    private emailService: EmailService,
    private logService: LogService,
    private reportService: ReportService
  ) {}
}
```

## 7. Impactos das Violações

### 1. Problemas de Manutenibilidade
- **Mudanças em cascata**: Alterações afetam múltiplas áreas
- **Código duplicado**: Lógica similar em diferentes métodos
- **Dificuldade de evolução**: Novas funcionalidades complexas

### 2. Problemas de Testabilidade
- **Testes complexos**: Muitas dependências para testar
- **Mocks complexos**: Muitas interfaces para mockar
- **Testes frágeis**: Mudanças quebram testes não relacionados

### 3. Problemas de Reutilização
- **Código duplicado**: Lógica não pode ser reutilizada
- **Acoplamento alto**: Dependências entre responsabilidades
- **Flexibilidade**: Dificulta mudanças e extensões

## 8. Prevenção de Violações

### 1. Análise de Responsabilidades
- **Identificar responsabilidades**: Separar diferentes aspectos
- **Uma responsabilidade por classe**: Cada classe tem um propósito
- **Coesão alta**: Métodos relacionados agrupados

### 2. Design de Classes
- **Classes pequenas**: Fáceis de entender e manter
- **Métodos relacionados**: Agrupar funcionalidades similares
- **Responsabilidade única**: Apenas um motivo para mudar

### 3. Composição de Objetos
- **Composição ao invés de herança**: Preferir composição
- **Injeção de dependências**: Dependências externas
- **Interfaces bem definidas**: Contratos claros

## 9. Conclusão

As violações do SRP são comuns e podem causar sérios problemas de manutenibilidade. É importante identificar e corrigir essas violações para criar sistemas mais robustos e maintíveis.

### Pontos-Chave
- **Uma responsabilidade**: Cada classe tem um propósito específico
- **Um motivo para mudar**: Facilita manutenção e evolução
- **Coesão alta**: Métodos relacionados agrupados
- **Baixo acoplamento**: Dependências mínimas

### Próximos Passos
- [Aplicar refatoração](./srp-refactoring.md)
- [Implementar composição](./srp-composition.md)
- [Aplicar boas práticas](./srp-best-practices.md)

---

**Última atualização**: 04/10/2025  
**Versão**: 1.0
