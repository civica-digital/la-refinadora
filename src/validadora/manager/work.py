# -*- coding: utf-8 -*-

from .recolector import write_to

class Work:
    """
    Work is the processing unit of the SRC

    - [ ] Every work mantains a status, these can be:
        * ready
        * active
        * stopped

    - [ ] Work updates it's own status:
        OBSERVATION:
             - consulting it's status in the container.
             - reflects it's status in the DB.

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