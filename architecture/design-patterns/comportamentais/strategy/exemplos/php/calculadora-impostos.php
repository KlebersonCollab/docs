<?php

/**
 * Exemplo do Padrão Strategy - Sistema de Cálculo de Impostos
 * 
 * Este exemplo demonstra como implementar o padrão Strategy para calcular
 * diferentes tipos de impostos (ICMS, ISS, IPI) de forma flexível e
 * respeitando os princípios SOLID.
 */

// Interface da estratégia
interface TaxTypeInterface 
{
    public function calculate(float $amount): float;
    public function getTaxName(): string;
    public function getTaxRate(): float;
}

// Estratégia concreta: ICMS
class ICMSTax implements TaxTypeInterface 
{
    private const TAX_RATE = 0.04; // 4%
    
    public function calculate(float $amount): float 
    {
        return $amount * self::TAX_RATE;
    }
    
    public function getTaxName(): string 
    {
        return 'ICMS';
    }
    
    public function getTaxRate(): float 
    {
        return self::TAX_RATE;
    }
}

// Estratégia concreta: ISS
class ISSTax implements TaxTypeInterface 
{
    private const TAX_RATE = 0.11; // 11%
    
    public function calculate(float $amount): float 
    {
        return $amount * self::TAX_RATE;
    }
    
    public function getTaxName(): string 
    {
        return 'ISS';
    }
    
    public function getTaxRate(): float 
    {
        return self::TAX_RATE;
    }
}

// Estratégia concreta: IPI
class IPITax implements TaxTypeInterface 
{
    private const TAX_RATE = 0.15; // 15%
    
    public function calculate(float $amount): float 
    {
        return $amount * self::TAX_RATE;
    }
    
    public function getTaxName(): string 
    {
        return 'IPI';
    }
    
    public function getTaxRate(): float 
    {
        return self::TAX_RATE;
    }
}

// Estratégia concreta: IVA (exemplo de extensão)
class IVATax implements TaxTypeInterface 
{
    private const TAX_RATE = 0.28; // 28%
    
    public function calculate(float $amount): float 
    {
        return $amount * self::TAX_RATE;
    }
    
    public function getTaxName(): string 
    {
        return 'IVA';
    }
    
    public function getTaxRate(): float 
    {
        return self::TAX_RATE;
    }
}

// Contexto - Calculadora de Impostos
class TaxCalculator 
{
    private ?TaxTypeInterface $taxType = null;
    
    public function setTaxType(TaxTypeInterface $taxType): self 
    {
        $this->taxType = $taxType;
        return $this;
    }
    
    public function calculate(float $amount): float 
    {
        if ($this->taxType === null) {
            throw new InvalidArgumentException('Tipo de imposto não definido');
        }
        
        return $this->taxType->calculate($amount);
    }
    
    public function getTaxInfo(): array 
    {
        if ($this->taxType === null) {
            throw new InvalidArgumentException('Tipo de imposto não definido');
        }
        
        return [
            'name' => $this->taxType->getTaxName(),
            'rate' => $this->taxType->getTaxRate(),
            'rate_percentage' => $this->taxType->getTaxRate() * 100
        ];
    }
}

// Factory para criar estratégias (padrão Factory + Strategy)
class TaxTypeFactory 
{
    public static function create(string $taxType): TaxTypeInterface 
    {
        return match($taxType) {
            'ICMS' => new ICMSTax(),
            'ISS' => new ISSTax(),
            'IPI' => new IPITax(),
            'IVA' => new IVATax(),
            default => throw new InvalidArgumentException("Tipo de imposto '{$taxType}' não suportado")
        };
    }
    
    public static function getAvailableTaxTypes(): array 
    {
        return ['ICMS', 'ISS', 'IPI', 'IVA'];
    }
}

// Controller (exemplo de uso)
class TaxController 
{
    private TaxCalculator $taxCalculator;
    
    public function __construct(TaxCalculator $taxCalculator) 
    {
        $this->taxCalculator = $taxCalculator;
    }
    
    public function calculateTax(string $taxType, float $amount): array 
    {
        try {
            // Criar estratégia usando Factory
            $strategy = TaxTypeFactory::create($taxType);
            
            // Configurar estratégia no contexto
            $this->taxCalculator->setTaxType($strategy);
            
            // Calcular imposto
            $taxAmount = $this->taxCalculator->calculate($amount);
            
            // Obter informações do imposto
            $taxInfo = $this->taxCalculator->getTaxInfo();
            
            return [
                'success' => true,
                'data' => [
                    'tax_type' => $taxInfo['name'],
                    'tax_rate' => $taxInfo['rate_percentage'] . '%',
                    'amount' => $amount,
                    'tax_amount' => $taxAmount,
                    'total' => $amount + $taxAmount
                ]
            ];
            
        } catch (InvalidArgumentException $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }
}

// Exemplo de uso
function demonstrateStrategyPattern(): void 
{
    echo "=== Demonstração do Padrão Strategy ===\n\n";
    
    // Criar calculadora
    $taxCalculator = new TaxCalculator();
    $controller = new TaxController($taxCalculator);
    
    // Dados de teste
    $testCases = [
        ['ICMS', 1000.00],
        ['ISS', 2000.00],
        ['IPI', 500.00],
        ['IVA', 1500.00],
        ['INVALID', 1000.00] // Caso de erro
    ];
    
    foreach ($testCases as [$taxType, $amount]) {
        echo "--- Calculando {$taxType} para R$ " . number_format($amount, 2, ',', '.') . " ---\n";
        
        $result = $controller->calculateTax($taxType, $amount);
        
        if ($result['success']) {
            $data = $result['data'];
            echo "✅ Tipo: {$data['tax_type']}\n";
            echo "📊 Taxa: {$data['tax_rate']}\n";
            echo "💰 Valor: R$ " . number_format($data['amount'], 2, ',', '.') . "\n";
            echo "💸 Imposto: R$ " . number_format($data['tax_amount'], 2, ',', '.') . "\n";
            echo "💵 Total: R$ " . number_format($data['total'], 2, ',', '.') . "\n";
        } else {
            echo "❌ Erro: {$result['error']}\n";
        }
        
        echo "\n";
    }
    
    // Demonstrar flexibilidade
    echo "=== Demonstração de Flexibilidade ===\n\n";
    
    $amount = 1000.00;
    echo "Valor base: R$ " . number_format($amount, 2, ',', '.') . "\n\n";
    
    foreach (TaxTypeFactory::getAvailableTaxTypes() as $taxType) {
        $strategy = TaxTypeFactory::create($taxType);
        $taxCalculator->setTaxType($strategy);
        
        $taxAmount = $taxCalculator->calculate($amount);
        $taxInfo = $taxCalculator->getTaxInfo();
        
        echo "{$taxInfo['name']}: R$ " . number_format($taxAmount, 2, ',', '.') . 
             " ({$taxInfo['rate_percentage']}%)\n";
    }
}

// Executar demonstração
if (php_sapi_name() === 'cli') {
    demonstrateStrategyPattern();
}




