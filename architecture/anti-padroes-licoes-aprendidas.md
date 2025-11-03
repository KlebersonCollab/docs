# Anti-padrões e Lições Aprendidas em Arquitetura

## Visão Geral

Este documento compila anti-padrões comuns e lições aprendidas de experiências reais em arquitetura de software, extraídas de discussões técnicas e transcrições.

**Baseado em**: Transcrição do Podcast "PPT Não Compila" - Episódio sobre Microsserviços (2025) e experiências práticas.

---

## ❌ Anti-padrões Comuns

### 1. Microserviços Extremamente Pequenos

**Anti-padrão**:
> "Qual o tamanho ideal do microsserviço?"

Criar microsserviços extremamente pequenos, dividindo funcionalidades que deveriam estar juntas.

**Exemplo Errado**:
- Serviço separado para CREATE
- Serviço separado para READ
- Serviço separado para UPDATE
- Serviço separado para DELETE

**Problemas**:
- Complexidade operacional desnecessária
- Múltiplos deploys para uma mudança simples
- Dificuldade de manter consistência
- Overhead de comunicação entre serviços

**Correção**:
> "Não é sobre o tamanho da aplicação, mas sobre o tamanho do domínio que ela tem."

- Agrupar por domínio, não por operação CRUD
- Usar CQRS dentro de um serviço quando necessário
- Considerar coesão do domínio, não tamanho do código

---

### 2. Decisão por Hype, Não por Necessidade

**Anti-padrão**:
Adotar microsserviços "porque é moderno" ou "porque todo mundo está fazendo", sem análise adequada.

**Sintomas**:
- Time de 5 desenvolvedores mantendo 20 microsserviços
- Complexidade alta sem benefício claro
- Custos operacionais desproporcionais
- Times frustrados com complexidade

**Correção**:
- Sempre analisar contexto antes de decidir
- Documentar justificativa objetiva
- Começar simples, evoluir quando necessário
- Resistir pressão de tendências

**Lição**:
> "A gente tem hype de tudo, né? A gente precisa ser ter mais parcimônia na avaliação das coisas."

---

### 3. Over-Engineering com Arquitetura de Referência

**Anti-padrão**:
Tentar criar arquitetura de referência que cubra 100% dos casos possíveis.

**Problema**:
> "Se você faz uma arquitetura de referência para cobrir 100% dos casos, ou você fez ela incompleta ou você gastou demais."

**Sintomas**:
- Framework interno gigantesco
- Tentar resolver todos os problemas do mercado
- Não conseguir evoluir ou manter
- Time preso em framework antigo

**Exemplo**:
- Empresa cria framework Java que não permite atualizar versão do Java
- 7 anos sem poder evoluir tecnologia
- Time preso em tecnologia obsoleta

**Correção**:
- Arquitetura de referência como **guidance**, não regra absoluta
- Usar ferramentas do mercado quando possível
- Focar no negócio, não em reinventar roda
- Permitir especialização por contexto

---

### 4. Ignorar Capacidade Operacional

**Anti-padrão**:
Escolher arquitetura complexa sem considerar capacidade do time para mantê-la.

**Sintomas**:
- Time pequeno tentando manter muitos microsserviços
- Falta de pessoas para operar arquitetura
- Complexidade operacional além da capacidade
- Burnout de desenvolvedores

**Exemplo**:
- 10 desenvolvedores para manter 50 microsserviços
- Cada desenvolvedor precisa entender múltiplos serviços
- Operação complexa demais para time disponível

**Correção**:
> "Você vai ter um time só, né? Você não tem mais vários squads, você tem um time mais enxuto cuidando de 50 microsserviços. Faz sentido? É muito difícil."

- Avaliar capacidade operacional antes de decidir
- Escalar arquitetura com capacidade do time
- Considerar curva de aprendizado
- Não criar complexidade além da capacidade

---

### 5. Lift and Shift Sem Adaptação

**Anti-padrão**:
Migrar aplicação legada para cloud sem adaptar para ser cloud-native.

**Sintomas**:
- Aplicação antiga rodando em VM na cloud
- Não aproveitando capacidades da cloud
- Custos altos sem benefícios
- Voltando para data center por custo

**Problema**:
> "Maior parte das empresas que fizeram o de volta para casa, digamos assim, da nuvem de volta pro DC, são empresas que não se modernizaram para ter arquiteturas que fossem cloud native."

**Correção**:
- Adaptar para cloud-native quando migrar
- Aproveitar serviços gerenciados
- Projetar para escala e elasticidade
- Usar containers e orquestração adequada

---

### 6. Vendor Lock-in Sem Consciência

**Anti-padrão**:
Usar serviços gerenciados sem entender as implicações de lock-in.

**Exemplo**:
> "SDK do DynamoDB e a mágica acontece sozinho. E aí, cara, você abraçou o capeta e você tá no confortinho do do loquin."

**Problemas**:
- Dependência total de um vendor
- Dificuldade de migração
- Custos altos em renovações
- Sem poder de negociação

**Correção**:
> "Você tem que entrar no quarto e saber para onde é a saída."

- Sempre ter plano de saída
- Usar abstrações sobre serviços externos
- Considerar multicloud desde o início
- Documentar dependências e alternativas

---

### 7. Comunicação Humana Pobre com Comunicação Técnica Boa

**Anti-padrão**:
Ter processos técnicos perfeitos (APIs, contratos) mas comunicação humana ruim entre times.

**Problema**:
> "Menos você tem uma prática de comunicação via API muito bem estabelecida, mas uma comunicação humana péssima, sem mais uma comunicação humana péssima vez uma merda."

**Sintomas**:
- Times não se comunicam diretamente
- Dependências criam gargalos
- Conflitos de merge/deploy frequentes
- Falta de alinhamento entre times

**Correção**:
- Investir em comunicação humana
- Reuniões regulares entre times
- Alinhamento de objetivos
- Cultura de colaboração

---

### 8. Framework Interno Competing com Mercado

**Anti-padrão**:
Criar framework interno que compete com soluções do mercado.

**Problema**:
> "Se eu acho que eu vou construir um um framework em Java para resolver todos os problemas da minha da minha empresa, pô, não tá certo, porque só só se minha empresa for tipo, sei lá, IBM que ela vai vender isso, né?"

**Exemplo Ruim**:
- Empresa cria framework Java completo
- 7 anos depois, não consegue atualizar versão do Java
- Time preso em tecnologia obsoleta
- Não consegue evoluir

**Correção**:
- Usar frameworks do mercado (Spring, Quarkus, etc.)
- Focar no negócio, não em tecnologia
- Aproveitar soluções existentes
- Evitar reinventar roda

---

## ✅ Lições Aprendidas

### 1. Maturidade Tecnológica Importa

**Lição**:
> "A gente tá agora no platô do de produtividade da tecnologia."

Tecnologias passam por ciclos. Use tecnologias no "platô de produtividade", não no pico do hype.

**Aplicação**:
- Aguardar maturidade antes de adoção crítica
- Reconhecer onde tecnologia está no ciclo
- Decisões baseadas em estabilidade, não hype

---

### 2. Stateless é Fundamental

**Lição**:
> "A gente manter o container stateless. Isso. E e assim, o monolito, ele pode ser stat, entendeu?"

Stateless não é exclusivo de microsserviços. Monolitos também devem ser stateless para permitir escala horizontal.

**Benefícios**:
- Escala horizontal possível
- Deploy zero-downtime
- Disaster recovery mais simples
- Elasticidade melhor

**Aplicação**:
- Sempre projetar aplicações stateless
- Estado em serviços externos (cache, DB, filas)
- Session em storage compartilhado
- Evitar estado em memória da aplicação

---

### 3. Monolito Bem Arquitetado é Válido

**Lição**:
> "Um monolito bem escrito é até atraente e e para quem tá começando, eh, talvez seja a melhor pedida mesmo."

Monolito não é vilão. Monolito bem estruturado com domínios separados pode ser melhor escolha para muitos casos.

**Quando Monolito é Adequado**:
- Times pequenos
- Domínios coesos
- Orçamento limitado
- Operação simples preferida

**Como Fazer Monolito Bem**:
- Separação de domínios mesmo dentro do monolito
- Arquitetura hexagonal
- Preparar para futura separação se necessário
- Stateless e cloud-ready

---

### 4. Evolução Gradual é Possível

**Lição**:
> "Se você não importa o tamanho do do da aplicação que você tá desenvolvendo, se você usa os mesmos conceitos de ser status, primeiro que se você fizer começar com um serviço só, com uma aplicação só e você seguir os padrões adequadamente, depois não tem que ser difícil você dividir isso em dois assets ou em duas aplicações."

Começar simples e evoluir gradualmente é melhor que começar complexo.

**Estratégia**:
1. Começar com monolito bem estruturado
2. Aplicar padrões que facilitem futura separação
3. Separar quando necessidade real surgir
4. Evoluir baseado em dados, não especulação

---

### 5. Custo Deve Ser Negociado

**Lição**:
> "Você consegue 50%, 60% se você tiver uma boa negociação de preço."

Negociação de contratos é crucial. Times de infraestrutura são melhores nisso que desenvolvedores.

**Estratégias**:
- Multicloud como poder de negociação
- Renovar contratos com negociação ativa
- Primeiros 3 anos são "lua de mel" - depois custos sobem
- Sempre negociar renovações

---

### 6. Decisões Devem Ser Contextuais

**Lição**:
> "Depende. [...] O tipo de arquitetura também é complicado, cara."

Não existe fórmula única. Cada decisão deve considerar:
- Contexto de negócio
- Capacidade operacional
- Custo disponível
- Demanda real

**Aplicação**:
- Sempre analisar contexto específico
- Documentar justificativa
- Evitar decisões por preferência pessoal
- Revisar periodicamente

---

### 7. Build and Run Melhora Qualidade

**Lição**:
> "O cara que tá no building, ele tem um cuidado um pouco melhor com a qualidade, porque a bomba vai est no colo dele, né, velho?"

Times que constroem E mantêm (build and run) têm melhor qualidade que times que apenas constroem.

**Benefícios**:
- Desenvolvedores mais cuidadosos
- Testes mais completos
- Documentação melhor
- Operação mais suave

**Aplicação**:
- Times devem ser responsáveis pelo que constroem
- Evitar separação rígida dev/ops
- Cultura de ownership
- Responsabilidade pelo ciclo completo

---

## 🎯 Princípios Práticos

### 1. Não Reinvente a Roda

> "Por favor, não seja esse cara, né? Esqueço. Vira um corte, por favor. Não reinvente a roda."

**Aplicação**:
- Use ferramentas e frameworks do mercado
- Foque no negócio, não em tecnologia
- Aproveite soluções existentes
- Evite criar framework interno desnecessário

---

### 2. Feito é Melhor que Perfeito (Mas Não Pior)

> "O perfeito é inimigo do feito? Alguma coisa assim."

**Lição**:
- Não buscar perfeição que trava entrega
- Mas também não aceitar qualquer coisa
- Equilíbrio entre qualidade e velocidade
- Contexto importa: MVP vs produção crítica

---

### 3. Medo é o Grande Vilão

> "Acho que o medo é é o é o grande vilão aqui."

**Aplicação**:
- Times não devem ter medo de código legado
- Legado pode ser melhorado gradualmente
- Não precisa reescrever tudo de uma vez
- Evolução incremental é válida

---

### 4. Parcimônia na Avaliação

> "A gente precisa ser ter mais parcimônia na avaliação das coisas."

**Aplicação**:
- Não adotar tecnologia só por hype
- Analisar criticamente antes de decidir
- Resistir pressão de tendências
- Decisões baseadas em necessidade real

---

## 📋 Checklist de Prevenção de Anti-padrões

Antes de tomar decisão arquitetural, verifique:

### Over-Engineering
- [ ] Complexidade se justifica pelo benefício?
- [ ] Time tem capacidade para manter?
- [ ] ROI da complexidade é claro?

### Under-Engineering
- [ ] Estrutura básica adequada?
- [ ] Preparado para evolução futura?
- [ ] Separação de domínios adequada?

### Hype vs Necessidade
- [ ] Decisão baseada em análise ou tendência?
- [ ] Justificativa objetiva documentada?
- [ ] Resistiu pressão de hype?

### Capacidade Operacional
- [ ] Time tem capacidade para operar?
- [ ] Curva de aprendizado considerada?
- [ ] Custo operacional viável?

### Vendor Lock-in
- [ ] Plano de saída documentado?
- [ ] Abstrações sobre serviços externos?
- [ ] Dependências mapeadas?

---

## 📚 Referências

- [ADR-000: Framework de Decisão Microsserviços vs Monolito](./adr-000-microsservicos-vs-monolito.md)
- [Critérios de Decisão Arquitetural](./criterios-decisao-arquitetural.md)
- [Insights de Arquitetura Corporativa](./insights-arquitetura-corporativa.md)
- Domain-Driven Design - Eric Evans
- Building Microservices - Sam Newman

---

**Última atualização**: 01/11/2025
**Mantenedor**: Equipe de Arquitetura Skynet

