# Template: Database Schema Documentation

## 1. Informações Básicas
- **ID do Schema**: [DB-XXX]
- **Nome do Banco de Dados**: [Nome do Banco]
- **Versão**: [1.0]
- **Data de Criação**: [DD/MM/AAAA]
- **Última Atualização**: [DD/MM/AAAA]
- **Autor**: [Nome do DBA/Arquiteto de Dados]
- **Status**: [Rascunho/Em Revisão/Aprovado]

## 2. Visão Geral
[Descrição geral do banco de dados, seu propósito, tecnologias utilizadas e como se encaixa na arquitetura do sistema.]

## 3. Informações Técnicas
- **SGBD**: [PostgreSQL, MySQL, MongoDB, SQL Server, etc.]
- **Versão**: [Versão do SGBD]
- **Charset**: [UTF-8, Latin1, etc.]
- **Collation**: [utf8_general_ci, etc.]
- **Timezone**: [UTC, America/Sao_Paulo, etc.]

## 4. Diagrama ER (Entity-Relationship)
[Incluir diagrama ER do banco de dados ou link para ele]
```
[Link ou imagem do Diagrama ER]
```
- **Descrição**: [Explicação do diagrama, principais entidades e relacionamentos]

## 5. Tabelas Principais

### 5.1. [Nome da Tabela 1]
**Descrição**: [Descrição da tabela e seu propósito]
**Chave Primária**: [Campo(s) que compõem a chave primária]

| Campo | Tipo | Tamanho | Null | Default | Descrição |
|-------|------|---------|------|---------|-----------|
| id | INT | - | NO | AUTO_INCREMENT | Identificador único |
| name | VARCHAR | 255 | NO | - | Nome do registro |
| email | VARCHAR | 255 | NO | - | Email do usuário |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | Data de criação |
| updated_at | TIMESTAMP | - | YES | NULL | Data de atualização |

**Índices**:
- PRIMARY KEY (id)
- UNIQUE KEY (email)
- INDEX (name)

**Relacionamentos**:
- **1:N** com [Tabela 2] (foreign_key)
- **N:1** com [Tabela 3] (foreign_key)

### 5.2. [Nome da Tabela 2]
**Descrição**: [Descrição da tabela e seu propósito]
**Chave Primária**: [Campo(s) que compõem a chave primária]

| Campo | Tipo | Tamanho | Null | Default | Descrição |
|-------|------|---------|------|---------|-----------|
| id | INT | - | NO | AUTO_INCREMENT | Identificador único |
| user_id | INT | - | NO | - | ID do usuário (FK) |
| title | VARCHAR | 255 | NO | - | Título do item |
| description | TEXT | - | YES | NULL | Descrição detalhada |
| status | ENUM | - | NO | 'active' | Status do item |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | Data de criação |

**Índices**:
- PRIMARY KEY (id)
- FOREIGN KEY (user_id) REFERENCES users(id)
- INDEX (status)
- INDEX (created_at)

**Relacionamentos**:
- **N:1** com [Tabela 1] (user_id)
- **1:N** com [Tabela 4] (id)

## 6. Tabelas de Relacionamento (Junction Tables)

### 6.1. [Nome da Tabela de Relacionamento]
**Descrição**: [Descrição da tabela de relacionamento N:N]

| Campo | Tipo | Tamanho | Null | Default | Descrição |
|-------|------|---------|------|---------|-----------|
| table1_id | INT | - | NO | - | ID da Tabela 1 (FK) |
| table2_id | INT | - | NO | - | ID da Tabela 2 (FK) |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | Data de criação |

**Índices**:
- PRIMARY KEY (table1_id, table2_id)
- FOREIGN KEY (table1_id) REFERENCES table1(id)
- FOREIGN KEY (table2_id) REFERENCES table2(id)

## 7. Views

### 7.1. [Nome da View 1]
**Descrição**: [Descrição da view e seu propósito]
**Tabelas Base**: [Lista das tabelas utilizadas]

```sql
CREATE VIEW view_name AS
SELECT 
    t1.field1,
    t1.field2,
    t2.field3
FROM table1 t1
JOIN table2 t2 ON t1.id = t2.table1_id
WHERE t1.status = 'active';
```

**Campos Retornados**:
| Campo | Tipo | Descrição |
|-------|------|-----------|
| field1 | VARCHAR | Descrição do campo |
| field2 | INT | Descrição do campo |
| field3 | VARCHAR | Descrição do campo |

## 8. Stored Procedures

### 8.1. [Nome da Procedure 1]
**Descrição**: [Descrição da procedure e seu propósito]
**Parâmetros**: [Lista de parâmetros de entrada e saída]

```sql
DELIMITER //
CREATE PROCEDURE procedure_name(
    IN param1 VARCHAR(255),
    IN param2 INT,
    OUT result INT
)
BEGIN
    -- Lógica da procedure
    SELECT COUNT(*) INTO result 
    FROM table_name 
    WHERE field1 = param1 AND field2 = param2;
END //
DELIMITER ;
```

**Parâmetros**:
| Nome | Tipo | Direção | Descrição |
|------|------|---------|-----------|
| param1 | VARCHAR(255) | IN | Descrição do parâmetro |
| param2 | INT | IN | Descrição do parâmetro |
| result | INT | OUT | Resultado da operação |

## 9. Triggers

### 9.1. [Nome do Trigger 1]
**Descrição**: [Descrição do trigger e quando é executado]
**Tabela**: [Nome da tabela]
**Evento**: [INSERT, UPDATE, DELETE]
**Timing**: [BEFORE, AFTER]

```sql
DELIMITER //
CREATE TRIGGER trigger_name
BEFORE INSERT ON table_name
FOR EACH ROW
BEGIN
    -- Lógica do trigger
    SET NEW.created_at = NOW();
END //
DELIMITER ;
```

## 10. Índices e Performance

### 10.1. Índices Principais
| Tabela | Índice | Tipo | Campos | Descrição |
|--------|--------|------|--------|-----------|
| users | PRIMARY | PRIMARY KEY | id | Chave primária |
| users | idx_email | UNIQUE | email | Índice único para email |
| orders | idx_user_id | INDEX | user_id | Índice para consultas por usuário |
| orders | idx_created_at | INDEX | created_at | Índice para consultas por data |

### 10.2. Otimizações de Performance
- **Particionamento**: [Descrição de particionamento se aplicável]
- **Arquivamento**: [Estratégia de arquivamento de dados antigos]
- **Cache**: [Estratégia de cache para consultas frequentes]

## 11. Segurança

### 11.1. Controle de Acesso
- **Usuários do Banco**: [Lista de usuários e suas permissões]
- **Roles**: [Roles definidas e suas permissões]
- **Políticas de Senha**: [Políticas de senha para usuários]

### 11.2. Criptografia
- **Dados Sensíveis**: [Campos que são criptografados]
- **Algoritmo**: [Algoritmo de criptografia utilizado]
- **Chaves**: [Gerenciamento de chaves de criptografia]

### 11.3. Auditoria
- **Logs de Acesso**: [Configuração de logs de acesso]
- **Logs de Modificação**: [Configuração de logs de modificação]
- **Retenção de Logs**: [Período de retenção dos logs]

## 12. Backup e Recuperação

### 12.1. Estratégia de Backup
- **Frequência**: [Diário, semanal, mensal]
- **Tipo**: [Completo, incremental, diferencial]
- **Retenção**: [Período de retenção dos backups]
- **Localização**: [Onde os backups são armazenados]

### 12.2. Procedimentos de Recuperação
- **RTO (Recovery Time Objective)**: [Tempo máximo para recuperação]
- **RPO (Recovery Point Objective)**: [Perda máxima de dados aceitável]
- **Procedimentos**: [Passos para recuperação em caso de falha]

## 13. Monitoramento

### 13.1. Métricas de Performance
- **Tempo de Resposta**: [Métricas de tempo de resposta das consultas]
- **Throughput**: [Número de transações por segundo]
- **Utilização de Recursos**: [CPU, memória, disco]

### 13.2. Alertas
- **Espaço em Disco**: [Alertas quando espaço em disco está baixo]
- **Conexões**: [Alertas quando número de conexões está alto]
- **Performance**: [Alertas quando performance está degradada]

## 14. Migrações

### 14.1. Estratégia de Versionamento
- **Versionamento**: [Como as mudanças no schema são versionadas]
- **Migrações**: [Ferramentas utilizadas para migrações]
- **Rollback**: [Procedimentos para rollback de mudanças]

### 14.2. Scripts de Migração
```sql
-- Exemplo de script de migração
-- Versão: 1.1
-- Data: DD/MM/AAAA
-- Descrição: Adicionar campo 'status' na tabela 'users'

ALTER TABLE users 
ADD COLUMN status ENUM('active', 'inactive', 'suspended') 
DEFAULT 'active' NOT NULL;

CREATE INDEX idx_users_status ON users(status);
```

## 15. Conformidade e Regulamentação

### 15.1. LGPD (Lei Geral de Proteção de Dados)
- **Dados Pessoais**: [Identificação de campos com dados pessoais]
- **Anonimização**: [Estratégias de anonimização]
- **Retenção**: [Políticas de retenção de dados pessoais]

### 15.2. Outras Regulamentações
- **SOX**: [Conformidade com Sarbanes-Oxley se aplicável]
- **HIPAA**: [Conformidade com HIPAA se aplicável]
- **PCI DSS**: [Conformidade com PCI DSS se aplicável]

## 16. Aprovações
- **DBA**: [Nome] - [Assinatura/Data]
- **Arquiteto de Dados**: [Nome] - [Assinatura/Data]
- **Gerente de Projeto**: [Nome] - [Assinatura/Data]

---

**Referências**:
- [Link para System Design relacionado]
- [Link para ADRs relevantes]
- [Link para Data Governance]

**Histórico de Revisões**:
| Versão | Data | Autor | Descrição da Mudança |
|--------|------|-------|----------------------|
| 1.0    | DD/MM/AAAA | [Autor] | Criação inicial do Database Schema |
