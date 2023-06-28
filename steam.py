from classes import SeleniumBrowser, Utils
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from classes import Utils
from bd import BancoDeDados

class Steam:                                                                        # responsavel por todos os metodos relacionados à steam    
    def __init__(self, site, chrome_options, db_file):                                  # recebe o link do web scrapping, o chrome options e o nome do banco de dados
        self.site = site                                                                    # recebe o link do site      
        self.browser = SeleniumBrowser().open_browser(chrome_options)                       # solicita a abertura do navegador com o chrome options passado
        self.db_file = db_file                                                              # recebe o nome do banco de dados
        self.banco_dados = BancoDeDados(self.db_file)                                       # instancia o banco de dados e passa o nome

    def search(self, pesquisa):                                                         # metodo responsavel pela pesquisa no link
        self.browser.get(self.site)                                                         # passa o link para o site
        self.pesquisa = pesquisa                                                            # recebe a pesquisa passada em "main.py"
        input_box = self.browser.find_element(By.XPATH, '//*[@id="findItemsSearchBox"]')    # procura a caixa de pesquisa
        input_box.send_keys(self.pesquisa)                                                  # preenche a caixa de pesquisa com a pesquisa passada
        input_box.submit()                                                                  # realiza a pesquisa 

    def nome_item(self, indice):                                                        # metodo responsavel por retornar o nome do item 
        try:
            self.indice = indice                                                            # recebe o indice do elemento de acordo com o XPATH (retorna a quantidade total de itens)
            element = self.browser.find_element(By.XPATH, f'//*[@id="result_{indice}_name"]') # atribui o elemento do XPATH a element (o nome do item)
            return element.text                                                             # retorna o texto contido no elemento (nome)
        except NoSuchElementException:
            return "Erro na pesquisa. Nome não encontrado."

    def valor(self, indice):                                                            # metodo responsavel por retornar o valor do item
        try:
            self.indice = indice                                                            # recebe o indice do elemento de acordo com o XPATH (retorna a quantidade total de itens)
            element = self.browser.find_element(By.XPATH, f'//*[@id="result_{indice}"]/div[1]/div[2]/span[1]/span[1]') # atribui o elemento do XPATH a element (o valor do item)
            return element.text                                                             # retorna o texto do elemento (valor)
        except NoSuchElementException:
            return "Erro na pesquisa. Valor não encontrado."

    def quantidade(self, indice):                                                       # metodo responsavel por me retornar a quantidade disponível de cada item específico (item A, quantidade: 957)  
        try:  
            self.indice = indice                                                            # recebe o indice do elemento de acordo com o XPATH (retorna a quantidade total de itens)
            element = self.browser.find_element(By.XPATH, f'//*[@id="result_{indice}"]/div[1]/div[1]/span/span') # atribui o elemento do XPATH a element (a quantidade disponível de cada item específico)
            return element.text                                                             # retorna o texto do elemento (quantidade)
        except NoSuchElementException:
            return "Erro na pesquisa. Quantidade não encontrada."

    def quantidade_item_por_pagina(self):                                               # metodo responsavel por pegar a quantidade total de itens disponiveis na loja com aquela pesquisa (Exibindo resultados 1–10 de 438.739)
        try:
            first_element = self.browser.find_element(By.XPATH, '//*[@id="searchResults_start"]') # pega o primeiro numero (..."1"–10 de ...)
            second_element = self.browser.find_element(By.XPATH, '//*[@id="searchResults_end"]') # pega o ultimo numero (...1–"10" de ...)

            first_element = int(first_element.text)                                         # converte o primeiro numero antes em str para int
            second_element = int(second_element.text)                                       # converte o ultimo numero antes em str para int
            qtd = (second_element + 1) - first_element                                      # atribui a qtd o resultado do segundo menos o primeiro ((10 + 1) - 1) = 10, se não somar 1 fica (10 - 1) = 9 (a pagina tem 10 itens)
            return qtd                                                                      # retorna a quantidade de itens por pagina

        except NoSuchElementException:
            return "Erro na pesquisa. Quantidade de itens na página não encontrada."

    def total_paginas(self):                                                            # metodo responsavel pelo numero total de paginas referentes a pesquisa          
        try:
            total_elementos = self.browser.find_element(By.XPATH, '//*[@id="searchResults_total"]') # pega o numero total de itens (... de "438.739" )
            total_elementos = float(total_elementos.text)                                   # converte o numero antes em str para int

            if total_elementos % 10 == 0:                                                   # se o resto do numero total / 10 for 0, a ultima pagina tem 10 itens
                n_paginas = total_elementos / 10
                return int(n_paginas)                                                       # retorna o numero de paginas

            else:
                n_paginas = (total_elementos / 10) + 1                                      # se o resto do numero total / 10 NÃO for 0, há uma pagina a mais e a ultima pagina tem menos de 10 itens                                
                return int(n_paginas)                                                       # retorna o numero de paginas 

        except NoSuchElementException:
            return "Erro na pesquisa. Quantidade de itens na página não encontrada."

    def inserir_item_banco_dados(self, nome, valor, quantidade, data, hora, data_hora): # metodo responsavel por inserir no banco os dados obtidos
        data_hora = Utils.data_hora()                                                       # recebe data/hora 
        self.banco_dados.inserir_item(nome, valor, quantidade, data, hora, data_hora)       # insere no banco de dados os dados obtidos, incçusive data/hora obtido acima
