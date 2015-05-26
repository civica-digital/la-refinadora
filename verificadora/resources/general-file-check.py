#!/usr/bin/python

import sys
import json
import csv
import cchardet


def detect_separator(data):
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(data.decode("UTF-8"))
    return dialect.delimiter

def utf8_validation(data):
    try:
        encoding = cchardet.detect(data)['encoding']
    except:
        enconding= "No UTF-8"
    
    if encoding != "UTF-8": 
        status = "Fail"
        reason = "No se detectó la codificación del Archivo, Verifica que esté guardado como UTF-8"
    else:
        status= "Pass"
        reason = "Se detectó la codificación UTF-8"
    response = {"status":status,"reason":reason}
    return response

def separator_validation(data):
    try:
        separator = detect_separator(data)
    except:
        separator = "No ,"
    if separator == ",":
        status = "Pass"
        reason = "Coma"
    elif separator ==";":
        status = "Pass"
        reason="Separador Válido, se prefiere el uso de coma"
    else:
        status= "Fail"
        reason = "Separador Inválido detectado"
    response = {"status":status,"reason":reason}
    return response

def read_sample(filepath):
    with open (filepath, "rb") as myfile:
        data=myfile.read()
    return data

def response_status(response_dict):
    status = "Pass"
    for response in response_dict.keys():
        if response_dict[response]['status'] == "Fail": status = "Fail"
    return status

def return_validation(filepath):
    sample = read_sample(filepath)
    utf8_response = utf8_validation(sample)
    separator_response = separator_validation(sample)
    response_dict = {"utf-8": utf8_response, "separator":separator_response}
    status = response_status(response_dict)
    output_dict = {"status":status,"validators":response_dict}
    return output_dict

def return_reqs():
    status = "general-file-check"
    response = {"unit":"row","number":"5","sampling":"random","raw":"true"}
    output_dict = {"status":status, "response":response}
    return output_dict


if len(sys.argv) == 1:
    output_dict = return_reqs()
else:
    #print sys.argv[1]
    output_dict = return_validation(sys.argv[1])
print(json.dumps(output_dict))