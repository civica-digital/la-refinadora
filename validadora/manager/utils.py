# -*- coding: utf-8 -*-

from datetime import datetime
import random
import requests
import json

"""
{
    'Created': 1437178689,
    'Labels': {},
    'VirtualSize': 109460979,
    'ParentId': u'2ff62b1c4295e436ab9b7bbbc46b02fe20a4859798ff992d817ede9f6d23fdaf',
    'RepoTags': ['docker.io/redis:latest'],
    'RepoDigests': [],
    'Id': '0ff407d5a7d9ed36acdf3e75de8cc127afecc9af234d05486be2981cdc01a38c',
    'Size': 0
}
"""
_schema = [
    'Created',
    'Labels',
    'VirtualSize',
    'ParentId',
    'RepoTags',
    'RepoDigests',
    'Id',
    'Size'
]


def is_validador_schema(schema):
    """
    Verifica si el schema del validador tiene los campos que identifican a un validador.
    """
    for element in _schema:
        if element not in schema:
            return False
    return True


def make_id():
    """
    Crea un identificador de 32 caracteres para identificar un work or workgroup.
    """
    random.seed(datetime.now())
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    length = len(alphabet) - 1
    return ''.join([alphabet[random.randint(0, length)] for i in range(1,32)])


def update_status(repo, work):
    """
    Actualiza el esquema del contendor comparando el estado existente en la base de datos con el contenedor.

    - Si el contenedor y el esquema en la DB tienen un `estatus` activo, actualiza `results` del contenedor.
    - Si el contenedor ha finalizado, pero en el esquema de la DB, actualiza `status` y `results` de la DB.
    - SI el contenedor y esquema de la DB tienen estado como finalizado no se realiza ninguna accion.
    """
    if not work.container:
        return {}

    Id = work.container
    logs = repo.logs(Id).decode('UTF-8')
    print(logs)

    if status(repo, Id) != work.status or work.status == "Up":
        work.status = status(repo, Id)
        if not work.status is "Created":
            work.results = logs
        work.save()

        return work

    return {}


def status(repo, _id):
    """
    Devuelve el status del contenedor.
    """

    i = repo.inspect_container(_id)["State"]["Status"]
    if i == "running":
        return "Up"
    if i == "exited":
        return "Down"
    if i == "created":
        return "Created"
    return i


def repo_origin(origin, names):
    for name in names:
        if name.split('/')[0] == origin:
            return  name
    return False

def notify_work(url, res):
    requests.post(url, json=json.dumps(res))

def notify_dcat(url, id):
    pass

def get_datasets_from_dcat(dcat):
    data = requests.get(dcat)
    if data.status_code < 300:
        try:
            jdcat = json.loads(data.text)
        except:
            return []
        if 'dataset' in jdcat.keys():
            datasets = []
            for element in jdcat["dataset"]:
                for entry in element['distribution']:
                    print(entry.keys())
                    datasets.append(entry["downloadURL"])
            return datasets

    return []