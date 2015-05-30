import json
from os import path
import configparser

def config_section_map(Config,section):
    """
    Extracts dictionary of the given keys

    :param section: Given section.
    :return dict1: dictionary of the given section
    """
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def load_config(config_file):
    """
    Loads the given config_file and builds a dictionary

    :param config_file: Given config file path.
    :return config_dict: dictionary of the config file.
    """
    Config = configparser.ConfigParser()
    Config.read(config_file)
    sections = Config.sections()
    config_dict = {}
    for section in sections:
        config_dict[section]=config_section_map(Config, section)
    return config_dict

def load_json(filename):
    with open(filename) as data_file:    
        data = json.load(data_file)
    return data

def extract_extension(filename):
    """
    Extracts file extension of given filename

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
