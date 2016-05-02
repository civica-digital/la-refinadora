from .utils import is_validador_schema, repo_origin

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


    @property
    def name(self):
        return repo_origin(self.repo.name, self.schema["RepoTags"])