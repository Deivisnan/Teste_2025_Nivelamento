from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Permitir requisições do Vue.js

# Caminho do CSV
CSV_PATH = 'Relatorio_cadop.csv'

# Tentativa de leitura do CSV com tratamento de erros
try:
    df = pd.read_csv(CSV_PATH, sep=None, engine='python', encoding='utf-8', on_bad_lines='skip')
except pd.errors.ParserError:
    df = pd.read_csv(CSV_PATH, delimiter=';', engine='python', encoding='utf-8', on_bad_lines='skip')

# Normalizar nomes das colunas
df.columns = df.columns.str.strip()

# Exibir as colunas disponíveis para verificação
print("Colunas do CSV:", df.columns.tolist())


@app.route('/buscar', methods=['GET'])
def buscar_operadoras():
    termo = request.args.get('q', '').lower()
    if not termo:
        return jsonify([])

    # Verifica qual coluna contém os nomes das operadoras
    colunas_possiveis = ['nome_operadora', 'Nome_Fantasia', 'Razao_Social']
    coluna_nome = next((col for col in colunas_possiveis if col in df.columns), None)

    if not coluna_nome:
        return jsonify({'erro': 'Nenhuma coluna de operadora encontrada no CSV'}), 400

    # Filtra os resultados que contêm o termo digitado
    resultados = df[df[coluna_nome].astype(str).str.lower().str.contains(termo, na=False)]
    return jsonify(resultados.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)