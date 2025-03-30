import requests
from bs4 import BeautifulSoup
import zipfile
import os
import time

# URL da página de onde vamos fazer o web scraping
URL = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

# Criar uma pasta temporária para armazenar os PDFs
PASTA_DOWNLOADS = 'downloads'
os.makedirs(PASTA_DOWNLOADS, exist_ok=True)

# Função para tentar a requisição várias vezes em caso de falha
def tentar_requisicao(url, tentativas=10, timeout=20):
    for tentativa in range(tentativas):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
            return response
        except requests.exceptions.RequestException as e:
            print(f"Tentativa {tentativa + 1} falhou: {e}")
            if tentativa < tentativas - 1:
                print("Tentando novamente em 5 segundos...")
                time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente
            else:
                print("Máximo de tentativas alcançado, erro persistente.")
                raise

# Fazer a requisição para obter o conteúdo da página
try:
    response = tentar_requisicao(URL)
except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
    exit(1)

# Processar o HTML com BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar e baixar os PDFs
pdf_links = []
for link in soup.find_all('a', href=True):
    texto_link = link.text.strip().lower()
    href = link['href'].lower()
    if ('anexo' in texto_link) and ('.pdf' in href):  # Filtra somente links .pdf
        pdf_links.append(link['href'])

# Garantir que os links são absolutos (caso estejam como links relativos)
pdf_links = [link if link.startswith('http') else f'https://www.gov.br{link}' for link in pdf_links]


# Garantir que os links sejam absolutos
pdf_links = [link if link.startswith('http') else f'https://www.gov.br{link}' for link in pdf_links]
# Criar um mapeamento entre o link e o nome do arquivo baixado

mapeamento = {}

# Baixar os PDFs encontrados
pdf_files = []
for i, link in enumerate(pdf_links, 1):
    try:
        print(f"Iniciando download do PDF {i} do link: {link}")  # Imprime o link do PDF
        response = requests.get(link, timeout=10)
        response.raise_for_status()  # Verifica se o download foi bem-sucedido
        filename = os.path.join(PASTA_DOWNLOADS, f'anexo_{i}.pdf')
        with open(filename, 'wb') as file:
            file.write(response.content)
        pdf_files.append(filename)

        # Adicionar o link e o arquivo baixado no mapeamento
        mapeamento[link] = filename
        print(f"Download concluído: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o PDF {i}: {e}")

# Imprimir o mapeamento dos links com seus respectivos arquivos
for link, arquivo in mapeamento.items():
    print(f"Link: {link} -> Arquivo: {arquivo}")

# Compactar os arquivos PDF em um arquivo ZIP
zip_filename = 'anexos.zip'
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for pdf in pdf_files:
        zipf.write(pdf, os.path.basename(pdf))  # Adiciona apenas o nome do arquivo ao ZIP

print(f"Compactação concluída: {zip_filename}")

# Limpeza dos arquivos temporários
for pdf in pdf_files:
    os.remove(pdf)
os.rmdir(PASTA_DOWNLOADS)

print("Processo finalizado com sucesso!")
