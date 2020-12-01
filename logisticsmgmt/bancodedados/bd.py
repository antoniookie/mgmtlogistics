import mysql.connector

class SQL:
    def __init__(self, usuario, senha):
        self.cnx = mysql.connector.connect(user=usuario, password=senha, database='ceub', host='localhost')
    def executar(self, comando, parametros):
        cursor = self.cnx.cursor()
        cursor.execute(comando, parametros)
        self.cnx.commit()
        cursor.close()
        return True
    def consultar(self, comando, parametros):
        cursor = self.cnx.cursor()
        cursor.execute(comando, parametros)
        return cursor
    def __del__(self):
        self.cnx.close()
