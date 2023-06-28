from selenium import webdriver
from datetime import datetime

class SeleniumBrowser:                                      # classe responsavel pela criação do navegador       
    def __init__(self):
        self.driver = None                                  # driver responsavel por criar a instancia do navegador quando passados os argumentos

    def open_browser(self, c_options):                      # abre o navegador, recebe o chrome options
        self.driver = webdriver.Chrome(options=c_options)       # recebe a instancia do chrome e passa a options fornecida em "main.py" (--headless)
        return self.driver                                      # retorna a instancia aberta do chrome (neste caso, sem a janela)

class Utils:                                                # classe responsavel pelos metodos de data e hora
    @staticmethod
    def data_hora():
        now = datetime.now()                                    # pega a data/hora atual 
        data_hora = now.strftime("%d/%m/%y - %H:%M:%S")         # formata par ao padrão (d/m/a - h:m:s)
        return data_hora                                        # retorna a data formatada

    @staticmethod
    def hora():                                             
        now = datetime.now()
        hora = now.strftime("%H:%M:%S")
        return hora                                             # retorna somente a hora no formato (h:m:s)
    @staticmethod
    def data():
        now = datetime.now()
        data = now.strftime("%d/%m/%y")
        return data                                         # retorna somente a data no formato (d/m/a)
