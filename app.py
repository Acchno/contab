from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Substitua por uma chave secreta segura

# Caminho do arquivo de dados
data_file = 'data/registros.csv'

# Certifique-se de que o arquivo exista e tenha as colunas necessárias
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.isfile(data_file) or os.stat(data_file).st_size == 0:
    df = pd.DataFrame(columns=['Tipo', 'Data_Hora', 'Nome', 'Item', 'Quantidade'])
    df.to_csv(data_file, index=False)

# Função de verificação de login
def check_login(username, password):
    return username == 'admin' and password == '94.666'

# Lista de itens sugeridos
item_suggestions = [
    'Maconha', 'Cocaína', 'Metanfetamina', 'Heroína',
    'Pistolas 9mm', 'Pistola fajuta', 'Bala 9mm', 'Bala .45', 'C4', 'Dinheiro sujo','Dinheiro' , 'Lockpick'
]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if check_login(username, password):
        session['logged_in'] = True
        return redirect(url_for('home'))
    else:
        return render_template('login.html', error="Credenciais inválidas")

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/entrada', methods=['GET', 'POST'])
def entrada():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        item = request.form['item']
        quantidade = int(request.form['quantidade'])
        df = pd.read_csv(data_file)
        new_row = pd.DataFrame([{'Tipo': 'Entrada', 'Data_Hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Nome': nome, 'Item': item, 'Quantidade': quantidade}])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(data_file, index=False)
        return redirect(url_for('home'))
    return render_template('entrada.html', item_suggestions=item_suggestions)

@app.route('/saida', methods=['GET', 'POST'])
def saida():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        item = request.form['item']
        quantidade = int(request.form['quantidade'])
        df = pd.read_csv(data_file)
        # Verifica se há quantidade suficiente do item para subtrair
        current_stock = df[df['Item'] == item]['Quantidade'].sum()
        if current_stock >= quantidade:
            new_row = pd.DataFrame([{'Tipo': 'Saída', 'Data_Hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Nome': nome, 'Item': item, 'Quantidade': -quantidade}])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(data_file, index=False)
        else:
            return render_template('saida.html', error="Quantidade insuficiente em estoque", item_suggestions=item_suggestions)
        return redirect(url_for('home'))
    return render_template('saida.html', item_suggestions=item_suggestions)

@app.route('/controle', methods=['GET'])
def controle():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    df = pd.read_csv(data_file)
    total_items = df.groupby('Item')['Quantidade'].sum().reset_index()
    return render_template('controle.html', items=total_items.to_dict(orient='records'))

@app.route('/gerar_relatorio', methods=['POST'])
def gerar_relatorio():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    df = pd.read_csv(data_file)
    relatorio_file = 'data/relatorio.xlsx'
    df.to_excel(relatorio_file, index=False)
    return send_file(relatorio_file, as_attachment=True)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

