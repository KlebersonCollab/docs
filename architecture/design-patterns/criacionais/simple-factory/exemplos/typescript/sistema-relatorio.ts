/**
 * Exemplo do Padrão Simple Factory - Sistema de Relatórios
 * 
 * Este exemplo demonstra como implementar o padrão Simple Factory para criar
 * diferentes tipos de geradores de relatórios (PDF, Excel, CSV, JSON) de forma
 * centralizada e reutilizável.
 */

// Enums para tipos e status
enum ReportType {
  PDF = 'pdf',
  EXCEL = 'excel',
  CSV = 'csv',
  JSON = 'json'
}

enum ReportStatus {
  PENDING = 'pending',
  GENERATING = 'generating',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

// Interfaces
interface ReportData {
  title: string;
  data: any[];
  columns: string[];
  metadata?: Record<string, any>;
}

interface ReportResult {
  status: ReportStatus;
  filename: string;
  size: number;
  downloadUrl?: string;
  error?: string;
}

// Interface para geradores de relatório
interface ReportGenerator {
  generate(data: ReportData): Promise<ReportResult>;
  getType(): ReportType;
  getSupportedFormats(): string[];
  getMaxSize(): number;
}

// Implementação concreta: PDF
class PDFReportGenerator implements ReportGenerator {
  private readonly type = ReportType.PDF;
  private readonly maxSize = 10 * 1024 * 1024; // 10MB

  async generate(data: ReportData): Promise<ReportResult> {
    console.log(`📄 Gerando relatório PDF: ${data.title}`);
    console.log(`📊 Dados: ${data.data.length} registros`);
    
    // Simular geração de PDF
    await this.simulatePDFGeneration(data);
    
    const filename = `${data.title.replace(/\s+/g, '_')}_${Date.now()}.pdf`;
    const size = Math.floor(Math.random() * 1024 * 1024) + 100000; // 100KB - 1MB
    
    return {
      status: ReportStatus.COMPLETED,
      filename,
      size,
      downloadUrl: `/reports/download/${filename}`
    };
  }

  getType(): ReportType {
    return this.type;
  }

  getSupportedFormats(): string[] {
    return ['A4', 'A3', 'Letter'];
  }

  getMaxSize(): number {
    return this.maxSize;
  }

  private async simulatePDFGeneration(data: ReportData): Promise<void> {
    // Simular delay de geração
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Simular falha ocasional (5% de chance)
    if (Math.random() < 0.05) {
      throw new Error('Erro na geração do PDF');
    }
  }
}

// Implementação concreta: Excel
class ExcelReportGenerator implements ReportGenerator {
  private readonly type = ReportType.EXCEL;
  private readonly maxSize = 50 * 1024 * 1024; // 50MB

  async generate(data: ReportData): Promise<ReportResult> {
    console.log(`📊 Gerando relatório Excel: ${data.title}`);
    console.log(`📊 Dados: ${data.data.length} registros`);
    
    // Simular geração de Excel
    await this.simulateExcelGeneration(data);
    
    const filename = `${data.title.replace(/\s+/g, '_')}_${Date.now()}.xlsx`;
    const size = Math.floor(Math.random() * 2 * 1024 * 1024) + 50000; // 50KB - 2MB
    
    return {
      status: ReportStatus.COMPLETED,
      filename,
      size,
      downloadUrl: `/reports/download/${filename}`
    };
  }

  getType(): ReportType {
    return this.type;
  }

  getSupportedFormats(): string[] {
    return ['XLSX', 'XLS'];
  }

  getMaxSize(): number {
    return this.maxSize;
  }

  private async simulateExcelGeneration(data: ReportData): Promise<void> {
    // Simular delay de geração
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Simular falha ocasional (3% de chance)
    if (Math.random() < 0.03) {
      throw new Error('Erro na geração do Excel');
    }
  }
}

// Implementação concreta: CSV
class CSVReportGenerator implements ReportGenerator {
  private readonly type = ReportType.CSV;
  private readonly maxSize = 100 * 1024 * 1024; // 100MB

  async generate(data: ReportData): Promise<ReportResult> {
    console.log(`📋 Gerando relatório CSV: ${data.title}`);
    console.log(`📊 Dados: ${data.data.length} registros`);
    
    // Simular geração de CSV
    await this.simulateCSVGeneration(data);
    
    const filename = `${data.title.replace(/\s+/g, '_')}_${Date.now()}.csv`;
    const size = Math.floor(Math.random() * 1024 * 1024) + 10000; // 10KB - 1MB
    
    return {
      status: ReportStatus.COMPLETED,
      filename,
      size,
      downloadUrl: `/reports/download/${filename}`
    };
  }

  getType(): ReportType {
    return this.type;
  }

  getSupportedFormats(): string[] {
    return ['UTF-8', 'ISO-8859-1'];
  }

  getMaxSize(): number {
    return this.maxSize;
  }

  private async simulateCSVGeneration(data: ReportData): Promise<void> {
    // Simular delay de geração
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Simular falha ocasional (2% de chance)
    if (Math.random() < 0.02) {
      throw new Error('Erro na geração do CSV');
    }
  }
}

// Implementação concreta: JSON
class JSONReportGenerator implements ReportGenerator {
  private readonly type = ReportType.JSON;
  private readonly maxSize = 200 * 1024 * 1024; // 200MB

  async generate(data: ReportData): Promise<ReportResult> {
    console.log(`📄 Gerando relatório JSON: ${data.title}`);
    console.log(`📊 Dados: ${data.data.length} registros`);
    
    // Simular geração de JSON
    await this.simulateJSONGeneration(data);
    
    const filename = `${data.title.replace(/\s+/g, '_')}_${Date.now()}.json`;
    const size = Math.floor(Math.random() * 512 * 1024) + 5000; // 5KB - 512KB
    
    return {
      status: ReportStatus.COMPLETED,
      filename,
      size,
      downloadUrl: `/reports/download/${filename}`
    };
  }

  getType(): ReportType {
    return this.type;
  }

  getSupportedFormats(): string[] {
    return ['JSON', 'JSONL'];
  }

  getMaxSize(): number {
    return this.maxSize;
  }

  private async simulateJSONGeneration(data: ReportData): Promise<void> {
    // Simular delay de geração
    await new Promise(resolve => setTimeout(resolve, 200));
    
    // Simular falha ocasional (1% de chance)
    if (Math.random() < 0.01) {
      throw new Error('Erro na geração do JSON');
    }
  }
}

// Simple Factory para criar geradores de relatório
class ReportGeneratorFactory {
  /**
   * Cria um gerador de relatório baseado no tipo
   */
  public static create(type: ReportType): ReportGenerator {
    const generators = {
      [ReportType.PDF]: PDFReportGenerator,
      [ReportType.EXCEL]: ExcelReportGenerator,
      [ReportType.CSV]: CSVReportGenerator,
      [ReportType.JSON]: JSONReportGenerator
    };

    const GeneratorClass = generators[type];
    if (!GeneratorClass) {
      throw new Error(`Tipo de relatório '${type}' não suportado`);
    }

    return new GeneratorClass();
  }

  /**
   * Retorna lista de tipos suportados
   */
  public static getSupportedTypes(): ReportType[] {
    return Object.values(ReportType);
  }

  /**
   * Verifica se um tipo é suportado
   */
  public static isSupported(type: ReportType): boolean {
    return Object.values(ReportType).includes(type);
  }
}

// Serviço de relatórios que usa a Factory
class ReportService {
  private factory: typeof ReportGeneratorFactory;

  constructor() {
    this.factory = ReportGeneratorFactory;
  }

  /**
   * Gera relatório usando a Factory
   */
  public async generateReport(type: ReportType, data: ReportData): Promise<ReportResult> {
    try {
      // Validar tipo antes de criar
      if (!this.factory.isSupported(type)) {
        return {
          status: ReportStatus.FAILED,
          filename: '',
          size: 0,
          error: `Tipo '${type}' não suportado`
        };
      }

      // Criar gerador usando Factory
      const generator = this.factory.create(type);

      // Gerar relatório
      const result = await generator.generate(data);

      return result;

    } catch (error) {
      return {
        status: ReportStatus.FAILED,
        filename: '',
        size: 0,
        error: error instanceof Error ? error.message : 'Erro desconhecido'
      };
    }
  }

  /**
   * Retorna informações sobre um tipo de relatório
   */
  public getReportInfo(type: ReportType): { type: ReportType; maxSize: number; formats: string[] } | null {
    try {
      const generator = this.factory.create(type);
      return {
        type: generator.getType(),
        maxSize: generator.getMaxSize(),
        formats: generator.getSupportedFormats()
      };
    } catch (error) {
      return null;
    }
  }
}

// Exemplo de uso
async function demonstrateReportFactory(): Promise<void> {
  console.log('=== Demonstração do Padrão Simple Factory para Relatórios ===\n');

  const service = new ReportService();

  // Dados de exemplo
  const sampleData: ReportData = {
    title: 'Relatório de Vendas',
    data: [
      { id: 1, produto: 'Produto A', valor: 100.00, data: '2024-01-01' },
      { id: 2, produto: 'Produto B', valor: 200.00, data: '2024-01-02' },
      { id: 3, produto: 'Produto C', valor: 300.00, data: '2024-01-03' }
    ],
    columns: ['id', 'produto', 'valor', 'data'],
    metadata: {
      generatedAt: new Date().toISOString(),
      totalRecords: 3,
      totalValue: 600.00
    }
  };

  // Casos de teste
  const testCases = [
    { type: ReportType.PDF, description: 'Relatório em PDF' },
    { type: ReportType.EXCEL, description: 'Planilha Excel' },
    { type: ReportType.CSV, description: 'Arquivo CSV' },
    { type: ReportType.JSON, description: 'Dados JSON' }
  ];

  for (const testCase of testCases) {
    console.log(`--- ${testCase.description} ---`);
    
    const result = await service.generateReport(testCase.type, sampleData);
    
    if (result.status === ReportStatus.COMPLETED) {
      console.log(`✅ Status: ${result.status}`);
      console.log(`📄 Arquivo: ${result.filename}`);
      console.log(`📊 Tamanho: ${(result.size / 1024).toFixed(2)} KB`);
      console.log(`🔗 Download: ${result.downloadUrl}`);
    } else {
      console.log(`❌ Status: ${result.status}`);
      console.log(`💥 Erro: ${result.error}`);
    }
    
    console.log();
  }
}

// Demonstração de informações dos geradores
function demonstrateGeneratorInfo(): void {
  console.log('=== Informações dos Geradores ===\n');

  const service = new ReportService();

  for (const type of ReportGeneratorFactory.getSupportedTypes()) {
    console.log(`--- ${type.toUpperCase()} ---`);
    
    const info = service.getReportInfo(type);
    
    if (info) {
      console.log(`📊 Tipo: ${info.type}`);
      console.log(`📏 Tamanho máximo: ${(info.maxSize / 1024 / 1024).toFixed(1)} MB`);
      console.log(`📋 Formatos: ${info.formats.join(', ')}`);
    } else {
      console.log('❌ Informações não disponíveis');
    }
    
    console.log();
  }
}

// Demonstração de flexibilidade
function demonstrateFlexibility(): void {
  console.log('=== Demonstração de Flexibilidade ===\n');

  console.log('Tipos de relatório suportados:');
  for (const type of ReportGeneratorFactory.getSupportedTypes()) {
    console.log(`- ${type}`);
  }

  console.log(`\nTotal de tipos: ${ReportGeneratorFactory.getSupportedTypes().length}`);

  console.log('\nVerificações de suporte:');
  const testTypes = [ReportType.PDF, ReportType.EXCEL, ReportType.CSV, ReportType.JSON];
  
  for (const type of testTypes) {
    const supported = ReportGeneratorFactory.isSupported(type);
    const status = supported ? '✅' : '❌';
    console.log(`${status} ${type}: ${supported ? 'Suportado' : 'Não suportado'}`);
  }
}

// Executar demonstrações
if (require.main === module) {
  demonstrateReportFactory()
    .then(() => {
      console.log('\n' + '='.repeat(50) + '\n');
      demonstrateGeneratorInfo();
      console.log('\n' + '='.repeat(50) + '\n');
      demonstrateFlexibility();
    })
    .catch(console.error);
}

export {
  ReportType,
  ReportStatus,
  ReportData,
  ReportResult,
  ReportGenerator,
  PDFReportGenerator,
  ExcelReportGenerator,
  CSVReportGenerator,
  JSONReportGenerator,
  ReportGeneratorFactory,
  ReportService
};




