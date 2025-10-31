# Guia de Implementação - Padrão Adapter

## 🎯 Visão Geral

Este guia fornece um roteiro completo para implementar o padrão Adapter em seus projetos, desde a identificação da necessidade até a implementação e testes.

## 📋 Checklist de Implementação

### ✅ Fase 1: Análise e Planejamento

#### 1.1 Identificar a Necessidade
- [ ] Interfaces incompatíveis
- [ ] Integração com bibliotecas externas
- [ ] Sistemas legados
- [ ] Necessidade de flexibilidade

#### 1.2 Mapear Interfaces
- [ ] Identificar interface desejada (Target)
- [ ] Analisar interface existente (Adaptee)
- [ ] Documentar incompatibilidades
- [ ] Definir contrato de adaptação

#### 1.3 Avaliar Complexidade
- [ ] Quantas interfaces precisam ser adaptadas?
- [ ] Qual a complexidade da adaptação?
- [ ] Vale a pena a complexidade adicional?
- [ ] Existem alternativas mais simples?

### ✅ Fase 2: Design da Arquitetura

#### 2.1 Definir Interface Target
```php
interface PdfAdapter {
    public function generate(string $filename, string $content): void;
    public function setPageSize(string $size): void;
    public function setOrientation(string $orientation): void;
}
```

#### 2.2 Criar Adapters
```php
class DomPdfAdapter implements PdfAdapter {
    private Dompdf $dompdf;
    
    public function __construct() {
        $this->dompdf = new Dompdf();
    }
    
    public function generate(string $filename, string $content): void {
        // Implementação específica do DomPDF
    }
}
```

#### 2.3 Implementar Cliente
```php
class SalesReportGenerator {
    private PdfAdapter $pdfAdapter;
    
    public function __construct(PdfAdapter $pdfAdapter) {
        $this->pdfAdapter = $pdfAdapter;
    }
    
    public function generate(): void {
        // Usa o adapter sem conhecer implementação específica
    }
}
```

### ✅ Fase 3: Implementação

#### 3.1 Estrutura de Arquivos
```
src/
├── Adapter/
│   ├── PdfAdapter.php           # Interface Target
│   ├── DomPdfAdapter.php        # Adapter para DomPDF
│   ├── TcpdfAdapter.php         # Adapter para TCPDF
│   └── MPdfAdapter.php          # Adapter para mPDF
├── SalesReportGenerator.php     # Cliente
└── command.php                  # Código cliente
```

#### 3.2 Implementação Passo a Passo

**Passo 1: Criar Interface Target**
```php
<?php

interface PdfAdapter {
    public function generate(string $filename, string $content): void;
    public function setPageSize(string $size): void;
    public function setOrientation(string $orientation): void;
}
```

**Passo 2: Implementar Adapter**
```php
<?php

class DomPdfAdapter implements PdfAdapter {
    private Dompdf $dompdf;
    
    public function __construct() {
        $this->dompdf = new Dompdf();
    }
    
    public function generate(string $filename, string $content): void {
        $this->dompdf->loadHtml($content);
        $this->dompdf->setPaper('A4', 'landscape');
        $this->dompdf->render();
        file_put_contents($filename, $this->dompdf->output());
    }
    
    public function setPageSize(string $size): void {
        $this->dompdf->setPaper($size, 'portrait');
    }
    
    public function setOrientation(string $orientation): void {
        $this->dompdf->setPaper('A4', $orientation);
    }
}
```

**Passo 3: Implementar Cliente**
```php
<?php

class SalesReportGenerator {
    private PdfAdapter $pdfAdapter;
    
    public function __construct(PdfAdapter $pdfAdapter) {
        $this->pdfAdapter = $pdfAdapter;
    }
    
    public function generate(): void {
        $filename = 'relatorio_' . time() . '.pdf';
        $content = '<h1>Relatório de Vendas</h1><p>Conteúdo...</p>';
        
        $this->pdfAdapter->generate($filename, $content);
    }
}
```

**Passo 4: Código Cliente**
```php
<?php

// Usando DomPDF
$domPdfAdapter = new DomPdfAdapter();
$generator = new SalesReportGenerator($domPdfAdapter);
$generator->generate();

// Usando TCPDF
$tcpdfAdapter = new TcpdfAdapter();
$generator = new SalesReportGenerator($tcpdfAdapter);
$generator->generate();
```

### ✅ Fase 4: Testes

#### 4.1 Testes Unitários
```php
<?php

class DomPdfAdapterTest extends PHPUnit\Framework\TestCase {
    public function testGeneratePdf() {
        $adapter = new DomPdfAdapter();
        $filename = 'test.pdf';
        $content = '<h1>Test</h1>';
        
        $adapter->generate($filename, $content);
        
        $this->assertFileExists($filename);
        unlink($filename);
    }
    
    public function testSetPageSize() {
        $adapter = new DomPdfAdapter();
        $adapter->setPageSize('A4');
        
        // Verificar se a configuração foi aplicada
        $this->assertTrue(true); // Implementar verificação específica
    }
}
```

#### 4.2 Testes de Integração
```php
<?php

class SalesReportGeneratorTest extends PHPUnit\Framework\TestCase {
    public function testGenerateReportWithDomPdf() {
        $adapter = new DomPdfAdapter();
        $generator = new SalesReportGenerator($adapter);
        
        $generator->generate();
        
        $this->assertTrue(true); // Verificar se o relatório foi gerado
    }
    
    public function testGenerateReportWithTcpdf() {
        $adapter = new TcpdfAdapter();
        $generator = new SalesReportGenerator($adapter);
        
        $generator->generate();
        
        $this->assertTrue(true); // Verificar se o relatório foi gerado
    }
}
```

#### 4.3 Testes com Mock
```php
<?php

class SalesReportGeneratorMockTest extends PHPUnit\Framework\TestCase {
    public function testGenerateReportWithMock() {
        $mockAdapter = $this->createMock(PdfAdapter::class);
        $mockAdapter->expects($this->once())
                   ->method('generate')
                   ->with($this->stringContains('relatorio_'), $this->stringContains('<h1>'));
        
        $generator = new SalesReportGenerator($mockAdapter);
        $generator->generate();
    }
}
```

## 🎯 Boas Práticas

### 1. **Nomenclatura Clara**

#### ✅ BOM
```php
class DomPdfAdapter implements PdfAdapter
class TcpdfAdapter implements PdfAdapter
class StripePaymentAdapter implements PaymentAdapter
```

#### ❌ RUIM
```php
class Adapter1 implements PdfAdapter
class Adapter2 implements PdfAdapter
class Adapter3 implements PaymentAdapter
```

### 2. **Interface Bem Definida**

#### ✅ BOM
```php
interface PdfAdapter {
    public function generate(string $filename, string $content): void;
    public function setPageSize(string $size): void;
    public function setOrientation(string $orientation): void;
}
```

#### ❌ RUIM
```php
interface Adapter {
    public function doSomething($data): void;
}
```

### 3. **Tratamento de Erros**

#### ✅ BOM
```php
public function generate(string $filename, string $content): void {
    try {
        $this->dompdf->loadHtml($content);
        $this->dompdf->render();
        file_put_contents($filename, $this->dompdf->output());
    } catch (Exception $e) {
        throw new PdfGenerationException("Erro ao gerar PDF: " . $e->getMessage());
    }
}
```

#### ❌ RUIM
```php
public function generate(string $filename, string $content): void {
    $this->dompdf->loadHtml($content);
    $this->dompdf->render();
    file_put_contents($filename, $this->dompdf->output());
}
```

### 4. **Documentação Clara**

#### ✅ BOM
```php
/**
 * Adapter para biblioteca DomPDF
 * 
 * Converte a interface da biblioteca DomPDF para
 * a interface padrão PdfAdapter
 * 
 * @package Adapter
 * @author Seu Nome
 * @version 1.0
 */
class DomPdfAdapter implements PdfAdapter {
    // Implementação...
}
```

### 5. **Configuração Flexível**

#### ✅ BOM
```php
class ConfigurablePdfAdapter implements PdfAdapter {
    private array $config;
    
    public function __construct(array $config = []) {
        $this->config = array_merge([
            'page_size' => 'A4',
            'orientation' => 'portrait',
            'font' => 'helvetica'
        ], $config);
    }
}
```

## 🚀 Extensões Avançadas

### 1. **Adapter com Cache**
```php
class CachedPdfAdapter implements PdfAdapter {
    private PdfAdapter $adapter;
    private CacheInterface $cache;
    
    public function generate(string $filename, string $content): void {
        $cacheKey = md5($content);
        
        if ($this->cache->has($cacheKey)) {
            $this->cache->get($cacheKey);
            return;
        }
        
        $this->adapter->generate($filename, $content);
        $this->cache->set($cacheKey, $filename);
    }
}
```

### 2. **Adapter com Logging**
```php
class LoggedPdfAdapter implements PdfAdapter {
    private PdfAdapter $adapter;
    private LoggerInterface $logger;
    
    public function generate(string $filename, string $content): void {
        $this->logger->info("Gerando PDF: {$filename}");
        
        $startTime = microtime(true);
        $this->adapter->generate($filename, $content);
        $duration = microtime(true) - $startTime;
        
        $this->logger->info("PDF gerado em {$duration}s");
    }
}
```

### 3. **Adapter com Validação**
```php
class ValidatedPdfAdapter implements PdfAdapter {
    private PdfAdapter $adapter;
    private ValidatorInterface $validator;
    
    public function generate(string $filename, string $content): void {
        if (!$this->validator->validate($content)) {
            throw new ValidationException("Conteúdo inválido para PDF");
        }
        
        $this->adapter->generate($filename, $content);
    }
}
```

### 4. **Adapter Factory**
```php
class PdfAdapterFactory {
    public function create(string $type, array $config = []): PdfAdapter {
        switch ($type) {
            case 'dompdf':
                return new DomPdfAdapter();
            case 'tcpdf':
                return new TcpdfAdapter();
            case 'mpdf':
                return new MPdfAdapter();
            default:
                throw new InvalidArgumentException("Tipo de adapter inválido: {$type}");
        }
    }
}
```

## 🔧 Ferramentas e Bibliotecas

### 1. **PHP**
- **Composer**: Gerenciamento de dependências
- **PHPUnit**: Testes unitários
- **Mockery**: Mocking de objetos
- **PSR-4**: Autoloading de classes

### 2. **Python**
- **pytest**: Testes unitários
- **unittest.mock**: Mocking de objetos
- **typing**: Type hints
- **abc**: Abstract base classes

### 3. **TypeScript**
- **Jest**: Testes unitários
- **ts-mockito**: Mocking de objetos
- **typescript**: Compilação
- **eslint**: Linting

### 4. **Java**
- **JUnit**: Testes unitários
- **Mockito**: Mocking de objetos
- **Spring**: Framework
- **Maven/Gradle**: Build tools

## 📊 Métricas e Monitoramento

### 1. **Métricas Importantes**

```php
class AdapterMetrics {
    private array $metrics = [];
    
    public function recordOperation(string $adapter, string $operation, float $duration): void {
        $key = "{$adapter}_{$operation}";
        $this->metrics[$key] = [
            'count' => ($this->metrics[$key]['count'] ?? 0) + 1,
            'total_duration' => ($this->metrics[$key]['total_duration'] ?? 0) + $duration,
            'avg_duration' => 0
        ];
        
        $this->metrics[$key]['avg_duration'] = 
            $this->metrics[$key]['total_duration'] / $this->metrics[$key]['count'];
    }
    
    public function getMetrics(): array {
        return $this->metrics;
    }
}
```

### 2. **Logging de Operações**

```php
class LoggedAdapter implements PdfAdapter {
    private PdfAdapter $adapter;
    private LoggerInterface $logger;
    private AdapterMetrics $metrics;
    
    public function generate(string $filename, string $content): void {
        $startTime = microtime(true);
        
        try {
            $this->adapter->generate($filename, $content);
            $this->logger->info("PDF gerado com sucesso: {$filename}");
        } catch (Exception $e) {
            $this->logger->error("Erro ao gerar PDF: {$e->getMessage()}");
            throw $e;
        } finally {
            $duration = microtime(true) - $startTime;
            $this->metrics->recordOperation('pdf', 'generate', $duration);
        }
    }
}
```

## ⚠️ Armadilhas Comuns

### 1. **Over-engineering**
- Não use o padrão Adapter para casos simples
- Avalie se a complexidade vale a pena
- Considere alternativas mais simples

### 2. **Interface Muito Genérica**
- Evite interfaces muito amplas
- Mantenha interfaces específicas e focadas
- Documente claramente o contrato

### 3. **Falta de Testes**
- Sempre teste os adapters
- Use mocks para testar o cliente
- Teste casos de erro e exceções

### 4. **Acoplamento com Implementação**
- Evite conhecer detalhes da implementação
- Mantenha o foco na interface
- Use injeção de dependência

### 5. **Falta de Documentação**
- Documente a interface claramente
- Explique o propósito de cada adapter
- Mantenha exemplos atualizados

## 🎯 Checklist de Qualidade

### ✅ Implementação
- [ ] Interface Target bem definida
- [ ] Adapters implementados corretamente
- [ ] Cliente desacoplado
- [ ] Tratamento de erros adequado

### ✅ Testes
- [ ] Testes unitários para cada adapter
- [ ] Testes de integração
- [ ] Testes com mocks
- [ ] Cobertura de código adequada

### ✅ Documentação
- [ ] Documentação da interface
- [ ] Exemplos de uso
- [ ] Guia de implementação
- [ ] Troubleshooting

### ✅ Monitoramento
- [ ] Logs de operações
- [ ] Métricas de performance
- [ ] Alertas de falhas
- [ ] Dashboard de monitoramento

## 🚀 Conclusão

O padrão Adapter é uma ferramenta poderosa para integrar sistemas incompatíveis, mas deve ser usado com cuidado. Siga este guia para implementações bem-sucedidas e mantenha sempre a qualidade do código.

### Quando Usar
- Interfaces incompatíveis
- Integração com bibliotecas externas
- Sistemas legados
- Necessidade de flexibilidade

### Quando NÃO Usar
- Interfaces já compatíveis
- Casos simples sem necessidade
- Quando a complexidade não justifica o padrão

---

**Última atualização**: $(date)
**Mantenedor**: Equipe Skynet
**Versão**: 1.0





