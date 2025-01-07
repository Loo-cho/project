from flask import Flask, request, jsonify
import models as m
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

m.db.init_app(app)
m.ma.init_app(app)


#lista piatti iniziale
@app.route('/piatti', methods=['GET'])
def get_all_ricette():

    piatto = m.Piatto.query.all()
    
    if not piatto:
        return jsonify({"message": "Nessun piatto trovato"}), 404


    piatto_schema = m.PiattoSchema(many=True)
    return piatto_schema.jsonify(piatto)


#piatto tramite nome
@app.route('/piatti/<string:nome>', methods=['GET'])
def get_piatto_by_name(nome):

    piatti = m.db.session.query(m.Piatto).join(m.Ricetta).join(m.Ingrediente).filter(m.Piatto.nome.ilike(f'%{nome}%')).all()

    if not piatti:
        return jsonify({"message": "Nessun piatto trovato con questo nome"}), 404
    
    ricetta_schema = m.RicettaSchema(many=True)
    return ricetta_schema.jsonify(piatti)



#cerca piatto tramite ingredienti
@app.route('/piatti/ingredienti', methods=['GET'])
def get_piatto_by_ingredienti():
    ingredienti = request.args.getlist('ingrediente')
    if not ingredienti:
        return jsonify({"message": "Inserisci almeno un ingrediente"}), 400
    
    piatti = m.db.session.query(m.Piatto).join(m.Ricetta).join(m.Ingrediente).filter(m.Ingrediente.nome.in_(ingredienti)).all()
    
    if not piatti:
        return jsonify({"message": "Nessun piatto trovato con questi ingredienti"}), 404
    
    piatti_schema = m.PiattoSchema(many=True)
    return piatti_schema.jsonify(piatti)


#aggiungi piatto
@app.route('/piatti/add', methods=['POST'])
def add_piatto():
    data = request.get_json()
    nome = data.get('nome')
    ricetta = data.get('ricetta')
    
    if not nome or not ricetta:
        return jsonify({"message": "Nome e ricetta sono richiesti"}), 400
    
    nuovo_piatto = m.Piatto(nome=nome, ricetta=ricetta)
    
    m.db.session.add(nuovo_piatto)
    m.db.session.commit()
    
    piatto_schema = m.PiattoSchema()
    return piatto_schema.jsonify(nuovo_piatto), 201


if __name__ == '__main__':
    app.run(debug=True)

