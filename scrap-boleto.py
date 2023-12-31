import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# from PyPDF2 import PdfWriter
import pathlib

print("Start...")

# Cria um objeto PdfWriter para combinar os PDFs salvos
# pdf_writer = PdfWriter()

# Defines
DEFAULT_PATH = pathlib.Path().resolve()
DEFAULT_DOWNLOAD_PATH = f'{DEFAULT_PATH}/downloaded_files';


# Configuração do WebDriver do Chrome

# Configuração do WebDriver do Chrome
# Certifique-se de fornecer o caminho correto para o driver do Chrome
chrome_options = Options()

# Define as preferências do ChromeOptions
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': DEFAULT_DOWNLOAD_PATH,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
    "download.open_pdf_in_system_reader": False,
    "profile.default_content_settings.popups": 0,
}
)

# Configurar a porta de depuração do Chrome
# debugging_port = 9222
# Adicionar a opção de depuração remota
# chrome_options.add_argument(f'--remote-debugging-port={debugging_port}')

# Certifique-se de fornecer o caminho correto para o driver do Chrome
# driver = webdriver.Chrome('./home/trodrigues/dev/repo/py-scrap-boletos/drivers/chromedriver_linux64/chromedriver')
driver = webdriver.Chrome(options=chrome_options)

#implicit wait
driver.implicitly_wait(0.8)

print("Configs ended...")

print("Load page...")
# Carrega a página do Google Chrome
# driver.get(f'file://{DEFAULT_PATH}/sample_pages/tabela-page-sample.html')
driver.get(f'https://www.itau.com.br/empresas')

# Wait Login to proceed
timeout = 900 #seconds - 15 minutes
myElem = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//table[@id="tabela-boletos"]/tbody/tr')))

print("Find table element...")
# Localiza todas as linhas da tabela
linhas_tabela = driver.find_elements(By.XPATH, '//table[@id="tabela-boletos"]/tbody/tr')

# Itera sobre as linhas da tabela
for linha in linhas_tabela:
    # Obtém os elementos da linha
    colunas = linha.find_elements(By.TAG_NAME, 'td')

    nome = colunas[0].text
    print("Nome:", nome)

    # Clique no botão para abrir a página do boleto
    botao_boleto = colunas[2].find_element(By.TAG_NAME, 'button')
    botao_boleto.click()

    # Aguarda a página do boleto ser carregada
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    # Obtém a nova janela do boleto
    janelas = driver.window_handles
    driver.switch_to.window(janelas[1])

    # Clique no botão de download do boleto
    botao_download = driver.find_element(By.XPATH, '//button[@id="download-arquivo"]')
    botao_download.click()

    # Aguarda um tempo para garantir que o download seja concluído
    time.sleep(2)

    # Renomeia o arquivo baixado para o nome da primeira coluna
    novo_nome_arquivo = f'{nome}.pdf'
    print("novo_nome_arquivo:", novo_nome_arquivo)

    nome_padrao_arquivo = 'boleto-fake.pdf'

    print("DEFAULT_DOWNLOAD_PATH:", DEFAULT_DOWNLOAD_PATH)
    # Verifica se o arquivo padrão foi baixado
    if nome_padrao_arquivo in os.listdir(DEFAULT_DOWNLOAD_PATH):
        print("List dir: rename file")
        os.rename( DEFAULT_DOWNLOAD_PATH + '/' + nome_padrao_arquivo, DEFAULT_DOWNLOAD_PATH + '/' + novo_nome_arquivo)

    # Feche a segunda janela
    driver.close()

    # Volta para a janela principal
    driver.switch_to.window(janelas[0])

# Encerra o navegador
driver.quit()

#TODO: select table class="TRNfundo"
#TODO: navegar na paginação <a href="javascript:Busca(2);" class="lnkpadrao01">2</a>
#TODO: nome do arquivo = coluna[0] (pagador) + "-" + coluna[5] (seu numero)

#TODO: botão da primeira tela
#<a onclick="javascript:window.open('PopUp.htm','BLOQUETO','resizable=yes,location=no,directories=no,status=yes,toolbar=yes,menubar=yes,scrollbars=yes,width=650,height=400,left=20,top=10')" href="javascript:ConsultaBoleto('2938353733','112','51015979','4','S');" class="lnkpadrao01">emitir</a>

#TODO: botão da segunda tela
#<a href="javascript:document.frmPDF.submit();"><img border="0" src="/Itau/Imagens/bt_gerar_boleto.gif" alt="Versão para Impressão"></a>