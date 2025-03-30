import os
import zipfile
import pdfplumber
import pandas as pd
from pathlib import Path

# Caminhos relativos para as pastas
input_folder = Path.cwd() / 'input_files'
extract_folder = Path.cwd() / 'extracted_files'
output_folder = Path.cwd() / 'output_files'

# Criando as pastas, caso não existam
input_folder.mkdir(parents=True, exist_ok=True)
extract_folder.mkdir(parents=True, exist_ok=True)
output_folder.mkdir(parents=True, exist_ok=True)

# Caminho para o arquivo zip
zip_file_path = input_folder / 'anexos.zip'


# Função para extrair os arquivos do zip
def extract_zip(zip_file_path, extract_folder):
    if not zip_file_path.exists():
        print(f"Erro: O arquivo {zip_file_path} não foi encontrado.")
        return False
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    print(f"Arquivos extraídos para: {extract_folder}")
    return True


# Extraindo o zip
if not extract_zip(zip_file_path, extract_folder):
    exit()

# Verifica PDFs extraídos
pdf_files = list(extract_folder.glob("*.pdf"))
if not pdf_files:
    print("Nenhum arquivo PDF encontrado na pasta extraída.")
    exit()

pdf_file_path = pdf_files[0]  # Pegando o primeiro PDF encontrado


# Função para extrair tabelas do PDF
def extract_pdf_tables(pdf_file_path):
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            all_data = []
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    clean_table = []
                    for row in table:
                        clean_row = [cell.replace("\n", " ").strip() if cell else "" for cell in row]
                        clean_table.append(clean_row)
                    all_data.extend(clean_table)
            return all_data
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
        return []


# Extraindo os dados do PDF
data = extract_pdf_tables(pdf_file_path)

# Verificando se há dados extraídos
if not data:
    print("Nenhum dado extraído do PDF.")
    exit()

# Convertendo para DataFrame
df = pd.DataFrame(data)

# Removendo linhas totalmente vazias
df.dropna(how='all', inplace=True)

# Ajustando colunas (pegando os nomes da primeira linha se forem válidos)
if all(df.iloc[0].notna()):
    df.columns = df.iloc[0]  # Define os nomes das colunas
    df = df[1:].reset_index(drop=True)  # Remove a primeira linha usada como cabeçalho

# Substituindo abreviações por nomes completos
abbreviations = {
    'OD': 'Odontológica',
    'AMB': 'Ambulatorial',
}
df.replace(abbreviations, inplace=True)

# Padronizando os dados (removendo espaços extras e colocando tudo em maiúsculas)
df = df.apply(lambda col: col.map(lambda x: x.strip().upper() if isinstance(x, str) else x))

# Removendo colunas desnecessárias (se houver colunas vazias ou irrelevantes)
df.dropna(axis=1, how='all', inplace=True)

# Criando o arquivo XLSX dentro do ZIP
zip_output = output_folder / f'Teste_{os.getlogin()}.zip'

# Criando o arquivo XLSX dentro do ZIP
with zipfile.ZipFile(zip_output, 'w') as zipf:
    with zipf.open('rol_de_procedimentos.xlsx', 'w') as buffer:
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Procedimentos')

            # Acessando o objeto da planilha
            workbook = writer.book
            worksheet = writer.sheets['Procedimentos']

            # Criando um formato de célula para a quebra de linha e altura de linha
            cell_format = workbook.add_format({'text_wrap': True, 'valign': 'top', 'border': 1})

            # Ajustando a largura das colunas
            column_widths = {}
            for idx, col in enumerate(df.columns):
                max_len = df[col].astype(str).apply(len).max()  # Encontrando o comprimento máximo de cada coluna
                adjusted_width = max_len + 4  # Dando um aumento de largura para garantir visibilidade
                column_widths[idx] = adjusted_width

            # Aumentando a largura das colunas
            for idx, width in column_widths.items():
                worksheet.set_column(idx, idx, width, cell_format)

            # Ajustando a largura específica da coluna "PROCEDIMENTO" para 40
            procedimento_col_idx = df.columns.get_loc("PROCEDIMENTO")  # Encontrando o índice da coluna "PROCEDIMENTO"
            worksheet.set_column(procedimento_col_idx, procedimento_col_idx, 40, cell_format)

            # Ajustando a altura das linhas para 30 (40 pixels)
            worksheet.set_default_row(30)

            # Destacando os títulos das colunas com uma cor específica
            header_format = workbook.add_format({'bold': True, 'bg_color': '#FFFF00', 'font_color': '#000000', 'border': 1})  # Amarelo com texto preto
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # Adicionando bordas em todas as células (inclusive no cabeçalho)
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    worksheet.write(row + 1, col, df.iloc[row, col], cell_format)

            # Adicionando borda para o cabeçalho
            for col_num in range(len(df.columns)):
                worksheet.write(0, col_num, df.columns[col_num], header_format)

print(f"Arquivo ZIP gerado com sucesso: {zip_output}")
