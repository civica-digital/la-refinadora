from validadora.manager.recolector import write_to
from validadora.proxy import  Proxy as proxy

db = proxy.db

class Work(db.Document):
    """
    Un work es la unidad de procesamiento en la src

    - [ ] Cada work mantiene un estado, pudiendo ser:
        * ready
        * active
        * stopped

    - [ ] El work se encarga de actualizar su estado.
        OBSERVATION:
             - consultado su estado del contenedor
             - refleja sus estado en la base de datos.

    """
    wid = db.StringField(max_length=100)
    fuente = db.URLField(max_length=800, required=True)
    validador = db.StringField(max_length=200, required=True)
    date = db.DateTimeField()
    status = db.StringField(required=True)
    results = db.StringField()
    container = db.StringField()
    callback = db.URLField()
    type = db.DictField()
    childrens = db.ListField()