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

        fig, ax = plt.subplots()

        for linha in dados:
            nome = linha[0]  # Coluna "nome"
            valor = float(linha[1].replace('$', '').replace(' USD', ''))  # Coluna "valor" convertida para float
            hora = linha[2]  # Coluna "hora"

            print(f"nome: {nome}, valor: {valor}, hora: {hora}")

            ax.plot(hora, valor, label=nome)

        ax.set_xlabel('Hora')
        ax.set_ylabel('Valor')
        ax.set_title(f'Gráfico de Linha - {filtro_nome}')

        ax.legend()
        plt.xticks(rotation=45)  # Rotaciona os rótulos do eixo X para melhor legibilidade

        plt.show()

        banco_dados.fechar_conexao()


Graficos.gerar_grafico_linha("Sticker | FURIA (Holo) | Paris 2023")  # precisa do nome completo
