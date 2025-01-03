from flask import Flask, request, jsonify
from models import db, ma, Piatto, Ingrediente, Ricetta, PiattoSchema, IngredienteSchema, RicettaSchema
from config import Config

# Crea l'applicazione Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inizializza SQLAlchemy e Marshmallow
db.init_app(app)
ma.init_app(app)

# API per cercare un piatto per nome
@app.route('/api/piatti/<string:nome>', methods=['GET'])
def get_piatto_by_name(nome):
    piatto = Piatto.query.filter(Piatto.nome.ilike(f'%{nome}%')).first()
    if piatto is None:
        return jsonify({"message": "Piatto non trovato"}), 404
    piatto_schema = PiattoSchema()
    return piatto_schema.jsonify(piatto)


@app.route('/api/piatti', methods=['POST'])
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

@app.route('/api/piatti/ingredienti', methods=['GET'])
def get_piatto_by_ingredienti():
    ingredienti = request.args.getlist('ingrediente')
    if not ingredienti:
        return jsonify({"message": "Inserisci almeno un ingrediente"}), 400
    
    piatti = db.session.query(Piatto).join(Ricetta).join(Ingrediente).filter(Ingrediente.nome.in_(ingredienti)).all()
    
    if not piatti:
        return jsonify({"message": "Nessun piatto trovato con questi ingredienti"}), 404
    
    piatti_schema = PiattoSchema(many=True)
    return piatti_schema.jsonify(piatti)

@app.route('/api/piatti', methods=['GET'])
def get_all_ricetti():

    piatto = Piatto.query.all()
    
    if not piatto:
        return jsonify({"message": "Nessun piatto trovato"}), 404


    piatto_schema = PiattoSchema(many=True)
    return piatto_schema.jsonify(piatto)


if __name__ == '__main__':
    app.run(debug=True)

