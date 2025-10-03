# Template: BDD (Behavior Driven Development)

## Informações Básicas
- **ID do BDD**: [BDD-XXX]
- **Funcionalidade**: [Nome da funcionalidade]
- **Versão**: [1.0]
- **Data de Criação**: [DD/MM/AAAA]
- **Última Atualização**: [DD/MM/AAAA]
- **Autor**: [Nome do Analista]
- **Linguagem**: Português (Gherkin)

## Descrição da Funcionalidade

### User Story Relacionada
```
Como [papel do usuário]
Quero [funcionalidade/objetivo]
Para que [benefício/valor de negócio]
```

### Contexto
[Descrição do contexto da funcionalidade e como ela se encaixa no sistema]

## Especificação BDD (Gherkin)

### Funcionalidade Principal
```gherkin
Funcionalidade: [Nome da funcionalidade]
  Como [papel do usuário]
  Quero [objetivo/funcionalidade]
  Para que [benefício/valor de negócio]
```

### Cenários de Sucesso

#### Cenário 1: [Nome do Cenário Principal]
```gherkin
Cenário: [Nome descritivo do cenário]
  Dado que [condição inicial/pré-requisito]
    E [condição adicional se necessário]
  Quando [ação do usuário]
    E [ação adicional se necessário]
  Então [resultado esperado]
    E [resultado adicional se necessário]
```

#### Cenário 2: [Nome do Cenário Alternativo]
```gherkin
Cenário: [Nome descritivo do cenário]
  Dado que [condição inicial/pré-requisito]
  Quando [ação do usuário]
  Então [resultado esperado]
```

### Cenários de Validação

#### Cenário 3: [Nome do Cenário de Validação]
```gherkin
Cenário: [Nome descritivo do cenário]
  Dado que [condição inicial/pré-requisito]
  Quando [ação do usuário com dados inválidos]
  Então [mensagem de erro esperada]
    E [comportamento do sistema]
```

### Cenários de Exceção

#### Cenário 4: [Nome do Cenário de Exceção]
```gherkin
Cenário: [Nome descritivo do cenário]
  Dado que [condição de erro]
  Quando [ação do usuário]
  Então [tratamento da exceção]
    E [comportamento do sistema]
```

## Palavras-Chave Gherkin

### Palavras Obrigatórias
- **Dado**: Define o estado inicial ou pré-condições
- **Quando**: Define a ação do usuário
- **Então**: Define o resultado esperado

### Palavras de Conexão
- **E**: Adiciona informações à mesma etapa
- **Mas**: Adiciona informações contrárias à etapa

### Exemplo de Uso das Palavras-Chave
```gherkin
Dado que o anunciante esteja cadastrado no sistema
  E tenha realizado autenticação no sistema
Quando o anunciante preencher os campos obrigatórios
  E clicar em salvar
Então o sistema exibe uma mensagem de sucesso
  E o anúncio ficará disponível para agendamento
```

## Regras de Negócio

### Regra 1: [Nome da Regra]
**Descrição**: [Descrição detalhada da regra]
**Aplicação**: [Quando se aplica]
**Exemplo**: [Exemplo prático]

### Regra 2: [Nome da Regra]
**Descrição**: [Descrição detalhada da regra]
**Aplicação**: [Quando se aplica]
**Exemplo**: [Exemplo prático]

## Critérios de Aceite Mapeados

### Critério 1: [Nome do Critério]
- **BDD**: [Referência ao cenário BDD]
- **Descrição**: [Descrição do critério]
- **Validação**: [Como validar]

### Critério 2: [Nome do Critério]
- **BDD**: [Referência ao cenário BDD]
- **Descrição**: [Descrição do critério]
- **Validação**: [Como validar]

## Dados de Teste

### Dados Válidos
- **Campo 1**: [Valor válido 1], [Valor válido 2]
- **Campo 2**: [Valor válido 1], [Valor válido 2]
- **Campo 3**: [Valor válido 1], [Valor válido 2]

### Dados Inválidos
- **Campo 1**: [Valor inválido 1], [Valor inválido 2]
- **Campo 2**: [Valor inválido 1], [Valor inválido 2]
- **Campo 3**: [Valor inválido 1], [Valor inválido 2]

## Cenários de Teste Automatizados

### Configuração
- **Ferramenta**: [Cucumber, SpecFlow, Behave, etc.]
- **Linguagem**: [Java, C#, Python, JavaScript, etc.]
- **Ambiente**: [Desenvolvimento, Teste, Homologação]

### Implementação
```[linguagem]
// Exemplo de implementação dos steps
@Dado("que o anunciante esteja cadastrado no sistema")
public void que_o_anunciante_esteja_cadastrado_no_sistema() {
    // Implementação do step
}

@Quando("o anunciante preencher os campos obrigatórios")
public void o_anunciante_preencher_os_campos_obrigatorios() {
    // Implementação do step
}

@Entao("o sistema exibe uma mensagem de sucesso")
public void o_sistema_exibe_uma_mensagem_de_sucesso() {
    // Implementação do step
}
```

## Rastreabilidade

### User Story Relacionada
- **ID**: [US-XXX]
- **Título**: [Título da User Story]
- **Link**: [Link para a User Story]

### Use Case Relacionado
- **ID**: [UC-XXX]
- **Título**: [Título do Use Case]
- **Link**: [Link para o Use Case]

### Testes Relacionados
- **Teste Unitário**: [ID do teste]
- **Teste de Integração**: [ID do teste]
- **Teste de Aceitação**: [ID do teste]

## Notas de Implementação

### Considerações Técnicas
- [Observações sobre a implementação]
- [Tecnologias envolvidas]
- [Integrações necessárias]

### Riscos Identificados
- [Risco 1]: [Descrição e mitigação]
- [Risco 2]: [Descrição e mitigação]

### Estimativas
- **Complexidade**: [Baixa/Média/Alta]
- **Esforço Estimado**: [X horas/dias]
- **Prioridade**: [Baixa/Média/Alta/Crítica]

## Validação e Aprovação

### Checklist de Validação
- [ ] Todos os cenários estão mapeados
- [ ] Palavras-chave Gherkin estão corretas
- [ ] Cenários cobrem casos de sucesso e exceção
- [ ] Regras de negócio estão documentadas
- [ ] Dados de teste estão definidos
- [ ] Rastreabilidade está estabelecida

### Aprovações
- **Analista de Negócio**: [Nome] - [Data]
- **Product Owner**: [Nome] - [Data]
- **Tech Lead**: [Nome] - [Data]

---

**Revisado por**: [Nome do Revisor]
**Aprovado por**: [Nome do Aprovador]
**Status**: [Rascunho/Em Revisão/Aprovado/Implementado]
