from classes import Steam
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

os.system("cls")

chrome_options = Options()
chrome_options.add_argument("--headless")
DEFAULT_PAGE = 1
steam = Steam(f'https://steamcommunity.com/market/search?category_730_ItemSet%5B0%5D=any&category_730_ProPlayer%5B0%5D=any&category_730_StickerCapsule%5B0%5D=any&category_730_TournamentTeam%5B0%5D=any&category_730_Weapon%5B0%5D=any&category_730_StickerCategory%5B0%5D=tag_TeamLogo&category_730_StickerCategory%5B1%5D=tag_Tournament&category_730_Tournament%5B0%5D=tag_Tournament21&appid=730#p{DEFAULT_PAGE}_default_desc', chrome_options=chrome_options)
steam.search('holo')

for pagina in range(steam.total_paginas()):

    for indice in range(steam.quantidade_item()): 
        nome = steam.nome_item(indice)
        valor = steam.valor(indice)
        quantidade = steam.quantidade(indice)
        data_hora = steam.data_hora()
        print(f"Nome: {nome}\nValor: {valor} - Quantidade: {quantidade}\n")
        steam.update_spreadsheet(nome, valor, quantidade, data_hora)
        time.sleep(5)

    if pagina < steam.total_paginas() - 1:
        next_button = steam.browser.find_element(By.XPATH, '//*[@id="searchResults_btn_next"]')
        next_button.click()
        time.sleep(5)  