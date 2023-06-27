import sqlite3

class BancoDeDados:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.conectar_bd()

    def conectar_bd(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
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
        self.conn.commit()

    def inserir_item(self, nome, valor, quantidade, data, hora, data_hora):
        query = 'INSERT INTO itens (nome, valor, quantidade, data_hora, data, hora, data_hora) VALUES (?, ?, ?, ?, ?, ?, ?)'
        self.cursor.execute(query, (nome, valor, quantidade, data_hora, data, hora, data_hora))
        self.conn.commit()

    def fechar_conexao(self):
        self.cursor.close()
        self.conn.close()

    def obter_dados(self, filtro_nome):
        self.cursor.execute('SELECT valor, data FROM itens WHERE nome = ?', (filtro_nome,))
        return self.cursor.fetchall()