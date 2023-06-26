from classes import SeleniumBrowser, Utils
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from classes import Utils
from bd import BancoDeDados


class Steam:
    def __init__(self, site, chrome_options, db_file):
        self.site = site
        self.browser = SeleniumBrowser().open_browser(chrome_options)
        self.db_file = db_file
        self.banco_dados = BancoDeDados(self.db_file)

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

    def quantidade(self, indice):
        try:
            self.indice = indice
            element = self.browser.find_element(By.XPATH, f'//*[@id="result_{indice}"]/div[1]/div[1]/span/span')
            return element.text
        except NoSuchElementException:
            return "Erro na pesquisa. Quantidade não encontrada."

    def quantidade_item(self):
        try:
            first_element = self.browser.find_element(By.XPATH, '//*[@id="searchResults_start"]')
            second_element = self.browser.find_element(By.XPATH, '//*[@id="searchResults_end"]')

            first_element = int(first_element.text)
            second_element = int(second_element.text)
            qtd = (second_element + 1) - first_element
            return qtd

        except NoSuchElementException:
            return "Erro na pesquisa. Quantidade de itens na página não encontrada."

    def total_paginas(self):
        try:
            total_elementos = self.browser.find_element(By.XPATH, '//*[@id="searchResults_total"]')
            total_elementos = float(total_elementos.text)

            if total_elementos % 10 == 0:
                n_paginas = total_elementos / 10
                return int(n_paginas)

            else:
                n_paginas = (total_elementos / 10) + 1
                return int(n_paginas)

        except NoSuchElementException:
            return "Erro na pesquisa. Quantidade de itens na página não encontrada."

    def inserir_item_banco_dados(self, nome, valor, quantidade, data, hora, data_hora):
        data_hora = Utils.data_hora()
        self.banco_dados.inserir_item(nome, valor, quantidade, data, hora, data_hora)
