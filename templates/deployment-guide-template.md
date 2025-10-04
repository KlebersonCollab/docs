# Template: Deployment Guide

## 1. Informações Básicas
- **ID do Deploy**: [DEP-XXX]
- **Nome do Projeto/Sistema**: [Nome do Projeto]
- **Versão**: [1.0]
- **Data de Criação**: [DD/MM/AAAA]
- **Última Atualização**: [DD/MM/AAAA]
- **Autor**: [Nome do DevOps/Engenheiro]
- **Status**: [Rascunho/Em Revisão/Aprovado]

## 2. Visão Geral
[Descrição geral do sistema, arquitetura de deploy, ambientes e estratégia de implantação.]

## 3. Arquitetura de Deploy
[Diagrama da arquitetura de deploy ou link para ele]
```
[Link ou imagem do Diagrama de Arquitetura de Deploy]
```
- **Descrição**: [Explicação da arquitetura, componentes e fluxo de deploy]

## 4. Ambientes

### 4.1. Desenvolvimento (DEV)
- **Propósito**: Desenvolvimento e testes locais
- **URL**: [URL do ambiente de desenvolvimento]
- **Infraestrutura**: [Descrição da infraestrutura]
- **Configurações**: [Configurações específicas do ambiente]

### 4.2. Homologação (HML)
- **Propósito**: Testes de integração e validação
- **URL**: [URL do ambiente de homologação]
- **Infraestrutura**: [Descrição da infraestrutura]
- **Configurações**: [Configurações específicas do ambiente]

### 4.3. Produção (PROD)
- **Propósito**: Ambiente de produção
- **URL**: [URL do ambiente de produção]
- **Infraestrutura**: [Descrição da infraestrutura]
- **Configurações**: [Configurações específicas do ambiente]

## 5. Pré-requisitos

### 5.1. Infraestrutura
- **Servidores**: [Especificações dos servidores]
- **Sistema Operacional**: [Versão e distribuição]
- **Memória**: [Quantidade de RAM necessária]
- **Disco**: [Espaço em disco necessário]
- **Rede**: [Requisitos de rede]

### 5.2. Software
- **Runtime**: [Versão do runtime necessário]
- **Banco de Dados**: [Versão do SGBD]
- **Web Server**: [Versão do servidor web]
- **Dependências**: [Lista de dependências]

### 5.3. Ferramentas
- **CI/CD**: [Ferramentas de integração contínua]
- **Container**: [Docker, Kubernetes, etc.]
- **Monitoramento**: [Ferramentas de monitoramento]
- **Logs**: [Ferramentas de log]

## 6. Configuração do Ambiente

### 6.1. Variáveis de Ambiente
```bash
# Configurações do banco de dados
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=myapp_user
DB_PASSWORD=secret_password

# Configurações da aplicação
APP_ENV=production
APP_DEBUG=false
APP_URL=https://myapp.com

# Configurações de segurança
JWT_SECRET=your_jwt_secret
ENCRYPTION_KEY=your_encryption_key
```

### 6.2. Configurações de Banco de Dados
```sql
-- Script de criação do banco
CREATE DATABASE myapp_production;
CREATE USER myapp_user WITH PASSWORD 'secret_password';
GRANT ALL PRIVILEGES ON DATABASE myapp_production TO myapp_user;
```

### 6.3. Configurações de Rede
- **Portas**: [Portas que devem estar abertas]
- **Firewall**: [Regras de firewall necessárias]
- **SSL/TLS**: [Configurações de certificados]

## 7. Processo de Deploy

### 7.1. Deploy Automatizado (CI/CD)
```yaml
# Exemplo de pipeline
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
    - docker push registry.example.com/myapp:$CI_COMMIT_SHA

test:
  stage: test
  script:
    - docker run --rm myapp:$CI_COMMIT_SHA npm test

deploy:
  stage: deploy
  script:
    - kubectl set image deployment/myapp myapp=registry.example.com/myapp:$CI_COMMIT_SHA
    - kubectl rollout status deployment/myapp
```

### 7.2. Deploy Manual
1. **Preparação**:
   - Verificar se todos os testes passaram
   - Backup do ambiente atual
   - Preparar rollback se necessário

2. **Deploy**:
   - Parar serviços
   - Atualizar código
   - Executar migrações
   - Reiniciar serviços

3. **Validação**:
   - Verificar saúde dos serviços
   - Executar testes de smoke
   - Monitorar logs

## 8. Scripts de Deploy

### 8.1. Script de Deploy Principal
```bash
#!/bin/bash
# deploy.sh

set -e

echo "Iniciando deploy da aplicação..."

# Variáveis
APP_NAME="myapp"
VERSION=$1
ENVIRONMENT=$2

if [ -z "$VERSION" ] || [ -z "$ENVIRONMENT" ]; then
    echo "Uso: ./deploy.sh <versão> <ambiente>"
    exit 1
fi

echo "Deployando versão $VERSION no ambiente $ENVIRONMENT"

# Backup
echo "Criando backup..."
./scripts/backup.sh $ENVIRONMENT

# Deploy
echo "Executando deploy..."
./scripts/update-app.sh $VERSION $ENVIRONMENT

# Migrações
echo "Executando migrações..."
./scripts/run-migrations.sh $ENVIRONMENT

# Validação
echo "Validando deploy..."
./scripts/health-check.sh $ENVIRONMENT

echo "Deploy concluído com sucesso!"
```

### 8.2. Script de Rollback
```bash
#!/bin/bash
# rollback.sh

set -e

echo "Iniciando rollback..."

# Variáveis
ENVIRONMENT=$1
PREVIOUS_VERSION=$2

if [ -z "$ENVIRONMENT" ] || [ -z "$PREVIOUS_VERSION" ]; then
    echo "Uso: ./rollback.sh <ambiente> <versão_anterior>"
    exit 1
fi

echo "Fazendo rollback para versão $PREVIOUS_VERSION no ambiente $ENVIRONMENT"

# Parar serviços
echo "Parando serviços..."
./scripts/stop-services.sh $ENVIRONMENT

# Restaurar versão anterior
echo "Restaurando versão anterior..."
./scripts/restore-version.sh $PREVIOUS_VERSION $ENVIRONMENT

# Reiniciar serviços
echo "Reiniciando serviços..."
./scripts/start-services.sh $ENVIRONMENT

# Validação
echo "Validando rollback..."
./scripts/health-check.sh $ENVIRONMENT

echo "Rollback concluído com sucesso!"
```

## 9. Monitoramento e Observabilidade

### 9.1. Health Checks
```bash
#!/bin/bash
# health-check.sh

# Verificar se a aplicação está respondendo
curl -f http://localhost:8080/health || exit 1

# Verificar banco de dados
pg_isready -h $DB_HOST -p $DB_PORT || exit 1

# Verificar logs de erro
if grep -q "ERROR" /var/log/myapp/app.log; then
    echo "Erros encontrados nos logs"
    exit 1
fi

echo "Health check passou com sucesso"
```

### 9.2. Métricas de Monitoramento
- **CPU**: [Limites de uso de CPU]
- **Memória**: [Limites de uso de memória]
- **Disco**: [Limites de uso de disco]
- **Rede**: [Limites de tráfego de rede]
- **Aplicação**: [Métricas específicas da aplicação]

### 9.3. Alertas
- **Disponibilidade**: [Alertas de indisponibilidade]
- **Performance**: [Alertas de degradação de performance]
- **Erros**: [Alertas de erros críticos]
- **Recursos**: [Alertas de recursos esgotados]

## 10. Segurança

### 10.1. Configurações de Segurança
- **Firewall**: [Regras de firewall]
- **SSL/TLS**: [Configurações de certificados]
- **Autenticação**: [Configurações de autenticação]
- **Autorização**: [Configurações de autorização]

### 10.2. Segredos e Credenciais
- **Gerenciamento**: [Como os segredos são gerenciados]
- **Rotação**: [Estratégia de rotação de credenciais]
- **Criptografia**: [Criptografia de dados sensíveis]

## 11. Backup e Recuperação

### 11.1. Estratégia de Backup
- **Frequência**: [Frequência dos backups]
- **Retenção**: [Período de retenção]
- **Localização**: [Onde os backups são armazenados]
- **Validação**: [Como os backups são validados]

### 11.2. Procedimentos de Recuperação
- **RTO**: [Tempo máximo para recuperação]
- **RPO**: [Perda máxima de dados aceitável]
- **Procedimentos**: [Passos para recuperação]

## 12. Troubleshooting

### 12.1. Problemas Comuns
| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| Aplicação não inicia | Porta ocupada | Verificar portas em uso |
| Erro de conexão com DB | Credenciais incorretas | Verificar variáveis de ambiente |
| Performance degradada | Recursos insuficientes | Verificar CPU/memória |
| Logs de erro | Bug na aplicação | Verificar logs e código |

### 12.2. Comandos de Diagnóstico
```bash
# Verificar status dos serviços
systemctl status myapp

# Verificar logs
tail -f /var/log/myapp/app.log

# Verificar recursos
htop
df -h
free -m

# Verificar conectividade
netstat -tulpn
ss -tulpn
```

## 13. Manutenção

### 13.1. Atualizações de Sistema
- **Frequência**: [Frequência das atualizações]
- **Processo**: [Processo de atualização]
- **Testes**: [Testes após atualização]

### 13.2. Limpeza e Otimização
- **Logs**: [Limpeza de logs antigos]
- **Cache**: [Limpeza de cache]
- **Dados**: [Arquivamento de dados antigos]

## 14. Documentação de Suporte

### 14.1. Contatos
- **Equipe de Desenvolvimento**: [Contatos]
- **Equipe de DevOps**: [Contatos]
- **Equipe de Suporte**: [Contatos]

### 14.2. Recursos
- **Documentação**: [Links para documentação]
- **Ferramentas**: [Ferramentas de monitoramento]
- **Procedimentos**: [Procedimentos de emergência]

## 15. Aprovações
- **DevOps**: [Nome] - [Assinatura/Data]
- **Arquiteto**: [Nome] - [Assinatura/Data]
- **Gerente de Projeto**: [Nome] - [Assinatura/Data]

---

**Referências**:
- [Link para System Design relacionado]
- [Link para ADRs relevantes]
- [Link para Infrastructure as Code]

**Histórico de Revisões**:
| Versão | Data | Autor | Descrição da Mudança |
|--------|------|-------|----------------------|
| 1.0    | DD/MM/AAAA | [Autor] | Criação inicial do Deployment Guide |
