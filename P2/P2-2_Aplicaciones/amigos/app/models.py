from app import db

class Amigo(db.Model):
    """
    Definición de la tabla 'amigos' de la base de datos
    """

    __tablename__ = "amigos"

    # Lo siguiente define las columnas de la base de datos y sus tipos
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    longi = db.Column(db.String(32))
    lati = db.Column(db.String(32))
    device = db.Column(db.String(255))

    # Podemos escribir la función siguiente para implementar cómo debe
    # mostrarse un objeto de esta clase si lo imprimes desde python
    def __repr__(self):
        return "<Amigo[{}]: {}>".format(self.id, self.name)
    
def get_all_devices():
    """
    Retorna una lista de strings con todos los tokens de dispositivo 
    que no sean nulos ni vacíos.
    """
    # Consultamos solo la columna 'device' filtrando nulos y vacíos
    query = db.session.query(Amigo.device).filter(Amigo.device != None, Amigo.device != "")
    
    # query.all() devuelve una lista de tuplas [('token1',), ('token2',)], 
    # así que usamos una list comprehension para extraer los strings.
    tokens = [row[0] for row in query.all()]
    return tokens