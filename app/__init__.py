from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import uuid

app = Flask(__name__)

# Abrir uma única conexão com o banco de dados
conn = sqlite3.connect('Estoque.db')
cursor = conn.cursor()

# Verificar se a tabela "Estoque" existe e criar se não existir
cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Estoque'")
if cursor.fetchone()[0] == 0:
    cursor.execute('''
                       CREATE TABLE Estoque(
                           id_produto TEXT PRIMARY KEY,
                           nome TEXT UNIQUE,
                           tipo TEXT,
                           quantidade INTEGER,
                           valor INTEGER
                       )
                       ''')
    conn.commit()  # Commit após a criação da tabela
    print('A tabela "Estoque" foi criada com sucesso.')

def obter_produtos():
    with sqlite3.connect('Estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Estoque')
        dados = cursor.fetchall()
    return dados

@app.route('/estoque')
def estoque():
    dados = obter_produtos()
    if dados is None:
        dados = []
    return render_template('estoque.html', dados=dados)

@app.route('/cadastrar', methods=['POST'])
def cadastrar_produto():
    nome = request.form['nome']
    tipo = request.form['tipo']
    quantidade = int(request.form['quantidade'])
    valor = int(request.form['valor'])
    id_produto = str(uuid.uuid4())

    with sqlite3.connect('Estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Estoque (id_produto, nome, tipo, quantidade, valor) VALUES (?, ?, ?, ?, ?)", 
                       (id_produto, nome, tipo, quantidade, valor))
        conn.commit()

    return redirect(url_for('estoque'))

@app.route('/modificar_produto', methods=['POST'])
def modificar_produto():
    id_modificar = request.form['id_modificar']
    nome_modificar = request.form['nome_modificar']
    tipo_modificar = request.form['tipo_modificar']
    quantidade_modificar = request.form['quantidade_modificar']
    valor_modificar = request.form['valor_modificar']

    with sqlite3.connect('Estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Estoque SET nome = ?, tipo = ?, quantidade = ?, valor = ? WHERE id_produto = ?",
                       (nome_modificar, tipo_modificar, quantidade_modificar, valor_modificar, id_modificar))
        conn.commit()

    return redirect(url_for('estoque'))

@app.route('/excluir_produto/<string:id_produto>', methods=['POST'])
def excluir_produto(id_produto):
    with sqlite3.connect('Estoque.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Estoque WHERE id_produto = ?", (id_produto,))
        conn.commit()

    return redirect(url_for('estoque'))

if __name__ == '__main__':
    app.run(debug=True)
