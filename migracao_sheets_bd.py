import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
import os
from bd import BancoDeDados

def migrar_dados():
    try:
        # Carrega as credenciais do arquivo JSON
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'credenciais.json'))
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

        # Autorizar o acesso à planilha
        client = gspread.authorize(creds)
        planilha = client.open('Paris 2023').sheet1  # Abre a planilha de nome Paris 2023 na pasta raiz do Google Drive

        # Conectar ao banco de dados
        db_file = 'steam_bd.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Correção: Remova a linha self.cursor.execute('''
        BancoDeDados.criar_tabela(cursor)  # Correção: Chame o método diretamente

        conn.commit()

        # Ler os dados do Google Sheets e inserir no banco de dados
        dados = planilha.get_all_values()
        BancoDeDados.adicionar_dados(cursor, dados)
        conn.commit()

    except Exception as e:
        print(f'Ocorreu um erro durante a migração dos dados: {str(e)}')

    finally:
        # Fechar conexão com o banco de dados
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    migrar_dados()
