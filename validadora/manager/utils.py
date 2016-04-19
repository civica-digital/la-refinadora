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
    Verifies if the validator schema has the identifier fields for a validator. 
    """
    for element in _schema:
        if element not in schema:
            return False
    return True


def make_id():
    """
    Builds a 32 character ID to identify a work or workgroup.
    """
    random.seed(datetime.now())
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    length = len(alphabet) - 1
    return ''.join([alphabet[random.randint(0, length)] for i in range(1,32)])


def update_status(repo, work):
    """
    Updates the container scheme comparing the existent state in the database with the container.

    - If the container and the scheme in the DB have an active `status` it updates `results` in the container.
    - If the container finalized, but not the scheme in the DB, update `status` and results` in the DB.
    - If the container and scheme of the DB have finalized status apply no action.
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
    Return the status of the container.
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