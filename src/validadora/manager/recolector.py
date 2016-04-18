# -*- coding: utf-8 -*-

import requests

def fetch_data(source, params={"stream": True}):
    """
    Permite obtener los recursos que tomara un validador.

    TODO: [ ] añadir soporte para ssl
    """
    return requests.get(source, **params)

def write_to(path, resource):
    with open(path, "w") as f:
        f.write(fetch_data(resource).content.decode("utf-8"))


if __name__ == "__main__":
    dataset = "http://datos.labcd.mx/dataset/3968a764-f85a-4b7c-903b-bd3e3e23fd78/resource/1f2b8d6b-c93a-4f63-b6c3-90293a91726b/download/embajadas.csv"
    destino = "/tmp/tmp.csv"
    ciclovias = fetch_data(dataset)


    with open(destino, "w") as f:
        count = 0
        for content in ciclovias.iter_lines():
            count += 1
            f.write(content)
            if count >= 40: break

    import os

    if os.path.exists(destino) and os.path.isfile(destino):
        print("Datos transferidos")
        for k, v in ciclovias.headers.items():
            print("{0}: {1}".format(k, v))