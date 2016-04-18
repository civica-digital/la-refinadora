#!/usr/bin/env python3
import argparse
import csv
import json
import re
import sys
from statistics import mode
from random import random

def is_rectangular(filepath):
    """ 
    Validates that the CSV file has a rectangular structure.
    """
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        header_columns = len(headers)
        next(reader)

        response = {}

        for row_number, row in enumerate(reader, start=1):
            data_columns = len(row)

            if header_columns > data_columns:
                status = "Fail"
                reason = "File has more header columns than data columns. {row_number}.".format(row_number=row_number)
                response = { "status": status, "reason": reason }
                return response
            elif header_columns < data_columns:
                status = "Fail"
                reason = "File has more data columns than header columns. {row_number}.".format(row_number=row_number)
                response = { "status": status, "reason": reason }
                return response
            else:
                status = "Pass"
                reason = "CSV file has a rectangular structure."
                response = { "status": status, "reason": reason }
    return response

def complete_cols(filepath):
    """ 
    Validates from a representative sample size that data columns are complete.
    """
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        header_columns = len(headers)
        next(reader)
        row_count = sum(1 for row in reader)

    response = {}
    
    if row_count < 1000 and row_count > 1:
        sample_size = row_count
    elif row_count > 1000:
        # Determines the sample size based on Slovin's formula at a 97% confidence level
        confidence_level = 97.0
        error = 1.0-(confidence_level/100)
        slovin = row_count/(1.0 + (row_count*(error**2)))
        sample_size = round(slovin)
    else:
        logging.error("You must provide at least one data column.")
        return 0
    
    # Reservoir Sampling
    sample_cols = []
    chances = sample_size/row_count
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row_number, row in enumerate(reader, start=1):
            if random() < chances:
                columns = len(row)
                sample_cols.append(columns)

    if mode(sample_cols) == header_columns:
        status = "Pass"
        reason = "Columns are complete."
        response = { "status": status, "reason": reason }
    else:
        status = "Fail"
        reason = "Columns are not complete."
        response = { "status": status, "reason": reason }

    return response

def has_alphanumeric_headers(filepath):
    """ 
    Validates that the header names contains only letters, numbers, dashes, and underscores.
    """
    regexp = re.compile('[^A-Za-z0-9-]')
    response = {}
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for column_number, column_name in enumerate(headers, start=1):
            if regexp.search(column_name):
                status = "Fail"
                reason = """Column name {column_name} in column {column_number} has an invalid name. Please use only letters, numbers, and dashes.""".format(column_name=column_name, column_number=column_number)
                response = { "status": status, "reason": reason }
                return response 
            else:
                status = "Pass"
                reason = "Headers have valid names."
                response = { "status": status, "reason": reason }
    return response

def response_status(response_dict):
    status = "Pass"
    for response in response_dict.keys():
        if response_dict[response]['status'] == "Fail": status = "Fail"
    return status

def run_validations(filepath):
    """
    Returns validation dictionary. Calls all validations of this set.

    :param filepath: Path of the data file to work with.
    :return output_dict: returns a response dictionary with a status key and a response key, with the validations made to the file.
    """
    responses = {}
    validation_results = {}
    
    alphanumeric_reponse = has_alphanumeric_headers(filepath)
    try:
        complete_cols_response = complete_cols(filepath)
    except StopIteration:
        complete_cols_response = {'status': 'failed'}

    rectangularity_reponse = is_rectangular(filepath)

    responses['Valid headers names'] = alphanumeric_reponse
    responses['Complete columns'] = complete_cols_response
    responses['Dataset rectangularity'] = rectangularity_reponse

    validators = { "Column checker": responses }
    status = response_status(responses)
    validation_results = { "status": status, "validators": validators }

    return validation_results

def return_reqs():
    """
    Returns requirements, when this code is called with no arguments.

    :return : returns a response dictionary with a status key and a response key, with requirements needed by the plugin.
    """
    status = "Column checker"
    response = {}
    output_dict = { "status": status, "response": response }
    return output_dict

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset')
    return parser.parse_args()

def main():
    args = get_args()
    dataset = args.dataset

    if dataset is None:
        requirements = return_reqs()
        print(json.dumps(requirements))
    else:
        validation_results = run_validations(dataset)
        print(json.dumps(validation_results))

if __name__ == '__main__':
    main()
