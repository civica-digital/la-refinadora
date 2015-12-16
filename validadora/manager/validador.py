from .utils import is_validador_schema, repo_origin
from .work import Work

import docker

class ValidadorSchemaInvalid(Exception):
    def __init__(self, msg):
        self.message = msg


class Validador:
    """
    Los manager deben de incluir su propio id y no pasarlo como parametro.
    """
    def __init__(self, schema, repo=None):
        """
        Los manager son construidos por el Repositorio.

        El parametro schema es la misma sintaxis que una imagen de docker.
        """

        self.repo = repo
        if is_validador_schema(schema):
            self.schema = schema.copy()
        else:
            output = detect_errors(schema)
            raise ValidadorSchemaInvalid("La estructura o los valores no son correctos " + str(output))


    def run(self, _id, fuente):
        container = {
            'image':  self.name,
            'name': _id,
            'command': '/datasets/{}.csv'.format(_id),
            'host_config': docker.utils.create_host_config(binds=[
              '/tmp/{}.csv:/datasets/{}.csv'.format(_id,_id), # TODO: Detect format
            ])
        }
        container = self.client.create_container(**container)
        work = Work(_id, container, self, fuente)
        work.run()
        return work

    @property
    def name(self):
        return repo_origin(self.repo.name, self.schema["RepoTags"])


if __name__ == "__main__":
    from docker import Client
    c = Client("unix:///var/run/docker.sock")
    esquema = {'Created': 1441279808,
               'Labels': {},
               'VirtualSize': 795865269,
               'ParentId': '9cce8d0ab3ceadd880b97330a259d362e51e303089fc096db5094f2642585bee',
               'RepoTags': ['iso8601:latest', 'src/iso8601:latest'],
               'RepoDigests': [],
               'Id': '15ef989c576bdc0ae8ed721f9c58a850ee050620ed8e9d816dacaffdb050e497',
               'Size': 0
               }

    from utils import make_id
    class tmp:
        pass
    val = Validador(esquema)
    val.client = c
    val.repo =tmp()
    val.repo.name = "src"
    dataset = "http://datos.labcd.mx/dataset/3968a764-f85a-4b7c-903b-bd3e3e23fd78/resource/1f2b8d6b-c93a-4f63-b6c3-90293a91726b/download/embajadas.csv"
    val.run(make_id(), dataset)