<?php

/**
 * Exemplo do Padrão Template Method - Sistema de Mineração de Dados
 * 
 * Este exemplo demonstra como implementar o padrão Template Method para
 * eliminar duplicação de código em um sistema de mineração de dados que
 * processa diferentes tipos de documentos (DOC, CSV, PDF).
 */

// Classe abstrata que define o template method
abstract class DataMiner 
{
    /**
     * Template Method - define o esqueleto do algoritmo
     * Este método não pode ser sobrescrito pelas subclasses
     */
    final public function mine(): void 
    {
        echo "🚀 Iniciando processo de mineração de dados...\n";
        
        // 1. Abrir arquivo
        $fileContent = $this->openFile();
        echo "📁 Arquivo aberto com sucesso\n";
        
        // 2. Extrair dados brutos
        $rawData = $this->extractData($fileContent);
        echo "📊 Dados extraídos: " . count($rawData) . " registros\n";
        
        // 3. Parsear dados
        $parsedData = $this->parseData($rawData);
        echo "🔍 Dados parseados: " . count($parsedData) . " registros processados\n";
        
        // 4. Analisar dados (implementação comum)
        $this->analyzeData($parsedData);
        
        // 5. Enviar relatório (implementação comum)
        $this->sendReport($parsedData);
        
        echo "✅ Processo de mineração concluído!\n\n";
    }
    
    /**
     * Método abstrato para abrir arquivo
     * Cada subclasse implementa sua própria lógica
     */
    abstract protected function openFile(): string;
    
    /**
     * Método abstrato para extrair dados
     * Cada subclasse implementa sua própria lógica
     */
    abstract protected function extractData(string $fileContent): array;
    
    /**
     * Método abstrato para parsear dados
     * Cada subclasse implementa sua própria lógica
     */
    abstract protected function parseData(array $rawData): array;
    
    /**
     * Método comum para analisar dados
     * Implementação compartilhada entre todas as subclasses
     */
    protected function analyzeData(array $data): void 
    {
        echo "🔬 Analisando dados...\n";
        
        if (empty($data)) {
            echo "⚠️ Nenhum dado para analisar\n";
            return;
        }
        
        // Análise estatística básica
        $totalRecords = count($data);
        $numericFields = 0;
        $textFields = 0;
        
        foreach ($data as $record) {
            foreach ($record as $field => $value) {
                if (is_numeric($value)) {
                    $numericFields++;
                } else {
                    $textFields++;
                }
            }
        }
        
        echo "📈 Estatísticas da análise:\n";
        echo "   - Total de registros: {$totalRecords}\n";
        echo "   - Campos numéricos: {$numericFields}\n";
        echo "   - Campos de texto: {$textFields}\n";
        
        // Análise de qualidade dos dados
        $this->performDataQualityAnalysis($data);
    }
    
    /**
     * Método comum para enviar relatório
     * Implementação compartilhada entre todas as subclasses
     */
    protected function sendReport(array $data): void 
    {
        echo "📧 Enviando relatório...\n";
        
        $reportData = [
            'timestamp' => date('Y-m-d H:i:s'),
            'total_records' => count($data),
            'data_type' => $this->getDataType(),
            'status' => 'success'
        ];
        
        // Simular envio de relatório
        $this->sendEmailReport($reportData);
        $this->saveReportToDatabase($reportData);
        $this->notifyStakeholders($reportData);
        
        echo "✅ Relatório enviado com sucesso\n";
    }
    
    /**
     * Método abstrato para obter tipo de dados
     * Cada subclasse retorna seu tipo específico
     */
    abstract protected function getDataType(): string;
    
    /**
     * Análise de qualidade dos dados
     * Método comum para todas as subclasses
     */
    private function performDataQualityAnalysis(array $data): void 
    {
        $qualityScore = 0;
        $totalFields = 0;
        $emptyFields = 0;
        
        foreach ($data as $record) {
            foreach ($record as $field => $value) {
                $totalFields++;
                if (empty($value) || $value === null) {
                    $emptyFields++;
                }
            }
        }
        
        if ($totalFields > 0) {
            $qualityScore = (($totalFields - $emptyFields) / $totalFields) * 100;
        }
        
        echo "🎯 Análise de qualidade:\n";
        echo "   - Score de qualidade: " . number_format($qualityScore, 2) . "%\n";
        echo "   - Campos vazios: {$emptyFields}/{$totalFields}\n";
        
        if ($qualityScore < 80) {
            echo "⚠️ Atenção: Qualidade dos dados abaixo do esperado\n";
        } else {
            echo "✅ Qualidade dos dados dentro do esperado\n";
        }
    }
    
    /**
     * Enviar relatório por email
     * Método comum para todas as subclasses
     */
    private function sendEmailReport(array $reportData): void 
    {
        echo "   📧 Email enviado para: admin@empresa.com\n";
        echo "   📧 Assunto: Relatório de Mineração - {$reportData['data_type']}\n";
    }
    
    /**
     * Salvar relatório no banco de dados
     * Método comum para todas as subclasses
     */
    private function saveReportToDatabase(array $reportData): void 
    {
        echo "   💾 Relatório salvo no banco de dados\n";
        echo "   💾 ID do relatório: " . uniqid() . "\n";
    }
    
    /**
     * Notificar stakeholders
     * Método comum para todas as subclasses
     */
    private function notifyStakeholders(array $reportData): void 
    {
        echo "   🔔 Notificações enviadas para stakeholders\n";
        echo "   🔔 Total de registros processados: {$reportData['total_records']}\n";
    }
}

// Implementação concreta para arquivos DOC
class DocDataMiner extends DataMiner 
{
    private string $filePath;
    
    public function __construct(string $filePath) 
    {
        $this->filePath = $filePath;
    }
    
    protected function openFile(): string 
    {
        echo "📄 Abrindo arquivo DOC: {$this->filePath}\n";
        
        // Simular abertura de arquivo DOC
        if (!file_exists($this->filePath)) {
            throw new Exception("Arquivo DOC não encontrado: {$this->filePath}");
        }
        
        // Simular conteúdo de arquivo DOC
        return "Conteúdo do arquivo DOC: Dados importantes do documento Word...";
    }
    
    protected function extractData(string $fileContent): array 
    {
        echo "📊 Extraindo dados do arquivo DOC...\n";
        
        // Simular extração de dados de arquivo DOC
        return [
            ['titulo' => 'Relatório Mensal', 'conteudo' => 'Dados importantes...', 'data' => '2024-01-15'],
            ['titulo' => 'Análise Financeira', 'conteudo' => 'Resultados do trimestre...', 'data' => '2024-01-20'],
            ['titulo' => 'Propostas Comerciais', 'conteudo' => 'Novas oportunidades...', 'data' => '2024-01-25']
        ];
    }
    
    protected function parseData(array $rawData): array 
    {
        echo "🔍 Parseando dados do arquivo DOC...\n";
        
        $parsedData = [];
        foreach ($rawData as $record) {
            $parsedData[] = [
                'documento' => $record['titulo'],
                'resumo' => substr($record['conteudo'], 0, 50) . '...',
                'data_criacao' => $record['data'],
                'tipo' => 'DOC',
                'tamanho' => strlen($record['conteudo'])
            ];
        }
        
        return $parsedData;
    }
    
    protected function getDataType(): string 
    {
        return 'DOC';
    }
}

// Implementação concreta para arquivos CSV
class CsvDataMiner extends DataMiner 
{
    private string $filePath;
    
    public function __construct(string $filePath) 
    {
        $this->filePath = $filePath;
    }
    
    protected function openFile(): string 
    {
        echo "📊 Abrindo arquivo CSV: {$this->filePath}\n";
        
        // Simular abertura de arquivo CSV
        if (!file_exists($this->filePath)) {
            throw new Exception("Arquivo CSV não encontrado: {$this->filePath}");
        }
        
        // Simular conteúdo de arquivo CSV
        return "nome,idade,email,departamento\nJoão Silva,30,joao@email.com,Vendas\nMaria Santos,25,maria@email.com,Marketing\nPedro Costa,35,pedro@email.com,TI";
    }
    
    protected function extractData(string $fileContent): array 
    {
        echo "📊 Extraindo dados do arquivo CSV...\n";
        
        $lines = explode("\n", $fileContent);
        $headers = str_getcsv($lines[0]);
        $data = [];
        
        for ($i = 1; $i < count($lines); $i++) {
            if (!empty($lines[$i])) {
                $values = str_getcsv($lines[$i]);
                $data[] = array_combine($headers, $values);
            }
        }
        
        return $data;
    }
    
    protected function parseData(array $rawData): array 
    {
        echo "🔍 Parseando dados do arquivo CSV...\n";
        
        $parsedData = [];
        foreach ($rawData as $record) {
            $parsedData[] = [
                'nome' => $record['nome'],
                'idade' => (int)$record['idade'],
                'email' => $record['email'],
                'departamento' => $record['departamento'],
                'tipo' => 'CSV',
                'ativo' => true
            ];
        }
        
        return $parsedData;
    }
    
    protected function getDataType(): string 
    {
        return 'CSV';
    }
}

// Implementação concreta para arquivos PDF
class PdfDataMiner extends DataMiner 
{
    private string $filePath;
    
    public function __construct(string $filePath) 
    {
        $this->filePath = $filePath;
    }
    
    protected function openFile(): string 
    {
        echo "📄 Abrindo arquivo PDF: {$this->filePath}\n";
        
        // Simular abertura de arquivo PDF
        if (!file_exists($this->filePath)) {
            throw new Exception("Arquivo PDF não encontrado: {$this->filePath}");
        }
        
        // Simular conteúdo de arquivo PDF
        return "Conteúdo do arquivo PDF: Documento técnico com gráficos e tabelas...";
    }
    
    protected function extractData(string $fileContent): array 
    {
        echo "📊 Extraindo dados do arquivo PDF...\n";
        
        // Simular extração de dados de arquivo PDF
        return [
            ['pagina' => 1, 'conteudo' => 'Introdução ao projeto...', 'tipo' => 'texto'],
            ['pagina' => 2, 'conteudo' => 'Gráfico de vendas...', 'tipo' => 'grafico'],
            ['pagina' => 3, 'conteudo' => 'Tabela de resultados...', 'tipo' => 'tabela'],
            ['pagina' => 4, 'conteudo' => 'Conclusões e recomendações...', 'tipo' => 'texto']
        ];
    }
    
    protected function parseData(array $rawData): array 
    {
        echo "🔍 Parseando dados do arquivo PDF...\n";
        
        $parsedData = [];
        foreach ($rawData as $record) {
            $parsedData[] = [
                'pagina' => $record['pagina'],
                'conteudo' => substr($record['conteudo'], 0, 100) . '...',
                'tipo_conteudo' => $record['tipo'],
                'tipo' => 'PDF',
                'tamanho' => strlen($record['conteudo'])
            ];
        }
        
        return $parsedData;
    }
    
    protected function getDataType(): string 
    {
        return 'PDF';
    }
}

// Implementação concreta para arquivos JSON
class JsonDataMiner extends DataMiner 
{
    private string $filePath;
    
    public function __construct(string $filePath) 
    {
        $this->filePath = $filePath;
    }
    
    protected function openFile(): string 
    {
        echo "📄 Abrindo arquivo JSON: {$this->filePath}\n";
        
        // Simular abertura de arquivo JSON
        if (!file_exists($this->filePath)) {
            throw new Exception("Arquivo JSON não encontrado: {$this->filePath}");
        }
        
        // Simular conteúdo de arquivo JSON
        return json_encode([
            'produtos' => [
                ['id' => 1, 'nome' => 'Produto A', 'preco' => 99.90, 'categoria' => 'Eletrônicos'],
                ['id' => 2, 'nome' => 'Produto B', 'preco' => 149.90, 'categoria' => 'Roupas'],
                ['id' => 3, 'nome' => 'Produto C', 'preco' => 79.90, 'categoria' => 'Casa']
            ]
        ]);
    }
    
    protected function extractData(string $fileContent): array 
    {
        echo "📊 Extraindo dados do arquivo JSON...\n";
        
        $data = json_decode($fileContent, true);
        return $data['produtos'] ?? [];
    }
    
    protected function parseData(array $rawData): array 
    {
        echo "🔍 Parseando dados do arquivo JSON...\n";
        
        $parsedData = [];
        foreach ($rawData as $record) {
            $parsedData[] = [
                'id' => $record['id'],
                'nome' => $record['nome'],
                'preco' => (float)$record['preco'],
                'categoria' => $record['categoria'],
                'tipo' => 'JSON',
                'ativo' => true
            ];
        }
        
        return $parsedData;
    }
    
    protected function getDataType(): string 
    {
        return 'JSON';
    }
}

// Exemplo de uso
function demonstrateTemplateMethod(): void 
{
    echo "=== Demonstração do Padrão Template Method - Sistema de Mineração de Dados ===\n\n";
    
    try {
        // Criar instâncias dos diferentes tipos de mineradores
        $docMiner = new DocDataMiner('/path/to/document.doc');
        $csvMiner = new CsvDataMiner('/path/to/data.csv');
        $pdfMiner = new PdfDataMiner('/path/to/report.pdf');
        $jsonMiner = new JsonDataMiner('/path/to/products.json');
        
        // Executar mineração para cada tipo
        echo "--- Mineração de Arquivo DOC ---\n";
        $docMiner->mine();
        
        echo "--- Mineração de Arquivo CSV ---\n";
        $csvMiner->mine();
        
        echo "--- Mineração de Arquivo PDF ---\n";
        $pdfMiner->mine();
        
        echo "--- Mineração de Arquivo JSON ---\n";
        $jsonMiner->mine();
        
    } catch (Exception $e) {
        echo "❌ Erro durante a mineração: " . $e->getMessage() . "\n";
    }
}

// Demonstração de extensibilidade
function demonstrateExtensibility(): void 
{
    echo "\n=== Demonstração de Extensibilidade ===\n\n";
    
    // Criar um novo tipo de minerador para XML
    class XmlDataMiner extends DataMiner 
    {
        private string $filePath;
        
        public function __construct(string $filePath) 
        {
            $this->filePath = $filePath;
        }
        
        protected function openFile(): string 
        {
            echo "📄 Abrindo arquivo XML: {$this->filePath}\n";
            return "<?xml version='1.0'?><root><item>Dados XML importantes...</item></root>";
        }
        
        protected function extractData(string $fileContent): array 
        {
            echo "📊 Extraindo dados do arquivo XML...\n";
            return [['conteudo' => 'Dados extraídos do XML', 'tipo' => 'xml']];
        }
        
        protected function parseData(array $rawData): array 
        {
            echo "🔍 Parseando dados do arquivo XML...\n";
            return [['dados' => $rawData[0]['conteudo'], 'tipo' => 'XML', 'processado' => true]];
        }
        
        protected function getDataType(): string 
        {
            return 'XML';
        }
    }
    
    // Usar o novo minerador
    $xmlMiner = new XmlDataMiner('/path/to/data.xml');
    $xmlMiner->mine();
}

// Demonstração de personalização
function demonstrateCustomization(): void 
{
    echo "\n=== Demonstração de Personalização ===\n\n";
    
    // Minerador personalizado que sobrescreve métodos comuns
    class CustomDataMiner extends DataMiner 
    {
        private string $filePath;
        
        public function __construct(string $filePath) 
        {
            $this->filePath = $filePath;
        }
        
        protected function openFile(): string 
        {
            echo "📄 Abrindo arquivo personalizado: {$this->filePath}\n";
            return "Conteúdo personalizado do arquivo...";
        }
        
        protected function extractData(string $fileContent): array 
        {
            echo "📊 Extraindo dados com lógica personalizada...\n";
            return [['dados' => 'Dados extraídos com lógica personalizada']];
        }
        
        protected function parseData(array $rawData): array 
        {
            echo "🔍 Parseando dados com lógica personalizada...\n";
            return [['dados' => $rawData[0]['dados'], 'tipo' => 'CUSTOM', 'personalizado' => true]];
        }
        
        protected function getDataType(): string 
        {
            return 'CUSTOM';
        }
        
        // Sobrescrever método comum para personalização
        protected function sendReport(array $data): void 
        {
            echo "📧 Enviando relatório personalizado...\n";
            echo "   📧 Email personalizado enviado\n";
            echo "   📧 Relatório personalizado salvo\n";
            echo "✅ Relatório personalizado enviado com sucesso\n";
        }
    }
    
    // Usar o minerador personalizado
    $customMiner = new CustomDataMiner('/path/to/custom.txt');
    $customMiner->mine();
}

// Executar demonstrações
if (php_sapi_name() === 'cli') {
    demonstrateTemplateMethod();
    demonstrateExtensibility();
    demonstrateCustomization();
}








