# Template: Database Schema

## 📋 **Informações do Documento**
- **Tipo**: Template de Arquitetura
- **Categoria**: Database
- **Versão**: 1.0
- **Data**: [DATA_ATUAL]
- **Autor**: [AUTOR]
- **Revisado por**: [REVISOR]

## 🎯 **Visão Geral**

Este template fornece uma estrutura completa para documentar schemas de banco de dados, incluindo tabelas, relacionamentos, índices, e estratégias de otimização.

## 📐 **Estrutura do Template**

### **1. Informações Gerais**
```markdown
# [Nome do Schema]

## Informações Gerais
- **Banco de Dados**: [PostgreSQL, MySQL, MongoDB, etc.]
- **Versão**: [v1.0.0]
- **Ambiente**: [Desenvolvimento, Produção]
- **Encoding**: [UTF-8]
- **Collation**: [utf8_general_ci]

## Objetivo
- [Descrição do propósito do schema]
- [Contexto de uso]
- [Principais funcionalidades suportadas]
```

### **2. Diagrama do Schema**
```markdown
## Diagrama do Schema

### ERD (Entity Relationship Diagram)
```
[Diagrama Mermaid ou referência para arquivo de imagem]

### Principais Entidades
- [Entidade 1]: [Descrição]
- [Entidade 2]: [Descrição]
- [Entidade 3]: [Descrição]
```

### **3. Tabelas e Estruturas**
```markdown
## Tabelas e Estruturas

### [Nome da Tabela]
**Descrição**: [Descrição da tabela e seu propósito]

**Colunas**:
| Nome | Tipo | Tamanho | Null | Default | Chave | Índice | Descrição |
|------|------|---------|------|---------|-------|--------|-----------|
| id | INT | 11 | NO | AUTO_INCREMENT | PK | PRIMARY | Identificador único |
| name | VARCHAR | 255 | NO | - | - | INDEX | Nome do registro |
| email | VARCHAR | 255 | NO | - | UNIQUE | UNIQUE | Email único |
| created_at | TIMESTAMP | - | NO | CURRENT_TIMESTAMP | - | INDEX | Data de criação |
| updated_at | TIMESTAMP | - | YES | NULL | - | - | Data de atualização |

**Relacionamentos**:
- **1:N** com [Tabela Relacionada]: [Descrição do relacionamento]
- **N:N** com [Tabela Relacionada]: [Descrição do relacionamento]

**Índices**:
- **PRIMARY**: id
- **UNIQUE**: email
- **INDEX**: created_at, name

**Constraints**:
- **CHECK**: email LIKE '%@%'
- **FOREIGN KEY**: user_id REFERENCES users(id)
```

### **4. Relacionamentos**
```markdown
## Relacionamentos

### Relacionamentos Principais
```
[Diagrama de relacionamentos ou descrição textual]

### Tipos de Relacionamento
- **1:1 (One-to-One)**: [Descrição e exemplos]
- **1:N (One-to-Many)**: [Descrição e exemplos]
- **N:N (Many-to-Many)**: [Descrição e exemplos]

### Tabelas de Junção
- **[tabela_juncao]**: [Propósito e campos]
- **[tabela_juncao]**: [Propósito e campos]
```

### **5. Índices e Performance**
```markdown
## Índices e Performance

### Índices Primários
- **PRIMARY KEY**: [Lista de chaves primárias]
- **UNIQUE**: [Lista de índices únicos]

### Índices Secundários
- **INDEX**: [Lista de índices para performance]
- **COMPOSITE**: [Lista de índices compostos]

### Estratégias de Otimização
- **Partitioning**: [Estratégia de particionamento]
- **Sharding**: [Estratégia de sharding]
- **Caching**: [Estratégia de cache]
- **Archiving**: [Estratégia de arquivamento]
```

### **6. Triggers e Procedures**
```markdown
## Triggers e Procedures

### Triggers
```sql
-- Trigger para atualizar updated_at
CREATE TRIGGER update_timestamp
BEFORE UPDATE ON [tabela]
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END;
```

### Stored Procedures
```sql
-- Procedure para buscar usuários
DELIMITER //
CREATE PROCEDURE GetUsers(IN search_term VARCHAR(255))
BEGIN
    SELECT * FROM users 
    WHERE name LIKE CONCAT('%', search_term, '%')
    ORDER BY created_at DESC;
END //
DELIMITER ;
```

### Functions
```sql
-- Function para calcular idade
DELIMITER //
CREATE FUNCTION CalculateAge(birth_date DATE)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    RETURN YEAR(CURDATE()) - YEAR(birth_date);
END //
DELIMITER ;
```
```

### **7. Views**
```markdown
## Views

### [Nome da View]
**Descrição**: [Propósito da view]

```sql
CREATE VIEW [nome_view] AS
SELECT 
    u.id,
    u.name,
    u.email,
    p.phone,
    a.address
FROM users u
LEFT JOIN profiles p ON u.id = p.user_id
LEFT JOIN addresses a ON u.id = a.user_id
WHERE u.active = 1;
```

### Views Materializadas
```sql
-- View materializada para relatórios
CREATE MATERIALIZED VIEW user_stats AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as new_users
FROM users
GROUP BY DATE(created_at);
```
```

### **8. Dados de Exemplo**
```markdown
## Dados de Exemplo

### Inserção de Dados
```sql
-- Inserir usuários de exemplo
INSERT INTO users (name, email, password, created_at) VALUES
('João Silva', 'joao@exemplo.com', 'hash_password', NOW()),
('Maria Santos', 'maria@exemplo.com', 'hash_password', NOW()),
('Pedro Costa', 'pedro@exemplo.com', 'hash_password', NOW());

-- Inserir perfis
INSERT INTO profiles (user_id, phone, birth_date) VALUES
(1, '11999999999', '1990-01-01'),
(2, '11888888888', '1985-05-15'),
(3, '11777777777', '1992-12-25');
```

### Dados de Teste
```sql
-- Script para popular dados de teste
INSERT INTO users (name, email, password, created_at) VALUES
('Test User 1', 'test1@exemplo.com', 'test_hash', NOW()),
('Test User 2', 'test2@exemplo.com', 'test_hash', NOW());
```
```

### **9. Migrações**
```markdown
## Migrações

### Versionamento
- **v1.0.0**: Schema inicial
- **v1.1.0**: Adicionada tabela profiles
- **v1.2.0**: Adicionado índice em email

### Scripts de Migração
```sql
-- Migration: Add profiles table
CREATE TABLE profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    phone VARCHAR(20),
    birth_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Migration: Add index to users.email
CREATE INDEX idx_users_email ON users(email);
```

### Rollback
```sql
-- Rollback: Remove profiles table
DROP TABLE IF EXISTS profiles;

-- Rollback: Remove index
DROP INDEX idx_users_email ON users;
```
```

### **10. Backup e Recovery**
```markdown
## Backup e Recovery

### Estratégias de Backup
- **Full Backup**: [Frequência e procedimento]
- **Incremental Backup**: [Frequência e procedimento]
- **Differential Backup**: [Frequência e procedimento]

### Scripts de Backup
```bash
# Backup completo
mysqldump -u username -p database_name > backup_full.sql

# Backup apenas estrutura
mysqldump -u username -p --no-data database_name > backup_structure.sql

# Backup apenas dados
mysqldump -u username -p --no-create-info database_name > backup_data.sql
```

### Recovery
```bash
# Restaurar backup completo
mysql -u username -p database_name < backup_full.sql

# Restaurar apenas estrutura
mysql -u username -p database_name < backup_structure.sql
```
```

### **11. Monitoramento**
```markdown
## Monitoramento

### Métricas Importantes
- **Tamanho do banco**: [Monitoramento de crescimento]
- **Performance de queries**: [Slow query log]
- **Conexões ativas**: [Monitoramento de conexões]
- **Uso de índices**: [Análise de eficiência]

### Queries de Monitoramento
```sql
-- Tamanho das tabelas
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = 'database_name'
ORDER BY (data_length + index_length) DESC;

-- Queries lentas
SELECT 
    query_time,
    lock_time,
    rows_sent,
    rows_examined,
    sql_text
FROM mysql.slow_log
ORDER BY query_time DESC
LIMIT 10;
```
```

### **12. Segurança**
```markdown
## Segurança

### Controle de Acesso
- **Usuários**: [Lista de usuários e permissões]
- **Roles**: [Definição de roles e responsabilidades]
- **Grants**: [Permissões específicas]

### Criptografia
- **Dados sensíveis**: [Estratégia de criptografia]
- **Passwords**: [Hash e salt]
- **PII**: [Proteção de dados pessoais]

### Auditoria
```sql
-- Tabela de auditoria
CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100),
    operation VARCHAR(10),
    old_values JSON,
    new_values JSON,
    user_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
```

### **13. Performance Tuning**
```markdown
## Performance Tuning

### Otimizações Implementadas
- **Índices**: [Lista de índices para performance]
- **Partitioning**: [Estratégia de particionamento]
- **Query Optimization**: [Otimizações de queries]

### Análise de Performance
```sql
-- Analisar performance de queries
EXPLAIN SELECT * FROM users WHERE email = 'test@exemplo.com';

-- Verificar uso de índices
SHOW INDEX FROM users;

-- Estatísticas de tabelas
ANALYZE TABLE users;
```

### Benchmarks
- **Query Performance**: [Tempos de resposta]
- **Concurrent Users**: [Usuários simultâneos]
- **Throughput**: [Transações por segundo]
```

## 📊 **Checklist de Schema**

### **Estrutura**
- [ ] Todas as tabelas documentadas
- [ ] Relacionamentos definidos
- [ ] Índices otimizados
- [ ] Constraints implementadas

### **Performance**
- [ ] Índices apropriados
- [ ] Queries otimizadas
- [ ] Partitioning se necessário
- [ ] Monitoramento configurado

### **Segurança**
- [ ] Controle de acesso
- [ ] Criptografia de dados sensíveis
- [ ] Auditoria implementada
- [ ] Backup e recovery testados

### **Manutenção**
- [ ] Migrações versionadas
- [ ] Scripts de backup
- [ ] Documentação atualizada
- [ ] Testes de integridade

## 🔗 **Recursos Adicionais**

### **Ferramentas Recomendadas**
- [MySQL Workbench](https://www.mysql.com/products/workbench/)
- [pgAdmin](https://www.pgadmin.org/)
- [DBeaver](https://dbeaver.io/)
- [Lucidchart](https://www.lucidchart.com/)

### **Referências**
- [Database Design Best Practices](https://www.vertabelo.com/blog/database-design-best-practices/)
- [MySQL Performance Tuning](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Última atualização**: [DATA]
**Mantenedor**: [EQUIPE]
**Próxima revisão**: [DATA]
