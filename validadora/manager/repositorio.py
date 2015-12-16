# -*- coding: utf-8 -*-

___name__ = "manager"

from docker import Client

from .utils import is_validador_schema, repo_origin
from .validador import Validador


_url_default = "unix:///var/run/docker.sock"

_c = Client(_url_default)


class Repositorio:
    """EL repositorio es el concentrador de manager;

    - [ ] Puedo verificar si un validador se encuentra en el repositorio.
    - [ ] Puedo consultar la información requerida por un validador tomando como parametro su nombre.
    - [ ] Puedo obtener un validador basado en su nombre.

    """
    def __init__(self, docker_client=_c, name="validadora"):
        self.client = docker_client
        self.name = name


    def list_validadores(self):
        validadores = [ Validador(image, repo=self) for image in self.client.images()
                 if is_validador_schema(schema=image)
                 and repo_origin(self.name, image["RepoTags"])]

        return validadores


    def get_validador(self, validador_name):
        for validador in self.list_validadores():
            if validador_name in validador.name or validador_name is validador:
                validador.repo = self
                return validador

        return None


if __name__ == '__main__':
    from docker import Client
    c = Client("unix:///var/run/docker.sock")
    rep = Repositorio(c)
    for val in rep.list_validadores():
        print(val.name)
