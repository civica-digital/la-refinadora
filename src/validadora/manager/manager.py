# -*- coding: utf-8 -*-

from docker import Client
from pymongo import MongoClient
from datetime import datetime
from threading import Thread
from queue import Queue

from .repositorio import Repositorio
from .utils import make_id, update_status

import time
import json
import os

class Manager:

    def __init__(self, repositorio=None):
        if not repositorio:
            self.client = Client("unix:///var/run/docker.sock")
            repositorio = Repositorio(self.client)

        self.repo = repositorio

        self.queue = Queue()
        self.db = MongoClient(os.environ['MONGO_PORT_27017_TCP_ADDR'], int(os.environ["MONGO_PORT_27017_TCP_PORT"]))

        self.w = Thread(target=self.control)
        self.w.daemon = True
        self.w.start()

        self.m = Thread(target=self.monitor)
        self.m.daemon = True
        self.m.start()


    def control(self):
        while True:
            db = self.db.validadora
            collection = db.works
            (work_id, validador, fuente) = self.queue.get()
            validador.client = self.client
            work = validador.run(work_id, fuente)
            print(dir(collection))
            collection.insert({
                'work_id': work_id,
                'fuente': fuente,
                'validador': validador.name,
                'container': work.container.get('Id'),
                'date': datetime.utcnow(),
                'status': 'UP',
                'result': ""
            })


    def monitor(self):
        while True:
            works = self.db.validadora.works
            for work in works.find():
                update = update_status(self.client, work)
                if update != {}:
                    self.db.validadora.works.find_one_and_update({'_id': work["_id"]}, update)
            time.sleep(10)


    def new_work(self, validador, dataset):
        validador = self.repo.get_validador(validador)
        work_id = make_id()
        self.queue.put([work_id, validador, dataset])
        return {"id_work":work_id}


    def dcat_work(self, dcat):
        pass


    def report_work(self, work):
        work = self.db.validadora.works.find_one({'work_id': work})
        if work['status'] == 'Up':
            return "Aún procesando"
        else:
            result = work['results'].decode("utf-8")
            print(result)
            try:
                res = json.loads(result)
            except:
                res = {'error': 'validador', 'msg': result}

            return res # TODO: Mejorar el manejo de error de los validadores

if __name__ == "__main__":
    m = Manager()
    dataset = "http://datos.labcd.mx/dataset/3968a764-f85a-4b7c-903b-bd3e3e23fd78/resource/1f2b8d6b-c93a-4f63-b6c3-90293a91726b/download/embajadas.csv"

    m.new_work("src/iso8601:latest", dataset)
    import time
    while True:
        time.sleep(10)
