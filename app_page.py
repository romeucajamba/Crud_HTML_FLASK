from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
import  sqlite3


app = Flask(__name__, static_folder='templates')
# Configurações de banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudantes.sqlite'

db = SQLAlchemy(app)
class Estudantes(db.Model):#fazendo o mapeamento
    __dabasename__ = 'Estudantes',
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    def __int__(self, name, age):
        self.name = name
        self.age = age


@app.route('/')
def index():
    estudantes = Estudantes.query.all() # Fazendo com que os dados dos estudantes cheguem até aqui
    return render_template('index.html', estudantes=estudantes)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        estudante = Estudantes(request.form['nome'], request.form['idade'])
        db.session.add(estudante)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('add.html'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    estudante = Estudantes.query.get(id)
    if request.method == 'POST':
        estudante.nome = request.form['nome']
        estudante.idade = request.form['idade']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', estudante=estudante)



@app.route('/delete/<int:id>')
def delete(id):
    estudante = Estudantes.query.get(id)
    db.session.delete(estudante)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()  # pegar a nossa classe vai criar toda estrutura no banco
    app.run()