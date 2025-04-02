# Web Scraping e Processamento de Dados com Python

Este repositório contém um projeto de web scraping que coleta arquivos PDF do site da ANS (Agência Nacional de Saúde), processa seus dados e os transforma em arquivos CSV e Excel, além de armazená-los em um banco de dados PostgreSQL para análise.

## 🛠️ Tecnologias Utilizadas
- **Linguagem**: Python
- **IDE**: PyCharm (ou VSCode)
- **Bibliotecas principais**:
  - `requests`
  - `BeautifulSoup`
  - `zipfile`
  - `pdfplumber`
  - `pandas`
  - `xlsxwriter`
  - `psycopg2` (para conexão com PostgreSQL)

## 🔧 Estrutura do Projeto
```
/
|-- web_scraping_ans.py  # Script para realizar web scraping e baixar PDFs
|-- Transformacao_dados.py  # Script para extrair dados dos PDFs e salvar em CSV/Excel
|-- database_queries.sql  # Consultas SQL para análise dos dados
|-- input_files/  # Armazena arquivos ZIP com PDFs baixados
|-- extracted_files/  # PDFs extraídos do ZIP
|-- output_files/  # Contém os arquivos CSV e Excel processados
|-- README.md  # Documentação do projeto
```

## 📝 Instalação e Configuração
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/Deivisnan/Teste_2025_Nivelamento.git
   cd seu-repositorio
   ```

2. **Crie um ambiente virtual e instale as dependências**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Execute o Web Scraping**:
   ```bash
   python web_scraping_ans.py
   ```
   - O script baixa os PDFs da ANS e os compacta em `input_files/anexos.zip`.

4. **Transforme os Dados**:
   ```bash
   python Transformacao_dados.py
   ```
   - Extrai tabelas dos PDFs e gera os arquivos `output_files/rol_de_procedimentos.csv` e `output_files/rol_de_procedimentos.xlsx`.

5. **Configurar e Popular o Banco de Dados (Opcional)**:
   - Crie um banco de dados PostgreSQL e configure suas credenciais no script.
   - Execute as queries SQL para análise dos dados.

## 📊 Consultas SQL para Análise
### Top 10 operadoras com mais despesas no último trimestre:
```sql
SELECT  
    reg_ans AS operadora,  
    trimestre,  
    SUM(vl_saldo_inicial - vl_saldo_final) AS total_despesas  
FROM despesas_operadoras  
WHERE descricao ILIKE '%EVENTOS%SINISTROS%'  
    AND trimestre = 4  
GROUP BY operadora, trimestre  
ORDER BY total_despesas DESC  
LIMIT 10;
```

### Top 10 operadoras com mais despesas no ano:
```sql
SELECT  
    reg_ans AS operadora,  
    trimestre,  
    SUM(vl_saldo_inicial - vl_saldo_final) AS total_despesas  
FROM despesas_operadoras  
WHERE descricao ILIKE '%EVENTOS%SINISTROS%'  
GROUP BY operadora, trimestre  
ORDER BY total_despesas DESC  
LIMIT 10;
```


