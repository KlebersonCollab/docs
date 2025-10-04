/**
 * Exemplo prático do padrão Decorator em Java
 * Sistema de cafeteria com diferentes tipos de café e adicionais
 */

// Interface base para café
interface Coffee {
    String getDescription();
    double getCost();
    String getSize();
}

// Implementação concreta - Café simples
class SimpleCoffee implements Coffee {
    private String size;
    
    public SimpleCoffee(String size) {
        this.size = size;
    }
    
    @Override
    public String getDescription() {
        return "Café simples";
    }
    
    @Override
    public double getCost() {
        return getBaseCost();
    }
    
    @Override
    public String getSize() {
        return size;
    }
    
    private double getBaseCost() {
        switch (size.toLowerCase()) {
            case "pequeno": return 2.0;
            case "médio": return 2.5;
            case "grande": return 3.0;
            default: return 2.5;
        }
    }
}

// Decorator abstrato
abstract class CoffeeDecorator implements Coffee {
    protected Coffee coffee;
    
    public CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }
    
    @Override
    public String getSize() {
        return coffee.getSize();
    }
}

// Decorador concreto - Leite
class MilkDecorator extends CoffeeDecorator {
    private String milkType;
    
    public MilkDecorator(Coffee coffee, String milkType) {
        super(coffee);
        this.milkType = milkType;
    }
    
    @Override
    public String getDescription() {
        return coffee.getDescription() + ", com leite " + milkType;
    }
    
    @Override
    public double getCost() {
        double milkCost = getMilkCost();
        return coffee.getCost() + milkCost;
    }
    
    private double getMilkCost() {
        switch (milkType.toLowerCase()) {
            case "integral": return 0.5;
            case "desnatado": return 0.4;
            case "soja": return 0.6;
            case "amêndoa": return 0.8;
            default: return 0.5;
        }
    }
}

// Decorador concreto - Açúcar
class SugarDecorator extends CoffeeDecorator {
    private int sugarSpoons;
    
    public SugarDecorator(Coffee coffee, int sugarSpoons) {
        super(coffee);
        this.sugarSpoons = Math.max(0, sugarSpoons); // Não permite valores negativos
    }
    
    @Override
    public String getDescription() {
        if (sugarSpoons == 0) {
            return coffee.getDescription() + ", sem açúcar";
        } else if (sugarSpoons == 1) {
            return coffee.getDescription() + ", com 1 colher de açúcar";
        } else {
            return coffee.getDescription() + ", com " + sugarSpoons + " colheres de açúcar";
        }
    }
    
    @Override
    public double getCost() {
        return coffee.getCost() + (sugarSpoons * 0.1); // Cada colher custa R$ 0,10
    }
}

// Decorador concreto - Xarope
class SyrupDecorator extends CoffeeDecorator {
    private String syrupFlavor;
    
    public SyrupDecorator(Coffee coffee, String syrupFlavor) {
        super(coffee);
        this.syrupFlavor = syrupFlavor;
    }
    
    @Override
    public String getDescription() {
        return coffee.getDescription() + ", com xarope de " + syrupFlavor;
    }
    
    @Override
    public double getCost() {
        double syrupCost = getSyrupCost();
        return coffee.getCost() + syrupCost;
    }
    
    private double getSyrupCost() {
        switch (syrupFlavor.toLowerCase()) {
            case "baunilha": return 0.8;
            case "caramelo": return 0.9;
            case "chocolate": return 1.0;
            case "lavanda": return 1.2;
            default: return 0.8;
        }
    }
}

// Decorador concreto - Espuma
class FoamDecorator extends CoffeeDecorator {
    private String foamType;
    
    public FoamDecorator(Coffee coffee, String foamType) {
        super(coffee);
        this.foamType = foamType;
    }
    
    @Override
    public String getDescription() {
        return coffee.getDescription() + ", com espuma de " + foamType;
    }
    
    @Override
    public double getCost() {
        double foamCost = getFoamCost();
        return coffee.getCost() + foamCost;
    }
    
    private double getFoamCost() {
        switch (foamType.toLowerCase()) {
            case "leite": return 0.6;
            case "soja": return 0.7;
            case "coco": return 0.8;
            default: return 0.6;
        }
    }
}

// Decorador concreto - Temperatura
class TemperatureDecorator extends CoffeeDecorator {
    private String temperature;
    
    public TemperatureDecorator(Coffee coffee, String temperature) {
        super(coffee);
        this.temperature = temperature;
    }
    
    @Override
    public String getDescription() {
        return coffee.getDescription() + " (" + temperature + ")";
    }
    
    @Override
    public double getCost() {
        // Temperatura não adiciona custo, apenas modifica a descrição
        return coffee.getCost();
    }
}

// Classe principal para demonstração
public class CoffeeShop {
    
    public static void main(String[] args) {
        System.out.println("☕ Demonstração do Padrão Decorator - Cafeteria\n");
        
        // Cenário 1: Café simples
        System.out.println("📝 Cenário 1: Café simples");
        Coffee coffee1 = new SimpleCoffee("médio");
        printCoffeeDetails(coffee1);
        
        // Cenário 2: Café com leite
        System.out.println("\n📝 Cenário 2: Café com leite");
        Coffee coffee2 = new MilkDecorator(
            new SimpleCoffee("grande"), 
            "integral"
        );
        printCoffeeDetails(coffee2);
        
        // Cenário 3: Café com múltiplos adicionais
        System.out.println("\n📝 Cenário 3: Café completo");
        Coffee coffee3 = new TemperatureDecorator(
            new FoamDecorator(
                new SyrupDecorator(
                    new SugarDecorator(
                        new MilkDecorator(
                            new SimpleCoffee("grande"), 
                            "soja"
                        ), 
                        2
                    ), 
                    "baunilha"
                ), 
                "leite"
            ), 
            "quente"
        );
        printCoffeeDetails(coffee3);
        
        // Cenário 4: Café gelado
        System.out.println("\n📝 Cenário 4: Café gelado");
        Coffee coffee4 = new TemperatureDecorator(
            new SyrupDecorator(
                new SugarDecorator(
                    new SimpleCoffee("médio"), 
                    1
                ), 
                "caramelo"
            ), 
            "gelado"
        );
        printCoffeeDetails(coffee4);
        
        // Cenário 5: Café sem açúcar (dietético)
        System.out.println("\n📝 Cenário 5: Café dietético");
        Coffee coffee5 = new TemperatureDecorator(
            new FoamDecorator(
                new MilkDecorator(
                    new SimpleCoffee("pequeno"), 
                    "desnatado"
                ), 
                "soja"
            ), 
            "morno"
        );
        printCoffeeDetails(coffee5);
        
        // Demonstração de flexibilidade na ordem
        System.out.println("\n📝 Cenário 6: Ordem diferente dos decoradores");
        Coffee coffee6a = new SugarDecorator(
            new MilkDecorator(
                new SimpleCoffee("médio"), 
                "integral"
            ), 
            1
        );
        
        Coffee coffee6b = new MilkDecorator(
            new SugarDecorator(
                new SimpleCoffee("médio"), 
                1
            ), 
            "integral"
        );
        
        System.out.println("Ordem A (Açúcar → Leite):");
        printCoffeeDetails(coffee6a);
        
        System.out.println("Ordem B (Leite → Açúcar):");
        printCoffeeDetails(coffee6b);
    }
    
    private static void printCoffeeDetails(Coffee coffee) {
        System.out.println("   📋 Descrição: " + coffee.getDescription());
        System.out.println("   💰 Custo: R$ " + String.format("%.2f", coffee.getCost()));
        System.out.println("   📏 Tamanho: " + coffee.getSize());
    }
}

