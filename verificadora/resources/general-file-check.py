#!/usr/bin/python
import cchardet
import csv
import argparse
import json
import logging

def detect_separator(data):
    """
    Detector: Detects the separator used by the data

    :param data: data to work with.
    :return dialect.delimiter: returns delimiter found in the data
    """
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(data.decode("UTF-8"))
    return dialect.delimiter

def utf8_validation(data):
    """
    Validator: Detects if the data is in utf-8 format

    :param data: data to work with.
    :return response: returns a response dictionary for the utf-8 validation, with a status key and a response key.
    """
    try:
        encoding = cchardet.detect(data)['encoding']
    except:
        enconding= "No UTF-8"
    
    if encoding != "UTF-8": 
        status = "Fail"
        reason = "Could not detect file encoding, please double-check if it is saved as UTF-8."
    else:
        status= "Pass"
        reason = "UTF-8 encoding detected"
    response = {"status":status,"reason":reason}
    return response

def separator_validation(data):
    """
    Validator: Detects if the data has coma as separator

    :param data: data to work with.
    :return response: returns a response dictionary for the coma, with a status key and a response key.
    """
    try:
        separator = detect_separator(data)
    except:
        separator = "No ,"
    if separator == ",":
        status = "Pass"
        reason = "Coma"
    elif separator ==";":
        status = "Pass"
        reason="Valid CSV Separator, coma is the common default separator."
    else:
        status= "Fail"
        reason = "Invalid separator detected"
    response = {"status":status,"reason":reason}
    return response

def read_sample(filepath):
    try:
        with open (filepath, "rb") as myfile:
            data=myfile.read()
    except FileNotFoundError as e:
        logging.error(e)
    return data

def response_status(response_dict):
    status = "Pass"
    for response in response_dict.keys():
        if response_dict[response]['status'] == "Fail": status = "Fail"
    return status

def return_validation(filepath):
    """
    Returns validation dictionary. Calls all validations of this set.

    :param filepath: Path of the data file to work with.
    :return output_dict: returns a response dictionary with a status key and a response key, with the validations made to the file.
    """
    sample = read_sample(filepath)
    utf8_response = utf8_validation(sample)
    separator_response = separator_validation(sample)
    response_dict = {"utf-8": utf8_response, "separator":separator_response}
    status = response_status(response_dict)
    output_dict = {"status":status,"validators":response_dict}
    return output_dict

def return_reqs():
    """
    Returns requirements, when this code is called with no arguments.

    :return : returns a response dictionary with a status key and a response key, with requirements needed by the plugin.
    """
    status = "general-file-check"
    response = {"unit":"row","number":"5","sampling":"random","raw":"true"}
    output_dict = {"status":status, "response":response}
    return output_dict

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset')
    return parser.parse_args()

def main():
    args = get_args()
    dataset = args.dataset
    if dataset is None:
        output_dict = return_reqs()
    else:
        output_dict = return_validation(dataset)
    print(json.dumps(output_dict))


if __name__ == "__main__":
    main()
