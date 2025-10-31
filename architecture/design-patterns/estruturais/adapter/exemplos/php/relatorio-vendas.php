<?php

/**
 * Exemplo prático do Padrão Adapter em PHP
 * Sistema de geração de relatórios de vendas
 * 
 * Este exemplo demonstra como implementar o padrão Adapter
 * para desacoplar a geração de relatórios de bibliotecas específicas
 */

// Interface que define o contrato para geradores de PDF
interface PdfAdapter {
    public function generate(string $filename, string $content): void;
}

/**
 * Adapter para biblioteca DomPDF
 * Envolve a biblioteca DomPDF para seguir a interface PdfAdapter
 */
class DomPdfAdapter implements PdfAdapter {
    private Dompdf $dompdf;
    
    public function __construct() {
        $this->dompdf = new Dompdf();
    }
    
    public function generate(string $filename, string $content): void {
        echo "🔄 Gerando PDF com DomPDF...\n";
        
        try {
            // Configuração específica do DomPDF
            $this->dompdf->loadHtml($content);
            $this->dompdf->setPaper('A4', 'landscape');
            $this->dompdf->render();
            
            // Salvar arquivo
            file_put_contents($filename, $this->dompdf->output());
            echo "✅ PDF gerado com DomPDF: {$filename}\n";
            
        } catch (Exception $e) {
            throw new RuntimeException("Erro ao gerar PDF com DomPDF: " . $e->getMessage());
        }
    }
}

/**
 * Adapter para biblioteca TCPDF
 * Envolve a biblioteca TCPDF para seguir a interface PdfAdapter
 */
class TcpdfAdapter implements PdfAdapter {
    private TCPDF $tcpdf;
    
    public function __construct() {
        $this->tcpdf = new TCPDF();
    }
    
    public function generate(string $filename, string $content): void {
        echo "🔄 Gerando PDF com TCPDF...\n";
        
        try {
            // Configuração específica do TCPDF
            $this->tcpdf->writeHTML($content);
            $this->tcpdf->setFont('helvetica', '', 12);
            $this->tcpdf->Output($filename, 'F');
            
            echo "✅ PDF gerado com TCPDF: {$filename}\n";
            
        } catch (Exception $e) {
            throw new RuntimeException("Erro ao gerar PDF com TCPDF: " . $e->getMessage());
        }
    }
}

/**
 * Adapter para biblioteca mPDF
 * Envolve a biblioteca mPDF para seguir a interface PdfAdapter
 */
class MPdfAdapter implements PdfAdapter {
    private mPDF $mpdf;
    
    public function __construct() {
        $this->mpdf = new mPDF();
    }
    
    public function generate(string $filename, string $content): void {
        echo "🔄 Gerando PDF com mPDF...\n";
        
        try {
            // Configuração específica do mPDF
            $this->mpdf->WriteHTML($content);
            $this->mpdf->Output($filename, 'F');
            
            echo "✅ PDF gerado com mPDF: {$filename}\n";
            
        } catch (Exception $e) {
            throw new RuntimeException("Erro ao gerar PDF com mPDF: " . $e->getMessage());
        }
    }
}

/**
 * Classe SalesReportGenerator - Cliente do padrão Adapter
 * Gera relatórios de vendas usando qualquer implementação de PdfAdapter
 */
class SalesReportGenerator {
    private PdfAdapter $pdfAdapter;
    private string $companyName;
    private array $salesData;
    
    public function __construct(PdfAdapter $pdfAdapter, string $companyName = "Empresa XYZ") {
        $this->pdfAdapter = $pdfAdapter;
        $this->companyName = $companyName;
        $this->salesData = [];
    }
    
    /**
     * Adiciona dados de venda ao relatório
     */
    public function addSale(string $product, float $value, int $quantity): void {
        $this->salesData[] = [
            'product' => $product,
            'value' => $value,
            'quantity' => $quantity,
            'total' => $value * $quantity
        ];
    }
    
    /**
     * Gera o relatório de vendas
     */
    public function generateReport(): void {
        echo "📊 Gerando relatório de vendas para {$this->companyName}\n";
        
        $filename = 'relatorio_vendas_' . date('Y-m-d_H-i-s') . '.pdf';
        $content = $this->buildReportContent();
        
        $this->pdfAdapter->generate($filename, $content);
        
        echo "📈 Relatório gerado com sucesso!\n";
        echo "📁 Arquivo: {$filename}\n";
        echo "💰 Total de vendas: R$ " . number_format($this->getTotalSales(), 2, ',', '.') . "\n\n";
    }
    
    /**
     * Constrói o conteúdo HTML do relatório
     */
    private function buildReportContent(): string {
        $totalSales = $this->getTotalSales();
        $totalItems = array_sum(array_column($this->salesData, 'quantity'));
        
        $html = "
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset='UTF-8'>
            <title>Relatório de Vendas</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; margin-bottom: 30px; }
                .company { font-size: 24px; font-weight: bold; color: #333; }
                .date { font-size: 14px; color: #666; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; font-weight: bold; }
                .total { font-size: 18px; font-weight: bold; color: #2c5aa0; }
                .summary { background-color: #f9f9f9; padding: 15px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class='header'>
                <div class='company'>{$this->companyName}</div>
                <div class='date'>Relatório de Vendas - " . date('d/m/Y H:i:s') . "</div>
            </div>
            
            <div class='summary'>
                <h3>Resumo Executivo</h3>
                <p><strong>Total de Vendas:</strong> R$ " . number_format($totalSales, 2, ',', '.') . "</p>
                <p><strong>Total de Itens:</strong> {$totalItems}</p>
                <p><strong>Número de Produtos:</strong> " . count($this->salesData) . "</p>
            </div>
            
            <h3>Detalhamento das Vendas</h3>
            <table>
                <thead>
                    <tr>
                        <th>Produto</th>
                        <th>Valor Unitário</th>
                        <th>Quantidade</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>";
        
        foreach ($this->salesData as $sale) {
            $html .= "
                    <tr>
                        <td>{$sale['product']}</td>
                        <td>R$ " . number_format($sale['value'], 2, ',', '.') . "</td>
                        <td>{$sale['quantity']}</td>
                        <td>R$ " . number_format($sale['total'], 2, ',', '.') . "</td>
                    </tr>";
        }
        
        $html .= "
                </tbody>
            </table>
            
            <div class='total'>
                Total Geral: R$ " . number_format($totalSales, 2, ',', '.') . "
            </div>
        </body>
        </html>";
        
        return $html;
    }
    
    /**
     * Calcula o total de vendas
     */
    private function getTotalSales(): float {
        return array_sum(array_column($this->salesData, 'total'));
    }
}

/**
 * Demonstração do uso do padrão Adapter
 */
function demonstrarPadraoAdapter(): void {
    echo "=== DEMONSTRAÇÃO DO PADRÃO ADAPTER ===\n\n";
    
    // Criar dados de exemplo
    $salesData = [
        ['produto' => 'Notebook Dell', 'valor' => 2500.00, 'quantidade' => 2],
        ['produto' => 'Mouse Logitech', 'valor' => 89.90, 'quantidade' => 5],
        ['produto' => 'Teclado Mecânico', 'valor' => 299.90, 'quantidade' => 3],
        ['produto' => 'Monitor 24"', 'valor' => 899.90, 'quantidade' => 1],
        ['produto' => 'Cabo HDMI', 'valor' => 29.90, 'quantidade' => 10]
    ];
    
    // Demonstração com DomPDF
    echo "=== TESTE COM DOMPDF ===\n";
    $domPdfAdapter = new DomPdfAdapter();
    $generator = new SalesReportGenerator($domPdfAdapter, "TechStore Ltda");
    
    foreach ($salesData as $sale) {
        $generator->addSale($sale['produto'], $sale['valor'], $sale['quantidade']);
    }
    
    $generator->generateReport();
    
    // Demonstração com TCPDF
    echo "=== TESTE COM TCPDF ===\n";
    $tcpdfAdapter = new TcpdfAdapter();
    $generator2 = new SalesReportGenerator($tcpdfAdapter, "TechStore Ltda");
    
    foreach ($salesData as $sale) {
        $generator2->addSale($sale['produto'], $sale['valor'], $sale['quantidade']);
    }
    
    $generator2->generateReport();
    
    // Demonstração com mPDF
    echo "=== TESTE COM MPDF ===\n";
    $mPdfAdapter = new MPdfAdapter();
    $generator3 = new SalesReportGenerator($mPdfAdapter, "TechStore Ltda");
    
    foreach ($salesData as $sale) {
        $generator3->addSale($sale['produto'], $sale['valor'], $sale['quantidade']);
    }
    
    $generator3->generateReport();
    
    echo "=== DEMONSTRAÇÃO CONCLUÍDA ===\n";
    echo "✅ O padrão Adapter permite trocar bibliotecas sem modificar o código!\n";
    echo "✅ Cada adapter encapsula a complexidade da biblioteca específica!\n";
    echo "✅ O código cliente permanece inalterado independente da biblioteca!\n";
}

/**
 * Demonstração de flexibilidade
 */
function demonstrarFlexibilidade(): void {
    echo "\n=== DEMONSTRAÇÃO DE FLEXIBILIDADE ===\n";
    
    // Configuração dinâmica do adapter
    $adapters = [
        'dompdf' => DomPdfAdapter::class,
        'tcpdf' => TcpdfAdapter::class,
        'mpdf' => MPdfAdapter::class
    ];
    
    $selectedAdapter = $adapters['dompdf']; // Pode vir de configuração
    
    $adapter = new $selectedAdapter();
    $generator = new SalesReportGenerator($adapter, "Empresa Configurável");
    
    // Adicionar algumas vendas
    $generator->addSale("Produto A", 100.00, 2);
    $generator->addSale("Produto B", 200.00, 1);
    
    $generator->generateReport();
    
    echo "✅ Adapter configurado dinamicamente!\n";
    echo "✅ Fácil troca de implementação via configuração!\n";
}

// Executar demonstrações
demonstrarPadraoAdapter();
demonstrarFlexibilidade();








