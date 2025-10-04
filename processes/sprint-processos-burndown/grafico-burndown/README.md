# Gráfico de Burndown

## Conceito e Definição

O **Gráfico de Burndown** é uma ferramenta visual que acompanha o progresso de uma Sprint de Processos, mostrando a evolução do trabalho restante ao longo do tempo. O nome "Burndown" (queima) vem da ideia de que você está "queimando" os pontos de trabalho até chegar ao zero, indicando a conclusão da Sprint.

## Estrutura do Gráfico

### Eixos do Gráfico

#### Eixo X (Horizontal) - Tempo
- **Unidade**: Dias úteis de trabalho
- **Sprint de 2 semanas**: 10 dias úteis
- **Sprint de 3 semanas**: 15 dias úteis
- **Sprint de 4 semanas**: 20 dias úteis

#### Eixo Y (Vertical) - Esforço
- **Unidade**: Pontos de trabalho
- **Escala**: Do total de pontos até zero
- **Exemplo**: 24 pontos → 0 pontos

### Linhas do Gráfico

#### Linha Ideal (Planejada)
- **Cor**: Amarela (convenção)
- **Formato**: Diagonal decrescente
- **Início**: Total de pontos no dia 0
- **Fim**: Zero pontos no último dia
- **Pressuposto**: Progresso linear e constante

#### Linha Real (Executada)
- **Cor**: Roxa (convenção)
- **Formato**: Curva baseada no progresso real
- **Atualização**: Diária
- **Dados**: Pontos concluídos por dia

## Interpretação do Gráfico

### Cenários de Análise

#### 1. Linha Real ACIMA da Linha Ideal
```
📈 Situação: ATRASO
🔍 Interpretação: "Boca do jacaré aberta"
⚠️ Significado: 
   - Trabalho está atrasado
   - Velocidade menor que o planejado
   - Risco de não entregar no prazo
```

#### 2. Linha Real ABAIXO da Linha Ideal
```
📉 Situação: ADIANTAMENTO
🔍 Interpretação: "Abaixo da meta"
✅ Significado:
   - Trabalho está adiantado
   - Velocidade maior que o planejado
   - Possibilidade de entregar antes
```

#### 3. Linha Real PRÓXIMA da Linha Ideal
```
📊 Situação: NO PRAZO
🔍 Interpretação: "Alinhado"
✅ Significado:
   - Trabalho no ritmo planejado
   - Velocidade adequada
   - Alta probabilidade de entrega no prazo
```

### Análise de Tendências

#### Padrões Comuns

##### Início Atrasado, Recuperação
```
Dias 1-3: Atraso inicial
Dias 4-10: Aceleração
Dias 11-15: Entrega no prazo
```

##### Progresso Constante
```
Todos os dias: Velocidade estável
Resultado: Entrega exata no prazo
```

##### Aceleração Final
```
Dias 1-10: Lento
Dias 11-15: Aceleração
Resultado: Entrega antecipada
```

## Implementação Prática

### Ferramentas Recomendadas

#### Planilha Excel
- **Vantagem**: Simplicidade e flexibilidade
- **Template**: Disponível para download
- **Cálculos**: Automáticos
- **Gráficos**: Gerados automaticamente

#### Ferramentas Especializadas
- **Jira**: Integração com backlog
- **Azure DevOps**: Gestão completa
- **Trello**: Simplicidade visual
- **Monday.com**: Colaboração

### Template Básico

#### Estrutura da Planilha
```
Coluna A: Data
Coluna B: Pontos Planejados
Coluna C: Pontos Concluídos
Coluna D: Pontos Restantes
Coluna E: Velocidade (pontos/dia)
```

#### Fórmulas Essenciais
```
Pontos Restantes = Total - Acumulado
Velocidade = Pontos Concluídos / Dias
Projeção = Pontos Restantes / Velocidade Média
```

### Preenchimento Diário

#### Processo
1. **Fim do dia**: Revisar trabalho realizado
2. **Contar pontos**: Quantificar entregas
3. **Atualizar planilha**: Registrar progresso
4. **Analisar tendência**: Verificar evolução
5. **Ajustar se necessário**: Tomar ações

#### Exemplo de Registro
```
Dia 1: 2 pontos concluídos
Dia 2: 0 pontos (impedimento)
Dia 3: 3 pontos concluídos
Dia 4: 2 pontos concluídos
Total: 7 pontos em 4 dias
```

## Benefícios do Gráfico de Burndown

### Para a Equipe

#### Visibilidade
- **Progresso**: Acompanhamento visual
- **Tendências**: Identificação de padrões
- **Riscos**: Detecção precoce de problemas

#### Motivação
- **Metas**: Objetivos claros
- **Progresso**: Sensação de avanço
- **Celebração**: Reconhecimento de conquistas

### Para o Cliente

#### Transparência
- **Status**: Visão clara do andamento
- **Comunicação**: Relatórios visuais
- **Confiança**: Transparência total

#### Controle
- **Acompanhamento**: Monitoramento ativo
- **Intervenção**: Possibilidade de ajustes
- **Expectativas**: Gestão adequada

### Para o Projeto

#### Gestão
- **Riscos**: Identificação precoce
- **Ajustes**: Correções de rota
- **Qualidade**: Foco na entrega

#### Aprendizado
- **Velocidade**: Calibração de estimativas
- **Padrões**: Identificação de tendências
- **Melhoria**: Otimização contínua

## Casos de Uso Práticos

### Cenário 1: Sprint de 3 Semanas - 24 Pontos

#### Situação Inicial
- **Total**: 24 pontos
- **Duração**: 15 dias úteis
- **Velocidade ideal**: 1,6 pontos/dia

#### Evolução
```
Dia 1: 2 pontos → 22 restantes
Dia 2: 0 pontos → 22 restantes (impedimento)
Dia 3: 3 pontos → 19 restantes
Dia 4: 2 pontos → 17 restantes
Dia 5: 2 pontos → 15 restantes
```

#### Análise
- **Velocidade real**: 1,8 pontos/dia
- **Status**: Adiantado
- **Projeção**: Entrega no dia 13

### Cenário 2: Atraso e Recuperação

#### Situação
- **Dias 1-5**: Atraso significativo
- **Dias 6-10**: Aceleração
- **Dias 11-15**: Entrega no prazo

#### Lições
- **Impedimentos**: Resolução rápida
- **Aceleração**: Possível com foco
- **Recuperação**: Viável com esforço

## Boas Práticas

### Implementação

#### Configuração Inicial
- **Dados históricos**: Usar experiências passadas
- **Estimativas realistas**: Baseadas em capacidade
- **Ferramentas adequadas**: Escolher a melhor opção

#### Acompanhamento
- **Frequência**: Diária
- **Consistência**: Mesmo horário
- **Precisão**: Dados confiáveis

### Interpretação

#### Análise Contextual
- **Fatores externos**: Considerar impedimentos
- **Qualidade**: Não comprometer qualidade
- **Equipe**: Manter motivação

#### Ações Corretivas
- **Atraso**: Identificar causas
- **Aceleração**: Manter qualidade
- **Ajustes**: Replanejar se necessário

## Desafios e Mitigações

### Desafios Comuns

#### Estimativas Imprecisas
- **Problema**: Pontos mal estimados
- **Solução**: Usar dados históricos

#### Mudanças de Escopo
- **Problema**: Alterações durante Sprint
- **Solução**: Processo de gestão de mudanças

#### Disponibilidade da Equipe
- **Problema**: Ausências e impedimentos
- **Solução**: Planejamento de contingência

### Mitigações

#### Preparação
- **Treinamento**: Capacitar a equipe
- **Ferramentas**: Implementar adequadamente
- **Processos**: Definir claramente

#### Execução
- **Comunicação**: Manter todos informados
- **Flexibilidade**: Adaptar-se a mudanças
- **Qualidade**: Não comprometer entregas

## Integração com Outras Ferramentas

### Gestão de Projetos
- **Gantt**: Complementar com cronograma
- **Kanban**: Visualizar fluxo de trabalho
- **Scrum**: Integrar com cerimônias

### BPM
- **Mapeamento**: Conectar com modelagem
- **Análise**: Integrar com diagnósticos
- **Melhoria**: Alinhar com otimizações

## Próximos Passos

1. **Implementar**: Começar com template simples
2. **Treinar**: Capacitar equipe e stakeholders
3. **Refinar**: Ajustar baseado em experiência
4. **Automatizar**: Usar ferramentas avançadas

---

**Referências**:
- Framework Scrum
- Experiência prática da equipe dheka
- Templates e ferramentas disponíveis
- Casos de uso reais em projetos BPM
