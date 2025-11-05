# Melhores Práticas de Performance FastAPI

**Versão em Inglês**: [FastAPI Performance Best Practices (EN)](../fastapi-performance-best-practices.md)

## Visão Geral

Este documento descreve práticas comprovadas de otimização de performance para aplicações FastAPI. Essas práticas são baseadas em experiência real e focam em gargalos reais ao invés de otimização prematura.

## ⚠️ Aviso Importante

**O gargalo NÃO está na linguagem ou framework.** Ao construir APIs e sistemas que entregam informações para usuários, os gargalos reais são:

1. **Comunicações com banco de dados** - Execução de queries, pooling de conexões
2. **Requisições HTTP** - Chamadas para APIs externas, latência de rede
3. **Operações de I/O** - Operações de arquivo, I/O de rede

Medições de performance mostram que:
- Operações de CPU em memória são medidas em **nanosegundos**
- Requisições HTTP são medidas em **milissegundos**
- Esta é uma diferença de **1000x** em magnitude

**Referência**: "Numbers Every Programmer Should Know" por Jeff Dean (Google)

### Quando Aplicar Estas Práticas

Essas otimizações devem ser aplicadas:
- ✅ Para casos específicos críticos de performance
- ✅ Quando você identificou gargalos reais
- ✅ Como parte de aprendizado por curiosidade
- ❌ NÃO como otimização prematura
- ❌ NÃO como substituto para otimização adequada de banco de dados/API

## Melhores Práticas

### 1. Use Async/Await em Tudo

**Por que importa:**
- Rotas síncronas podem bloquear a execução
- Código sequencial espera cada operação completar
- Operações assíncronas podem rodar independentemente
- Melhora significativamente o throughput

**Implementação:**

```python
# ❌ RUIM: Rota síncrona
@app.get("/users")
def get_users():
    users = db.query(User).all()  # Bloqueia até completar
    return users

# ✅ BOM: Rota assíncrona
@app.get("/users")
async def get_users():
    users = await db.query(User).all()  # Não-bloqueante
    return users
```

**Pontos Chave:**
- Python agora tem um ecossistema assíncrono maduro
- Use bibliotecas compatíveis com async:
  - `asyncpg` ao invés de `psycopg2` (PostgreSQL)
  - `aiosqlite` ao invés de `sqlite3` (SQLite)
  - `aiomysql` ao invés de `mysql-connector` (MySQL)
  - `motor` para operações assíncronas do MongoDB

**Ganho de Performance:**
- Pode lidar com 3-5x mais requisições concorrentes
- Melhor utilização de recursos
- Menor latência sob carga

---

### 2. Use UVLoop para Event Loop

**Por que importa:**
- Uvicorn padrão usa `asyncio` (event loop padrão do Python)
- UVLoop é uma implementação de event loop de alta performance
- Baseado em `libuv` (mesma biblioteca usada pelo Node.js)
- **4-5x mais rápido** que `asyncio` padrão

**Instalação:**

```bash
# ❌ Instalação padrão (usa asyncio)
pip install uvicorn

# ✅ Com UVLoop (otimizado)
pip install uvicorn[standard]
```

**O que você obtém:**
- `uvloop` - Event loop otimizado
- `httptools` - Parsing HTTP mais rápido
- Outras dependências otimizadas para performance

**Considerações Importantes:**

1. **Compatibilidade de Plataforma:**
   - ✅ Funciona muito bem em **sistemas Unix-like** (Linux, macOS)
   - ❌ **NÃO funciona no Windows**
   - Melhor para deployments Linux em produção

2. **Compatibilidade:**
   - Funciona perfeitamente com imports `asyncio`
   - Nenhuma mudança de código necessária
   - Usa UVLoop automaticamente quando disponível

**Ganho de Performance:**
- 4-5x mais rápido no processamento do event loop
- Menor uso de CPU
- Melhor tratamento de conexões concorrentes

**Erro Comum:**
Muitos desenvolvedores pensam que estão usando UVLoop com `pip install uvicorn` padrão, mas não estão. Sempre use `uvicorn[standard]`.

---

### 3. Configuração Ótima de Servidor

**Melhor Prática:** FastAPI rodando em modo assíncrono com workers Uvicorn gerenciados por Gunicorn.

**Por que esta configuração:**
- **Gunicorn**: Gerenciador de processos e load balancer
- **Workers Uvicorn**: Lidam com requisições assíncronas eficientemente
- Melhor performance para deployments em produção

**Instalação:**

```bash
pip install gunicorn uvicorn[standard]
```

**Configuração:**

Crie `gunicorn_config.py`:

```python
# gunicorn_config.py
import multiprocessing

# Socket do servidor
bind = "0.0.0.0:8000"
backlog = 2048

# Processos worker
# Fórmula: (2 × núcleos de CPU) + 1
workers = (2 * multiprocessing.cpu_count()) + 1
worker_class = "uvicorn.workers.UvicornWorker"

# Configuração dos workers
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Nome do processo
proc_name = "fastapi-app"
```

**Cálculo da Quantidade de Workers:**

```python
# Fórmula: (2 × núcleos de CPU) + 1
workers = (2 * multiprocessing.cpu_count()) + 1

# Opcional: Adicionar mais 1 worker se tiver hyperthreading
# workers = (2 * multiprocessing.cpu_count()) + 2
```

**Executando o Servidor:**

```bash
gunicorn -c gunicorn_config.py main:app
```

**Arquitetura:**
```
Gunicorn (Processo Master)
    ├── Uvicorn Worker 1
    ├── Uvicorn Worker 2
    ├── Uvicorn Worker 3
    └── ... (N workers)
```

**Benefícios:**
- Isolamento de processos (crash de worker não mata todos)
- Balanceamento de carga entre workers
- Reinício gracioso de workers
- Configuração pronta para produção

---

### 4. Use Pydantic v2

**Por que importa:**
- Pydantic v2 tem um **core escrito em Rust**
- Validação muito mais rápida que v1
- Significativamente mais rápido que alternativas:
  - `marshmallow`
  - `serpy`
  - Outros validadores Python

**Instalação:**

```bash
pip install "pydantic>=2.0.0"
```

**Melhor Prática: Use nas Bordas da Aplicação**

```python
# ✅ BOM: Validar nas bordas de requisição/resposta HTTP
@app.post("/users")
async def create_user(user: UserCreate):  # Modelo Pydantic
    # Validar entrada (rápido com Pydantic v2)
    validated_data = user.model_dump()
    
    # Processar com modelos internos (sem overhead de validação)
    result = await user_service.create(validated_data)
    
    return result  # Serialização rápida com Pydantic v2
```

**Quando Usar:**
- ✅ **Validação de entrada** - Ao receber requisições HTTP
- ✅ **Serialização de saída** - Ao retornar respostas HTTP
- ❌ **Evitar** - Estruturas de dados internas (overhead desnecessário)
- ❌ **Evitar** - Validar valores de retorno (validar apenas entradas)

**Ganho de Performance:**
- 5-10x mais rápido que Pydantic v1
- 10-50x mais rápido que outros validadores Python
- Menor uso de memória

**Migração de v1:**
- Maior parte do código é compatível
- Algumas mudanças que quebram compatibilidade em features avançadas
- Veja [Guia de Migração Pydantic v2](https://docs.pydantic.dev/2.0/migration/)

---

### 5. Use orjson para Serialização JSON

**Por que importa:**
- Serialização JSON mais rápida que biblioteca padrão
- Escrito em Rust para performance
- Substituição direta para JSON padrão

**Instalação:**

```bash
pip install orjson
```

**Configuração no FastAPI:**

```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    default_response_class=ORJSONResponse
)

# Ou usar por rota
@app.get("/users", response_class=ORJSONResponse)
async def get_users():
    return {"users": [...]}
```

**Ganho de Performance:**
- 2-3x mais rápido na serialização JSON
- Menor uso de CPU
- Melhor tratamento de payloads grandes

**Compatibilidade:**
- Compatível com todas as features do FastAPI
- Lida com todos os tipos JSON padrão
- Pode ser usado junto com JSON padrão onde necessário

---

## Resumo de Comparação de Performance

| Prática | Ganho de Performance | Caso de Uso |
|----------|-----------------|----------|
| Async/Await | 3-5x throughput | Todas operações I/O |
| UVLoop | 4-5x event loop | Sistemas Unix-like (Linux/macOS) |
| Gunicorn + Uvicorn | Melhor concorrência | Deployments em produção |
| Pydantic v2 | 5-10x validação | Bordas de entrada/saída |
| orjson | 2-3x serialização | Todas respostas JSON |

## Checklist de Implementação

- [ ] Converter todas as rotas para async/await
- [ ] Usar drivers de banco de dados compatíveis com async
- [ ] Instalar `uvicorn[standard]` para UVLoop
- [ ] Configurar Gunicorn com workers Uvicorn
- [ ] Calcular quantidade ótima de workers
- [ ] Atualizar para Pydantic v2
- [ ] Usar Pydantic apenas nas bordas da aplicação
- [ ] Instalar e configurar orjson
- [ ] Atualizar FastAPI para usar ORJSONResponse

## Testando Performance

### Ferramentas de Benchmarking

1. **TechEmpower Web Framework Benchmarks**
   - Comparar performance do FastAPI
   - Ver impacto das otimizações

2. **Apache Bench (ab)**
   ```bash
   ab -n 10000 -c 100 http://localhost:8000/users
   ```

3. **wrk**
   ```bash
   wrk -t12 -c400 -d30s http://localhost:8000/users
   ```

### Métricas para Monitorar

- **Tempo de Resposta** (p50, p95, p99)
- **Throughput** (requisições por segundo)
- **Taxa de Erro** (percentual de requisições falhadas)
- **Uso de CPU** (deve diminuir com otimizações)
- **Uso de Memória** (monitorar vazamentos)

## Erros Comuns a Evitar

1. ❌ **Usar código síncrono em rotas assíncronas**
   ```python
   # Não faça isso
   @app.get("/users")
   async def get_users():
       users = db.query(User).all()  # Bloqueante!
       return users
   ```

2. ❌ **Instalar uvicorn padrão ao invés de uvicorn[standard]**
   ```bash
   # Errado
   pip install uvicorn
   
   # Correto
   pip install uvicorn[standard]
   ```

3. ❌ **Usar Pydantic para estruturas de dados internas**
   ```python
   # Não valide tudo
   def process_data(data: UserModel):  # Validação desnecessária
       ...
   ```

4. ❌ **Não otimizar queries de banco de dados**
   - Lembre-se: DB geralmente é o gargalo
   - Otimize queries antes de otimizar o framework

5. ❌ **Otimização prematura**
   - Perfile primeiro, otimize depois
   - Foque em gargalos reais

## Exemplo do Mundo Real

### Antes da Otimização

```python
from fastapi import FastAPI
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/users")
def get_users(db: Session):
    # Síncrono, bloqueante
    users = db.query(User).all()
    return users
```

**Performance:**
- ~100 requisições/segundo
- Alto uso de CPU
- Operações bloqueantes

### Depois da Otimização

```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(default_response_class=ORJSONResponse)

@app.get("/users")
async def get_users(db: AsyncSession):
    # Assíncrono, não-bloqueante
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users
```

**Configuração:**
```bash
# gunicorn_config.py
workers = (2 * multiprocessing.cpu_count()) + 1
worker_class = "uvicorn.workers.UvicornWorker"
```

**Performance:**
- ~500-1000 requisições/segundo
- Menor uso de CPU
- Operações não-bloqueantes
- Melhor utilização de recursos

## Recursos Adicionais

### Recursos de Aprendizado

- [Documentação FastAPI Async](https://fastapi.tiangolo.com/async/)
- [Documentação Pydantic v2](https://docs.pydantic.dev/2.0/)
- [Repositório GitHub UVLoop](https://github.com/MagicStack/uvloop)
- [Configuração Gunicorn](https://docs.gunicorn.org/en/stable/settings.html)

### Referências de Performance

- "Numbers Every Programmer Should Know" - Jeff Dean (Google)
- TechEmpower Web Framework Benchmarks
- FastAPI Performance Benchmarks

## Conclusão

Essas práticas podem melhorar significativamente a performance do FastAPI, mas lembre-se:

1. **Perfile primeiro** - Identifique gargalos reais
2. **Otimize banco de dados** - Geralmente o maior gargalo
3. **Meça o impacto** - Verifique melhorias com benchmarks
4. **Não otimize demais** - Foque em problemas reais

A combinação de async/await, UVLoop, configuração adequada de servidor, Pydantic v2 e orjson pode proporcionar melhorias substanciais de performance, mas sempre meça e verifique o impacto no seu caso de uso específico.

---

**Última Atualização**: 2025-01-XX
**Mantenedor**: Equipe de Arquitetura Skynet
**Versão**: 1.0

