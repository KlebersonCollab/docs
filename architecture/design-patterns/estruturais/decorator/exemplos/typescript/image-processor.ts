/**
 * Exemplo prático do padrão Decorator em TypeScript
 * Sistema de processamento de imagens com funcionalidades modulares
 */

// Interface base para processamento de imagens
interface ImageProcessor {
  process(imagePath: string): string;
}

// Implementação concreta - Processamento básico
class BasicImageProcessor implements ImageProcessor {
  process(imagePath: string): string {
    console.log(`🔍 Processando imagem básica: ${imagePath}`);
    
    // Simulação de validação básica
    this.validateImage(imagePath);
    
    // Simulação de verificação de metadados
    this.checkMetadata(imagePath);
    
    const processedPath = `processed_${imagePath}`;
    console.log(`✅ Imagem processada: ${processedPath}`);
    
    return processedPath;
  }

  private validateImage(path: string): void {
    console.log(`   📋 Validando formato e integridade: ${path}`);
  }

  private checkMetadata(path: string): void {
    console.log(`   📊 Verificando metadados: ${path}`);
  }
}

// Decorator abstrato
abstract class ImageProcessorDecorator implements ImageProcessor {
  protected processor: ImageProcessor;

  constructor(processor: ImageProcessor) {
    this.processor = processor;
  }

  abstract process(imagePath: string): string;
}

// Decorador concreto - Marca d'água
class WatermarkDecorator extends ImageProcessorDecorator {
  private watermarkText: string;
  private position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';

  constructor(
    processor: ImageProcessor, 
    watermarkText: string, 
    position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' = 'bottom-right'
  ) {
    super(processor);
    this.watermarkText = watermarkText;
    this.position = position;
  }

  process(imagePath: string): string {
    console.log(`🎨 Aplicando marca d'água: "${this.watermarkText}"`);
    
    // Primeiro processa a imagem base
    const processedPath = this.processor.process(imagePath);
    
    // Depois adiciona a marca d'água
    const watermarkedPath = this.addWatermark(processedPath);
    
    console.log(`✅ Marca d'água aplicada: ${watermarkedPath}`);
    return watermarkedPath;
  }

  private addWatermark(imagePath: string): string {
    console.log(`   📍 Posição: ${this.position}`);
    console.log(`   🎯 Texto: ${this.watermarkText}`);
    return `watermarked_${imagePath}`;
  }
}

// Decorador concreto - Redimensionamento
class ResizeDecorator extends ImageProcessorDecorator {
  private width: number;
  private height: number;
  private maintainAspectRatio: boolean;

  constructor(
    processor: ImageProcessor, 
    width: number, 
    height: number, 
    maintainAspectRatio: boolean = true
  ) {
    super(processor);
    this.width = width;
    this.height = height;
    this.maintainAspectRatio = maintainAspectRatio;
  }

  process(imagePath: string): string {
    console.log(`📏 Redimensionando imagem para ${this.width}x${this.height}`);
    
    // Primeiro processa a imagem base
    const processedPath = this.processor.process(imagePath);
    
    // Depois redimensiona
    const resizedPath = this.resizeImage(processedPath);
    
    console.log(`✅ Imagem redimensionada: ${resizedPath}`);
    return resizedPath;
  }

  private resizeImage(imagePath: string): string {
    console.log(`   📐 Dimensões: ${this.width}x${this.height}`);
    console.log(`   🔄 Manter proporção: ${this.maintainAspectRatio}`);
    return `resized_${imagePath}`;
  }
}

// Decorador concreto - Filtros
class FilterDecorator extends ImageProcessorDecorator {
  private filterType: 'blur' | 'sharpen' | 'grayscale' | 'sepia';
  private intensity: number;

  constructor(
    processor: ImageProcessor, 
    filterType: 'blur' | 'sharpen' | 'grayscale' | 'sepia', 
    intensity: number = 1.0
  ) {
    super(processor);
    this.filterType = filterType;
    this.intensity = Math.max(0, Math.min(1, intensity)); // Clamp entre 0 e 1
  }

  process(imagePath: string): string {
    console.log(`🎭 Aplicando filtro: ${this.filterType} (intensidade: ${this.intensity})`);
    
    // Primeiro processa a imagem base
    const processedPath = this.processor.process(imagePath);
    
    // Depois aplica o filtro
    const filteredPath = this.applyFilter(processedPath);
    
    console.log(`✅ Filtro aplicado: ${filteredPath}`);
    return filteredPath;
  }

  private applyFilter(imagePath: string): string {
    console.log(`   🎨 Tipo: ${this.filterType}`);
    console.log(`   💪 Intensidade: ${this.intensity}`);
    return `filtered_${imagePath}`;
  }
}

// Decorador concreto - Compressão
class CompressionDecorator extends ImageProcessorDecorator {
  private quality: number;
  private format: 'jpeg' | 'png' | 'webp';

  constructor(
    processor: ImageProcessor, 
    quality: number = 0.8, 
    format: 'jpeg' | 'png' | 'webp' = 'jpeg'
  ) {
    super(processor);
    this.quality = Math.max(0, Math.min(1, quality)); // Clamp entre 0 e 1
    this.format = format;
  }

  process(imagePath: string): string {
    console.log(`🗜️ Comprimindo imagem (qualidade: ${this.quality}, formato: ${this.format})`);
    
    // Primeiro processa a imagem base
    const processedPath = this.processor.process(imagePath);
    
    // Depois comprime
    const compressedPath = this.compressImage(processedPath);
    
    console.log(`✅ Imagem comprimida: ${compressedPath}`);
    return compressedPath;
  }

  private compressImage(imagePath: string): string {
    console.log(`   📊 Qualidade: ${this.quality}`);
    console.log(`   📁 Formato: ${this.format}`);
    return `compressed_${imagePath}`;
  }
}

// Exemplo de uso
function demonstrateDecoratorPattern(): void {
  console.log('🚀 Demonstração do Padrão Decorator\n');

  // Cenário 1: Processamento básico apenas
  console.log('📸 Cenário 1: Processamento básico');
  let processor: ImageProcessor = new BasicImageProcessor();
  let result = processor.process('foto.jpg');
  console.log(`Resultado: ${result}\n`);

  // Cenário 2: Adicionando marca d'água
  console.log('📸 Cenário 2: Com marca d\'água');
  processor = new WatermarkDecorator(processor, 'Minha Empresa', 'bottom-right');
  result = processor.process('foto.jpg');
  console.log(`Resultado: ${result}\n`);

  // Cenário 3: Adicionando redimensionamento
  console.log('📸 Cenário 3: Com redimensionamento');
  processor = new ResizeDecorator(processor, 800, 600, true);
  result = processor.process('foto.jpg');
  console.log(`Resultado: ${result}\n`);

  // Cenário 4: Adicionando filtro
  console.log('📸 Cenário 4: Com filtro');
  processor = new FilterDecorator(processor, 'sepia', 0.7);
  result = processor.process('foto.jpg');
  console.log(`Resultado: ${result}\n`);

  // Cenário 5: Adicionando compressão
  console.log('📸 Cenário 5: Com compressão');
  processor = new CompressionDecorator(processor, 0.9, 'jpeg');
  result = processor.process('foto.jpg');
  console.log(`Resultado: ${result}\n`);

  // Cenário 6: Ordem diferente dos decoradores
  console.log('📸 Cenário 6: Ordem diferente');
  let processor2: ImageProcessor = new BasicImageProcessor();
  processor2 = new CompressionDecorator(processor2, 0.8, 'webp');
  processor2 = new FilterDecorator(processor2, 'grayscale', 1.0);
  processor2 = new ResizeDecorator(processor2, 400, 300, true);
  processor2 = new WatermarkDecorator(processor2, 'Copyright 2024', 'top-left');
  
  result = processor2.process('foto.jpg');
  console.log(`Resultado: ${result}\n`);
}

// Para execução em ambiente Node.js, verifique se 'require' e 'module' existem
declare const require: any;
declare const module: any;

if (typeof require !== 'undefined' && typeof module !== 'undefined' && require.main === module) {
  demonstrateDecoratorPattern();
}

export {
  ImageProcessor,
  BasicImageProcessor,
  ImageProcessorDecorator,
  WatermarkDecorator,
  ResizeDecorator,
  FilterDecorator,
  CompressionDecorator
};

