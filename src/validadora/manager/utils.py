# -*- coding: utf-8 -*-

from datetime import datetime
import random

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
    Id = work["container"]
    logs = repo.logs(Id)


    if status(repo, Id) != work["status"] or work["status"] == "UP":
        return { "$set": {
            "status": status(repo, Id),
            "results": logs
        }}

    return {}


def status(repo, _id):
    """
    Return the status of the container.
    """

    i = repo.inspect_container(_id)["State"]["Running"]
    if i:
        return "Up"
    else:
        return "Down"


def repo_origin(origin, names):
    for name in names:
        if name.split('/')[0] == origin:
            return  name
    return False