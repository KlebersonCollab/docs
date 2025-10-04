# Aula: Design Patterns em Flutter - MVC, MVP e MVVM

## 📚 Informações da Aula

- **Título**: Design Patterns em Flutter - MVC, MVP e MVVM
- **Instrutor**: Jacob Moura
- **Duração**: Aproximadamente 2-3 horas
- **Nível**: Intermediário
- **Tecnologia**: Flutter
- **Data**: [Data da transcrição]
- **Formato**: Live/Workshop

## 🎯 Objetivos da Aula

### **Objetivos Gerais**
- Compreender os conceitos de design patterns em desenvolvimento mobile
- Diferenciar entre MVC, MVP e MVVM
- Aplicar padrões arquiteturais em projetos Flutter
- Implementar state management adequado
- Seguir boas práticas de desenvolvimento

### **Objetivos Específicos**
- Entender quando usar cada padrão arquitetural
- Implementar separação de responsabilidades
- Criar aplicações reativas com Flutter
- Aplicar testes unitários em arquiteturas bem estruturadas
- Desenvolver aplicações escaláveis e manuteníveis

## 📋 Conteúdo Programático

### **1. Introdução aos Design Patterns**
- **Conceitos fundamentais**
- **Importância dos padrões arquiteturais**
- **Evolução dos padrões no desenvolvimento mobile**
- **Benefícios da aplicação de padrões**

### **2. MVC (Model-View-Controller)**
- **Conceitos fundamentais**
- **Estrutura e responsabilidades**
- **Implementação em Flutter**
- **Vantagens e desvantagens**
- **Quando usar MVC**

### **3. MVP (Model-View-Presenter)**
- **Diferenças entre MVC e MVP**
- **Estrutura e responsabilidades**
- **Implementação em Flutter**
- **Casos de uso apropriados**

### **4. MVVM (Model-View-ViewModel)**
- **Conceitos de MVVM**
- **Reatividade e data binding**
- **Implementação em Flutter**
- **State management com MVVM**

### **5. Exemplo Prático: Calculadora de IMC**
- **Análise do problema**
- **Implementação com MVC**
- **Refatoração para MVVM**
- **Comparação das abordagens**

### **6. Boas Práticas**
- **Separação de responsabilidades**
- **Testabilidade**
- **Manutenibilidade**
- **Escalabilidade**

## 🛠️ Exemplo Prático: Calculadora de IMC

### **Descrição do Projeto**
Desenvolvimento de uma calculadora de IMC (Índice de Massa Corporal) utilizando diferentes padrões arquiteturais para demonstrar as diferenças práticas entre MVC, MVP e MVVM.

### **Funcionalidades**
- **Entrada de dados**: Altura e peso
- **Cálculo automático**: IMC baseado na fórmula peso/(altura²)
- **Classificação**: Abaixo do peso, normal, sobrepeso, obesidade
- **Interface reativa**: Atualização automática dos resultados

### **Implementação MVC**

#### **Model (Pessoa)**
```dart
class Pessoa {
  double altura;
  double peso;
  
  Pessoa({required this.altura, required this.peso});
  
  double calcularIMC() {
    return peso / (altura * altura);
  }
  
  String getClassificacao() {
    double imc = calcularIMC();
    if (imc < 18.5) return "Abaixo do peso";
    if (imc < 25) return "Normal";
    if (imc < 30) return "Sobrepeso";
    return "Obesidade";
  }
}
```

#### **Controller**
```dart
class HomeController {
  Pessoa? _pessoa;
  String _resultado = "";
  
  String get resultado => _resultado;
  
  void calcularIMC(double altura, double peso) {
    _pessoa = Pessoa(altura: altura, peso: peso);
    _resultado = "IMC: ${_pessoa!.calcularIMC().toStringAsFixed(1)} - ${_pessoa!.getClassificacao()}";
  }
}
```

#### **View**
```dart
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
      appBar: AppBar(title: Text("Calculadora IMC")),
      body: Column(
        children: [
          TextField(
            controller: _alturaController,
            decoration: InputDecoration(labelText: "Altura (m)"),
          ),
          TextField(
            controller: _pesoController,
            decoration: InputDecoration(labelText: "Peso (kg)"),
          ),
          ElevatedButton(
            onPressed: () {
              _controller.calcularIMC(
                double.parse(_alturaController.text),
                double.parse(_pesoController.text),
              );
              setState(() {});
            },
            child: Text("Calcular"),
          ),
          Text(_controller.resultado),
        ],
      ),
    );
  }
}
```

### **Implementação MVVM**

#### **ViewModel**
```dart
class HomeViewModel extends ChangeNotifier {
  double _altura = 0;
  double _peso = 0;
  String _resultado = "";
  
  double get altura => _altura;
  double get peso => _peso;
  String get resultado => _resultado;
  
  void setAltura(double valor) {
    _altura = valor;
    _calcularIMC();
    notifyListeners();
  }
  
  void setPeso(double valor) {
    _peso = valor;
    _calcularIMC();
    notifyListeners();
  }
  
  void _calcularIMC() {
    if (_altura > 0 && _peso > 0) {
      final pessoa = Pessoa(altura: _altura, peso: _peso);
      _resultado = "IMC: ${pessoa.calcularIMC().toStringAsFixed(1)} - ${pessoa.getClassificacao()}";
    }
  }
}
```

#### **View Reativa**
```dart
class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => HomeViewModel(),
      child: Consumer<HomeViewModel>(
        builder: (context, viewModel, child) {
          return Scaffold(
            appBar: AppBar(title: Text("Calculadora IMC")),
            body: Column(
              children: [
                TextField(
                  onChanged: (valor) => viewModel.setAltura(double.tryParse(valor) ?? 0),
                  decoration: InputDecoration(labelText: "Altura (m)"),
                ),
                TextField(
                  onChanged: (valor) => viewModel.setPeso(double.tryParse(valor) ?? 0),
                  decoration: InputDecoration(labelText: "Peso (kg)"),
                ),
                Text(viewModel.resultado),
              ],
            ),
          );
        },
      ),
    );
  }
}
```

## 🔍 Análise Comparativa dos Padrões

### **MVC vs MVP vs MVVM**

| Aspecto | MVC | MVP | MVVM |
|---------|-----|-----|------|
| **Acoplamento** | Médio | Baixo | Muito Baixo |
| **Testabilidade** | Média | Alta | Muito Alta |
| **Reatividade** | Manual | Manual | Automática |
| **Complexidade** | Baixa | Média | Média |
| **Manutenibilidade** | Média | Alta | Muito Alta |
| **Casos de Uso** | Aplicações simples | Aplicações médias | Aplicações complexas |

### **Quando Usar Cada Padrão**

#### **MVC**
- ✅ Aplicações simples
- ✅ Protótipos rápidos
- ✅ Equipes pequenas
- ❌ Aplicações complexas
- ❌ Muitas interações

#### **MVP**
- ✅ Aplicações médias
- ✅ Testes importantes
- ✅ Equipes intermediárias
- ❌ Aplicações muito simples
- ❌ Aplicações muito complexas

#### **MVVM**
- ✅ Aplicações complexas
- ✅ Reatividade importante
- ✅ Equipes experientes
- ✅ Manutenibilidade crítica
- ❌ Aplicações muito simples

## 🧪 Testes Unitários

### **Testando o Model**
```dart
void main() {
  group('Pessoa', () {
    test('deve calcular IMC corretamente', () {
      final pessoa = Pessoa(altura: 1.75, peso: 70);
      expect(pessoa.calcularIMC(), closeTo(22.86, 0.01));
    });
    
    test('deve classificar IMC corretamente', () {
      final pessoa = Pessoa(altura: 1.75, peso: 70);
      expect(pessoa.getClassificacao(), equals("Normal"));
    });
  });
}
```

### **Testando o ViewModel**
```dart
void main() {
  group('HomeViewModel', () {
    test('deve calcular IMC automaticamente', () {
      final viewModel = HomeViewModel();
      viewModel.setAltura(1.75);
      viewModel.setPeso(70);
      expect(viewModel.resultado, contains("22.9"));
    });
  });
}
```

## 📚 Boas Práticas

### **1. Separação de Responsabilidades**
- **Model**: Apenas dados e regras de negócio
- **View**: Apenas apresentação
- **Controller/Presenter/ViewModel**: Apenas lógica de apresentação

### **2. Testabilidade**
- Escreva testes unitários para cada camada
- Use injeção de dependência
- Evite acoplamento forte

### **3. Reatividade**
- Use ChangeNotifier para MVVM
- Implemente data binding
- Evite setState manual

### **4. Manutenibilidade**
- Documente decisões arquiteturais
- Use nomes descritivos
- Mantenha código limpo

### **5. Escalabilidade**
- Planeje para crescimento
- Use padrões consistentes
- Documente arquitetura

## 🎯 Exercícios Práticos

### **Exercício 1: Refatoração MVC para MVVM**
1. Pegue o exemplo MVC da calculadora de IMC
2. Refatore para MVVM
3. Implemente reatividade
4. Adicione testes unitários

### **Exercício 2: Nova Funcionalidade**
1. Adicione validação de entrada
2. Implemente histórico de cálculos
3. Adicione persistência local
4. Crie testes de integração

### **Exercício 3: Aplicação Completa**
1. Crie uma aplicação de lista de tarefas
2. Implemente CRUD completo
3. Use MVVM com Provider
4. Adicione testes completos

## 📖 Recursos Adicionais

### **Documentação Oficial**
- [Flutter Architecture](https://flutter.dev/docs/development/data-and-backend/state-mgmt)
- [Provider Package](https://pub.dev/packages/provider)
- [BLoC Pattern](https://bloclibrary.dev/)

### **Livros Recomendados**
- "Clean Architecture" - Robert C. Martin
- "Design Patterns" - Gang of Four
- "Flutter in Action" - Eric Windmill

### **Cursos e Tutoriais**
- [Flutter Official Codelabs](https://flutter.dev/docs/codelabs)
- [Provider Tutorial](https://flutter.dev/docs/development/data-and-backend/state-mgmt/simple)
- [BLoC Tutorial](https://bloclibrary.dev/#/flutterbloccoreconcepts)

## 🎓 Avaliação

### **Critérios de Avaliação**
- [ ] Compreensão dos conceitos
- [ ] Implementação correta dos padrões
- [ ] Qualidade do código
- [ ] Cobertura de testes
- [ ] Documentação adequada

### **Projeto Final**
Desenvolva uma aplicação Flutter utilizando MVVM que demonstre:
- Separação adequada de responsabilidades
- Reatividade implementada
- Testes unitários
- Código limpo e documentado

## 📝 Conclusão

### **Principais Aprendizados**
1. **Design patterns** são fundamentais para código limpo e manutenível
2. **MVVM** é ideal para aplicações Flutter complexas
3. **Reatividade** melhora significativamente a experiência do usuário
4. **Testes** são essenciais para arquiteturas bem estruturadas
5. **Separação de responsabilidades** facilita manutenção e evolução

### **Próximos Passos**
1. Pratique implementando os padrões
2. Estude outros padrões como BLoC e GetX
3. Aplique em projetos reais
4. Continue aprendendo sobre arquitetura limpa

---

**Instrutor**: Jacob Moura  
**Data**: [Data da aula]  
**Versão**: 1.0
