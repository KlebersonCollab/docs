# Violações de Pós-condições no Princípio da Substituição de Liskov

## Informações Básicas
- **ID do Documento**: LSP-002
- **Nome**: Violações de Pós-condições no LSP
- **Versão**: 1.0
- **Data de Criação**: 04/10/2025
- **Última Atualização**: 04/10/2025
- **Autor**: Sistema de Documentação Skynet
- **Aprovado por**: Governança CMMV-Hive

## Visão Geral

As violações de pós-condições no Princípio da Substituição de Liskov ocorrem quando uma subclasse retorna valores ou comportamentos diferentes do esperado pela classe base, mesmo respeitando a tipagem do contrato.

## O que são Pós-condições

### Definição
Pós-condições são condições que devem ser verdadeiras **após** a execução de um método. Elas definem:
- **Tipo de retorno**: O que o método deve retornar
- **Comportamento**: Como o retorno deve se comportar
- **Formato**: Em que formato os dados devem ser apresentados

### Características
- **Obrigatórias**: Devem ser cumpridas por todas as implementações
- **Consistentes**: Devem ser iguais em toda a hierarquia
- **Previsíveis**: O código cliente deve poder confiar nelas

## Exemplo Prático: Sistema de Relatórios

### Cenário
Um sistema que gera relatórios em diferentes formatos (CSV, PDF, S3) com uma interface comum.

### Interface Base
```typescript
interface ReportGenerator {
  generate(): string; // Retorna caminho do arquivo
}
```

### Implementações Corretas (Respeitando LSP)

#### CSV Report Generator
```typescript
class CsvReportGenerator implements ReportGenerator {
  generate(): string {
    // Lógica para gerar relatório CSV
    const fileName = `report-${this.generateUniqueId()}.csv`;
    const filePath = `./reports/${fileName}`;
    
    // Salva arquivo localmente
    this.saveFileLocally(filePath, csvData);
    
    return filePath; // Retorna caminho local
  }
}
```

#### PDF Report Generator
```typescript
class PdfReportGenerator implements ReportGenerator {
  generate(): string {
    // Lógica para gerar relatório PDF
    const fileName = `report-${this.generateUniqueId()}.pdf`;
    const filePath = `./reports/${fileName}`;
    
    // Salva arquivo localmente
    this.saveFileLocally(filePath, pdfData);
    
    return filePath; // Retorna caminho local
  }
}
```

### Implementação Problemática (Violando LSP)

#### S3 Report Generator
```typescript
class S3ReportGenerator implements ReportGenerator {
  generate(): string {
    // Lógica para gerar relatório
    const fileName = `report-${this.generateUniqueId()}.pdf`;
    
    // Salva no S3 (nuvem)
    const s3Url = this.uploadToS3(fileName, reportData);
    
    return s3Url; // ❌ Retorna URL, não caminho local
  }
}
```

## O Problema da Violação

### Código Cliente Afetado
```typescript
class ReportProcessor {
  processReport(generator: ReportGenerator) {
    const filePath = generator.generate();
    
    // ❌ Este código assume que filePath é um caminho local
    if (!this.fileExists(filePath)) {
      throw new Error('Arquivo não existe');
    }
    
    // ❌ Este código falhará com URLs do S3
    const fileContent = this.readFile(filePath);
    this.attachToEmail(fileContent);
  }
  
  private fileExists(path: string): boolean {
    // Verifica se arquivo existe no sistema de arquivos local
    return fs.existsSync(path);
  }
}
```

### Consequências da Violação

#### 1. Código Cliente Quebrado
- **Falha silenciosa**: `fileExists()` retorna `false` para URLs
- **Exceções inesperadas**: `readFile()` falha com URLs
- **Comportamento inconsistente**: Diferentes geradores funcionam diferentemente

#### 2. Perda do Polimorfismo
```typescript
// ❌ Código cliente precisa conhecer implementações específicas
if (generator instanceof S3ReportGenerator) {
  // Lógica específica para S3
  const url = generator.generate();
  this.downloadFromS3(url);
} else {
  // Lógica para arquivos locais
  const path = generator.generate();
  this.processLocalFile(path);
}
```

#### 3. Violação dos Princípios SOLID
- **SRP**: Classe cliente tem múltiplas responsabilidades
- **OCP**: Não pode ser estendida sem modificação
- **LSP**: Substituições não funcionam
- **ISP**: Interface não está bem segregada
- **DIP**: Depende de implementações concretas

## Soluções para Violações de Pós-condições

### Solução 1: Segregação de Interfaces

#### Interfaces Específicas
```typescript
interface LocalReportGenerator {
  generate(): string; // Caminho local
}

interface CloudReportGenerator {
  generate(): string; // URL ou identificador
}
```

#### Implementações Segregadas
```typescript
class CsvReportGenerator implements LocalReportGenerator {
  generate(): string {
    // Retorna caminho local
    return this.saveLocally();
  }
}

class S3ReportGenerator implements CloudReportGenerator {
  generate(): string {
    // Retorna URL
    return this.uploadToS3();
  }
}
```

#### Processadores Específicos
```typescript
class LocalReportProcessor {
  processReport(generator: LocalReportGenerator) {
    const filePath = generator.generate();
    // Lógica para arquivos locais
  }
}

class CloudReportProcessor {
  processReport(generator: CloudReportGenerator) {
    const url = generator.generate();
    // Lógica para arquivos na nuvem
  }
}
```

### Solução 2: Objeto de Resultado Padronizado

#### Interface de Resultado
```typescript
interface ReportResult {
  type: 'local' | 'cloud';
  path: string;
  metadata?: any;
}
```

#### Implementação Unificada
```typescript
class CsvReportGenerator implements ReportGenerator {
  generate(): ReportResult {
    const filePath = this.saveLocally();
    return {
      type: 'local',
      path: filePath
    };
  }
}

class S3ReportGenerator implements ReportGenerator {
  generate(): ReportResult {
    const url = this.uploadToS3();
    return {
      type: 'cloud',
      path: url,
      metadata: { bucket: 'reports', region: 'us-east-1' }
    };
  }
}
```

#### Processador Unificado
```typescript
class ReportProcessor {
  processReport(generator: ReportGenerator) {
    const result = generator.generate();
    
    if (result.type === 'local') {
      this.processLocalFile(result.path);
    } else {
      this.processCloudFile(result.path, result.metadata);
    }
  }
}
```

## Padrões para Evitar Violações

### 1. Design por Contrato
```typescript
interface ReportGenerator {
  /**
   * Gera um relatório e retorna o caminho para acessá-lo
   * @returns Caminho local do arquivo gerado
   * @throws Error se não conseguir gerar o relatório
   */
  generate(): string;
}
```

### 2. Testes de Contrato
```typescript
describe('ReportGenerator Contract', () => {
  const generators = [
    new CsvReportGenerator(),
    new PdfReportGenerator(),
    new S3ReportGenerator() // ❌ Falhará no teste
  ];
  
  generators.forEach(generator => {
    it('should return a valid file path', () => {
      const result = generator.generate();
      expect(typeof result).toBe('string');
      expect(result.length).toBeGreaterThan(0);
      // ❌ S3 falhará aqui se retornar URL
    });
  });
});
```

### 3. Validação de Pós-condições
```typescript
class ReportGeneratorValidator {
  validatePostCondition(generator: ReportGenerator): boolean {
    const result = generator.generate();
    
    // Verifica se é um caminho válido
    return this.isValidFilePath(result);
  }
  
  private isValidFilePath(path: string): boolean {
    // Verifica se é um caminho local válido
    return path.startsWith('./') || path.startsWith('/');
  }
}
```

## Detecção de Violações

### 1. Análise Estática
```typescript
// ❌ Padrão que indica violação
if (obj instanceof SpecificImplementation) {
  // Lógica específica
}
```

### 2. Testes de Substituição
```typescript
// ✅ Teste que deve passar para todas as implementações
function testSubstitution(generator: ReportGenerator) {
  const result = generator.generate();
  
  // Todas as implementações devem passar neste teste
  expect(this.canAccessFile(result)).toBe(true);
}
```

### 3. Métricas de Acoplamento
- **Alto acoplamento**: Muitas verificações `instanceof`
- **Baixa coesão**: Lógica específica espalhada
- **Fragilidade**: Mudanças quebram código cliente

## Boas Práticas

### 1. Documentação Clara
- Documente pós-condições explicitamente
- Use exemplos de retorno esperado
- Especifique formatos e comportamentos

### 2. Testes Abrangentes
- Teste todas as implementações com o mesmo código cliente
- Valide pós-condições em testes automatizados
- Use property-based testing para validar contratos

### 3. Refatoração Preventiva
- Identifique violações cedo
- Refatore hierarquias problemáticas
- Use composição quando herança não for apropriada

## Conclusão

As violações de pós-condições são um dos problemas mais comuns no LSP, pois são sutis e podem passar despercebidas durante o desenvolvimento. A chave é:

### Pontos-Chave
- **Consistência**: Todas as implementações devem retornar o mesmo tipo de dado
- **Comportamento**: O formato e significado do retorno devem ser iguais
- **Testes**: Valide substituições com testes automatizados
- **Documentação**: Especifique claramente o que cada método deve retornar

### Próximos Passos
- [Estudar violações de pré-condições](./liskov-pre-conditions.md)
- [Estudar violações de invariância](./liskov-invariants.md)
- [Aplicar boas práticas](./liskov-best-practices.md)

---

**Última atualização**: 04/10/2025  
**Versão**: 1.0
