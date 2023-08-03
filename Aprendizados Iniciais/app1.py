# podemos registra uma url de 2 maneiras usando o flask

import db
from flask import Flask, abort

app = Flask(__name__)

# ulr raíz 'http://localhost:5000' = '/'

# 1º MANEIRA: REGISTRANDO A URL COM APP.ROUTE('/')
@app.route('/') # decorator usado para definir minha url raíz
def index():
    html = ['<ul>']
    for username, user in db.users.items(): # para cada username e user data (dados) dentro de db.users.items eu começo a criar objetos html
        html.append(
            f"<li><a href='/user/{username}'>{user['name']}</a></li>" # manda para uma url /user/{username}(parametro dinâmico) e o texto do link vai ser o próprio nome do usuário
        )
    html.append('</ul>')
    return '\n'.join(html) # pega a lista elementos html e transforma em texto, para cada \n faz um join com a lista html

def profile(username):
    user = db.users.get(username) # consultando o bando de dados com o método get atras do username, se ele existir ele vai retornar os outros dados, se não vai retornar none

    if user: # vai retornar um texto/html se achar
        # f""" é um string multilinha em python que também é uma f string
        # dentro dessa f string estou crinado um template html que mostra o título do username, telefone,cpf e botao de voltar
        return f"""
            <h1>{user['name']}</h1>
            <p>Telefone: {user['tel']}</p>
            <p>CPF: {user['cpf']}</p>
            <a href="/">Voltar</a>
            """
    else: # se tento acessar o /username sem ter achado, dai que usamos a função abort importada que trata o erro que retorna um response com o erro http código 400 ou 500
        return abort(404, "User not found")
    
# 2º MANEIRA
'''
Maneira imperativa de chamar, as vezes não posemos usar o decorator(app.route('/')) ou queremos automatizar o registro de URLS
como dessa maneira não usa o decorator, é obrigado a indentificar a view_func onde passamos a função profile e informar o endpoint chamdo de 'user'
se não informar o endpoint ele vai usar o próprio nome da função (profile)
'''
app.add_url_rule('/user/<username>/', view_func=profile, endpoint='user') # / no final da url para que não seja necessário o redirect (algumas APIs n permitem redirection)
'''
PROBLEMA: estamos usando url hardcoded (no href colocamos a url direto f"<li><a href='/user/{username}'>{user['name']}</a></li>")
logo se mudarmos a rota (app.add_url_rule('/user/<username>/') de /user/ para /profile/ por exemplo
quando tentarmos acessar teremos um not found, pois a url alterou apenas na definição mas não em todas as referências que estão chamando ela
para evitar esse problema, nunca internamente usamos ulr hardcoded, usamos o endpoint para garantir que o endpoint não mude, mesmo que a ulr exposta mude
'''

# SOLUÇÂO NO app.py

app.run(use_reloader=True) # o reloader faz com que cada vez que salvo o arquivo reflete na aplicação sem ter que ficar reiniciando