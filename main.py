from steam import Steam
from classes import Utils
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import sys
import time
#from migracao_sheets_bd import migrar_dados
import sys
import ctypes

os.system("cls")

chrome_options = Options()
chrome_options.add_argument("--headless")
DEFAULT_PAGE = 1
db_file = 'steam_bd.db'

steam = Steam(f'https://steamcommunity.com/market/search?category_730_ItemSet%5B0%5D=any&category_730_ProPlayer%5B0%5D=any&category_730_StickerCapsule%5B0%5D=any&category_730_TournamentTeam%5B0%5D=any&category_730_Weapon%5B0%5D=any&category_730_StickerCategory%5B0%5D=tag_TeamLogo&category_730_StickerCategory%5B1%5D=tag_Tournament&category_730_Tournament%5B0%5D=tag_Tournament21&appid=730#p{DEFAULT_PAGE}_default_desc', chrome_options=chrome_options, db_file=db_file)
steam.search('holo')

for pagina in range(steam.total_paginas()):

    for indice in range(steam.quantidade_item()): 
        nome = steam.nome_item(indice)
        valor = steam.valor(indice)
        quantidade = steam.quantidade(indice)
        data = Utils.data()
        hora = Utils.hora()
        data_hora = Utils.data_hora()

        print(f"Nome: {nome}\nValor: {valor} - Quantidade: {quantidade}\n")

        steam.inserir_item_banco_dados(nome, valor, quantidade, data, hora, data_hora)

    if pagina < steam.total_paginas() - 1:
        next_button = steam.browser.find_element(By.XPATH, '//*[@id="searchResults_btn_next"]')
        next_button.click()
        time.sleep(5)

if sys.platform.startswith('win32'):
    ctypes.windll.kernel32.ExitProcess(0)
