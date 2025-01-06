from flask import Flask, request, jsonify
from models import db, ma, Piatto, Ingrediente, Ricetta, PiattoSchema, IngredienteSchema, RicettaSchema
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)


#lista piatti iniziale
@app.route('/piatti', methods=['GET'])
def get_all_ricette():

    piatto = Piatto.query.all()
    
    if not piatto:
        return jsonify({"message": "Nessun piatto trovato"}), 404


    piatto_schema = PiattoSchema(many=True)
    return piatto_schema.jsonify(piatto)


#piatto tramite nome
@app.route('/piatti/<string:nome>', methods=['GET'])
def get_piatto_by_name(nome):
    piatto = Piatto.query.filter(Piatto.nome.ilike(f'%{nome}%')).first()
    if piatto is None:
        return jsonify({"message": "Piatto non trovato"}), 404
    piatto_schema = PiattoSchema()
    return piatto_schema.jsonify(piatto)


#cerca piatto tramite ingredienti
@app.route('/piatti/ingredienti', methods=['GET'])
def get_piatto_by_ingredienti():
    ingredienti = request.args.getlist('ingrediente')
    if not ingredienti:
        return jsonify({"message": "Inserisci almeno un ingrediente"}), 400
    
    piatti = db.session.query(Piatto).join(Ricetta).join(Ingrediente).filter(Ingrediente.nome.in_(ingredienti)).all()
    
    if not piatti:
        return jsonify({"message": "Nessun piatto trovato con questi ingredienti"}), 404
    
    piatti_schema = PiattoSchema(many=True)
    return piatti_schema.jsonify(piatti)


#aggiugngi piatto
@app.route('/piatti/add', methods=['POST'])
def add_piatto():
    data = request.get_json()
    nome = data.get('nome')
    ricetta = data.get('ricetta')
    
    if not nome or not ricetta:
        return jsonify({"message": "Nome e ricetta sono richiesti"}), 400
    
    nuovo_piatto = Piatto(nome=nome, ricetta=ricetta)
    
    db.session.add(nuovo_piatto)
    db.session.commit()
    
    piatto_schema = PiattoSchema()
    return piatto_schema.jsonify(nuovo_piatto), 201


if __name__ == '__main__':
    app.run(debug=True)

