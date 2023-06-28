import sqlite3

class BancoDeDados:                                                 # classe responsável por todos os metodos relacionados ao banco de dados
    def __init__(self, db_file):                                        # metodo incicializador da classe de banco de dados, 
        self.db_file = db_file                                              # recebe o nome do banco passado em "main.py"
        self.conn = None                                                    # atributo que recebe a conexão com o banco de dados
        self.cursor = None                                                  # atributo responsavel por interagir diretamente com o banco permitindo a execução de operações SQL e a manipulação de dados armazenados no banco
        self.conectar_bd()                                                  # responsavel por conectar o banco de dados

    def conectar_bd(self):                                              # metodo responsavel por conectar o banco de dados
        self.conn = sqlite3.connect(self.db_file)                           # atribui a conexão passando o nome do banco recebido de "main.py"
        self.cursor = self.conn.cursor()                                    # atribui cursor (manipulador) à conexão do banco de dados
        self.criar_tabela()                                                 # cria a tabela do banco

    def criar_tabela(self):                                             # metodo responsavel por criar a tabela e as colunas do banco
        # o manipulador cria a tabela caso não exista e insere as colunas abaixo
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

        self.conn.commit() # envia as mudanças para o banco de dados                                      

    def inserir_item(self, nome, valor, quantidade, data, hora, data_hora):                                                     # metodo responsavel pela insersão de itens no banco de dados   
        query = 'INSERT INTO itens (nome, valor, quantidade, data_hora, data, hora, data_hora) VALUES (?, ?, ?, ?, ?, ?, ?)'        # query passada para o banco de dados interpretar e inserir de acordo com as colunas criadas os valores passados 
        self.cursor.execute(query, (nome, valor, quantidade, data_hora, data, hora, data_hora))                                     # o manipulador envia a query e os valores para o banco
        self.conn.commit()                                                                                                          # envia as mudanças para o banco

    def fechar_conexao(self):                                           # metodo responsável por fechar a conexão com o banco de dados
        self.cursor.close()                                                 # fecha o manipulador do banco
        self.conn.close()                                                   # fecha a tabela

    def obter_dados(self, filtro_nome):                                 # metodo responsável por resgatar os dados do banco de dados
        self.cursor.execute('SELECT id, nome, valor, hora FROM itens WHERE nome = ?', (filtro_nome,)) # faz a consulta dos itens das colunas passadas com base no filtro informado
        return self.cursor.fetchall()                                       # resgata todos os itens selecionados e retorna uma lista de tupla [(item)]
   