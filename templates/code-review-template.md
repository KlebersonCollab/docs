# Template: Code Review

## 1. Informações Básicas
- **ID da Review**: [CR-XXX]
- **Pull Request**: [Link para o PR]
- **Autor**: [Nome do Desenvolvedor]
- **Revisor**: [Nome do Revisor]
- **Data da Review**: [DD/MM/AAAA]
- **Status**: [Pendente/Em Revisão/Aprovado/Rejeitado]

## 2. Visão Geral
[Descrição geral das mudanças, objetivo do PR e contexto necessário para entender as alterações.]

## 3. Checklist de Revisão

### 3.1. Funcionalidade
- [ ] **Funcionalidade Implementada**: O código implementa corretamente a funcionalidade solicitada?
- [ ] **Casos de Uso**: Todos os casos de uso foram considerados?
- [ ] **Edge Cases**: Casos extremos foram tratados?
- [ ] **Validações**: Validações de entrada estão implementadas?
- [ ] **Tratamento de Erros**: Erros são tratados adequadamente?

### 3.2. Qualidade do Código
- [ ] **Legibilidade**: O código é fácil de ler e entender?
- [ ] **Nomenclatura**: Nomes de variáveis, funções e classes são descritivos?
- [ ] **Comentários**: Comentários são claros e úteis?
- [ ] **Complexidade**: A complexidade ciclomática está dentro dos limites?
- [ ] **Duplicação**: Há código duplicado que pode ser refatorado?

### 3.3. Arquitetura e Design
- [ ] **Padrões**: Padrões de design apropriados foram utilizados?
- [ ] **Separação de Responsabilidades**: Cada classe/função tem uma responsabilidade clara?
- [ ] **Acoplamento**: O acoplamento entre componentes está adequado?
- [ ] **Coesão**: A coesão interna está adequada?
- [ ] **Reutilização**: O código pode ser reutilizado?

### 3.4. Performance
- [ ] **Algoritmos**: Algoritmos são eficientes?
- [ ] **Consultas**: Consultas ao banco são otimizadas?
- [ ] **Memória**: Uso de memória está adequado?
- [ ] **Cache**: Oportunidades de cache foram consideradas?
- [ ] **Escalabilidade**: O código suporta crescimento?

### 3.5. Segurança
- [ ] **Validação de Entrada**: Entradas são validadas adequadamente?
- [ ] **Sanitização**: Dados são sanitizados antes do uso?
- [ ] **Autenticação**: Autenticação está implementada corretamente?
- [ ] **Autorização**: Autorização está implementada corretamente?
- [ ] **Dados Sensíveis**: Dados sensíveis são tratados adequadamente?

### 3.6. Testes
- [ ] **Cobertura**: Cobertura de testes está adequada?
- [ ] **Testes Unitários**: Testes unitários foram implementados?
- [ ] **Testes de Integração**: Testes de integração foram implementados?
- [ ] **Casos de Teste**: Casos de teste cobrem cenários importantes?
- [ ] **Dados de Teste**: Dados de teste são apropriados?

### 3.7. Documentação
- [ ] **README**: README foi atualizado se necessário?
- [ ] **Comentários**: Comentários explicam lógica complexa?
- [ ] **Documentação de API**: Documentação de API foi atualizada?
- [ ] **Changelog**: Changelog foi atualizado?
- [ ] **Tutorials**: Tutoriais foram atualizados?

### 3.8. Padrões e Convenções
- [ ] **Style Guide**: Código segue o style guide da equipe?
- [ ] **Convenções**: Convenções de nomenclatura foram seguidas?
- [ ] **Formatação**: Código está formatado corretamente?
- [ ] **Imports**: Imports estão organizados adequadamente?
- [ ] **Estrutura**: Estrutura de arquivos está adequada?

## 4. Análise Detalhada

### 4.1. Pontos Fortes
[Lista dos pontos positivos identificados na revisão]
- [Ponto forte 1]
- [Ponto forte 2]
- [Ponto forte 3]

### 4.2. Pontos de Melhoria
[Lista dos pontos que precisam ser melhorados]

#### 4.2.1. Críticos (Must Fix)
- [ ] [Problema crítico 1] - **Linha**: [X] - **Descrição**: [Descrição]
- [ ] [Problema crítico 2] - **Linha**: [X] - **Descrição**: [Descrição]

#### 4.2.2. Importantes (Should Fix)
- [ ] [Problema importante 1] - **Linha**: [X] - **Descrição**: [Descrição]
- [ ] [Problema importante 2] - **Linha**: [X] - **Descrição**: [Descrição]

#### 4.2.3. Sugestões (Nice to Have)
- [ ] [Sugestão 1] - **Linha**: [X] - **Descrição**: [Descrição]
- [ ] [Sugestão 2] - **Linha**: [X] - **Descrição**: [Descrição]

### 4.3. Comentários Específicos
[Comentários detalhados sobre partes específicas do código]

#### 4.3.1. Arquivo: [nome_do_arquivo]
```python
# Linha X: [Comentário sobre esta linha]
def function_name():
    # Linha Y: [Comentário sobre esta linha]
    pass
```

#### 4.3.2. Arquivo: [nome_do_arquivo]
```python
# Linha X: [Comentário sobre esta linha]
class ClassName:
    # Linha Y: [Comentário sobre esta linha]
    pass
```

## 5. Sugestões de Melhoria

### 5.1. Refatoração
- [ ] [Sugestão de refatoração 1]
- [ ] [Sugestão de refatoração 2]
- [ ] [Sugestão de refatoração 3]

### 5.2. Otimização
- [ ] [Sugestão de otimização 1]
- [ ] [Sugestão de otimização 2]
- [ ] [Sugestão de otimização 3]

### 5.3. Boas Práticas
- [ ] [Sugestão de boas práticas 1]
- [ ] [Sugestão de boas práticas 2]
- [ ] [Sugestão de boas práticas 3]

## 6. Testes e Validação

### 6.1. Testes Recomendados
- [ ] [Teste 1]
- [ ] [Teste 2]
- [ ] [Teste 3]

### 6.2. Cenários de Teste
- [ ] [Cenário 1]
- [ ] [Cenário 2]
- [ ] [Cenário 3]

### 6.3. Validação Manual
- [ ] [Validação 1]
- [ ] [Validação 2]
- [ ] [Validação 3]

## 7. Impacto e Riscos

### 7.1. Impacto das Mudanças
- **Funcionalidades Afetadas**: [Lista de funcionalidades]
- **APIs Afetadas**: [Lista de APIs]
- **Banco de Dados**: [Mudanças no banco]
- **Configurações**: [Mudanças de configuração]

### 7.2. Riscos Identificados
| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| [Risco 1] | [Alta/Média/Baixa] | [Alto/Médio/Baixo] | [Mitigação] |
| [Risco 2] | [Alta/Média/Baixa] | [Alto/Médio/Baixo] | [Mitigação] |

### 7.3. Dependências
- **Dependências Internas**: [Lista de dependências]
- **Dependências Externas**: [Lista de dependências]
- **Ordem de Deploy**: [Ordem necessária]

## 8. Aprovação e Próximos Passos

### 8.1. Status da Review
- [ ] **Aprovado**: Código pode ser mergeado
- [ ] **Aprovado com Condições**: Código pode ser mergeado após correções
- [ ] **Rejeitado**: Código precisa de revisão significativa
- [ ] **Pendente**: Aguardando mais informações

### 8.2. Condições para Aprovação
- [ ] [Condição 1]
- [ ] [Condição 2]
- [ ] [Condição 3]

### 8.3. Próximos Passos
- [ ] [Passo 1] - **Responsável**: [Nome] - **Prazo**: [Data]
- [ ] [Passo 2] - **Responsável**: [Nome] - **Prazo**: [Data]
- [ ] [Passo 3] - **Responsável**: [Nome] - **Prazo**: [Data]

## 9. Acompanhamento

### 9.1. Métricas
- **Tempo de Review**: [X horas]
- **Número de Comentários**: [X comentários]
- **Número de Mudanças**: [X mudanças]
- **Taxa de Aprovação**: [X%]

### 9.2. Aprendizados
- [ ] [Aprendizado 1]
- [ ] [Aprendizado 2]
- [ ] [Aprendizado 3]

## 10. Aprovações
- **Revisor**: [Nome] - [Assinatura/Data]
- **Tech Lead**: [Nome] - [Assinatura/Data]
- **Autor**: [Nome] - [Assinatura/Data]

---

**Referências**:
- [Link para Pull Request]
- [Link para User Story relacionada]
- [Link para Testes]

**Histórico de Revisões**:
| Versão | Data | Autor | Descrição da Mudança |
|--------|------|-------|----------------------|
| 1.0    | DD/MM/AAAA | [Autor] | Criação inicial da Code Review |
