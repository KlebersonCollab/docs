<?php

/**
 * Exemplo do Padrão Observer - Sistema de Criptomoedas
 * 
 * Este exemplo demonstra como implementar o padrão Observer para monitorar
 * mudanças no preço do Bitcoin e notificar automaticamente múltiplos
 * observadores com regras de negócio específicas.
 */

// Interface para observadores do preço do Bitcoin
interface BitcoinPriceObserver 
{
    public function update(float $price): void;
}

// Classe observável - Bitcoin
class Bitcoin 
{
    private float $price = 0.0;
    private array $observers = [];
    
    public function getPrice(): float 
    {
        return $this->price;
    }
    
    public function setPrice(float $newPrice): void 
    {
        // Só atualiza se o preço for diferente
        if ($newPrice !== $this->price) {
            $oldPrice = $this->price;
            $this->price = $newPrice;
            
            echo "💰 Bitcoin: R$ {$oldPrice} → R$ {$newPrice}\n";
            $this->notifyObservers();
        }
    }
    
    public function addObserver(BitcoinPriceObserver $observer): void 
    {
        $this->observers[] = $observer;
        echo "👁️ Observador adicionado: " . get_class($observer) . "\n";
    }
    
    public function removeObserver(BitcoinPriceObserver $observer): void 
    {
        $key = array_search($observer, $this->observers, true);
        if ($key !== false) {
            unset($this->observers[$key]);
            $this->observers = array_values($this->observers);
            echo "❌ Observador removido: " . get_class($observer) . "\n";
        }
    }
    
    private function notifyObservers(): void 
    {
        echo "🔔 Notificando " . count($this->observers) . " observadores...\n\n";
        
        foreach ($this->observers as $observer) {
            try {
                $observer->update($this->price);
            } catch (Exception $e) {
                echo "❌ Erro ao notificar " . get_class($observer) . ": " . $e->getMessage() . "\n";
            }
        }
    }
}

// Observador 1: Logger de preços
class BitcoinPriceLogger implements BitcoinPriceObserver 
{
    private array $priceHistory = [];
    
    public function update(float $price): void 
    {
        $this->priceHistory[] = [
            'price' => $price,
            'timestamp' => date('Y-m-d H:i:s')
        ];
        
        echo "📊 [LOGGER] Preço registrado: R$ {$price} em " . date('H:i:s') . "\n";
        
        // Manter apenas os últimos 10 registros
        if (count($this->priceHistory) > 10) {
            array_shift($this->priceHistory);
        }
    }
    
    public function getPriceHistory(): array 
    {
        return $this->priceHistory;
    }
    
    public function getAveragePrice(): float 
    {
        if (empty($this->priceHistory)) {
            return 0.0;
        }
        
        $sum = array_sum(array_column($this->priceHistory, 'price'));
        return $sum / count($this->priceHistory);
    }
}

// Observador 2: Notificador de investidores
class InvestorNotifier implements BitcoinPriceObserver 
{
    private float $lastNotifiedPrice = 0.0;
    private const VARIATION_THRESHOLD = 0.10; // 10%
    
    public function update(float $price): void 
    {
        if ($this->lastNotifiedPrice === 0.0) {
            $this->lastNotifiedPrice = $price;
            return;
        }
        
        $variation = abs($price - $this->lastNotifiedPrice) / $this->lastNotifiedPrice;
        
        if ($variation >= self::VARIATION_THRESHOLD) {
            $this->notifyInvestors($price, $variation);
            $this->lastNotifiedPrice = $price;
        }
    }
    
    private function notifyInvestors(float $price, float $variation): void 
    {
        $variationPercent = $variation * 100;
        echo "📱 [INVESTOR] Notificação enviada: R$ {$price} (variação: {$variationPercent}%)\n";
        
        // Simular envio de notificação
        $this->sendPushNotification($price, $variationPercent);
        $this->sendEmailNotification($price, $variationPercent);
    }
    
    private function sendPushNotification(float $price, float $variation): void 
    {
        echo "    📲 Push: Bitcoin R$ {$price} ({$variation}%)\n";
    }
    
    private function sendEmailNotification(float $price, float $variation): void 
    {
        echo "    📧 Email: Bitcoin R$ {$price} ({$variation}%)\n";
    }
}

// Observador 3: Plataforma de notícias
class NewsPlatform implements BitcoinPriceObserver 
{
    private float $lastUpdatedPrice = 0.0;
    private const VARIATION_THRESHOLD = 0.20; // 20%
    
    public function update(float $price): void 
    {
        if ($this->lastUpdatedPrice === 0.0) {
            $this->lastUpdatedPrice = $price;
            return;
        }
        
        $variation = abs($price - $this->lastUpdatedPrice) / $this->lastUpdatedPrice;
        
        if ($variation >= self::VARIATION_THRESHOLD) {
            $this->updateNews($price, $variation);
            $this->lastUpdatedPrice = $price;
        }
    }
    
    private function updateNews(float $price, float $variation): void 
    {
        $variationPercent = $variation * 100;
        echo "📰 [NEWS] Plataforma atualizada: R$ {$price} (variação: {$variationPercent}%)\n";
        
        // Simular atualização da plataforma
        $this->publishArticle($price, $variationPercent);
        $this->updateHomepage($price, $variationPercent);
    }
    
    private function publishArticle(float $price, float $variation): void 
    {
        echo "    📝 Artigo: \"Bitcoin atinge R$ {$price} com variação de {$variation}%\"\n";
    }
    
    private function updateHomepage(float $price, float $variation): void 
    {
        echo "    🏠 Homepage: Preço atualizado para R$ {$price}\n";
    }
}

// Observador 4: Analisador de tendências
class TrendAnalyzer implements BitcoinPriceObserver 
{
    private array $pricePoints = [];
    private const POINTS_NEEDED = 5;
    
    public function update(float $price): void 
    {
        $this->pricePoints[] = [
            'price' => $price,
            'timestamp' => time()
        ];
        
        // Manter apenas os últimos pontos necessários
        if (count($this->pricePoints) > self::POINTS_NEEDED) {
            array_shift($this->pricePoints);
        }
        
        if (count($this->pricePoints) >= self::POINTS_NEEDED) {
            $this->analyzeTrend();
        }
    }
    
    private function analyzeTrend(): void 
    {
        $prices = array_column($this->pricePoints, 'price');
        $trend = $this->calculateTrend($prices);
        
        echo "📈 [TREND] Análise de tendência: {$trend}\n";
        
        if ($trend === 'ALTA') {
            $this->generateBuySignal();
        } elseif ($trend === 'BAIXA') {
            $this->generateSellSignal();
        }
    }
    
    private function calculateTrend(array $prices): string 
    {
        $firstHalf = array_slice($prices, 0, 3);
        $secondHalf = array_slice($prices, 2);
        
        $firstAvg = array_sum($firstHalf) / count($firstHalf);
        $secondAvg = array_sum($secondHalf) / count($secondHalf);
        
        $variation = ($secondAvg - $firstAvg) / $firstAvg;
        
        if ($variation > 0.05) {
            return 'ALTA';
        } elseif ($variation < -0.05) {
            return 'BAIXA';
        } else {
            return 'LATERAL';
        }
    }
    
    private function generateBuySignal(): void 
    {
        echo "    🟢 Sinal de COMPRA gerado\n";
    }
    
    private function generateSellSignal(): void 
    {
        echo "    🔴 Sinal de VENDA gerado\n";
    }
}

// Simulador de API da Binance
class BinanceApi 
{
    public function getBitcoinPrice(): float 
    {
        // Simular requisição à API da Binance
        $basePrice = 200000.0; // Preço base em reais
        $variation = (rand(-1000, 1000) / 1000.0) * 0.1; // Variação de ±10%
        
        return $basePrice + ($basePrice * $variation);
    }
}

// Comando para simular atualizações de preço
class BitcoinPriceUpdater 
{
    private Bitcoin $bitcoin;
    private BinanceApi $binanceApi;
    
    public function __construct(Bitcoin $bitcoin, BinanceApi $binanceApi) 
    {
        $this->bitcoin = $bitcoin;
        $this->binanceApi = $binanceApi;
    }
    
    public function updatePrice(): void 
    {
        $newPrice = $this->binanceApi->getBitcoinPrice();
        $this->bitcoin->setPrice($newPrice);
    }
    
    public function runSimulation(int $iterations = 10): void 
    {
        echo "🚀 Iniciando simulação de {$iterations} atualizações de preço...\n\n";
        
        for ($i = 1; $i <= $iterations; $i++) {
            echo "--- Iteração {$i} ---\n";
            $this->updatePrice();
            echo "\n";
            
            // Pausa entre atualizações
            sleep(1);
        }
    }
}

// Exemplo de uso
function demonstrateObserverPattern(): void 
{
    echo "=== Demonstração do Padrão Observer - Sistema de Criptomoedas ===\n\n";
    
    // Criar instâncias
    $bitcoin = new Bitcoin();
    $binanceApi = new BinanceApi();
    $updater = new BitcoinPriceUpdater($bitcoin, $binanceApi);
    
    // Criar observadores
    $priceLogger = new BitcoinPriceLogger();
    $investorNotifier = new InvestorNotifier();
    $newsPlatform = new NewsPlatform();
    $trendAnalyzer = new TrendAnalyzer();
    
    // Adicionar observadores ao Bitcoin
    $bitcoin->addObserver($priceLogger);
    $bitcoin->addObserver($investorNotifier);
    $bitcoin->addObserver($newsPlatform);
    $bitcoin->addObserver($trendAnalyzer);
    
    echo "✅ Todos os observadores adicionados!\n\n";
    
    // Executar simulação
    $updater->runSimulation(8);
    
    // Mostrar estatísticas
    echo "=== Estatísticas Finais ===\n";
    echo "📊 Histórico de preços: " . count($priceLogger->getPriceHistory()) . " registros\n";
    echo "📈 Preço médio: R$ " . number_format($priceLogger->getAveragePrice(), 2) . "\n";
    echo "💰 Preço atual: R$ " . number_format($bitcoin->getPrice(), 2) . "\n";
}

// Demonstração de remoção de observadores
function demonstrateObserverRemoval(): void 
{
    echo "\n=== Demonstração de Remoção de Observadores ===\n\n";
    
    $bitcoin = new Bitcoin();
    $priceLogger = new BitcoinPriceLogger();
    $investorNotifier = new InvestorNotifier();
    
    // Adicionar observadores
    $bitcoin->addObserver($priceLogger);
    $bitcoin->addObserver($investorNotifier);
    
    // Atualizar preço com todos os observadores
    echo "--- Com todos os observadores ---\n";
    $bitcoin->setPrice(250000.0);
    
    // Remover um observador
    $bitcoin->removeObserver($investorNotifier);
    
    // Atualizar preço sem o observador removido
    echo "\n--- Após remover InvestorNotifier ---\n";
    $bitcoin->setPrice(260000.0);
}

// Demonstração de tratamento de erros
function demonstrateErrorHandling(): void 
{
    echo "\n=== Demonstração de Tratamento de Erros ===\n\n";
    
    // Observador que gera erro
    class ErrorObserver implements BitcoinPriceObserver 
    {
        public function update(float $price): void 
        {
            throw new Exception("Erro simulado no observador");
        }
    }
    
    $bitcoin = new Bitcoin();
    $priceLogger = new BitcoinPriceLogger();
    $errorObserver = new ErrorObserver();
    
    // Adicionar observadores (um normal, um com erro)
    $bitcoin->addObserver($priceLogger);
    $bitcoin->addObserver($errorObserver);
    
    // Atualizar preço (deve continuar funcionando mesmo com erro)
    $bitcoin->setPrice(270000.0);
}

// Executar demonstrações
if (php_sapi_name() === 'cli') {
    demonstrateObserverPattern();
    demonstrateObserverRemoval();
    demonstrateErrorHandling();
}








