# Python_WebScraping_RetornandoDistritos_BuscandoPeloCEP
Esse código retorna os distritos de São Paulo referentes ao CEP utilizado para busca por meio de web scraping com Python e BS4. A procura do valor é feita no site LocalizaSampa da Prefeitura.

Este código coleta informações de distritos para diferentes CEPs acessando uma página da prefeitura de São Paulo. Ele realiza as seguintes etapas:

Acessa a página: Utiliza o Playwright para abrir um navegador (Chromium) e acessar uma URL específica para cada CEP fornecido. <br>
Captura dados de uma tabela: Espera que a tabela com o ID myTable seja carregada, e então usa BeautifulSoup para fazer o parsing do HTML e extrair os dados da tabela. <br>
Armazena os dados: Coleta os dados da tabela, especificamente o distrito associado ao CEP, e os armazena em uma lista. <br>
Itera sobre os CEPs: Carrega uma lista de CEPs de um arquivo Excel, itera sobre cada um, coleta os dados e armazena as informações coletadas. <br>
Salva os resultados: Ao final, os dados coletados são salvos em um arquivo Excel chamado resultados.xlsx. Caso haja erros na coleta de dados para algum CEP, esses CEPs são registrados em um arquivo erros.xlsx. <br><br>
O código é útil para automatizar a coleta de informações de distritos associados a diferentes CEPs em São Paulo podendo ser adaptado para outras necessidades que exijam raspagem de dados da web. <br>
