# Data Pipeline: MongoDB to Supabase (Medallion Architecture)
Este projeto demonstra a construção de um pipeline de dados ponta a ponta, integrando fontes NoSQL locais/nuvem a um Data Warehouse moderno no PostgreSQL (Supabase), orquestrado por Apache Airflow.

## 🚀 Tecnologias Utilizadas
- **Ingestão:** Airbyte Cloud
- **Orquestração:** Apache Airflow (Docker)
- **Banco de Dados:** MongoDB Atlas (Fonte) & Supabase / PostgreSQL (Destino)
- **Visualização:** Apache Zeppelin
- **Transformação:** SQL (PostgreSQL JSONB)

## 🏗️ Arquitetura do Projeto
O pipeline segue os princípios da **Medallion Architecture:**
- **Bronze (Raw):** Ingestão bruta de documentos JSON do MongoDB para tabelas `raw_` no PostgreSQL.
- **Silver (Clean):** Transformação e tipagem de dados via Airflow, convertendo campos JSONB em colunas relacionais.
- **Gold (Analytics):** Visualização de métricas de filmes e notas para consumo de BI.

## 🛠️ Desafios Técnicos Superados
**1. Autenticação SCRAM-SHA-256 (Authentication Type 10)**
Ao conectar ferramentas locais ao Supabase, identifiquei uma incompatibilidade de handshake. Resolvi o problema atualizando os **artifacts JDBC** para a versão `42.5.4` e configurando a string de conexão com parâmetros de `tenant/project ID`.

**2. Tratamento de Qualidade de Dados (Null Treatment)**
Implementei lógica de `CASE WHEN` em SQL para tratar strings vazias vindas da fonte NoSQL, garantindo que a conversão para `FLOAT` e `INT` não quebrasse as ferramentas de visualização.

```
SQL

CASE 
    WHEN (imdb->>'rating') = '' THEN NULL 
    ELSE (imdb->>'rating')::float 
END as rating
```
## 📊 Resultados
- **Pipeline Automatizado:** DAGs do Airflow configuradas com sucesso.
- **Dados Estruturados:** Visualização limpa no editor do Supabase.
- **Insights Gerados:** Dashboards funcionais no Apache Zeppelin.
