# -*- coding: utf-8 -*-

from os import getcwd
import argparse
import logging
import subprocess
import random
import sys

from tools import *
from filtercsv import *

__author__ = "Codeando México"
__credits__ = "Ricardo Alanís, Miguel Salazar, Miguel Ángel Gordián"
__license__ = "GPL"
__version__ = "0.05"
__status__ = "Prototype"

CONFIGFILE = ".validadora"
RESOURCES_DIR = "resources"
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
    with open(filename, 'rb') as fp:
        for line in fp:
            count = count + 1
            if count > 1: valor = 1
    return valor

def csv_validation(filename):
    extension = extract_extension(filename)
    if extension == "csv": 
        status = "Pass"
        reason = "CSV extension was detected"
    else:
        status = "Fail"
        reason = extension   
    response = {"status":status,"reason":reason}
    return response

def morethan1line_validation(filename):
    test_result = verify_morethan11ine(filename)
    if test_result == 1 : 
        status = "Pass"
        reason = "The given File has more than one line"
    else:
        status = "Fail"
        reason = "The given file does not have enough content, double check that it has at least one row of values"
    response = {"status":status,"reason":reason}
    return response

def base_validation(filename):
    """
    Performs a base validation of a dataset. Specifically:
    * CSV extention
    * File has more than one line

    :param filename: Dataset filename.
    :return output_dict: A dictionary with the response codes.
    """
    csv_response = csv_validation(filename)
    morethan1line_response = morethan1line_validation(filename)
    response_dict = {"csv": csv_response, "morethan1line":morethan1line_response}
    status = response_status(response_dict)
    output_dict = {"status":status,"validators":response_dict}
    return output_dict

def load_resources(resources_filename):
    data = load_json(resources_filename)
    return data['resources']


def call_local_resource(resource, filename=None):
    resource_path = RESOURCES_DIR + "/" + resource
    command = get_launcher(resource)
    
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

def run_validators(resource_list, dataset):
    status = "Pass"
    response_dict = {}
    for resource in resource_list:
        response_dict[resource]= call_resource(resource, dataset)
        if response_status(response_dict) != "Pass": status = "Fail"
    return_dict = {"status":status,"detail":response_dict}
    logging.info("Response %s",return_dict)
    return return_dict

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset')
    parser.add_argument('--resources')
    return parser.parse_args()

def get_launcher(plugin):
    executable = os.path.basename(plugin)
    extension = executable.split('.')[-1]

    compilers = load_json(COMPILER_FILE)
    if extension in compilers:
        command = compilers[extension]
    
    return command

def main():
    logging.basicConfig(level=logging.INFO)
    global config
    config = configparser.ConfigParser()
    config.read(CONFIGFILE)
    args = get_args()
    dataset = args.dataset
    resources = args.resources

    compiler_dictionary = load_json(COMPILER_FILE)
    # Base validation should be a validator on its own.
    base_response_dict = base_validation(dataset)

    base_status = base_response_dict['status']
    if base_status == "Fail": 
        logging.info("Error: ", base_response_dict)
        sys.exit()

    # Resources must be loaded from the resources directory, not from a json.
    resource_list = load_resources(resources)
    response_dict = run_validators(resource_list, dataset)
    logging.info("Response: %s", response_dict)

if __name__ == "__main__":
    main()