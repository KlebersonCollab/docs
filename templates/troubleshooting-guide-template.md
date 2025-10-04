# Template: Troubleshooting Guide

## 1. Informações Básicas
- **ID do Guia**: [TS-XXX]
- **Nome do Sistema/Componente**: [Nome do Sistema]
- **Versão**: [1.0]
- **Data de Criação**: [DD/MM/AAAA]
- **Última Atualização**: [DD/MM/AAAA]
- **Autor**: [Nome do Engenheiro/Support]
- **Status**: [Rascunho/Em Revisão/Aprovado]

## 2. Visão Geral
[Descrição geral do sistema, componentes principais e áreas comuns de problemas.]

## 3. Informações de Contato
- **Equipe de Suporte**: [Contatos da equipe]
- **Escalação**: [Procedimentos de escalação]
- **Horário de Funcionamento**: [Horários de atendimento]
- **Emergências**: [Contatos para emergências]

## 4. Problemas Comuns e Soluções

### 4.1. Problemas de Conectividade

#### Problema: "Erro de conexão com o banco de dados"
**Sintomas**:
- Aplicação não consegue conectar ao banco
- Mensagem de erro: "Connection refused"
- Timeout em operações de banco

**Possíveis Causas**:
- Banco de dados indisponível
- Credenciais incorretas
- Firewall bloqueando conexão
- Configuração de rede incorreta

**Soluções**:
1. **Verificar status do banco**:
   ```bash
   # PostgreSQL
   pg_isready -h localhost -p 5432
   
   # MySQL
   mysqladmin ping -h localhost -P 3306
   ```

2. **Verificar credenciais**:
   ```bash
   # Testar conexão
   psql -h localhost -U username -d database_name
   ```

3. **Verificar firewall**:
   ```bash
   # Verificar portas abertas
   netstat -tulpn | grep 5432
   ```

4. **Verificar configurações**:
   - Verificar variáveis de ambiente
   - Verificar arquivo de configuração
   - Verificar logs do banco

**Prevenção**:
- Monitorar saúde do banco
- Implementar health checks
- Configurar alertas de conectividade

---

#### Problema: "Timeout em requisições HTTP"
**Sintomas**:
- Requisições demoram muito para responder
- Erro 504 Gateway Timeout
- Aplicação lenta

**Possíveis Causas**:
- Sobrecarga do servidor
- Consultas lentas no banco
- Problemas de rede
- Recursos insuficientes

**Soluções**:
1. **Verificar recursos do servidor**:
   ```bash
   # CPU
   top
   htop
   
   # Memória
   free -m
   
   # Disco
   df -h
   ```

2. **Verificar consultas lentas**:
   ```sql
   -- PostgreSQL
   SELECT query, mean_time, calls 
   FROM pg_stat_statements 
   ORDER BY mean_time DESC 
   LIMIT 10;
   ```

3. **Verificar logs da aplicação**:
   ```bash
   tail -f /var/log/myapp/app.log | grep -i error
   ```

4. **Otimizar consultas**:
   - Adicionar índices
   - Revisar queries
   - Implementar cache

**Prevenção**:
- Monitorar performance
- Implementar cache
- Otimizar consultas
- Configurar alertas de performance

---

### 4.2. Problemas de Autenticação

#### Problema: "Token de autenticação inválido"
**Sintomas**:
- Erro 401 Unauthorized
- Usuários não conseguem fazer login
- Sessões expiram rapidamente

**Possíveis Causas**:
- Token expirado
- Chave JWT incorreta
- Problema no serviço de autenticação
- Configuração de timezone incorreta

**Soluções**:
1. **Verificar configuração JWT**:
   ```bash
   # Verificar variáveis de ambiente
   echo $JWT_SECRET
   echo $JWT_EXPIRATION
   ```

2. **Testar geração de token**:
   ```bash
   # Testar endpoint de login
   curl -X POST http://localhost:8080/auth/login \
        -H "Content-Type: application/json" \
        -d '{"username":"test","password":"test"}'
   ```

3. **Verificar logs de autenticação**:
   ```bash
   grep -i "auth\|token\|jwt" /var/log/myapp/app.log
   ```

4. **Verificar configuração de timezone**:
   ```bash
   date
   timedatectl status
   ```

**Prevenção**:
- Monitorar logs de autenticação
- Implementar alertas de falha de login
- Configurar rotação de chaves

---

### 4.3. Problemas de Performance

#### Problema: "Aplicação lenta"
**Sintomas**:
- Tempo de resposta alto
- Usuários reclamam de lentidão
- CPU alta
- Memória alta

**Possíveis Causas**:
- Consultas lentas no banco
- Falta de cache
- Recursos insuficientes
- Código ineficiente

**Soluções**:
1. **Análise de performance**:
   ```bash
   # Profiling da aplicação
   strace -p $(pgrep myapp)
   
   # Análise de rede
   netstat -i
   ss -tulpn
   ```

2. **Otimizar banco de dados**:
   ```sql
   -- Verificar consultas lentas
   EXPLAIN ANALYZE SELECT * FROM large_table WHERE condition;
   
   -- Verificar índices
   \d+ table_name
   ```

3. **Implementar cache**:
   ```bash
   # Redis
   redis-cli ping
   redis-cli info memory
   ```

4. **Otimizar código**:
   - Revisar algoritmos
   - Implementar cache
   - Otimizar queries

**Prevenção**:
- Monitorar métricas de performance
- Implementar profiling contínuo
- Configurar alertas de performance

---

### 4.4. Problemas de Memória

#### Problema: "Out of Memory"
**Sintomas**:
- Erro "OutOfMemoryError"
- Aplicação trava
- Sistema lento

**Possíveis Causas**:
- Memory leak no código
- Configuração de heap insuficiente
- Processo consumindo muita memória
- Cache muito grande

**Soluções**:
1. **Verificar uso de memória**:
   ```bash
   # Verificar memória do sistema
   free -m
   
   # Verificar processos
   ps aux --sort=-%mem | head -10
   ```

2. **Análise de heap (Java)**:
   ```bash
   # Gerar heap dump
   jmap -dump:format=b,file=heap.hprof <pid>
   
   # Analisar heap
   jhat heap.hprof
   ```

3. **Ajustar configurações**:
   ```bash
   # Aumentar heap (Java)
   export JAVA_OPTS="-Xmx2g -Xms1g"
   ```

4. **Identificar memory leaks**:
   - Revisar código
   - Usar ferramentas de profiling
   - Implementar monitoramento

**Prevenção**:
- Monitorar uso de memória
- Implementar alertas
- Revisar código regularmente

---

## 5. Comandos de Diagnóstico

### 5.1. Comandos de Sistema
```bash
# Verificar status do sistema
uptime
who
w

# Verificar recursos
top
htop
free -m
df -h

# Verificar processos
ps aux
ps aux | grep myapp

# Verificar rede
netstat -tulpn
ss -tulpn
ip addr show
```

### 5.2. Comandos de Aplicação
```bash
# Verificar logs
tail -f /var/log/myapp/app.log
tail -f /var/log/myapp/error.log

# Verificar status da aplicação
curl -f http://localhost:8080/health
curl -f http://localhost:8080/status

# Verificar configurações
cat /etc/myapp/config.yml
env | grep MYAPP
```

### 5.3. Comandos de Banco de Dados
```bash
# PostgreSQL
psql -h localhost -U username -d database_name
SELECT * FROM pg_stat_activity;
SELECT * FROM pg_stat_database;

# MySQL
mysql -h localhost -u username -p
SHOW PROCESSLIST;
SHOW STATUS;
```

## 6. Logs e Monitoramento

### 6.1. Localização dos Logs
- **Aplicação**: `/var/log/myapp/app.log`
- **Erros**: `/var/log/myapp/error.log`
- **Acesso**: `/var/log/nginx/access.log`
- **Sistema**: `/var/log/syslog`

### 6.2. Comandos de Análise de Logs
```bash
# Buscar erros
grep -i error /var/log/myapp/app.log
grep -i "exception\|error\|fatal" /var/log/myapp/app.log

# Buscar por padrões
grep "pattern" /var/log/myapp/app.log
awk '/pattern/ {print $0}' /var/log/myapp/app.log

# Análise de frequência
grep -c "error" /var/log/myapp/app.log
sort | uniq -c | sort -nr
```

### 6.3. Ferramentas de Monitoramento
- **Prometheus**: Métricas de sistema
- **Grafana**: Dashboards de monitoramento
- **ELK Stack**: Análise de logs
- **New Relic**: APM (Application Performance Monitoring)

## 7. Procedimentos de Escalação

### 7.1. Níveis de Escalação
1. **Nível 1**: Suporte básico
   - Problemas simples
   - Soluções documentadas
   - Tempo de resposta: 2 horas

2. **Nível 2**: Suporte técnico
   - Problemas complexos
   - Análise detalhada
   - Tempo de resposta: 1 hora

3. **Nível 3**: Especialistas
   - Problemas críticos
   - Desenvolvimento
   - Tempo de resposta: 30 minutos

### 7.2. Critérios de Escalação
- **Crítico**: Sistema indisponível
- **Alto**: Performance degradada
- **Médio**: Problemas não críticos
- **Baixo**: Melhorias e otimizações

## 8. Procedimentos de Emergência

### 8.1. Sistema Indisponível
1. **Identificar causa**:
   - Verificar logs
   - Verificar recursos
   - Verificar dependências

2. **Aplicar solução rápida**:
   - Restart de serviços
   - Rollback se necessário
   - Ativação de backup

3. **Comunicar stakeholders**:
   - Notificar usuários
   - Atualizar status
   - Estimar tempo de resolução

### 8.2. Perda de Dados
1. **Avaliar impacto**:
   - Quantificar perda
   - Identificar dados afetados
   - Verificar backups

2. **Recuperação**:
   - Restaurar backup
   - Validar integridade
   - Testar funcionalidades

3. **Comunicação**:
   - Notificar stakeholders
   - Documentar incidente
   - Implementar melhorias

## 9. Prevenção de Problemas

### 9.1. Monitoramento Proativo
- **Health Checks**: Verificação contínua
- **Alertas**: Notificações automáticas
- **Métricas**: Monitoramento de KPIs
- **Logs**: Análise contínua

### 9.2. Manutenção Preventiva
- **Atualizações**: Patches de segurança
- **Limpeza**: Logs e dados antigos
- **Otimização**: Performance contínua
- **Backup**: Verificação de backups

### 9.3. Documentação
- **Runbooks**: Procedimentos operacionais
- **Playbooks**: Resposta a incidentes
- **Conhecimento**: Base de conhecimento
- **Treinamento**: Capacitação da equipe

## 10. Aprovações
- **Engenheiro de Suporte**: [Nome] - [Assinatura/Data]
- **Gerente de Operações**: [Nome] - [Assinatura/Data]
- **Arquiteto**: [Nome] - [Assinatura/Data]

---

**Referências**:
- [Link para Deployment Guide]
- [Link para System Design]
- [Link para ADRs relevantes]

**Histórico de Revisões**:
| Versão | Data | Autor | Descrição da Mudança |
|--------|------|-------|----------------------|
| 1.0    | DD/MM/AAAA | [Autor] | Criação inicial do Troubleshooting Guide |
