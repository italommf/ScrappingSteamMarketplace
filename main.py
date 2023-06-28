from steam import Steam
from classes import Utils
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import sys                                                      # também para o fechamento da janela do prompt
import time                                                     # usada para o timesleep
import ctypes                                                   # usada para o fechamento da janela do prompt

os.system("cls")                                                # limpa o teminal antes de executar o codigo

chrome_options = Options()                                      # instancia a classe Options()
chrome_options.add_argument("--headless")                       # invota o metodo e passa o argumento para executar sem a janela aberta
DEFAULT_PAGE = 1                                                # pagina padrão utilizada no link passado para o inicializador de Steam
db_file = 'steam_bd.db'                                         # nome do arquivo do banco de dados a ser criado

# link fornecido para o web scrapping, chrome_options e db_file
steam = Steam(f'https://steamcommunity.com/market/search?category_730_ItemSet%5B0%5D=any&category_730_ProPlayer%5B0%5D=any&category_730_StickerCapsule%5B0%5D=any&category_730_TournamentTeam%5B0%5D=any&category_730_Weapon%5B0%5D=any&category_730_StickerCategory%5B0%5D=tag_TeamLogo&category_730_StickerCategory%5B1%5D=tag_Tournament&category_730_Tournament%5B0%5D=tag_Tournament21&appid=730#p{DEFAULT_PAGE}_default_desc', chrome_options=chrome_options, db_file=db_file)
steam.search('holo')                                            # pesquisa a ser feita no marketplace (link passado)                                     

for pagina in range(steam.total_paginas()):                     # para cada pagina da pesquisa me retorna:

    for indice in range(steam.quantidade_item_por_pagina()):    # no intervalo entre 1 e a quantidade total de itens na pagina
        nome = steam.nome_item(indice)                              # nome do item
        valor = steam.valor(indice)                                 # valor do item
        quantidade = steam.quantidade(indice)                       # quantidade do item a venda
        data = Utils.data()                                         # data atual
        hora = Utils.hora()                                         # hora atual
        data_hora = Utils.data_hora()                               # data e hora atual (serve como filtro de ordem "mais recente / mais antigo")

        print(f"Nome: {nome}\nValor: {valor} - Quantidade: {quantidade}\n") # mostra no terminal os resultados da busca e scrapping

        steam.inserir_item_banco_dados(nome, valor, quantidade, data, hora, data_hora)  # insere os dados no banco de dados

    if pagina < steam.total_paginas() - 1:                      # se a pagina atual não é a ultima pagina, clica no botão para passar de pagina
        next_button = steam.browser.find_element(By.XPATH, '//*[@id="searchResults_btn_next"]') # resgata o botão de next
        next_button.click()                                     # clica no botão next
        time.sleep(5)                                           # aguarda 5 segundos para o carregamento completo da pagina
'''
if sys.platform.startswith('win32'):                            # se existe a janela (win32) fecha a mesma
    ctypes.windll.kernel32.ExitProcess(0)                       # encerra o processo
'''                     
