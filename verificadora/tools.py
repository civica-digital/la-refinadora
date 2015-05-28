import json
from os import path

def load_json(filename):
    with open(filename) as data_file:    
        data = json.load(data_file)
    return data

def extract_extension(filename):
    """
    extracts file extension of given filename

    :param filename: Given file name.
    :return extension: dictionary of resources responses
    """
    extension = path.splitext(filename)[1][1:]
    return extension

def detect_api(resource):
    if resource[0:3] == "http": return "1"
    return "0"

def detect_compiler(resource,compiler_dictionary):
    """
    detects required compiler given the file extension

    :param resource: resource filename.
    :param compiler_dictionary: dictionary of {extensions:compiler}
    :return compiler: returns process name to call in order to run such resource
    """
    resource_extension = extract_extension(resource)
    compiler = compiler_dictionary[resource_extension]
    return compiler
