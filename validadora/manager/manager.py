# -*- coding: utf-8 -*-

from docker import Client
from datetime import datetime
from threading import Thread
from queue import Queue

from .repositorio import Repositorio
from .utils import make_id, update_status, notify_work, notify_dcat, get_datasets_from_dcat
from .work import  Work as Worker
from validadora.models.work import Work
import json, os, time


from validadora.proxy import Proxy as proxy

class Manager:

    def __init__(self, repositorio=None):
        self.works = {}

        if not repositorio:
            self.client = Client("unix:///var/run/docker.sock")
            repositorio = Repositorio(self.client)

        self.repo = proxy.repo = repositorio

        self.queue = Queue()

        self.w = Thread(target=self.control)
        self.w.daemon = True
        self.w.start()

        self.m = Thread(target=self.monitor)
        self.m.daemon = True
        self.m.start()


    def control(self):
        while True:
            work = self.queue.get()
            worker = Worker(work)
            worker.run() # call container


    def monitor(self):
        while True:

            for work in Work.objects(status__in=["Waiting", "Created","Up", "Down"]):
                print("actualizado works {} ".format(work.wid))
                if work.type and work.type["dcat"] == "owner":
                    try:
                        if work.type["counter"] == 0:
                            try:
                              notify_dcat(work.callback, work.wid)
                            except:
                                pass

                            work.status = "Finished"
                            work.save()
                        else:
                            next
                    except:
                        pass

                if work.status == 'Down':
                    if work.callback:
                        try:
                            notify_work(work.callback, work.results)
                        except:
                            next
                    if work.type and work.type["dcat"]=='member':
                        parent = Work.objects(wid=work.type["owner"]).first()
                        try:
                            parent.type["counter"] -= 1
                        except:
                            pass

                        parent.save()
                    work.status = "Finished"
                    work.save()
                else:
                    if work.container:
                        update = update_status(self.client, work)



            time.sleep(10)


    def new_work(self, validadors, dataset, callback=False, owner=False):
        work_id = make_id()
        for validador in validadors:
            w = Work(wid=work_id, validador=validador, fuente=dataset, date=datetime.utcnow(), status="Waiting")

            if callback:
                w.callback = callback

            if owner:
                w.type["dcat"] = 'member'
                w.type["owner"] = owner

            w.save()
            self.queue.put(w)


        return work_id


    def dcat_work(self, validadors, dataset, callback=False):
        childrens = []
        work_id = make_id()

        w = Work(wid=work_id, validador=str(validadors), fuente=dataset, date=datetime.now(), status="Up",
                 type={
                     "dcat": "owner",
                 })

        if callback:
            w.callback = callback

        datasets = get_datasets_from_dcat(dataset)
        if not datasets:
            return None

        for dataset in datasets:
            id = self.new_work(validadors, dataset, owner=work_id)
            childrens = [id] + childrens

        w.childrens = childrens
        w.type["counter"] = len(childrens)
        w.save()

        return work_id



    def report_work(self, work):
        work = Work.objects(wid=work).first()
        print(work.results)
        if work.status == 'Waiting':
            return "En cola de trabajo"
        elif work.status == 'Up':
            return "Aún procesando"
        else:
            result = work.results
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
