# -*- coding: utf-8 -*-

from os import getcwd
from os import path
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
config_dict = load_config(CONFIGFILE)

RESOURCES_DIR = config_dict["general"]["resources_dir"]
COMPILER_FILE = config_dict["general"]["compiler_file"]
TMP_DIR = config_dict["general"]["tmp_dir"]

#Pending Directory call using os.path.
CURRENT_DIRECTORY = getcwd()
RESOURCES_FULLPATH = CURRENT_DIRECTORY + "/" + RESOURCES_DIR
TEMP_FULLPATH = CURRENT_DIRECTORY + "/" + TMP_DIR

def response_status(response_dict):
    """
    Determines the status of the call to the resource, wether it failed or not
    
    :param response_dict: dictionary of the response gotten by the call to search
    :returns valor: returns the status variable as "Fail" if any of the "status" keys in the response dict is shown as so.
            returns "Pass" otherwise.
    """ 

    status = "Pass"
    for response in response_dict.keys():
        if response_dict[response]['status'] == "Fail": status = "Fail"
    return status

def verify_morethan11ine(filename):
    """
    Tool function that verifies if given file has more than 1 line
    
    :param filename: name of the file
    :return response: returns 1 if the file has more than 1 line, this is csv agnostic.
    """ 
    count = 0
    valor = 0
    try:
        with open(filename, 'rb') as fp:
            for line in fp:
                count = count + 1
                if count > 1: valor = 1
    except FileNotFoundError as e:
        logging.error(e)
    return valor

def csv_validation(filename):
    """
    Detects and returns wether or not the file veing analyzed is a .csv or not.
    
    :param filename: name of the file
    :return response: returns a dictionary with two keys: "status": "Pass" or "Failed"; "reason".
    """ 

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
    """
    Detects and returns wether or not the file veing analyzed has more than 1 line.
    
    :param filename: name of the file
    :return response: returns a dictionary with two keys: "status": "Pass" or "Failed"; "reason".
    """ 
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

def load_resources(config_dict):
    resources = config_dict["general"]["resources"]
    resources_list = resources.split(",")
    return resources_list

def resource_error(resource,code):
    """
    Helps build a dictionary when a error when calliing a resource arises

    :param resource: resource name in order to build error
    :param code: code of error in order to add a reason to the error
    :return return_dict: response dictionary when the call fails

    """

    return_dict = {"status":"Error","code":code}
    return return_dict


def call_local_resource(resource, filename=None):
    """
    Performs a call to a local plugin by running the required code

    :param resource: plugin filename.
    :param filename: dataset filename.
    :return output_dict: Dictionary with the response of the resource.
    """
    resource_path =  RESOURCES_DIR + "/" + resource
    command = get_launcher(resource)
    if filename is None: 
        output = subprocess.check_output([command,resource_path])
    else:
        output = subprocess.check_output([command,resource_path,"--dataset",filename])
    output_dict = json.loads(output.decode("utf-8"))
    return output_dict

def get_requirements(resource,id_api):
    """
    Performs the first call to the resource, in order to recieve the requirements.

    :param resource: resource filename.
    :param id_api: whether or not the resource is an api: 1 if it is.
    :return requirements: returns requirements of the resource in a response dictionary.
    """
    if id_api == 1: return None
    requirements = call_local_resource(resource)
    return requirements

def validate_response(resource,response):
    """
    Validates if the current response does have a "status" code.
    
    :param resource: resource filename.
    :param response: current response.
    :return response: response dictionary, which is changed to a error form if no "status" key found in dictionary
    """
    try:
        resp_status =response["status"]
    except:
        response = resource_error(resource,"Invalid JSON form of response")
    return response

def get_resource_results(resource,filename, id_api):
    """
    Performs the call to the resource, in order to recieve the verification results.

    :param resource: resource filename.
    :param filename: dataset filename.
    :param id_api: whether or not the resource is an api: 1 if it is.
    :return response: returns response dictionary
    """
    if id_api == 1: return None
    try:
        response = call_local_resource(resource,filename)
    except:
        response = resource_error(resource,"Error calling local resource")

    response = validate_response(resource,response)
    return response

def call_resource(resource,filename):
    """
    Recieves the resource and decides whether it is going to be called locally or is it an API, and procedes to call it

    :param resource: resource filename.
    :param filename: dataset filename.
    :return resource_return: dictionary of resource response
    """
    id_api = detect_api(resource)
    resource_requirements = get_requirements(resource,id_api)
    filtered_csv = prepare_csv(resource_requirements,filename,resource,TMP_DIR)
    resource_return = get_resource_results(resource,filtered_csv,id_api)
    return resource_return

def run_validators(resource_list, dataset):
    """
    Iterates over validators in order to recieve their validation results

    :param resource_list: resources filenames in a list.
    :param dataset: dataset filename.
    :return return_dict: dictionary of resources responses
    """
    status = "Pass"
    response_dict = {}
    for resource in resource_list:
        response_dict[resource]= call_resource(resource, dataset)
        if response_status(response_dict) != "Pass": status = "Fail"
    return_dict = {"status":status,"detail":response_dict}
    return return_dict

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset')
    return parser.parse_args()

def get_launcher(plugin):
    executable = path.basename(plugin)
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

    compiler_dictionary = load_json(COMPILER_FILE)
    # Base validation should be a validator on its own.
    base_response_dict = base_validation(dataset)

    base_status = base_response_dict['status']
    if base_status == "Fail": 
        logging.info("Error: ", base_response_dict)
        sys.exit()

    # Resources must be loaded from the resources directory, not from a json.
    resource_list = load_resources(config_dict)
    response_dict = run_validators(resource_list, dataset)
    logging.info("Response: %s", response_dict)

if __name__ == "__main__":
    main()