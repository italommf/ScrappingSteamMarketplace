from bd import BancoDeDados
import os
import matplotlib.pyplot as plt 

class Graficos:    
    
    @staticmethod
    def gerar_grafico_linha(filtro_nome):
        caminho_banco_dados = os.path.abspath("steam_bd.db")
        banco_dados = BancoDeDados(caminho_banco_dados)
        dados = banco_dados.obter_dados(filtro_nome)

        if not dados:
            print("Não há dados disponíveis para gerar o gráfico.")
            return

        ids = []
        valores = []
        data_horas = []

        for linha in dados:
            id = linha[0]  # Coluna "id"
            valor = float(linha[2].replace('$', '').replace(' USD', ''))  # Coluna "valor" convertida para float
            data_hora = linha[3]  # Coluna "data_hora"

            print(f"id: {id}, valor: {valor}, data_hora: {data_hora}")

            ids.append(id)
            valores.append(valor)
            data_horas.append(data_hora)

        fig, ax = plt.subplots()

        ax.plot(ids, valores, label=filtro_nome)

        ax.set_xlabel('Data e Hora')
        ax.set_ylabel('Valor')
        ax.set_title('Gráfico de Linha')

        ax.legend()
        plt.xticks(ids, data_horas, rotation=45)  # Rotaciona e exibe as datas e horas no eixo X

        plt.show()

        banco_dados.fechar_conexao()

Graficos.gerar_grafico_linha("Sticker | FURIA (Holo) | Paris 2023")  # precisa do nome completo
