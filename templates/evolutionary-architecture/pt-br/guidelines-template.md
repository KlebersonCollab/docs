# Template de Diretrizes Arquiteturais

## 📋 Visão Geral

Este template ajuda você a documentar diretrizes arquiteturais que suportam arquitetura evolutiva. Diretrizes fornecem direção para como a arquitetura deve evoluir mantendo integridade arquitetural.

**Uso**: Copie este template e preencha as seções para cada diretriz arquitetural que deseja estabelecer.

---

## Diretriz: [Nome da Diretriz]

### Descrição

[Breve descrição do que esta diretriz aplica e por que existe]

**Exemplo**:
> Esta diretriz garante que a camada de domínio permaneça independente de preocupações de infraestrutura, permitindo testes mais fáceis e evolução de ambas as camadas independentemente.

### Racionalização

[Explique por que esta diretriz é importante para arquitetura evolutiva]

**Pontos Principais**:
- [Razão 1]
- [Razão 2]
- [Razão 3]

### Regra

[Declaração clara da regra ou restrição]

**Formato**: 
- ✅ **FAÇA**: [O que deve ser feito]
- ❌ **NÃO FAÇA**: [O que deve ser evitado]

**Exemplo**:
- ✅ **FAÇA**: Entidades de domínio devem conter apenas lógica de negócio
- ❌ **NÃO FAÇA**: Entidades de domínio não devem depender de infraestrutura (bancos de dados, clientes HTTP, etc.)

### Validação

[Como esta diretriz é validada - verificações automatizadas, revisões, etc.]

**Verificações Automatizadas**:
- [ ] [Verificação 1]: [Descrição]
- [ ] [Verificação 2]: [Descrição]

**Revisões Manuais**:
- [ ] [Revisão 1]: [Descrição]
- [ ] [Revisão 2]: [Descrição]

**Ferramentas Usadas**:
- [Ferramenta 1]: [Propósito]
- [Ferramenta 2]: [Propósito]

### Exemplos

#### ✅ Bom Exemplo

[Mostre um exemplo de código que segue a diretriz]

```typescript
// ✅ Bom: Entidade de domínio sem dependências de infraestrutura
export class Pedido {
  constructor(
    private id: PedidoId,
    private items: ItemPedido[],
    private total: Dinheiro
  ) {}
  
  adicionarItem(item: ItemPedido): void {
    // Apenas lógica de negócio
    if (this.items.length >= 10) {
      throw new Error('Máximo de 10 itens por pedido');
    }
    this.items.push(item);
    this.total = this.recalcularTotal();
  }
  
  private recalcularTotal(): Dinheiro {
    // Apenas lógica de negócio
    return this.items.reduce(
      (soma, item) => soma.add(item.preco),
      Dinheiro.zero()
    );
  }
}
```

#### ❌ Exemplo Ruim

[Mostre um exemplo de código que viola a diretriz]

```typescript
// ❌ Ruim: Entidade de domínio com dependência de infraestrutura
import { Database } from '../infrastructure/database';
import { EmailService } from '../infrastructure/email';

export class Pedido {
  constructor(
    private id: PedidoId,
    private items: ItemPedido[],
    private total: Dinheiro,
    private db: Database,  // ❌ Dependência de infraestrutura
    private emailService: EmailService  // ❌ Dependência de infraestrutura
  ) {}
  
  async adicionarItem(item: ItemPedido): Promise<void> {
    // Lógica de negócio misturada com infraestrutura
    await this.db.save(item);  // ❌ Acesso direto ao banco
    await this.emailService.send(/* ... */);  // ❌ Envio direto de email
  }
}
```

### Função de Fitness

[Opcional: Função de fitness automatizada que valida esta diretriz]

```typescript
// Exemplo de função de fitness
describe('Diretriz Arquitetural: Independência de Domínio', () => {
  it('não deve permitir que camada de domínio importe infraestrutura', () => {
    const arquivosDomain = findFiles('src/domain/**/*.ts');
    const violacoes = arquivosDomain.filter(arquivo => {
      const content = readFileSync(arquivo, 'utf-8');
      return content.includes('from "../infrastructure"') ||
             content.includes('from "../application"');
    });
    
    expect(violacoes).toHaveLength(0);
  });
});
```

### Estratégia de Evolução

[Como esta diretriz pode evoluir ao longo do tempo]

**Estado Atual**: [Descreva aplicação atual]

**Evolução Futura**:
- [ ] [Passo de evolução 1]
- [ ] [Passo de evolução 2]

**Condições para Mudança**:
- [Condição 1]: [O que desencadearia uma mudança nesta diretriz]
- [Condição 2]: [Outra condição desencadeadora]

### Diretrizes Relacionadas

[Links para diretrizes relacionadas]

- [Nome da Diretriz](./guideline-name.md)
- [Nome da Diretriz](./guideline-name.md)

### Exceções

[Documente quaisquer exceções a esta diretriz e por que existem]

| Exceção | Razão | Duração |
|---------|-------|---------|
| [Exceção 1] | [Por que existe] | [Temporária/Permanente] |
| [Exceção 2] | [Por que existe] | [Temporária/Permanente] |

### Métricas

[Como medir conformidade com esta diretriz]

| Métrica | Meta | Atual | Status |
|---------|------|-------|--------|
| [Métrica 1] | [Valor meta] | [Valor atual] | ✅/❌ |
| [Métrica 2] | [Valor meta] | [Valor atual] | ✅/❌ |

---

## Catálogo de Diretrizes Template

Use esta seção para manter um catálogo de todas as diretrizes:

### Diretrizes por Categoria

#### Gerenciamento de Dependências
- [Diretriz: Direção de Dependência](./guidelines/dependency-direction.md)
- [Diretriz: Prevenção de Dependência Circular](./guidelines/no-circular-deps.md)

#### Arquitetura em Camadas
- [Diretriz: Isolamento de Camadas](./guidelines/layer-isolation.md)
- [Diretriz: Inversão de Dependência](./guidelines/dependency-inversion.md)

#### Qualidade de Código
- [Diretriz: Limites de Complexidade de Código](./guidelines/complexity-limits.md)
- [Diretriz: Requisitos de Cobertura de Testes](./guidelines/test-coverage.md)

#### Performance
- [Diretriz: Metas de Tempo de Resposta](./guidelines/response-time.md)
- [Diretriz: Limites de Uso de Recursos](./guidelines/resource-limits.md)

### Cronograma de Revisão de Diretrizes

| Diretriz | Última Revisão | Próxima Revisão | Proprietário |
|----------|----------------|-----------------|--------------|
| [Diretriz 1] | [Data] | [Data] | [Nome] |
| [Diretriz 2] | [Data] | [Data] | [Nome] |

---

## 📝 Usando Este Template

### Passo 1: Identificar Necessidade

Antes de criar uma diretriz, pergunte:
- Isso é um problema arquitetural recorrente?
- Validação automatizada ajudaria?
- Isso suporta objetivos de arquitetura evolutiva?

### Passo 2: Rascunhar Diretriz

1. Copie a seção de template de diretriz
2. Preencha todas as seções
3. Adicione exemplos (bons e ruins)
4. Defina abordagem de validação

### Passo 3: Revisar e Aprovar

1. Revisar com equipe de arquitetura
2. Obter aprovação de stakeholders
3. Documentar quaisquer exceções

### Passo 4: Implementar Validação

1. Criar funções de fitness
2. Adicionar ao pipeline CI/CD
3. Configurar monitoramento

### Passo 5: Monitorar e Evoluir

1. Revisar métricas de conformidade regularmente
2. Atualizar diretrizes conforme arquitetura evolui
3. Remover diretrizes que não servem mais a um propósito

---

## 🎯 Melhores Práticas

### Manter Diretrizes Focadas

✅ **FAÇA**:
- Manter cada diretriz focada em uma preocupação
- Tornar diretrizes específicas e acionáveis
- Atualizar diretrizes conforme arquitetura evolui

❌ **NÃO FAÇA**:
- Criar diretrizes muito amplas
- Definir diretrizes difíceis de validar
- Manter diretrizes desatualizadas

### Validar Automaticamente

Sempre que possível, crie funções de fitness automatizadas para validar diretrizes. Isso garante:
- Aplicação consistente
- Detecção precoce de violações
- Ciclos de feedback mais rápidos

### Documentar Exceções

Quando exceções são necessárias, documente-as claramente com:
- Razão para exceção
- Duração (temporária ou permanente)
- Data de revisão para exceções temporárias

### Revisar Regularmente

Diretrizes devem ser revisadas regularmente para garantir que:
- Ainda servem ao seu propósito
- Alinham com arquitetura atual
- Suportam objetivos evolutivos

---

**Versão do Template**: 1.0  
**Última Atualização**: 2025-01-20  
**Mantenedor**: Equipe de Documentação Skynet

---

**Documentos Relacionados**:
- [Guia de Arquitetura Evolutiva](../../architecture/evolutionary-architecture/pt-br/README.md)
- [Definição de Métricas](../../architecture/evolutionary-architecture/pt-br/metrics-definition.md)
- [Estratégias de Automação](../../architecture/evolutionary-architecture/pt-br/automation-strategies.md)

**Versão em Inglês**: [Architectural Guidelines Template (EN)](../guidelines-template.md)

