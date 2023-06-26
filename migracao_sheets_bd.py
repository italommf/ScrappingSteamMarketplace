import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
import os


def migrar_dados():
    try:
        # Carrega as credenciais do arquivo JSON
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'credenciais.json'))
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

        # Autorizar o acesso à planilha
        client = gspread.authorize(creds)
        planilha = client.open('Paris 2023').sheet1  # Abre a planilha de nome Paris 2023 na pasta raiz do Google Drive

        print('Autorizei a planilha')

        # Conectar ao banco de dados
        db_file = 'dados.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        print('Conectei ao banco de dados')

        # Criar tabela no banco de dados, se ainda não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                valor TEXT,
                quantidade TEXT,
                data TEXT,
                hora TEXT,
                data_hora TEXT
            )
        ''')

        print('Criei a tabela')

        conn.commit()

        print('Comitei')

        # Ler os dados do Google Sheets e inserir no banco de dados
        dados = planilha.get_all_values()
        for linha in dados[1:]:  # Ignorar o cabeçalho da planilha
            nome = linha[0]
            valor = linha[1]
            quantidade = linha[2]
            data = linha[4]
            hora = linha[5]
            data_hora = linha[3]
            cursor.execute('INSERT INTO itens (nome, valor, quantidade, data, hora, data_hora) VALUES (?, ?, ?, ?, ?, ?)',
                           (nome, valor, quantidade, data, hora, data_hora))
        conn.commit()

        print('Terminei o for do Sheets')

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
