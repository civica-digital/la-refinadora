# -*- coding: utf-8 -*-

from .recolector import write_to

class Work:
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
    def __init__(self, _id, container, validador, fuente):
        self.id =_id
        self.container = container
        self.validador = validador
        self.fuente = fuente


    def run(self):
        write_to('/datasets/{}.csv'.format(self.id), self.fuente)
        response = self.validador.client.start(self.container.get('Id'))
        return response


    def update_status(self, work, validador, fuente):
        pass