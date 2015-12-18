# -*- coding: utf-8 -*-

from .recolector import write_to
from validadora.proxy import Proxy as proxy
import docker

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
    def __init__(self, work):
        self.work = work


    def run(self):
        validator = proxy.repo.get_validador(self.work.validador)
        print("validador {}".format(validator))
        container_config = {
            'image':  self.work.validador,
            'name': self.work.wid,
            'command': '/datasets/{}.csv'.format(self.work.wid),
            'host_config': docker.utils.create_host_config(binds=[
              '/tmp/{}.csv:/datasets/{}.csv'.format(self.work.wid, self.work.wid), # TODO: Detect format
            ])
        }

        container = validator.client.create_container(**container_config)
        self.work.container = container.get('Id')

        self.work.status='UP'

        self.work.save()


        write_to('/datasets/{}.csv'.format(self.work.wid), self.work.fuente)


        response = validator.client.start(self.work.container)
        return response


    def update_status(self, work, validador, fuente):
        pass