import os
import logging
from flask import Flask, jsonify, request, abort
from flask_cors import CORS  # <-- Hier importieren
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv
import pymysql
import flask 








"""
wichtig um das programm ausuführen:


1.  ich muss mich in mysql workbench mit passwort einloggen in die datenbank, also explizt anmelden in mysql workbench mit dem apfelkuchen passwort., ansonsten geht es nicht. man könnte alternativ einfach ein modul installieren um das zu umgehen.

2. die datenbank starten bzw. das programm: "Backend.py2 ausführen.

einmal konsole bzw. shell in vscode öffnen.
(in den richtigen ordner gehen)-->Dort dann: npm run dev


"""











#WICHTIG: starte erst mysql workbench und logge dich ein, sonst funktioniert das nicht oder installiere halt noch das eine modul halt noch

#WICHTIG: wenn ich npm nutzen will muss ich immer davor: Set-ExecutionPolicy Unrestricted -Scope CurrentUser ausführen in der konsole

#http://127.0.0.1:5000/ -->wichtige adresse im browser um es zu checken quasi.
# Erstellt eine Flask-Anwendung und bestimmt den Speicherort für Dateien wie Templates und statische Dateien.
app = Flask(__name__)

# CORS aktivieren
CORS(app)

@app.route("/")
def home():
    return "Willkommen in der Bücherverwaltung!"


# Zum ersten mal sqlalchemy genutzt mit orm, mir persönlich hat es nicht so gefallen wie explizite sql statements mit bspw. mysql connect

# Logging einrichten (statt print) -->Hab ich zum ersten Mal genutzt.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Umgebungsvariablen laden
load_dotenv()

# Verbindungsdetails aus .env
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
DATABASE_NAME = "BücherverwaltungsDatenbank"

"""  
Engine für Datenbank ohne DB (zum Erstellen der Datenbank)
Erstellt eine SQLAlchemy-Engine für MySQL OHNE spezifische Datenbank
Diese Engine wird genutzt, um die Datenbank zu erstellen, falls sie nicht existiert"""
DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}"
engine = create_engine(DATABASE_URL, echo=False)


"""
# Engine für spezifische Datenban
# Erstellt eine zweite SQLAlchemy-Engine für MySQL MIT spezifischer Datenbank
# Sobald die Datenbank existiert, wird diese Engine für alle weiteren Operationen genutzt
"""
DATABASE_URL_WITH_DB = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{DATABASE_NAME}"
engine_with_db = create_engine(DATABASE_URL_WITH_DB, echo=False)

# Erstellt eine SessionFactory, die für alle Datenbank-Interaktionen verwendet wird
# Mit `Session()` kann später eine Session erstellt werden, um SQL-Abfragen auszuführen
Session = sessionmaker(bind=engine_with_db)
Base = declarative_base()

# ORM-Modelle
class Verlag(Base):
    __tablename__ = 'verlag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    buecher = relationship("Buch", back_populates="verlag")

class Autor(Base):
    __tablename__ = 'autor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    buecher = relationship("Buch", secondary="buch_autor", back_populates="autoren")

class Buch(Base):
    __tablename__ = 'buch'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titel = Column(String(255), nullable=False)
    verlag_id = Column(Integer, ForeignKey('verlag.id', ondelete='CASCADE'))
    verlag = relationship("Verlag", back_populates="buecher")
    autoren = relationship("Autor", secondary="buch_autor", back_populates="buecher")

class BuchAutor(Base):
    __tablename__ = 'buch_autor'
    buch_id = Column(Integer, ForeignKey('buch.id', ondelete='CASCADE'), primary_key=True)
    autor_id = Column(Integer, ForeignKey('autor.id', ondelete='CASCADE'), primary_key=True)






#CRUD
"""  

GET-Methoden dienen zum Abrufen von Daten aus der Datenbank (Bücher in diesem Fall).

POST-Methoden werden verwendet, um neue Daten zu erstellen.

PUT-Methoden dienen zur Aktualisierung bestehender Daten.

DELETE-Methoden löschen bestehende Daten.
"""


@app.route('/buecher', methods=['GET'])
def get_buecher():
    session = Session()
    try:
        buecher = session.query(Buch).all()
        result = [{"id": buch.id, "titel": buch.titel, "verlag_id": buch.verlag_id} for buch in buecher]
        return jsonify(result)
    except Exception as e:
        logging.error(f"Fehler beim Abrufen der Bücher: {e}")
        abort(500)
    finally:
        session.close()



@app.route('/buch/<int:id>', methods=['GET'])
def get_buch(id):
    session = Session()
    try:
        buch = session.query(Buch).filter_by(id=id).first()
        if buch is None:
            abort(404)
        result = {
            "id": buch.id,
            "titel": buch.titel,
            "verlag_id": buch.verlag_id  # Hier wird die verlag_id hinzugefügt
        }
        return jsonify(result)
    except Exception as e:
        logging.error(f"Fehler beim Abrufen des Buches: {e}")
        abort(500)
    finally:
        session.close()

























# CRUD: Erstelloperationen
@app.route('/buch', methods=['POST'])
def create_buch():
    data = request.get_json()
    
    logging.info(f"Empfangene Daten: {data}")  # Debugging-Log

    if not data or 'titel' not in data or 'verlag_id' not in data:
        logging.error("Fehlende Parameter!")
        abort(400, "Fehlende Parameter")
    
    try:
        verlag_id = int(data['verlag_id'])  # Sicherstellen, dass es eine Zahl ist
        logging.info(f"Verlag ID: {verlag_id}")  # Prüfen, ob verlag_id korrekt ist
    except ValueError:
        logging.error(f"Ungültige verlag_id: {data['verlag_id']}")
        abort(400, "Verlag-ID muss eine Zahl sein")

    session = Session()
    try:
        # Prüfen, ob der Verlag existiert
        verlag = session.query(Verlag).filter_by(id=verlag_id).first()
        if not verlag:
            logging.error(f"Verlag mit ID {verlag_id} existiert nicht!")
            abort(400, "Verlag existiert nicht")

        buch = Buch(titel=data['titel'], verlag_id=verlag_id)
        session.add(buch)
        session.commit()
        
        logging.info(f"Buch erstellt: ID={buch.id}, Titel={buch.titel}, Verlag={buch.verlag_id}")
        return jsonify({"id": buch.id, "titel": buch.titel, "verlag_id": buch.verlag_id}), 201
    
    except Exception as e:
        session.rollback()
        logging.error(f"Fehler beim Erstellen des Buches: {e}")
        abort(500)
    
    finally:
        session.close()



# CRUD: Updateoperationen
@app.route('/buch/<int:id>', methods=['PUT'])
def update_buch(id):
    data = request.get_json()
    
    if not data or 'titel' not in data or 'verlag_id' not in data:
        abort(400, "Fehlende Parameter: Titel und Verlag-ID sind erforderlich.")
    
    session = Session()
    try:
        buch = session.query(Buch).filter_by(id=id).first()
        if buch is None:
            abort(404)
        
        # Sicherstellen, dass der Verlag existiert
        verlag_id = int(data['verlag_id'])
        verlag = session.query(Verlag).filter_by(id=verlag_id).first()
        if not verlag:
            abort(400, "Verlag mit der angegebenen ID existiert nicht.")
        
        buch.titel = data['titel']
        buch.verlag_id = verlag_id  # Hier aktualisieren wir die Verlag-ID
        session.commit()
        
        return jsonify({"id": buch.id, "titel": buch.titel, "verlag_id": buch.verlag_id})
    
    except Exception as e:
        session.rollback()
        logging.error(f"Fehler beim Aktualisieren des Buches: {e}")
        abort(500)
    
    finally:
        session.close()

# CRUD: Löschoperationen
@app.route('/buch/<int:id>', methods=['DELETE'])
def delete_buch(id):
    session = Session()
    try:
        buch = session.query(Buch).filter_by(id=id).first()
        if buch is None:
            abort(404)
        session.delete(buch)
        session.commit()
        return '', 204
    except Exception as e:
        session.rollback()
        logging.error(f"Fehler beim Löschen des Buches: {e}")
        abort(500)
    finally:
        session.close()


# CRUD: Verlage

# Alle Verlage abrufen
@app.route('/verlage', methods=['GET'])
def get_verlage():
    session = Session()
    try:
        verlage = session.query(Verlag).all()
        result = [{"id": verlag.id, "name": verlag.name} for verlag in verlage]
        return jsonify(result)
    except Exception as e:
        logging.error(f"Fehler beim Abrufen der Verlage: {e}")
        abort(500)
    finally:
        session.close()

# Einzelnen Verlag abrufen
@app.route('/verlag/<int:id>', methods=['GET'])
def get_verlag(id):
    session = Session()
    try:
        verlag = session.query(Verlag).filter_by(id=id).first()
        if verlag is None:
            abort(404)
        return jsonify({"id": verlag.id, "name": verlag.name})
    except Exception as e:
        logging.error(f"Fehler beim Abrufen des Verlags: {e}")
        abort(500)
    finally:
        session.close()

# Neuen Verlag erstellen
@app.route('/verlag', methods=['POST'])
def create_verlag():
    data = request.get_json()
    
    if not data or 'name' not in data:
        abort(400, "Fehlender Parameter: Name ist erforderlich.")

    session = Session()
    try:
        verlag = Verlag(name=data['name'])
        session.add(verlag)
        session.commit()
        return jsonify({"id": verlag.id, "name": verlag.name}), 201
    except Exception as e:
        session.rollback()
        logging.error(f"Fehler beim Erstellen des Verlags: {e}")
        abort(500)
    finally:
        session.close()

# Verlag aktualisieren
@app.route('/verlag/<int:id>', methods=['PUT'])
def update_verlag(id):
    data = request.get_json()
    
    if not data or 'name' not in data:
        abort(400, "Fehlender Parameter: Name ist erforderlich.")

    session = Session()
    try:
        verlag = session.query(Verlag).filter_by(id=id).first()
        if verlag is None:
            abort(404)
        
        verlag.name = data['name']
        session.commit()
        return jsonify({"id": verlag.id, "name": verlag.name})
    except Exception as e:
        session.rollback()
        logging.error(f"Fehler beim Aktualisieren des Verlags: {e}")
        abort(500)
    finally:
        session.close()

# Verlag löschen
@app.route('/verlag/<int:id>', methods=['DELETE'])
def delete_verlag(id):
    session = Session()
    try:
        verlag = session.query(Verlag).filter_by(id=id).first()
        if verlag is None:
            abort(404)
        session.delete(verlag)
        session.commit()
        return '', 204
    except Exception as e:
        session.rollback()
        logging.error(f"Fehler beim Löschen des Verlags: {e}")
        abort(500)
    finally:
        session.close()





# GET: Alle Autoren abrufen
@app.route('/autoren', methods=['GET'])
def get_autoren():
    session = Session()
    try:
        autoren = session.query(Autor).all()
        result = [{"id": autor.id, "name": autor.name} for autor in autoren]
        return jsonify(result)
    except Exception as e:
        logging.error(f"Fehler beim Abrufen der Autoren: {e}")
        abort(500)
    finally:
        session.close()

# GET: Einzelnen Autor abrufen
@app.route('/autor/<int:id>', methods=['GET'])
def get_autor(id):
    session = Session()
    try:
        autor = session.query(Autor).filter_by(id=id).first()
        if autor is None:
            abort(404)
        return jsonify({"id": autor.id, "name": autor.name})
    except Exception as e:
        logging.error(f"Fehler beim Abrufen des Autors: {e}")
        abort(500)
    finally:
        session.close()

# POST: Neuen Autor erstellen
@app.route('/autor', methods=['POST'])
def create_autor():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, "Fehlende Parameter: Name erforderlich")

    session = Session()
    try:
        autor = Autor(name=data['name'])
        session.add(autor)
        session.commit()
        return jsonify({"id": autor.id, "name": autor.name}), 201
    except Exception as e:
        session.rollback()
        logging.error(f"Fehler beim Erstellen des Autors: {e}")
        abort(500)
    finally:
        session.close()

# PUT: Autor aktualisieren
@app.route('/autor/<int:id>', methods=['PUT'])
def update_autor(id):
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, "Fehlende Parameter: Name erforderlich")

    session = Session()
    try:
        autor = session.query(Autor).filter_by(id=id).first()
        if autor is None:
            abort(404)

        autor.name = data['name']
        session.commit()
        return jsonify({"id": autor.id, "name": autor.name})
    except Exception as e:
        session.rollback()
        logging.error(f"Fehler beim Aktualisieren des Autors: {e}")
        abort(500)
    finally:
        session.close()

# DELETE: Autor löschen
@app.route('/autor/<int:id>', methods=['DELETE'])
def delete_autor(id):
    session = Session()
    try:
        autor = session.query(Autor).filter_by(id=id).first()
        if autor is None:
            abort(404)
        session.delete(autor)
        session.commit()
        return '', 204
    except Exception as e:
        session.rollback()
        logging.error(f"Fehler beim Löschen des Autors: {e}")
        abort(500)
    finally:
        session.close()









# Fehlerbehandlung
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500






# Funktion zum Erstellen der Datenbank, falls sie nicht existiert -->Hier braucht man keine Transaktionen, weil wenn man nur eine Datenbank erstellt, die schon atomar ist.
def create_database_if_not_exists():
    try:
        with engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"))
            logging.info(f"Datenbank '{DATABASE_NAME}' existiert oder wurde erfolgreich erstellt.")
    except Exception as e:
        logging.error(f"Fehler beim Erstellen der Datenbank: {e}")

# Funktion zum Erstellen der Tabellen
def create_tables():
    try:
        Base.metadata.create_all(engine_with_db)  ## Erstellt alle Tabellen, überspringt jedoch bereits existierende Tabellen -->Deswegen ist auch keine Transaktionen für mich hier nötig.
        logging.info("Tabellen wurden erfolgreich erstellt!")
    except Exception as e:
        logging.error(f"Fehler beim Erstellen der Tabellen: {e}")

# Funktion zum Befüllen der Datenbank mit Beispieldaten
def fill_database():
    session = Session()
    try:
        # Verlage hinzufügen
        verlage = ["Verlag A", "Verlag B", "Verlag C", "Verlag D", "Verlag E"]
        for verlag_name in verlage:
            verlag = session.query(Verlag).filter_by(name=verlag_name).first()
            if not verlag:
                verlag = Verlag(name=verlag_name)
                session.add(verlag)

        # Autoren hinzufügen
        autoren = ["Autor A", "Autor B", "Autor C", "Autor D", "Autor E"]
        for autor_name in autoren:
            autor = session.query(Autor).filter_by(name=autor_name).first()
            if not autor:
                autor = Autor(name=autor_name)
                session.add(autor)

        # Bücher hinzufügen und mit Autoren und Verlagen verknüpfen
        buecher = [
            {"titel": "Buch A", "verlag_name": "Verlag A", "autoren": ["Autor A", "Autor B"]},
            {"titel": "Buch B", "verlag_name": "Verlag B", "autoren": ["Autor C", "Autor D"]},
            {"titel": "Buch C", "verlag_name": "Verlag C", "autoren": ["Autor A", "Autor E"]},
            {"titel": "Buch D", "verlag_name": "Verlag D", "autoren": ["Autor B", "Autor D"]},
            {"titel": "Buch E", "verlag_name": "Verlag E", "autoren": ["Autor C", "Autor E"]}
        ]
        
        for buch_info in buecher:
            verlag = session.query(Verlag).filter_by(name=buch_info["verlag_name"]).first()
            buch = session.query(Buch).filter_by(titel=buch_info["titel"]).first()
            if not buch:
                buch = Buch(titel=buch_info["titel"], verlag=verlag)
                # Autoren hinzufügen
                for autor_name in buch_info["autoren"]:
                    autor = session.query(Autor).filter_by(name=autor_name).first()
                    if autor:
                        buch.autoren.append(autor)
                session.add(buch)

        session.commit()
        logging.info("Datenbank erfolgreich befüllt!")
    except Exception as e:
        session.rollback()
        logging.error(f"Fehler beim Befüllen der Datenbank: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    create_database_if_not_exists()
    create_tables()
    fill_database()
    app.run(debug=True)
