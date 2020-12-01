from bancodedados import bd
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def logar():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login():
    username = str(request.form['user'])
    password = str(request.form['password'])
    mysql = bd.SQL('root', '')
    comando = "SELECT * from tb_usuarios where user='" + username + "' and password= '" + password + "';"
    cursor = mysql.consultar(comando, ())
    dados = cursor.fetchone()
    if len(dados) != 2:
        return redirect(url_for('menu'))
        print(len(dados))
    else:
        return "falha"

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form['nome']
    vlrCompra = float(request.form['vlrCompra'])
    vlrVenda = float(request.form['vlrVenda'])
    quantidade = int(request.form['quantidade'])
    categoria = request.form['categoria']
    mysql = bd.SQL('root', '')
    comando = '''INSERT INTO tb_produtos(nme_produto, vlrCompra_produto, vlrVenda_produto, quatidade_produto, categoria_produto) values
     (%s, %s, %s, %s, %s);'''
    if mysql.executar(comando, [nome, vlrCompra, vlrVenda, quantidade, categoria]):
        msg = 'Produto adicionado com sucesso!'
    else:
        msg = 'Falha na adicao do produto...'
    return render_template('cadastro.html', msg=msg)

@app.route('/cadastrarclientes')
def cadastrarclientes():
    return render_template('cadastrarclientes.html')
@app.route('/cadastroclientes', methods=['POST'])
def cadastroclientes():
    nome = request.form['nome']
    cpf = request.form['cpf']

    mysql = bd.SQL('root', '')
    comando = '''INSERT INTO tb_clientes(nme_cliente, cpf_cliente) values (%s, %s);'''

    if mysql.executar(comando, [nome, cpf]):
        msg = 'Sucesso na inclusao do cliente!'
    else:
        msg = 'Falha na inclusao.'
    return render_template('cadastroclientes.html', msg=msg)
@app.route('/consultarProdutos')
def consultarProdutos():
    mysql = bd.SQL('root', '')
    comando = '''SELECT distinct nme_produto from tb_produtos order by nme_produto;'''
    cs = mysql.consultar(comando, ())
    sel = "<SELECT NAME='nome'>"
    for [nome] in cs:
        sel += "<OPTION>" + nome + "</OPTION>"
    sel += "</SELECT>"
    cs.close()
    return render_template('consultar.html', nome=sel)
@app.route('/produtos', methods=['POST'])
def produtos():
    nome = request.form['nome']
    mysql = bd.SQL('root', '')
    comando = '''SELECT * FROM tb_produtos where nme_produto like concat('%', %s, '%') order by quatidade_produto;'''
    cs = mysql.consultar(comando, [nome])
    produtos = ""
    for [idt, nomep, vlrVenda, vlrCompra, categoria, quantidade] in cs:
        produtos += "<TR scope='row'>"
        produtos += "<TD>" + str(idt) + "</TD>"
        produtos += "<TD>" + nomep + "</TD>"
        produtos += "<TD>" + str(vlrCompra) + "</TD>"
        produtos += "<TD>" + str(vlrVenda) + "</TD>"
        produtos += "<TD>" + categoria + "</TD>"
        produtos += "<TD>" + str(quantidade) + "</TD>"
        produtos += "</TR>"
    cs.close()

    return render_template('produtos.html', produtos=produtos)
@app.route('/edicao')
def edicao():
    return render_template('edicao.html')
@app.route('/formalterar', methods=['POST'])
def formalterar():
    nome = request.form['nome']
    mysql = bd.SQL('root', '')
    comando = '''SELECT * FROM tb_produtos where nme_produto=%s;'''
    cs = mysql.consultar(comando, [nome])
    dados = cs.fetchone()
    cs.close()

    if dados == None:
        return render_template('naoencontrado.html')
    else:
        return render_template('formalterar.html', idt=dados[0], nome=dados[1], vlrCompra=dados[2], vlrVenda=dados[3], categoria=dados[4], quantidade=dados[5])
@app.route('/alterar', methods=['POST'])
def alterar():
    nome = request.form['nome']
    vlrCompra = float(request.form['vlrcompra'])
    vlrVenda = float(request.form['vlrvenda'])
    categoria = request.form['categoria']
    quantidade = request.form['quantidade']

    mysql = bd.SQL('root', '')
    comando = '''UPDATE tb_produtos set nme_produto=%s, vlrCompra_produto=%s, vlrVenda_produto=%s, categoria_produto=%s, quatidade_produto=%s where nme_produto=%s;'''
    if mysql.executar(comando, [nome, vlrCompra, vlrVenda, categoria, quantidade, nome]):
        msg = "Produto " + nome + " alterado com sucesso..."
    else:
        msg = "Falha na inclusao do produto..."
    return render_template('alterar.html', msg=msg)

@app.route('/edicaoclientes')
def edicaoclientes():
    return render_template('edicaoclientes.html')
@app.route('/formalterarcliente', methods=['POST'])
def formalterarcliente():
    nome = request.form['nomecliente']
    mysql = bd.SQL('root', '')
    comando = '''SELECT * FROM tb_clientes where nme_cliente=%s;'''
    cs = mysql.consultar(comando, [nome])
    dados = cs.fetchone()
    cs.close()
    if dados == None:
        return render_template('naoencontrado.html')
    else:
        return render_template('formalterarclientes.html', idt=dados[0], nome=dados[1], cpf_cliente=dados[2])
@app.route('/alterarclientes', methods=['POST'])
def alterarclientes():
    nome = request.form['nomecliente']
    cpf = request.form['cpf']
    mysql = bd.SQL('root', '')
    comando = '''UPDATE tb_clientes set nme_cliente=%s, cpf_cliente=%s where nme_cliente=%s;'''
    if mysql.executar(comando, [nome, cpf, nome]):
        msg = "Cliente " + nome + " alterado com sucesso..."
    else:
        msg = "Falha na alteracao do cliente..."
    return render_template('alterar.html', msg=msg)
@app.route('/clientes')
def consultarclientes():
    mysql = bd.SQL('root', '')
    comando ='''SELECT distinct nme_cliente, cpf_cliente from tb_clientes order by nme_cliente;'''
    cs = mysql.consultar(comando, ())
    pessoas = "<TABLE>"
    for [nome, cpf] in cs:
        pessoas += "<TR>"
        pessoas += "<TD> Nome: " + nome + "</TD>" + "<TD> CPF: " + cpf + "</TD>"
    pessoas += "</TR>"
    pessoas += "</TABLE>"
    cs.close()
    return render_template('clientes.html', pessoas=pessoas)
@app.route('/excluirpdts')
def excluirpdts():
    return render_template('excluirprodutos.html')
@app.route('/excluirprodutos', methods=['POST'])
def excluirprodutos():
    mysql = bd.SQL('root', '')
    nome = request.form['nome']
    comando = '''DELETE from tb_produtos where nme_produto=%s;'''
    if mysql.executar(comando, [nome]):
        msg = 'Sucesso na exclusao do produto' + nome
    else:
        msg = 'Produto nao encontrado'
    return render_template('cadastroclientes.html', msg=msg)
@app.route('/excluircli')
def excluircli():
    return render_template('excluirclientes.html')
@app.route('/excluirclientes', methods=['POST'])
def excluirclientes():
    mysql = bd.SQL('root', '')
    nome = request.form['nome']
    comando = '''DELETE from tb_clientes where nme_cliente=%s;'''
    if mysql.executar(comando,[nome]):
        msg = 'Sucesso na exclusao do cliente ' + nome
    else:
        msg = 'Falha na exclusao do cliente.'
    return render_template('cadastroclientes.html', msg=msg)






