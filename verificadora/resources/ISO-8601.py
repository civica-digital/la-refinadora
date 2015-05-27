#!/usr/bin/python

import sys
import json
import csv
import iso8601

def stringify_columns(column_list):
    string = ""
    for number in column_list:
        if len(column_list)>1 and (column_list.index(number) == len(column_list-1)):
            string = string + " and " + str(number)
        elif column_list.index(number)==0:
            string = str(number)
        else:
            string = string + ", " + str(number)
    return string

def detect_columns_dates(data):
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
    with open(dataset, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

def response_status(response_dict):
    status = "Pass"
    for response in response_dict.keys():
        if response_dict[response]['status'] == "Fail": status = "Fail"
    return status

def return_validation(filepath):
    sample = read_sample(filepath)
    date_response = date_validation(sample)
    response_dict = {"ISO-8601": date_response}
    status = response_status(response_dict)
    output_dict = {"status":status,"validators":response_dict}
    return output_dict

def return_reqs():
    status = "ISO-8601"
    response = {"unit":"row","number":"20","sampling":"random","raw":"false"}
    output_dict = {"status":status, "response":response}
    return output_dict


if len(sys.argv) == 1:
    output_dict = return_reqs()
else:
    #print sys.argv[1]
    output_dict = return_validation(sys.argv[1])
print(json.dumps(output_dict))