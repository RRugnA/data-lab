# Data Pipeline: MongoDB → Lakehouse (Medallion Architecture)

Este projeto demonstra a construção de um **pipeline de dados end‑to‑end**, integrando uma fonte **NoSQL (MongoDB Atlas)** a um ambiente analítico moderno, com **orquestração via Apache Airflow**, **ingestão com Airbyte** e **camadas Medallion (Bronze/Silver/Gold)**. O foco está em **qualidade de dados, escalabilidade e governança**.

> Projeto apresentado em um post no LinkedIn (link nos comentários do post).

---

## 🚀 Tecnologias Utilizadas
- **Ingestão (EL):** Airbyte Cloud
- **Orquestração:** Apache Airflow (Docker)
- **Fonte:** MongoDB Atlas (Replica Set)
- **Camada Relacional (Silver):** Supabase / PostgreSQL
- **Processamento Analítico:** SQL (PostgreSQL / JSONB)
- **Analytics:** Apache Zeppelin

---

## 📥 Ingestão de Dados (Airbyte)
Para a fase de extração e carga (EL), foi utilizado o **Airbyte Cloud**:
- **Source:** MongoDB Atlas (Replica Set).
- **Destination:** PostgreSQL no Supabase.
- **Sync Mode:** Incremental Append + Dedup *(Full Refresh utilizado neste laboratório)*.
- **Persistência:** Documentos NoSQL mapeados para colunas `JSONB` na tabela `raw_movies`, preservando a estrutura original para transformações posteriores.

---

## ⚙️ Orquestração e Transformação (Airflow)
- **Automação:** DAGs em Python para controlar a execução das transformações.
- **Transformação (Silver):** Limpeza, padronização e tipagem de dados.
- **SQL Moderno:** Uso de `CASE WHEN`, `CAST` e operadores JSON (`->`, `->>`) para converter estruturas JSON complexas em colunas relacionais (`FLOAT`, `INT`, `TEXT`).

---

## 🏗️ Arquitetura do Projeto
O pipeline segue os princípios da **Medallion Architecture**, com uma adaptação híbrida:

- **Bronze (Raw):** Ingestão bruta de documentos JSON do MongoDB em tabelas `raw_` no PostgreSQL.
- **Silver (Clean):** Transformações e tipagem via Airflow, extraindo campos JSONB para colunas relacionais no PostgreSQL.
- **Gold (Analytics):** Consumo analítico e visualização no Apache Zeppelin.

> Observação: a arquitetura Medallion foi aplicada de forma híbrida, utilizando PostgreSQL como camada intermediária antes do consumo analítico.

---

## 🛠️ Desafios Técnicos Superados

### 1️⃣ Autenticação SCRAM‑SHA‑256 (Authentication Type 10)
Ao conectar ferramentas locais ao Supabase, foi identificada uma incompatibilidade de handshake JDBC.

**Solução:**
- Atualização do driver JDBC para a versão **42.5.4**.
- Ajuste da string de conexão com parâmetros corretos de **tenant/project ID**.

### 2️⃣ Tratamento de Qualidade de Dados (Null Treatment)
Alguns campos vinham como **strings vazias** a partir da fonte NoSQL, quebrando conversões numéricas.

**Solução:**
Implementação de lógica defensiva em SQL para garantir conversões seguras:

```sql
CASE
    WHEN (imdb->>'rating') = '' THEN NULL
    ELSE (imdb->>'rating')::float
END AS rating
```

---

## ⏳ Time Travel e Versionamento de Dados (Delta Lake)

Como parte da camada analítica, foi implementado **Time Travel utilizando Delta Lake**, permitindo:
- Auditoria de alterações ao longo do tempo.
- Recuperação de versões históricas dos dados.
- Comparação entre estados antigos e atuais das tabelas analíticas.

A funcionalidade foi validada por meio de consultas a versões específicas da tabela, garantindo rastreabilidade e confiabilidade do dado — um requisito essencial em ambientes de dados governados.

> Exemplo de uso: consultas a versões anteriores para análise de regressão de métricas e validação de correções de dados.

---

## 📊 Resultados
- **Conectividade Cloud‑to‑Cloud:** Ingestão bem‑sucedida do **MongoDB Atlas** para o **PostgreSQL no Supabase**.
- **Mapeamento NoSQL → Relacional:** Persistência de dados em `JSONB` com posterior normalização.
- **Pipeline Automatizado:** DAGs do Airflow executando transformações de forma reprodutível.
- **Dados Prontos para Análise:** Estrutura limpa e tipada para consumo analítico.
- **Insights Gerados:** Dashboards funcionais no Apache Zeppelin.

<p align="center">
  <img src="images/Airbyte.jpg" alt="Airbyte" width="600" />
  <img src="images/Airflow 2.jpg" alt="Airflow" width="600" />
  <img src="images/Databricks-Describe-History.jpg" alt="Databricks" width="600" />
  <img src="images/zeppelin.jpg" alt="Apache Zeppelin" width="600" />
</p>

---

## 🔮 Próximos Passos
- Expandir o uso de **Time Travel** para cenários de rollback automatizado.
- Implementar **testes de qualidade de dados** (Great Expectations / Soda).
- Adicionar **observabilidade do pipeline** (SLAs, alertas e métricas).

