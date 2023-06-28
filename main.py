from steam import Steam
from classes import Utils
from plot import Graficos
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import sys                                                      # também para o fechamento da janela do prompt
import time                                                     # usada para o timesleep
import ctypes                                                   # usada para o fechamento da janela do prompt
from colorama import Fore, Style

chrome_options = Options()                                      # instancia a classe Options()
#chrome_options.add_argument("--headless")                       # invota o metodo e passa o argumento para executar sem a janela aberta
DEFAULT_PAGE = 1                                                # pagina padrão utilizada no link passado para o inicializador de Steam
#db_file = 'steam_bd.db'                                         # nome do arquivo do banco de dados a ser criado
db_file = 'steam_bd_teste.db'

def menu():
    
    print('')
    print(Fore.GREEN + 'ScrappingSteam' + Style.RESET_ALL + '\n\n')
    print('O que deseja fazer?:\n     1 - ' + Fore.LIGHTBLUE_EX + 'Atualizar o banco de dados com os itens mais recentes\n' + Style.RESET_ALL + '     2 - ' + Fore.LIGHTBLUE_EX + 'Plotar gráfico\n' + Style.RESET_ALL)

    try:
        opcao = int(input('Digite aqui: '))

        if opcao == 1:
            return opcao
        
        elif opcao == 2:
            return opcao
        else:
            os.system('cls')
            print(Fore.RED + 'ERRO: Opção inválida. Por favor, digite uma opção válida' + Style.RESET_ALL)
            return menu()
     
    except ValueError:
        os.system('cls')
        print(Fore.RED + 'Erro: Digite um numero' + Style.RESET_ALL)
        return menu()  

def busca_dados_e_atualiza_banco():
    
    print('')
    os.system('cls')
    print(Fore.GREEN + 'ScrappingSteam' + Style.RESET_ALL + '\n\n')
    print('Voce esta na opção ' + Fore.LIGHTBLUE_EX + '"Atualizar o banco de dados com os itens mais recentes"' + Style.RESET_ALL + '\n')
    print('Digite um termo para pesquisar e atualizar / inserir no banco de dados...\nExemplo: ' + Fore.LIGHTBLUE_EX + "caixa" + Fore.WHITE + ', ' + Fore.LIGHTBLUE_EX +  "fallen" + Fore.WHITE + ', ' + Fore.LIGHTBLUE_EX + "paris 2023 holo" + Style.RESET_ALL + '...\n')

    pesquisa_input = input('Digite aqui: ')

    print(f'\n{Fore.GREEN}Realizando busca por {Fore.WHITE} {pesquisa_input}{Fore.GREEN}...{Style.RESET_ALL}')

    #===================================
    
    steam = Steam(f'https://steamcommunity.com/market/search?appid=730#p{DEFAULT_PAGE}_default_desc', chrome_options=chrome_options, db_file=db_file)
    steam.search(pesquisa_input)
    
    for pagina in range(steam.total_paginas()):                     # para cada pagina da pesquisa me retorna:

        for indice in range(steam.quantidade_item_por_pagina()):    # no intervalo entre 1 e a quantidade total de itens na pagina
            nome = steam.nome_item(indice)                              # nome do item
            valor = steam.valor(indice)                                 # valor do item
            quantidade = steam.quantidade(indice)                       # quantidade do item a venda
            data = Utils.data()                                         # data atual
            hora = Utils.hora()                                         # hora atual
            data_hora = Utils.data_hora()                               # data e hora atual (serve como filtro de ordem "mais recente / mais antigo")

            print(f"{Fore.LIGHTBLUE_EX}Nome: {Fore.WHITE}{nome}\n{Fore.LIGHTBLUE_EX}Valor: {Fore.WHITE}{valor} - {Fore.LIGHTBLUE_EX}Quantidade: {Fore.WHITE}{quantidade}\n") # mostra no terminal os resultados da busca e scrapping

            steam.inserir_item_banco_dados(nome, valor, quantidade, data, hora, data_hora)  # insere os dados no banco de dados

        if pagina < steam.total_paginas() - 1:                      # se a pagina atual não é a ultima pagina, clica no botão para passar de pagina
            next_button = steam.browser.find_element(By.XPATH, '//*[@id="searchResults_btn_next"]') # resgata o botão de next
            next_button.click()                                     # clica no botão next
            time.sleep(5)                                           # aguarda 5 segundos para o carregamento completo da pagina

def plota_grafico():

    print('')
    print(Fore.GREEN + 'ScrappingSteam' + Style.RESET_ALL + '\n\n')
    filtro = input('Digite o nome do item que voce deseja plotar o gráfico: \n')
    
    Graficos.gerar_grafico_linha(filtro)











'''if sys.platform.startswith('win32'):                            # se existe a janela (win32) fecha a mesma
    ctypes.windll.kernel32.ExitProcess(0)                       # encerra o processo
  '''                 


opcao_escolhida = menu() 

if opcao_escolhida == 1:
    busca_dados_e_atualiza_banco()

elif opcao_escolhida == 2:
    plota_grafico()