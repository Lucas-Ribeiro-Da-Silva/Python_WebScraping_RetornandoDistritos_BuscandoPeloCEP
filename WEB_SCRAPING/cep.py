from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

# Função para capturar os dados
def capture_table_data(cep):
    with sync_playwright() as p:
        # Inicia um navegador (pode ser 'chromium', 'firefox' ou 'webkit')
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Acessa a página
        url = f'http://www.sinasc.saude.prefeitura.sp.gov.br/localizasampa/default.asp?cep={cep}'
        print(f"Acessando a URL: {url}")
        
        response = page.goto(url)
        if response.status != 200:
            print(f"Erro ao acessar a URL: Status {response.status} para CEP {cep}")
            browser.close()
            return None  # Retorna None se houver erro

        # Aguarda a tabela aparecer na página
        try:
            page.wait_for_selector('#myTable', timeout=60000)  # Aumenta o timeout para 60 segundos
        except Exception as e:
            print(f"Erro ao esperar pelo seletor: {e} para CEP {cep}")
            browser.close()
            return None  # Retorna None se houver erro

        # Obtém o HTML da página
        html = page.content()

        # Usa Beautiful Soup para fazer o parsing
        soup = BeautifulSoup(html, 'html.parser')

        # Encontra a tabela
        tabela = soup.find('table', id='myTable')

        # Se a tabela não for encontrada, registra o erro
        if tabela is None:
            print(f"Tabela não encontrada para CEP {cep}")
            browser.close()
            return None  # Retorna None se a tabela não for encontrada

        # Lista para armazenar os dados
        dados = []

        # Extrai os dados da tabela
        for linha in tabela.find_all('tr'):
            colunas = linha.find_all('td')
            # Verifica se a linha possui colunas suficientes
            if len(colunas) > 3:  # O índice 3 é o quarto item (considerando índice 0)
                distrito = colunas[3].text.strip()  # O quarto item é no índice 3
                dados.append((cep, distrito))  # Adiciona tupla (cep, distrito) à lista
                print(f"Dados coletados para o CEP {cep}: DISTRITO = {distrito}")

        # Fecha o navegador
        browser.close()
        return dados  # Retorna os dados coletados

# Carregar os CEPs do arquivo Excel
df_ceps = pd.read_excel('cep.xlsx')  # Lê o arquivo 'cep.xlsx'
cep_list = df_ceps['CEPS'].tolist()  # Converte a coluna 'CEPS' em uma lista
print(f"Total de CEPs carregados: {len(cep_list)}")

# Lista para armazenar todos os dados coletados e uma lista para erros
todos_dados = []
erros = []

# Itera sobre cada CEP e coleta os dados
for cep in cep_list:
    dados = capture_table_data(cep)  # Captura os dados para o CEP atual
    if dados:  # Verifica se dados foram coletados
        todos_dados.extend(dados)  # Adiciona os dados à lista geral
    else:
        erros.append(cep)  # Adiciona o CEP à lista de erros

print(f"Total de dados coletados: {len(todos_dados)}")
print(f"Total de erros: {len(erros)}")

# Cria um DataFrame do pandas com todos os dados coletados
df_resultados = pd.DataFrame(todos_dados, columns=['CEP', 'distrito'])

# Salva o DataFrame em um arquivo Excel
df_resultados.to_excel('resultados.xlsx', index=False)  # Salva como 'resultados.xlsx'
print("Resultados salvos em 'resultados.xlsx'")

# Se houver erros, salva em um arquivo separado
if erros:
    df_erros = pd.DataFrame(erros, columns=['CEPs com Erro'])
    df_erros.to_excel('erros.xlsx', index=False)  # Salva como 'erros.xlsx'
    print("CEPs com erro salvos em 'erros.xlsx'")
