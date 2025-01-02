#prova merge
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import models as m

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mariadbconnector://root@127.0.0.1:3306/project'

m.sa.init_app(app)

with app.app_context():
    m.sa.create_all()

# Lista json
@app.route('/lista_ricette_cond', methods=['GET'])
def listaRicetteCond():
    data = m.Ricetta.query.all()

    lista_dict = [
        {
            'id': item.idStudente,
            'nome': item.nome,
            'cognome': item.cognome,
            'dataDiNascita': item.dataDiNascita
        }
        for item in data
    ]

    return lista_dict

@app.route("/find/<int:id_ricetta>", methods=['PATCH'])
def findRicettaId(id_ricetta):

    ricetta=m.Ricetta.query.get(id=id_ricetta) #un solo  elemento, posso usare get
    
    return redirect ( url_for( 'index'))

@app.route('/')
def index():
    data = m.Ricetta.query.all()

    lista_dict = [
        {
            'id': item.idStudente,
            'nome': item.nome,
            'cognome': item.cognome,
            'dataDiNascita': item.dataDiNascita
        }
        for item in data
    ]

    return lista_dict



if __name__ == '__main__':
    app.run(debug=True)


