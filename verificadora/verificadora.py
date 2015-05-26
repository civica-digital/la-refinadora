from os import getcwd
import subprocess
import random
import sys

from tools import *
from filtercsv import *

FILE = sys.argv[1]
RESOURCES_FILE = sys.argv[2]
RESOURCES_DIR="resources"
COMPILER_FILE = "compilers.json"

CURRENT_DIRECTORY = getcwd()
RESOURCES_FULLPATH = CURRENT_DIRECTORY + "/" + RESOURCES_DIR
TEMP_FULLPATH = CURRENT_DIRECTORY + "/" + TMP_DIR

def response_status(response_dict):
    status = "Pass"
    for response in response_dict.keys():
        if response_dict[response]['status'] == "Fail": status = "Fail"
    return status

def verify_morethan11ine(filename):
    count = 0
    valor = 0
    with open(filename) as fp:
        for line in fp:
            count = count + 1
            if count > 1: valor = 1
    return valor

def csv_validation(filename):
    extension = extract_extension(filename)
    if extension == "csv": 
        status = "Pass"
        reason = "Se detectó la codificación csv"
    else:
        status = "Fail"
        reason = extension   
    response = {"status":status,"reason":reason}
    return response

def morethan1line_validation(filename):
    test_result = verify_morethan11ine(filename)
    if test_result == 1 : 
        status = "Pass"
        reason = "El archivo cuenta con más de una fila"
    else:
        status = "Fail"
        reason = "El archivo no cuenta con contenido suficiente, verificar que al menos tenga una fila de valores"
    response = {"status":status,"reason":reason}
    return response

def base_validation(filename):
    csv_response = csv_validation(filename)
    morethan1line_response = morethan1line_validation(filename)
    response_dict = {"csv": csv_response, "morethan1line":morethan1line_response}
    status = response_status(response_dict)
    output_dict = {"status":status,"validators":response_dict}
    return output_dict

def load_resources(resources_filename):
    data = load_json(resources_filename)
    return data['resources']


def call_local_resource(resource,filename = None):
    resource_path = RESOURCES_DIR + "/" + resource
    compiler_dictionary = load_json(COMPILER_FILE)
    compiler = detect_compiler(resource,compiler_dictionary)
    if filename is None: 
        output = subprocess.check_output([compiler,resource_path])
    else:
        output = subprocess.check_output([compiler,resource_path,filename])
    output_dict = json.loads(output.decode("utf-8"))
    return output_dict

def get_requirements(resource,id_api):
    if id_api == 1: return None
    requirements = call_local_resource(resource)
    return requirements


def get_resource_results(resource,filename, id_api):
    if id_api == 1: return None
    response = call_local_resource(resource,filename)
    return response

def call_resource(resource,filename):
    id_api = detect_api(resource)
    resource_requirements = get_requirements(resource,id_api)
    filtered_csv = prepare_csv(resource_requirements,filename,resource)
    resource_return = get_resource_results(resource,filtered_csv,id_api)
    return resource_return

def run_validators(resource_list):
    status = "Pass"
    response_dict = {}
    for resource in resource_list:
        response_dict[resource]= call_resource(resource,FILE)
        if response_status(response_dict) != "Pass": status = "Fail"
    return_dict = {"status":status,"detail":response_dict}
    return return_dict

def main():
    compiler_dictionary = load_json(COMPILER_FILE)

    base_response_dict = base_validation(FILE)
    base_status = base_response_dict['status']
    if base_status == "Fail": 
        print(base_response_dict)
        sys.exit() 
    resource_list = load_resources(RESOURCES_FILE)
    response_dict = run_validators(resource_list)
    print(response_dict)

if __name__ == "__main__":
    main()