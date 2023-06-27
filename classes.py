from selenium import webdriver
from datetime import datetime
from bd import BancoDeDados
import os
import matplotlib.pyplot as plt

class SeleniumBrowser:
    def __init__(self):
        self.driver = None

    def open_browser(self, c_options):
        self.driver = webdriver.Chrome(options=c_options)
        return self.driver

class Utils:
    @staticmethod
    def data_hora():
        now = datetime.now()
        data_hora = now.strftime("%d/%m/%y - %H:%M:%S")
        return data_hora

    @staticmethod
    def hora():
        now = datetime.now()
        hora = now.strftime("%H:%M:%S")
        return hora
    @staticmethod
    def data():
        now = datetime.now()
        data = now.strftime("%d/%m/%y")
        return data

'''class Graficos:
    
    @staticmethod
    def gerar_grafico_linha(filtro_nome):
        caminho_banco_dados = os.path.abspath("steam_bd.db")
        banco_dados = BancoDeDados(caminho_banco_dados)
        dados = banco_dados.obter_dados(filtro_nome)

        if not dados:
            print("Não há dados disponíveis para gerar o gráfico.")
            return

        nomes = list(set([linha[1] for linha in dados]))  # Obtém os nomes únicos das linhas
        nomes.sort()  # Ordena os nomes em ordem alfabética

        fig, ax = plt.subplots()

        for nome in nomes:
            valores = [linha[2] for linha in dados if linha[1] == nome]  # Filtra os valores correspondentes ao nome
            datas = [linha[4] for linha in dados if linha[1] == nome]  # Filtra as datas correspondentes ao nome
            ax.plot(datas, valores, label=nome)

        ax.set_xlabel('Data')
        ax.set_ylabel('Valor')
        ax.set_title(f'Gráfico de Linha - {filtro_nome}')

        ax.legend()
        plt.xticks(rotation=45)  # Rotaciona os rótulos do eixo X para melhor legibilidade

        plt.show()

        banco_dados.fechar_conexao()


'''