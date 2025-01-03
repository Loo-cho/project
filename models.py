from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Inizializza SQLAlchemy e Marshmallow
db = SQLAlchemy()
ma = Marshmallow()

# Modelli del database
class Piatto(db.Model):
    __tablename__ = 'piatto'
    id_piatto = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    ricetta = db.Column(db.Text, nullable=False)
    
    # Relazione con la tabella ricetta
    ricette = db.relationship('Ricetta', backref='piatto', lazy=True)

class Ingrediente(db.Model):
    __tablename__ = 'elenco_ingredienti'
    id_ing = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    descrizione = db.Column(db.String(100))

class Ricetta(db.Model):
    __tablename__ = 'ricetta'
    id_p = db.Column(db.Integer, db.ForeignKey('piatto.id_piatto'), primary_key=True)
    id_i = db.Column(db.Integer, db.ForeignKey('ingredienti.id_ing'), primary_key=True)
    quantita = db.Column(db.Integer, nullable=False)
    
    # Relazioni con le tabelle piatto e ingrediente


# Schemi per la serializzazione con Marshmallow
class PiattoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Piatto

class IngredienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ingrediente

class RicettaSchema(ma.SQLAlchemyAutoSchema):
    # Includiamo il piatto e l'ingrediente per ogni ricetta
    piatto = ma.Nested(PiattoSchema)
    ingrediente = ma.Nested(IngredienteSchema)
    
    class Meta:
        model = Ricetta

