#!/usr/bin/env python3
import csv
import json
import logging
import re
import sys
from statistics import mode
from random import random

def is_rectangular(data):
    """ 
    Validates that the CSV file has a rectangular structure.
    """
    with open(data, 'r') as f:
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

def complete_cols(data):
    """ 
    Validates from a representative sample size that data columns are complete.
    """
    with open(data, 'r') as f:
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
    with open(data, 'r') as f:
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

def has_alphanumeric_headers(data):
    """ 
    Validates that the header names contains only letters, numbers, dashes, and underscores.
    """
    regexp = re.compile('[^A-Za-z0-9-]')
    response = {}
    with open(data, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for column_number, column_name in enumerate(headers, start=1):
            print(regexp.search(column_name))
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

def main():
    logging.basicConfig(level=logging.INFO)
    data = '../tramites_lerma.csv'
    
    headers_response = has_headers(data)
    rectangularity_reponse = is_rectangular(data)
    complete_cols_response = complete_cols(data)
    alphanumeric_reponse = has_alphanumeric_headers(data)
    print(alphanumeric_reponse)
    
    #if len(sys.argv) == 1:
    #    output_dict = return_reqs()
    #else:
        #print sys.argv[1]
    #    output_dict = return_validation(sys.argv[1])
    #print(json.dumps(output_dict))

if __name__ == '__main__':
    main()