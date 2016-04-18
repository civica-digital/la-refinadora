#!/usr/bin/python

import argparse
import csv
import iso8601
import json
import logging

def stringify_columns(column_list):
    """
    Detector: Detects if the given data has values in ISO 8601 format

    :param column_list: list of columns with valid date values.
    :return string: returns a string with the columns with valid ISO 8601 data
    """
    string = ""
    for number in column_list:
        if len(column_list)>1 and (column_list.index(number) == (len(column_list)-1)):
            string = string + " and " + str(number)
        elif column_list.index(number)==0:
            string = str(number)
        else:
            string = string + ", " + str(number)
    return string

def detect_columns_dates(data):
    """
    Detector: Detects if the given data has values in ISO 8601 format

    :param data: data to work with.
    :return dialect.delimiter: returns a string with the columns with valid ISO 8601 data
    """
    correct_values = 0
    values_read = 0
    correct_columns_list = []
    for row in data:
        for value in row:
            try:
                iso8601.parse_date(value)
                correct_values = correct_values + 1
                correct_column = (row.index(value) + 1)
                if correct_column not in correct_columns_list:
                    correct_columns_list.append(correct_column)
            except:
                values_read = values_read + 1
    correct_columns_string = stringify_columns(correct_columns_list)
    return correct_columns_string

def date_validation(data):
    """
    Validator: Detects if the data has dates in a ISO 8601 compatible format

    :param data: data to work with.
    :return response: returns a response dictionary for the date validation, with a status key and a response key.
    """
    column_with_valid_dates = detect_columns_dates(data)
    if column_with_valid_dates == "": 
        status = "Fail"
        reason = "No data with a valid ISO8601 format was found in the file. Verify that such format is being used in any date field"
    else:
        status= "Pass"
        reason = "Data with a valid ISO8601 format was found in columns " + column_with_valid_dates
    response = {"status":status,"reason":reason}
    return response

def read_sample(dataset):
    try:
        with open(dataset, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
    except FileNotFoundError as e:
        logging.error(e)
        raise e
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
    date_response = date_validation(sample)
    response_dict = {"ISO-8601": date_response}
    status = response_status(response_dict)
    output_dict = {"status":status,"validators":response_dict}
    return output_dict

def return_reqs():
    """
    Returns requirements, when this code is called with no arguments.

    :return : returns a response dictionary with a status key and a response key, with requirements needed by the plugin.
    """
    status = "ISO-8601"
    response = {"unit":"row","number":"20","sampling":"random","raw":"false"}
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

