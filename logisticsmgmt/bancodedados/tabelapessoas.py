import mysql.connector
from bancodedados import bd
sql = bd.SQL('root', '')

comando = '''DROP TABLE IF EXISTS tb_clientes;'''
if sql.executar(comando, ()):
    print('Tabela apagada com sucesso...')

comando = '''CREATE table tb_clientes(
idt_cliente int auto_increment primary key,
nme_cliente varchar(50) not null, 
cpf_cliente varchar(11) not null);'''

if sql.executar(comando, ()):
    print('Tabela criada com sucesso')
