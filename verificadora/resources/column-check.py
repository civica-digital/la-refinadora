#!/usr/bin/env python3
import csv
import json
import re
import sys

def has_headers(data):
    """ 
    Validates that the CSV file has header columns.
    """
    with open(data, 'r') as f:
        has_header = csv.Sniffer().has_header(f.read(1024))
    reponse = {}
    if has_header:
        status = "Pass"
        reason = "CSV file has a rectangular structure."
        response = { "status": status, "reason": reason }
    else:
        status = "Fail"
        reason = "File appear to have no headers."
        response = { "status": status, "reason": reason }
    return reponse

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

# Nombres de columnas completos = Que la primera fila de columnas tenga el mismo número que los valores.
def complete_cols(data):
    """ 
    Validates that the CSV file has a rectangular structure.
    """

    with open(data, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        header_columns = len(headers)
        next(reader)

        response = {}

        row_count = sum(1 for row in reader)

        if row_count < 1000:
            sample_size = 1000
            pass
        elif row_count > 1000:
            # Determines the sample size based on Slovin's formula at a 95% confidence level
            confidence_level = 95.0
            error = 1.0-(confidence_level/100)
            sample_size = row_count/(1 + (row_count*(error*error)))
        else:
            # Error
            pass

        samples = []
        chances_selected = sample_size/row_count

        for row in csv.reader(f):
            if random() < chances_selected:
                samples.append(line)
    return samples

def has_alphanumeric_headers(data):
    """ 
    Validates that the header names contains only letters, numbers, dashes, and underscores.
    """
    regexp = re.compile('^[A-Za-z0-9-]')
    response = {}
    with open(data, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for column_number, column_name in enumerate(headers, start=1):
            if regexp.match(column_name):
                status = "Pass"
                reason = "Headers have valid names."
                response = { "status": status, "reason": reason }
            else:
                status = "Fail"
                reason = """Column name {column_name} in column {column_number} has an invalid name. 
                            Please use only letters, numbers, dashes and underscores.""".format(column_name=column_name, column_number=column_number)
                response = { "status": status, "reason": reason }
                return response
    return response

def main():
    data = '../tramites_lerma.csv'
    headers_response = has_headers(data)
    rectangularity_reponse = is_rectangular(data)
    complete_cols_response = complete_cols(data)
    alphanumeric_reponse = has_alphanumeric_headers(data)

    r = complete_cols('../tramites_lerma.csv')
    print(r)
    sys.exit(1)
    

    if len(sys.argv) == 1:
        output_dict = return_reqs()
    else:
        #print sys.argv[1]
        output_dict = return_validation(sys.argv[1])
    print(json.dumps(output_dict))

if __name__ == '__main__':
    main()