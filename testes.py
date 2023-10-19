from flask import Flask
from flask import redirect
from flask import url_for

application = Flask(__name__)
# Trabalhando com rotas
@application.route("/formulario/<nome>")
def form(nome):
    return f"""
                <h1> Faça o cadastro {nome} </h1>
                <from>
                    <label>Nome</label>
                    <input type='text' name='name' placeholder='Insira teu nome de usuário'/>
                    <input type='email' name='email' placeholder='Insera o seu email' />
                    <button>Enviar</button>
                </form>
            """.format(nome)

@application.route("/blog/<int:postId>")
def blogue(postId=1):
    if postId >= 0:
        return f"""
                   <p> Informações do Blogue {postId}</p>
                """.format(postId)
    else:
        return "<p>Bolgue de todos</p>"

@application.route("/admin")

def rotas1():
    return "<h1>Rota1</h1>"

@application.route("/rota2/<rota2>")
def rota2(rota2):
    return "<h2>Rota2</h2> {}".format(rota2)

@application.route("/")
def vazio():
    return '<p>Não reconhecido/não faz-se presente no sistema ou BD</p>'

@application.route("/google")
def google():
    return redirect('http://google.com')

@application.route("/user/<name>")
def user(name):
    if name == 'admin':
        return redirect('admin')
    elif name == '':
        return redirect(url_for('vazio'))
    elif name == 'google':
        return redirect(url_for('google'))
    else:
        return redirect(url_for('rota2', rota2 = name))

if __name__ == '__main__':
    application.run(debug=True, port=3000)


# Consumindo dados do formulário

from flask import Flask
from flask import request
from flask import redirect
from json import dumps

app = Flask(__name__, static_folder='page')

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        return dumps(request.form)
    elif request.method == 'GET':
        return redirect('http://facebook.com/romeucajamba/')
    else:
        return '<h1>Não foi poosível executar o pedido</h1>'

if __name__ == '__main__':
    app.run(debug=False, port=3000)

#Requesição

from flask import Flask
from flask import request
from json import dumps

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def requesicao():
    print(request.method, request.args)
    return dumps(request.args)

if __name__ == '__main__':
    app.run(debug=False)



# Redirecionamento e erros

from flask import Flask
from flask import request
from flask import abort
from flask import redirect
from flask import url_for


app = Flask(__name__, static_folder='page')

@app.route("/form", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['pass'] == 'admin':
             return redirect(url_for('sucesso'), code=200)
        else: abort(401)
    else:
        abort(403)

@app.route("/sucesso")
def sucesso():
    return 'sucesso'

if __name__ == '__main__':
    app.run(port=3000)

# Template

# Templates usando o modelo jinga 2
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__, template_folder='templates')

@app.route("/")
def notas():
    return render_template('modelo.html')


@app.route("/calculo", methods=['POST'])
def calculo():
    total = request.form.to_dict().values()
    return total

if __name__ == '__main__':
    app.run(debug=True)

# Session
from flask import Flask
from flask import render_template
from flask import session
from flask import request
from flask import url_for
from flask import redirect


app = Flask(__name__, static_folder='templates')

@app.route("/")
def index():
    username = ''
    if 'username' in session:
        username = session['username']
    return render_template('modelo.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['username'] == '':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/setsession/<s>')
def setsession(s):
    session['username'] = s
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()

 # Upload de arquivos

from flask import Flask
from flask import render_template
from flask import request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='templates')

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    savepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(savepath)
    return 'upload feito com sucesso'

@app.route('/get-file/<filename>')
def getfile(filename):
    file = os.path.join(UPLOAD_FOLDER, filename + '.png')
    return send_file(file, filename, mimetypes="image/png")

if __name__ == '__main__':
    app.run()