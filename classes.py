from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os


class SeleniumBrowser:
    def __init__(self):
        self.driver = None

    def open_browser(self, c_options):
        self.driver = webdriver.Chrome(options=c_options)
        return self.driver

class Steam:
    def __init__(self, site, chrome_options):
        self.site = site
        self.browser = SeleniumBrowser().open_browser(chrome_options)

    def search(self, pesquisa):
        self.browser.get(self.site)
        self.pesquisa = pesquisa
        input_box = self.browser.find_element(By.XPATH, '//*[@id="findItemsSearchBox"]')
        input_box.send_keys(self.pesquisa)
        input_box.submit()

    def nome_item(self, indice):
        try:
            self.indice = indice
            element = self.browser.find_element(By.XPATH, f'//*[@id="result_{indice}_name"]')
            return element.text
        except NoSuchElementException:
            return "Erro na pesquisa. Nome não encontrado."
        
    def valor(self, indice):
        try:
            self.indice = indice
            element = self.browser.find_element(By.XPATH, f'//*[@id="result_{indice}"]/div[1]/div[2]/span[1]/span[1]')
            return element.text
        except NoSuchElementException:
            return "Erro na pesquisa. Valor não encontrado."

    def quantidade(self, indice): #quantidade total de adesivos (furia - 458)
        try:
            self.indice = indice
            element = self.browser.find_element(By.XPATH, f'//*[@id="result_{indice}"]/div[1]/div[1]/span/span')
            return element.text
        except NoSuchElementException:
            return "Erro na pesquisa. Quantidade não encontrada."
        
    def quantidade_item(self): #quantidade total por pagina (pagina 1, 10 itens)
        try:
            first_element = self.browser.find_element(By.XPATH, '//*[@id="searchResults_start"]')
            second_element = self.browser.find_element(By.XPATH, '//*[@id="searchResults_end"]')

            first_element = int(first_element.text)
            second_element = int(second_element.text) 
            qtd = (second_element + 1) - first_element
            return qtd
        
        except NoSuchElementException:
            return "Erro na pesquisa. Quantidade de itens na pagina não encontrada."
        
    def total_paginas(self):
        try:
            total_elementos = self.browser.find_element(By.XPATH, '//*[@id="searchResults_total"]') #busca o numero total de items
            total_elementos = float(total_elementos.text)
 
            if total_elementos % 10 == 0: #verifica se é inteiro
                n_paginas = total_elementos / 10
                return int(n_paginas)
        
            else:
                n_paginas = (total_elementos / 10) + 1
                return int(n_paginas)
        
        except NoSuchElementException:
            return "Erro na pesquisa. Quantidade de itens na pagina não encontrada."         

    def update_spreadsheet(self, nome_item, valor, quantidade, data_hora):

    # Carrega as credenciais do arquivo JSON
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'credenciais.json'))
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

    # Autorizar o acesso à planilha
        client = gspread.authorize(creds)
        planilha = client.open('Paris 2023').sheet1 #abre a planinha de nome Paris 2023 na pasta raiz do google drive

        ultima_linha = len(planilha.col_values(1)) + 1 #ultima linha preenchida da tabela + 1

        planilha.update_cell(ultima_linha, 1, nome_item)
        planilha.update_cell(ultima_linha, 2, valor)
        planilha.update_cell(ultima_linha, 3, quantidade)
        planilha.update_cell(ultima_linha, 4, data_hora)
        
    @staticmethod
    def data_hora():
        now = datetime.now()
        data_hora_formatada = now.strftime("%d/%m/%y - %H:%M:%S")
        return data_hora_formatada
