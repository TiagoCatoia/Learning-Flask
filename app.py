'''
PARA EVITAR O PROBLEMA:
Vamos importar a função ulr_for, responsável por criar urls reversas
apagamos a ulr hardcoded (/user/{username}) e substitui pela chamada da url_for ('{url_for('user', username=username)} ')
chamo a função url_for, passo o nome do endpoint ('user') ao invés de passar a url fazendo math com o argumento->(, endpoint='user'))
e passo os argumentos que a função recebe, ou seja todos os argumentos que estão mapeados na url e na definição da função deixando assim dinâmico
podendo alterar a url de /user/<username>/ para /profile/<username>/ por exemplo
'''
'''
Então podemos definir urls usando o app.route ou da maneira imperativa usando o app.add_url_rule
na verdade são equivalentes, oque muda é que um é usado como decorator e o outro é utilizado diretamente como um método para fazer automatizações (maior flexibilidade)
'''
import db
from flask import Flask, abort, url_for

app = Flask(__name__)

@app.route('/') 
def index():
    html = ['<ul>']
    for username, user in db.users.items():
        html.append(
            f"<li><a href='{url_for('user', username=username)} '>{user['name']}</a></li>"
        )
    html.append('</ul>')
    return '\n'.join(html)

def profile(username):
    user = db.users.get(username)
    if user:
        return f"""
            <h1>{user['name']}</h1>
            <p>Telefone: {user['tel']}</p>
            <p>CPF: {user['cpf']}</p>
            <a href="/">Voltar</a>
            """
    else:
        return abort(404, "User not found")
    
app.add_url_rule('/profile/<username>/', view_func=profile, endpoint='user')

app.run(use_reloader=True)

'''
Para interagir com o flask através do terminal e inspecionar como que é montado o mapa de resolução de URL
usando a extensão flask-shell-ipython e além dela é necessário o ipython
o ipython é um terminal python mais inteligente com algumas facilidades

COMANDOS:  (Ctrl+C para o servidor da aplicação para ser reiniciado no terminal)
ls (Lista o conteúdo do diretório atual)

export FLASK_APP=app.py (Exporta uma variável de ambiente chamada FLASK_APP apontando para o arquivo onde está a aplicação flask)

flask shell (Abre um terminal do ipython, dentro temos o acesso ao app, onde as alterações dentro do app não serão salvas,
é apenas um terminal interativo para explorar e testar possibilidades do flask, testes de API e testes de retorno)

1º '/user/David/' ou nesse caso '/profile/David/'
2º app.url_map
app.url_map (Mostra o mapa de regras, que aparece quando um usuário acessa por exemplo o '/user/David/'(ou nesse caso '/profile/David/'),
esse mapa é uma lista de regras com o url acessado, quais os métodos http que ele aceita
(por padrão o GET e o HEAD E OPTIONS metódos http de controle usado pelo navegador e clientes e qual a função que está apontando ->user))
além disso o flask possui uma rota padrão para arquivos estáticos

Podemos testar as rotas sem precisar do navegador:
1º client = app.test_client()
2º client
client = app.test_client() (Retorna uma instância da classe FlaskClient)

O client é como se fosse um navegador que funciona somente no terminal, esse navegador expõe vários métodos  para cada um dos métodos http
que podem ser vistos com client.
exemplos: client.get, client.put, client.post, client.delete, client.patch, client.head, client.options, etc...

client.get (Chama uma url e vizualiza o seu retorno)
1º client.get('/profile/David/')  200 OK
2º client.get('/profile/David') 308 REDIRECT
3º para seguir o REDIRECT client.get('/profile/David', follow_redirects=True) 200 OK

.status (Mostra o status de uma url ex: client.get('/profile/David/').status
.headers (Mostra os headers http na url que foram trafegados ex: client.get('/profile/David/').headers
.data (Mostra os dados ex: client.get('/profile/David/').data)
'''