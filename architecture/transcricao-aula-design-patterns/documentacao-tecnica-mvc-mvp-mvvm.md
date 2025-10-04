# Documentação Técnica: Padrões Arquiteturais MVC, MVP e MVVM

## 📋 Informações do Documento

- **Título**: Padrões Arquiteturais MVC, MVP e MVVM
- **Versão**: 1.0
- **Data**: [Data atual]
- **Autor**: Sistema de Documentação Automática
- **Tipo**: Documentação Técnica
- **Tecnologia**: Flutter/Dart
- **Nível**: Intermediário a Avançado

## 🎯 Objetivo

Este documento apresenta uma análise técnica detalhada dos padrões arquiteturais **MVC (Model-View-Controller)**, **MVP (Model-View-Presenter)** e **MVVM (Model-View-ViewModel)** no contexto do desenvolvimento Flutter, incluindo implementações práticas, comparações técnicas e diretrizes de uso.

## 📚 Visão Geral dos Padrões

### **Definições Fundamentais**

#### **MVC (Model-View-Controller)**
- **Model**: Representa dados e regras de negócio
- **View**: Interface do usuário
- **Controller**: Intermediário entre Model e View

#### **MVP (Model-View-Presenter)**
- **Model**: Dados e regras de negócio
- **View**: Interface passiva
- **Presenter**: Lógica de apresentação

#### **MVVM (Model-View-ViewModel)**
- **Model**: Dados e regras de negócio
- **View**: Interface reativa
- **ViewModel**: Estado e lógica de apresentação

## 🏗️ Análise Técnica Detalhada

### **1. MVC (Model-View-Controller)**

#### **Características Técnicas**
- **Acoplamento**: Médio
- **Testabilidade**: Média
- **Reatividade**: Manual
- **Complexidade**: Baixa
- **Manutenibilidade**: Média

#### **Estrutura Técnica**
```dart
// Model
class Pessoa {
  final double altura;
  final double peso;
  
  Pessoa({required this.altura, required this.peso});
  
  double calcularIMC() => peso / (altura * altura);
  
  String getClassificacao() {
    final imc = calcularIMC();
    if (imc < 18.5) return "Abaixo do peso";
    if (imc < 25) return "Normal";
    if (imc < 30) return "Sobrepeso";
    return "Obesidade";
  }
}

// Controller
class HomeController {
  Pessoa? _pessoa;
  String _resultado = "";
  
  String get resultado => _resultado;
  
  void calcularIMC(double altura, double peso) {
    _pessoa = Pessoa(altura: altura, peso: peso);
    _resultado = "IMC: ${_pessoa!.calcularIMC().toStringAsFixed(1)} - ${_pessoa!.getClassificacao()}";
  }
}

// View
class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _controller = HomeController();
  final _alturaController = TextEditingController();
  final _pesoController = TextEditingController();
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Calculadora IMC - MVC")),
      body: Column(
        children: [
          TextField(
            controller: _alturaController,
            decoration: InputDecoration(labelText: "Altura (m)"),
            keyboardType: TextInputType.number,
          ),
          TextField(
            controller: _pesoController,
            decoration: InputDecoration(labelText: "Peso (kg)"),
            keyboardType: TextInputType.number,
          ),
          ElevatedButton(
            onPressed: () {
              final altura = double.tryParse(_alturaController.text) ?? 0;
              final peso = double.tryParse(_pesoController.text) ?? 0;
              _controller.calcularIMC(altura, peso);
              setState(() {});
            },
            child: Text("Calcular IMC"),
          ),
          if (_controller.resultado.isNotEmpty)
            Padding(
              padding: EdgeInsets.all(16),
              child: Text(
                _controller.resultado,
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ),
        ],
      ),
    );
  }
}
```

#### **Vantagens Técnicas**
- ✅ Implementação simples
- ✅ Curva de aprendizado baixa
- ✅ Adequado para aplicações pequenas
- ✅ Separação básica de responsabilidades

#### **Desvantagens Técnicas**
- ❌ Acoplamento entre View e Controller
- ❌ Dificuldade para testes unitários
- ❌ Reatividade manual (setState)
- ❌ Escalabilidade limitada

### **2. MVP (Model-View-Presenter)**

#### **Características Técnicas**
- **Acoplamento**: Baixo
- **Testabilidade**: Alta
- **Reatividade**: Manual
- **Complexidade**: Média
- **Manutenibilidade**: Alta

#### **Estrutura Técnica**
```dart
// Model (mesmo do MVC)
class Pessoa {
  final double altura;
  final double peso;
  
  Pessoa({required this.altura, required this.peso});
  
  double calcularIMC() => peso / (altura * altura);
  
  String getClassificacao() {
    final imc = calcularIMC();
    if (imc < 18.5) return "Abaixo do peso";
    if (imc < 25) return "Normal";
    if (imc < 30) return "Sobrepeso";
    return "Obesidade";
  }
}

// View Interface
abstract class IHomeView {
  void mostrarResultado(String resultado);
  void mostrarErro(String erro);
}

// Presenter
class HomePresenter {
  final IHomeView _view;
  final Pessoa _model;
  
  HomePresenter(this._view, this._model);
  
  void calcularIMC(double altura, double peso) {
    try {
      if (altura <= 0 || peso <= 0) {
        _view.mostrarErro("Altura e peso devem ser maiores que zero");
        return;
      }
      
      final pessoa = Pessoa(altura: altura, peso: peso);
      final imc = pessoa.calcularIMC();
      final classificacao = pessoa.getClassificacao();
      
      _view.mostrarResultado("IMC: ${imc.toStringAsFixed(1)} - $classificacao");
    } catch (e) {
      _view.mostrarErro("Erro ao calcular IMC: ${e.toString()}");
    }
  }
}

// View Implementation
class HomePage extends StatefulWidget implements IHomeView {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late HomePresenter _presenter;
  final _alturaController = TextEditingController();
  final _pesoController = TextEditingController();
  String _resultado = "";
  String _erro = "";
  
  @override
  void initState() {
    super.initState();
    _presenter = HomePresenter(this, Pessoa(altura: 0, peso: 0));
  }
  
  @override
  void mostrarResultado(String resultado) {
    setState(() {
      _resultado = resultado;
      _erro = "";
    });
  }
  
  @override
  void mostrarErro(String erro) {
    setState(() {
      _erro = erro;
      _resultado = "";
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Calculadora IMC - MVP")),
      body: Column(
        children: [
          TextField(
            controller: _alturaController,
            decoration: InputDecoration(labelText: "Altura (m)"),
            keyboardType: TextInputType.number,
          ),
          TextField(
            controller: _pesoController,
            decoration: InputDecoration(labelText: "Peso (kg)"),
            keyboardType: TextInputType.number,
          ),
          ElevatedButton(
            onPressed: () {
              final altura = double.tryParse(_alturaController.text) ?? 0;
              final peso = double.tryParse(_pesoController.text) ?? 0;
              _presenter.calcularIMC(altura, peso);
            },
            child: Text("Calcular IMC"),
          ),
          if (_resultado.isNotEmpty)
            Padding(
              padding: EdgeInsets.all(16),
              child: Text(
                _resultado,
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.green),
              ),
            ),
          if (_erro.isNotEmpty)
            Padding(
              padding: EdgeInsets.all(16),
              child: Text(
                _erro,
                style: TextStyle(fontSize: 16, color: Colors.red),
              ),
            ),
        ],
      ),
    );
  }
}
```

#### **Vantagens Técnicas**
- ✅ Baixo acoplamento
- ✅ Alta testabilidade
- ✅ Separação clara de responsabilidades
- ✅ Interface bem definida

#### **Desvantagens Técnicas**
- ❌ Complexidade adicional
- ❌ Reatividade ainda manual
- ❌ Mais código boilerplate
- ❌ Curva de aprendizado média

### **3. MVVM (Model-View-ViewModel)**

#### **Características Técnicas**
- **Acoplamento**: Muito Baixo
- **Testabilidade**: Muito Alta
- **Reatividade**: Automática
- **Complexidade**: Média
- **Manutenibilidade**: Muito Alta

#### **Estrutura Técnica**
```dart
// Model (mesmo dos anteriores)
class Pessoa {
  final double altura;
  final double peso;
  
  Pessoa({required this.altura, required this.peso});
  
  double calcularIMC() => peso / (altura * altura);
  
  String getClassificacao() {
    final imc = calcularIMC();
    if (imc < 18.5) return "Abaixo do peso";
    if (imc < 25) return "Normal";
    if (imc < 30) return "Sobrepeso";
    return "Obesidade";
  }
}

// ViewModel
class HomeViewModel extends ChangeNotifier {
  double _altura = 0;
  double _peso = 0;
  String _resultado = "";
  String _erro = "";
  bool _isLoading = false;
  
  // Getters
  double get altura => _altura;
  double get peso => _peso;
  String get resultado => _resultado;
  String get erro => _erro;
  bool get isLoading => _isLoading;
  bool get hasResultado => _resultado.isNotEmpty;
  bool get hasErro => _erro.isNotEmpty;
  
  // Setters
  void setAltura(double valor) {
    _altura = valor;
    _clearResultado();
    _calcularIMC();
    notifyListeners();
  }
  
  void setPeso(double valor) {
    _peso = valor;
    _clearResultado();
    _calcularIMC();
    notifyListeners();
  }
  
  // Métodos privados
  void _clearResultado() {
    _resultado = "";
    _erro = "";
  }
  
  void _calcularIMC() {
    if (_altura <= 0 || _peso <= 0) {
      _erro = "Altura e peso devem ser maiores que zero";
      notifyListeners();
      return;
    }
    
    try {
      final pessoa = Pessoa(altura: _altura, peso: _peso);
      final imc = pessoa.calcularIMC();
      final classificacao = pessoa.getClassificacao();
      _resultado = "IMC: ${imc.toStringAsFixed(1)} - $classificacao";
      _erro = "";
    } catch (e) {
      _erro = "Erro ao calcular IMC: ${e.toString()}";
      _resultado = "";
    }
    
    notifyListeners();
  }
  
  // Métodos públicos
  void limpar() {
    _altura = 0;
    _peso = 0;
    _clearResultado();
    notifyListeners();
  }
}

// View
class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => HomeViewModel(),
      child: Consumer<HomeViewModel>(
        builder: (context, viewModel, child) {
          return Scaffold(
            appBar: AppBar(
              title: Text("Calculadora IMC - MVVM"),
              actions: [
                IconButton(
                  icon: Icon(Icons.clear),
                  onPressed: viewModel.limpar,
                ),
              ],
            ),
            body: Padding(
              padding: EdgeInsets.all(16),
              child: Column(
                children: [
                  TextField(
                    onChanged: (valor) => viewModel.setAltura(double.tryParse(valor) ?? 0),
                    decoration: InputDecoration(
                      labelText: "Altura (m)",
                      hintText: "Ex: 1.75",
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.number,
                  ),
                  SizedBox(height: 16),
                  TextField(
                    onChanged: (valor) => viewModel.setPeso(double.tryParse(valor) ?? 0),
                    decoration: InputDecoration(
                      labelText: "Peso (kg)",
                      hintText: "Ex: 70",
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.number,
                  ),
                  SizedBox(height: 24),
                  if (viewModel.hasResultado)
                    Container(
                      width: double.infinity,
                      padding: EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.green.shade50,
                        border: Border.all(color: Colors.green),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        viewModel.resultado,
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.green.shade800,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  if (viewModel.hasErro)
                    Container(
                      width: double.infinity,
                      padding: EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.red.shade50,
                        border: Border.all(color: Colors.red),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        viewModel.erro,
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.red.shade800,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
```

#### **Vantagens Técnicas**
- ✅ Muito baixo acoplamento
- ✅ Reatividade automática
- ✅ Alta testabilidade
- ✅ Excelente manutenibilidade
- ✅ Escalabilidade

#### **Desvantagens Técnicas**
- ❌ Curva de aprendizado média
- ❌ Complexidade inicial
- ❌ Overhead de reatividade
- ❌ Debugging mais complexo

## 📊 Comparação Técnica Detalhada

### **Métricas de Qualidade**

| Métrica | MVC | MVP | MVVM |
|---------|-----|-----|------|
| **Acoplamento** | 6/10 | 8/10 | 9/10 |
| **Coesão** | 6/10 | 8/10 | 9/10 |
| **Testabilidade** | 5/10 | 8/10 | 9/10 |
| **Manutenibilidade** | 6/10 | 8/10 | 9/10 |
| **Reatividade** | 3/10 | 3/10 | 9/10 |
| **Performance** | 8/10 | 8/10 | 7/10 |
| **Escalabilidade** | 5/10 | 7/10 | 9/10 |
| **Complexidade** | 3/10 | 6/10 | 7/10 |

### **Análise de Complexidade Ciclomática**

#### **MVC**
- **Complexidade**: Baixa
- **Pontos de decisão**: 2-3 por método
- **Manutenibilidade**: Média

#### **MVP**
- **Complexidade**: Média
- **Pontos de decisão**: 3-5 por método
- **Manutenibilidade**: Alta

#### **MVVM**
- **Complexidade**: Média-Alta
- **Pontos de decisão**: 4-6 por método
- **Manutenibilidade**: Muito Alta

## 🧪 Estratégias de Teste

### **Testes Unitários por Padrão**

#### **MVC - Testes**
```dart
void main() {
  group('MVC Tests', () {
    test('Model - Pessoa deve calcular IMC corretamente', () {
      final pessoa = Pessoa(altura: 1.75, peso: 70);
      expect(pessoa.calcularIMC(), closeTo(22.86, 0.01));
    });
    
    test('Controller - deve calcular IMC', () {
      final controller = HomeController();
      controller.calcularIMC(1.75, 70);
      expect(controller.resultado, contains("22.9"));
    });
  });
}
```

#### **MVP - Testes**
```dart
void main() {
  group('MVP Tests', () {
    test('Presenter - deve calcular IMC corretamente', () {
      final mockView = MockHomeView();
      final presenter = HomePresenter(mockView, Pessoa(altura: 0, peso: 0));
      
      presenter.calcularIMC(1.75, 70);
      
      verify(mockView.mostrarResultado(any)).called(1);
    });
  });
}

class MockHomeView extends Mock implements IHomeView {}
```

#### **MVVM - Testes**
```dart
void main() {
  group('MVVM Tests', () {
    test('ViewModel - deve calcular IMC automaticamente', () {
      final viewModel = HomeViewModel();
      
      viewModel.setAltura(1.75);
      viewModel.setPeso(70);
      
      expect(viewModel.resultado, contains("22.9"));
      expect(viewModel.hasResultado, isTrue);
    });
    
    test('ViewModel - deve mostrar erro para valores inválidos', () {
      final viewModel = HomeViewModel();
      
      viewModel.setAltura(-1);
      viewModel.setPeso(70);
      
      expect(viewModel.hasErro, isTrue);
      expect(viewModel.erro, contains("maiores que zero"));
    });
  });
}
```

### **Cobertura de Testes Recomendada**

| Padrão | Cobertura Mínima | Cobertura Ideal |
|--------|------------------|-----------------|
| **MVC** | 70% | 85% |
| **MVP** | 80% | 90% |
| **MVVM** | 85% | 95% |

## 🚀 Performance e Otimização

### **Análise de Performance**

#### **MVC**
- **Renderização**: Manual (setState)
- **Memory Usage**: Baixo
- **CPU Usage**: Baixo
- **Battery Impact**: Baixo

#### **MVP**
- **Renderização**: Manual (setState)
- **Memory Usage**: Baixo-Médio
- **CPU Usage**: Baixo-Médio
- **Battery Impact**: Baixo-Médio

#### **MVVM**
- **Renderização**: Automática (ChangeNotifier)
- **Memory Usage**: Médio
- **CPU Usage**: Médio
- **Battery Impact**: Médio

### **Otimizações Recomendadas**

#### **Para MVC**
```dart
// Use const constructors quando possível
const Text("Calculadora IMC")

// Evite rebuilds desnecessários
if (mounted) setState(() {});
```

#### **Para MVP**
```dart
// Use interfaces para baixo acoplamento
abstract class IHomeView {
  void mostrarResultado(String resultado);
}

// Implemente validação no Presenter
void calcularIMC(double altura, double peso) {
  if (altura <= 0 || peso <= 0) {
    _view.mostrarErro("Valores inválidos");
    return;
  }
  // ... resto da lógica
}
```

#### **Para MVVM**
```dart
// Use ValueNotifier para valores simples
class HomeViewModel extends ChangeNotifier {
  final ValueNotifier<double> altura = ValueNotifier(0);
  final ValueNotifier<double> peso = ValueNotifier(0);
  
  // Otimize notificações
  void _calcularIMC() {
    if (_altura <= 0 || _peso <= 0) return;
    // ... lógica
    notifyListeners();
  }
}
```

## 🔧 Ferramentas e Bibliotecas

### **Para MVC**
- **State Management**: setState nativo
- **Testing**: flutter_test
- **Dependency Injection**: Manual

### **Para MVP**
- **State Management**: setState + Interfaces
- **Testing**: flutter_test + mockito
- **Dependency Injection**: Manual

### **Para MVVM**
- **State Management**: Provider, Riverpod, BLoC
- **Testing**: flutter_test + mockito
- **Dependency Injection**: Provider, GetIt

### **Bibliotecas Recomendadas**

#### **Provider (MVVM)**
```yaml
dependencies:
  provider: ^6.0.0
```

#### **Riverpod (MVVM Avançado)**
```yaml
dependencies:
  flutter_riverpod: ^2.0.0
```

#### **BLoC (MVVM Alternativo)**
```yaml
dependencies:
  flutter_bloc: ^8.0.0
```

## 📋 Diretrizes de Implementação

### **1. Escolha do Padrão**

#### **Use MVC quando:**
- Aplicação simples (< 10 telas)
- Equipe pequena (< 3 desenvolvedores)
- Protótipo ou MVP
- Curva de aprendizado deve ser baixa

#### **Use MVP quando:**
- Aplicação média (10-50 telas)
- Testes são importantes
- Equipe intermediária (3-8 desenvolvedores)
- Manutenibilidade é prioridade

#### **Use MVVM quando:**
- Aplicação complexa (> 50 telas)
- Reatividade é importante
- Equipe experiente (> 8 desenvolvedores)
- Escalabilidade é crítica

### **2. Boas Práticas por Padrão**

#### **MVC - Boas Práticas**
```dart
// ✅ Faça
class HomeController {
  String _resultado = "";
  String get resultado => _resultado;
  
  void calcularIMC(double altura, double peso) {
    // Lógica aqui
  }
}

// ❌ Evite
class HomeController {
  String resultado = ""; // Campo público
}
```

#### **MVP - Boas Práticas**
```dart
// ✅ Faça
abstract class IHomeView {
  void mostrarResultado(String resultado);
}

class HomePresenter {
  final IHomeView _view;
  HomePresenter(this._view);
}

// ❌ Evite
class HomePresenter {
  HomePage _view; // Acoplamento forte
}
```

#### **MVVM - Boas Práticas**
```dart
// ✅ Faça
class HomeViewModel extends ChangeNotifier {
  double _altura = 0;
  double get altura => _altura;
  
  void setAltura(double valor) {
    _altura = valor;
    _calcularIMC();
    notifyListeners();
  }
}

// ❌ Evite
class HomeViewModel extends ChangeNotifier {
  double altura = 0; // Campo público
}
```

### **3. Padrões de Nomenclatura**

#### **MVC**
- **Model**: `Pessoa`, `Usuario`, `Produto`
- **View**: `HomePage`, `LoginPage`, `ProfilePage`
- **Controller**: `HomeController`, `LoginController`

#### **MVP**
- **Model**: `Pessoa`, `Usuario`, `Produto`
- **View**: `IHomeView`, `ILoginView`
- **Presenter**: `HomePresenter`, `LoginPresenter`

#### **MVVM**
- **Model**: `Pessoa`, `Usuario`, `Produto`
- **View**: `HomePage`, `LoginPage`
- **ViewModel**: `HomeViewModel`, `LoginViewModel`

## 🎯 Casos de Uso Específicos

### **Aplicações Financeiras**
- **Padrão Recomendado**: MVVM
- **Justificativa**: Reatividade, complexidade, testes críticos

### **Aplicações de E-commerce**
- **Padrão Recomendado**: MVVM
- **Justificativa**: Estado complexo, múltiplas telas, performance

### **Aplicações de Produtividade**
- **Padrão Recomendado**: MVP
- **Justificativa**: Testabilidade, manutenibilidade

### **Prototipagem Rápida**
- **Padrão Recomendado**: MVC
- **Justificativa**: Simplicidade, velocidade de desenvolvimento

## 📚 Recursos e Referências

### **Documentação Oficial**
- [Flutter Architecture](https://flutter.dev/docs/development/data-and-backend/state-mgmt)
- [Provider Package](https://pub.dev/packages/provider)
- [BLoC Library](https://bloclibrary.dev/)

### **Livros Técnicos**
- "Clean Architecture" - Robert C. Martin
- "Design Patterns" - Gang of Four
- "Flutter in Action" - Eric Windmill

### **Artigos e Tutoriais**
- [Flutter State Management](https://flutter.dev/docs/development/data-and-backend/state-mgmt)
- [Provider Tutorial](https://flutter.dev/docs/development/data-and-backend/state-mgmt/simple)
- [BLoC Pattern](https://bloclibrary.dev/#/flutterbloccoreconcepts)

---

**Revisado por**: [Nome do Revisor]  
**Aprovado por**: [Nome do Aprovador]  
**Status**: [Rascunho/Em Revisão/Aprovado/Implementado]
