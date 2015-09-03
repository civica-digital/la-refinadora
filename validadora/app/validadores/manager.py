# -*- coding: utf-8 -*-

from docker import Client
from pymongo import MongoClient
from datetime import datetime
from threading import Thread
from Queue import Queue

from .repositorio import Repositorio
from .utils import make_id, update_status

import time

class Manager:

    def __init__(self, repositorio=None):
        if not repositorio:
            c = Client("unix:///var/run/docker.sock")
            repositorio = Repositorio(c)

        self.repo = repositorio

        self.queue = Queue()
        self.db = MongoClient('172.17.0.1', 27017)

        self.w = Thread(target=self.control)
        self.w.daemon = True
        self.w.start()

        self.m = Thread(target=self.monitor)
        self.m.daemon = True
        self.m.start()


    def control(self):
        while True:
            (work_id, validador, fuente) = self.queue.get()
            container = validador.run(fuente)
            self.db.works.insert_one({
                'work_id': work_id,
                'fuente': fuente,
                'validador': validador.name,
                'container': container,
                'date': datetime.utcnow(),
                'status': 'UP',
                'result': {}
            })


    def monitor(self):
        while True:
            for work in self.db.works.find():
                update = update_status(self.repo, work)
                self.db.works.find_one_and_replace({'_id': work["_id"]}, update)
            time.sleep(10)


    def new_work(self, validador, dataset):
        validador = self.repo.getValidador(validador)
        work_id = make_id()
        self.queue.put([work_id, validador, dataset])
        return work_id


    def dcat_work(self, dcat):
        pass


    def report_work(self, work):
        work = self.db.works.find_one({'work_id': work})
        if work['status'] == 'Up':
            return "Aún procesando"
        else:
            return work['result']