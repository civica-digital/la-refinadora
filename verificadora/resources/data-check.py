#!/usr/bin/python

import argparse
import csv
import json
import logging
import re

"""
The following functions detect string characteristics in order to see if a given value matches any of the criteria of things to avoid in a csv.

:param input_string: String to work with
:return flag: Returns a 1 if a given criteria is matched by string.
"""

def detect_white_cells(input_string):
    flag = 0
    if input_string == "": flag = 1
    return flag

def detect_calculus(input_string):
    flag = 0
    calculus_characters = ["+","-","=","/"]
    for char in calculus_characters:
        if char in input_string: flag = 1
    return flag

def detect_non_standard(input_string):
    flag = 0
    regexp = re.compile('[^A-Za-z0-9-]')
    results = regexp.search(input_string)
    if results is not None: flag = 1
    return flag

def detect_file_path(input_string):
    flag = 0
    if "C:/" in input_string: flag = 1
    return flag

def detect_double_spaces(input_string):
    flag = 0
    if "  " in input_string: flag = 1
    return flag

def detect_trailing_leading_spaces(input_string):
    flag = 0
    if len(input_string)>0:
        if input_string[0] == " " or input_string[-1] == " ": 
            flag = 1
    return flag


def construct_response(function_flags):
    """
    Buids a dictionary in the form needed by the JSON of the validators category of the response

    :param function_flags: dictionary of validators and their status in a flag that is 1 if such (bad) criteria is found
    :return response_dict: returns a dictionary with the needed form.
    """

    response_dict = {}

    for key in function_flags:
        if function_flags[key][0]==1:
            status = "Fail"
            reason = "Error Found in row " + str(function_flags[key][1])
        else:
            status = "Pass"
            reason = "Error Not Found"
        response_dict[key] = {"status":status,"reason":reason}
 
    return response_dict

def per_value_function_dictionary():
    """
    Buids a dictionary for each string 

    :param function_flags: dictionary of validators and their status in a flag that is 1 if such (bad) criteria is found
    :return response_dict: returns a dictionary with the needed form.
    """
    per_value_functions = {
        "white cells": detect_white_cells, 
        "special characters": detect_non_standard, 
        "file path":detect_file_path, 
        "double spaces": detect_double_spaces, 
        "trailing and leading spaces":detect_trailing_leading_spaces,
        "calculus":detect_calculus
        }
    return per_value_functions


def data_validation(data):
    """
    Runs validations and builds a dictionary with the responses. This validations are made iteratively by rows (detect duplicate rows) and by values. The latter are done in a way in which if a validation was found to be positive in any value, it is not checked further in the file.

    :param data: list of lists built from the csv to work with.
    :return response_dict: Dictionary with status of the validations
    """
    found = set()

    #build dictionary of functions
    per_value_functions = per_value_function_dictionary()

    function_flags = {}

    #build function status dictionary
    for key in per_value_functions:
        function_flags[key] = [0,0]
    function_flags["duplicate rows"] = [0,0]

    row_dictionary = {}
    number_row_error = 1
    for row in data:

        #iterate each row and build a dictionary with the tuple built from the row. If a given row is found in such dictionary: The duplicate flag is risen.
        if tuple(row) not in found:
            row_dictionary[tuple(row)] = 1
        else:
            function_flags["duplicate rows"] = [1,number_row_error]
        for value in row:
            #Iterate each value and run the validations that have not been found as positive. 
            if len(per_value_functions) > 0:
                remove_function = []
                for function_string in per_value_functions:
                    flag = per_value_functions[function_string](value)
                    if flag == 1:
                        #If the current string was found to be positive to a validation, store the status and store it in a temporal list to remove it later (You can't change dictionaries while iterating them in python).
                        function_flags[function_string]=[1,number_row_error]
                        remove_function.append(function_string)
                
                #This is when the function is removed from dictionary so we don't further test such criteria
                if len(remove_function) is not None: 
                    for function in remove_function:
                        per_value_functions.pop(function, None)
        number_row_error = number_row_error + 1

        response_dict = construct_response(function_flags)

    return response_dict

def read_sample(dataset):
    try:
        with open(dataset, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
    except FileNotFoundError as e:
        logging.error(e)
    return data

def response_status(response_dict):
    status = "Pass"
    for response in response_dict:
        if response_dict[response]['status'] == "Fail": status = "Fail"
    return status

def return_validation(filepath):
    """
    Returns validation dictionary. Calls all validations of this set.

    :param filepath: Path of the data file to work with.
    :return output_dict: returns a response dictionary with a status key and a response key, with the validations made to the file.
    """
    sample = read_sample(filepath)
    
    #Aquí va la validación
    #date_response = date_validation(sample)
    data_response_dict = data_validation(sample)
    status = response_status(data_response_dict)
    output_dict = {"status":status,"validators":data_response_dict}
    return output_dict

def return_reqs():
    """
    Returns requirements, when this code is called with no arguments.

    :return : returns a response dictionary with a status key and a response key, with requirements needed by the plugin.
    """
    status = "data-check"
    response = {"unit":"file"}
    output_dict = {"status":status, "response":response}
    return output_dict

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset')
    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO)
    args = get_args()
    dataset = args.dataset
    if dataset is None:
        output_dict = return_reqs()
    else:
        output_dict = return_validation(dataset)
    print(json.dumps(output_dict))


if __name__ == "__main__":
    main()

