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
# 📌 Guia para Executar o Projeto

Este repositório contém um projeto que integra um **backend em Flask** com um **frontend em Vue.js**, permitindo a busca de operadoras de planos de saúde a partir de um arquivo CSV.

## 📂 Estrutura do Projeto

```
/
├── backend/      # Servidor Flask (API REST)
├── frontend/     # Aplicação Vue.js (Interface do Usuário)
└── README.md     # Documentação
```

---

# 🔧 Configuração do Backend (Flask)

## 🛠 1. Instalação das Dependências

O backend utiliza Python e Flask para processar a busca de operadoras. Certifique-se de ter o Python instalado e, em seguida, execute os comandos abaixo no terminal:

```sh
cd backend  # Acesse a pasta do backend
python -m venv venv  # Cria um ambiente virtual
source venv/bin/activate  # Ativa o ambiente virtual (Linux/macOS)
venv\Scripts\activate  # Ativa o ambiente virtual (Windows)

pip install -r requirements.txt  # Instala as dependências
```

##  2. Executar o Servidor Flask

O servidor Flask carrega os dados do arquivo CSV e disponibiliza uma API para busca. Para rodar o servidor, execute:

```sh
python app.py
```

Se tudo estiver correto, você verá a mensagem:

```
 * Running on http://127.0.0.1:5000
```

A API terá uma rota principal:

- **GET ****`/buscar?q=<termo>`** → Retorna as operadoras que contêm `<termo>` no nome fantasia.

### Exemplo de Uso no Postman:

**Requisição:**

```
GET http://127.0.0.1:5000/buscar?q=ALMA ODONTO
```

**Resposta esperada:**

```json
[
    {
        "Nome_Fantasia": "ALMA ODONTO",
        "Cidade": "Campinas",
        "UF": "SP"
    }
]
```

---

# 🌐 Configuração do Frontend (Vue.js)

## 🛠 1. Instalação das Dependências

Certifique-se de ter o **Node.js** instalado e, em seguida, execute:

```sh
cd frontend  # Acesse a pasta do frontend
npm install  # Instala as dependências do Vue.js
```

##  2. Executar o Servidor Vue.js

Agora, rode a aplicação Vue.js:

```sh
npm run dev
```

Isso iniciará um servidor local, geralmente acessível em:

```
http://localhost:5173
```

Agora você pode testar a interface de busca! 🔍

---

# 🔗 Fluxo de Funcionamento

1️⃣ O usuário digita um termo na interface Vue.js.\
2️⃣ O Vue.js faz uma requisição GET para `http://127.0.0.1:5000/buscar?q=TERMO`.\
3️⃣ O Flask procura os dados no CSV e retorna uma lista de operadoras.\
4️⃣ O Vue.js exibe os resultados na tela.

**Componente Vue.js principal:** `BuscaOperadoras.vue`\
Certifique-se de que o nome do componente está correto ao importá-lo:

```vue
<script>
import BuscaOperadoras from "./components/BuscaOperadoras.vue";

export default {
  components: {
    BuscaOperadoras,
  },
};
</script>
```

---





