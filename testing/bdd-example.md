# Exemplo Prático: BDD - Cadastrar Anúncio

## Informações Básicas
- **ID do BDD**: BDD-001
- **Funcionalidade**: Cadastrar Anúncio
- **Versão**: 1.0
- **Data de Criação**: 03/10/2025
- **Autor**: Equipe de Desenvolvimento
- **Linguagem**: Português (Gherkin)

## Descrição da Funcionalidade

### User Story Relacionada
```
Como anunciante
Quero publicar um anúncio do meu serviço
Para que clientes possam agendar a realização desse serviço
```

### Contexto
Esta funcionalidade permite que anunciantes cadastrem anúncios de serviços, definindo periodicidade (dia, hora, semana), tipo (gratuito ou pago) e disponibilizando para agendamento pelos clientes.

## Especificação BDD (Gherkin)

### Funcionalidade Principal
```gherkin
Funcionalidade: Cadastrar Anúncio
  Como anunciante
  Quero cadastrar um anúncio do meu serviço
  Para que clientes possam agendar a realização desse serviço
```

### Cenários de Sucesso

#### Cenário 1: Cadastro com Sucesso
```gherkin
Cenário: Cadastro de anúncio com sucesso
  Dado que o anunciante esteja cadastrado no sistema
    E tenha realizado autenticação no sistema
  Quando o anunciante preencher os campos obrigatórios
    E clicar em salvar
  Então o sistema exibe uma mensagem de sucesso
    E o anúncio ficará disponível para agendamento
```

#### Cenário 2: Definir Periodicidade do Anúncio
```gherkin
Cenário: Definir periodicidade do anúncio
  Dado que o anunciante esteja logado no sistema
  Quando o anunciante selecionar a periodicidade "por dia"
    E preencher os campos obrigatórios
  Então o sistema salva o anúncio com periodicidade diária
    E o anúncio fica disponível para agendamento
```

#### Cenário 3: Criar Anúncio Gratuito
```gherkin
Cenário: Criar anúncio gratuito
  Dado que o anunciante esteja logado no sistema
  Quando o anunciante selecionar "anúncio gratuito"
    E preencher os campos obrigatórios
  Então o sistema salva o anúncio como gratuito
    E o anúncio fica disponível para agendamento
```

#### Cenário 4: Validar Cálculo de Pagamento
```gherkin
Cenário: Validar cálculo de pagamento por periodicidade
  Dado que o anunciante esteja logado no sistema
  Quando o anunciante selecionar periodicidade "por hora"
    E definir o valor como R$ 50,00
  Então o sistema calcula o valor por hora como R$ 50,00
    E exibe o valor total calculado
```

### Cenários de Validação

#### Cenário 5: Campos Obrigatórios Não Preenchidos
```gherkin
Cenário: Campos obrigatórios não preenchidos
  Dado que o anunciante esteja logado no sistema
  Quando o anunciante tentar salvar sem preencher campos obrigatórios
  Então o sistema exibe mensagem de erro
    E destaca os campos obrigatórios não preenchidos
```

#### Cenário 6: Dados Inválidos
```gherkin
Cenário: Preenchimento com dados inválidos
  Dado que o anunciante esteja logado no sistema
  Quando o anunciante preencher campos com dados inválidos
  Então o sistema exibe mensagem de erro
    E solicita correção dos dados
```

### Cenários de Exceção

#### Cenário 7: Despublicar Anúncio
```gherkin
Cenário: Despublicar anúncio
  Dado que o anunciante tenha um anúncio publicado
  Quando o anunciante clicar em "despublicar"
  Então o sistema remove o anúncio da disponibilidade
    E o anúncio não ficará disponível para agendamento
```

## Regras de Negócio

### Regra 1: Periodicidade
**Descrição**: Anúncios podem ser definidos por dia, hora, semana ou mês
**Aplicação**: Durante o cadastro do anúncio
**Exemplo**: Anunciante seleciona "por dia" para serviços diários

### Regra 2: Anúncios Gratuitos
**Descrição**: Anúncios podem ser gratuitos ou pagos
**Aplicação**: Durante o cadastro do anúncio
**Exemplo**: Anunciante pode escolher "anúncio gratuito" para promoções

### Regra 3: Cálculo de Pagamento
**Descrição**: O valor é calculado conforme a periodicidade selecionada
**Aplicação**: Durante o cadastro de anúncios pagos
**Exemplo**: R$ 50,00 por hora = R$ 50,00 x 1 hora

## Critérios de Aceite Mapeados

### Critério 1: Cadastro com Sucesso
- **BDD**: Cenário 1
- **Descrição**: Anunciante consegue cadastrar anúncio com sucesso
- **Validação**: Mensagem de sucesso exibida e anúncio disponível

### Critério 2: Periodicidade
- **BDD**: Cenário 2
- **Descrição**: Anunciante pode definir periodicidade do anúncio
- **Validação**: Periodicidade salva corretamente no sistema

### Critério 3: Anúncio Gratuito
- **BDD**: Cenário 3
- **Descrição**: Anunciante pode criar anúncios gratuitos
- **Validação**: Anúncio marcado como gratuito e disponível

### Critério 4: Cálculo de Pagamento
- **BDD**: Cenário 4
- **Descrição**: Sistema calcula valor conforme periodicidade
- **Validação**: Cálculo correto do valor total

### Critério 5: Validação de Campos
- **BDD**: Cenários 5 e 6
- **Descrição**: Sistema valida campos obrigatórios e dados
- **Validação**: Mensagens de erro apropriadas

### Critério 6: Despublicar
- **BDD**: Cenário 7
- **Descrição**: Anunciante pode despublicar anúncios
- **Validação**: Anúncio removido da disponibilidade

## Dados de Teste

### Dados Válidos
- **Título do Anúncio**: "Limpeza Residencial", "Consultoria Empresarial"
- **Descrição**: "Serviço completo de limpeza", "Consultoria em gestão"
- **Valor**: R$ 50,00, R$ 100,00, R$ 200,00
- **Periodicidade**: "por hora", "por dia", "por semana"

### Dados Inválidos
- **Título do Anúncio**: "", "   " (espaços em branco)
- **Descrição**: "" (vazio)
- **Valor**: -R$ 50,00 (negativo), "abc" (texto)
- **Periodicidade**: "" (não selecionada)

## Cenários de Teste Automatizados

### Configuração
- **Ferramenta**: Cucumber
- **Linguagem**: Java
- **Ambiente**: Teste

### Implementação
```java
@Dado("que o anunciante esteja cadastrado no sistema")
public void que_o_anunciante_esteja_cadastrado_no_sistema() {
    // Configurar usuário anunciante no sistema
    anunciante = new Anunciante("João Silva", "joao@email.com");
    sistema.cadastrarUsuario(anunciante);
}

@Dado("tenha realizado autenticação no sistema")
public void tenha_realizado_autenticacao_no_sistema() {
    // Realizar login do anunciante
    sistema.realizarLogin(anunciante.getEmail(), anunciante.getSenha());
}

@Quando("o anunciante preencher os campos obrigatórios")
public void o_anunciante_preencher_os_campos_obrigatorios() {
    // Preencher formulário de anúncio
    anuncio = new Anuncio("Limpeza Residencial", "Serviço completo", 50.00);
    sistema.preencherFormulario(anuncio);
}

@Quando("clicar em salvar")
public void clicar_em_salvar() {
    // Clicar no botão salvar
    sistema.clicarSalvar();
}

@Entao("o sistema exibe uma mensagem de sucesso")
public void o_sistema_exibe_uma_mensagem_de_sucesso() {
    // Verificar mensagem de sucesso
    assertTrue(sistema.exibeMensagemSucesso());
}

@Entao("o anúncio ficará disponível para agendamento")
public void o_anuncio_ficara_disponivel_para_agendamento() {
    // Verificar se anúncio está disponível
    assertTrue(sistema.anuncioDisponivelParaAgendamento(anuncio));
}
```

## Rastreabilidade

### User Story Relacionada
- **ID**: US-001
- **Título**: Cadastrar Anúncio
- **Link**: [Link para a User Story]

### Use Case Relacionado
- **ID**: UC-001
- **Título**: Cadastrar Anúncio
- **Link**: [Link para o Use Case]

### Testes Relacionados
- **Teste Unitário**: TU-001 (Validação de campos)
- **Teste de Integração**: TI-001 (Integração com banco de dados)
- **Teste de Aceitação**: TA-001 (Fluxo completo de cadastro)

## Notas de Implementação

### Considerações Técnicas
- Formulário deve validar campos em tempo real
- Cálculo de valores deve ser dinâmico
- Persistência no banco de dados
- Notificações para clientes sobre novos anúncios

### Riscos Identificados
- **Risco 1**: Validação de dados - Mitigação: Validação client-side e server-side
- **Risco 2**: Performance com muitos anúncios - Mitigação: Paginação e cache

### Estimativas
- **Complexidade**: Média
- **Esforço Estimado**: 16 horas
- **Prioridade**: Alta

## Validação e Aprovação

### Checklist de Validação
- [x] Todos os cenários estão mapeados
- [x] Palavras-chave Gherkin estão corretas
- [x] Cenários cobrem casos de sucesso e exceção
- [x] Regras de negócio estão documentadas
- [x] Dados de teste estão definidos
- [x] Rastreabilidade está estabelecida

### Aprovações
- **Analista de Negócio**: Ana Silva - 03/10/2025
- **Product Owner**: Carlos Santos - 03/10/2025
- **Tech Lead**: Maria Oliveira - 03/10/2025

---

**Revisado por**: João Costa
**Aprovado por**: Ana Silva
**Status**: Aprovado
