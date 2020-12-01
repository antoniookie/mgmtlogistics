from bancodedados import bd

mysql = bd.SQL('root', '')

comando = '''DROP TABLE IF EXISTS tb_produtos;'''

if mysql.executar(comando, ()):
    print('Tabela excluida com sucesso...')

comando = '''CREATE TABLE tb_produtos(
idt_produto int auto_increment primary key,
nme_produto varchar(50) not null,
vlrCompra_produto decimal(5,2) not null,
vlrVenda_produto decimal(5,2) not null,
categoria_produto varchar(50) not null,  
quatidade_produto int(10) not null);'''

if mysql.executar(comando, ()):
    print('Tabela criada com sucesso...')
