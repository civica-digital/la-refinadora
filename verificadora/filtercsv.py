import string
import random
import time
import csv

TMP_DIR="tmp"

def read_file(filepath):
    with open (filepath, "rb") as myfile:
        data=myfile.read()
    return data

def detect_lines(filename):
    count = 0
    with open(filename,'rb') as fp:
        for line in fp:
            count = count + 1
    return int(count)

def read_top_lines(filename, N):
    with open(filename,'rb') as fp:
        head = fp.readlines(N)
        print(head)
    return head

def name_id_generator(size=24, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_random_filename():
    stringname = name_id_generator()
    ext = ".csv"
    filename = stringname+ext
    return filename

def generate_random_list(N,n_lines):
    r_list=[]
    for _ in range(N):
        r_int =random.randint(1,n_lines)
        r_list.append(r_int)
    r_list = sorted(r_list)
    return r_list

def read_random_lines(filename, N,n_lines):
    random_list = generate_random_list(N,n_lines)
    count = 0
    with open(filename,'rb') as fp:
        for line in fp:
            count = count + 1
            if count == random_list[0]:
                data=fp.read()
                random_list.pop(0)
        fp.close()
    return data

def write_data_list(data):
    sample_filename = generate_random_filename()
    file_path= TMP_DIR + "/" + sample_filename
    with open(file_path, "w") as file_write:
        writer = csv.writer(file_write)
        writer.writerow(data)
    return file_path

def write_data_raw(data):
    sample_filename = generate_random_filename()
    file_path= TMP_DIR + "/" + sample_filename
    file_write = open(file_path, 'wb')
    file_write.write(data)
    file_write.close()
    return file_path

def csv_data_filter(filename,unit, sampling, number_units = 0):
    with open(filename, 'r') as f: n_lines = sum(1 for row in f)
    with open(filename, 'r') as f:
        rowdata = []
        reader = csv.reader(f)
        count = 1
        if n_lines < number_units:
            number_units = n_lines
            print('Warning: Less lines than required by resource')
        random_list = generate_random_list(number_units,n_lines)
        for row in reader:
            if unit == "title" and count == 1: 
                return row
            elif unit == "row":
                if sampling == "top" and count <= number_units: 
                    rowdata.append(row)
                if sampling == "random":
                    if len(random_list) > 0:
                        if count == random_list[0]:
                            rowdata.append(row)
                            random_list.pop(0)
            else:
                rowdata.append(row)
            count = count +1 
    temp_data_path = write_data_list(rowdata)
    return temp_data_path 

def raw_data_filter(filename,unit,sampling,number_units = 0):
    data = b''
    if unit == "file":
        data = read_file(filename)
    elif unit == "title":
        data = read_top_lines(filename,1)
    elif unit == "row":
        n_lines = detect_lines(filename)
        if n_lines < number_units:
            number_units = n_lines
            print('Warning: Less lines than required by resource')
        if sampling == "top":
            data = read_top_lines(filename,number_units)
        elif sampling == "random":
            data = read_random_lines(filename,number_units,n_lines)
    temp_data_path = write_data_raw(data)
    return temp_data_path


def filter_data(raw,unit,filename,sampling,number_units = 0):
    if raw == "true":
        temp_data_path = raw_data_filter(filename,unit,sampling,number_units)
    else:
        temp_data_path = csv_data_filter(filename,unit,sampling,number_units)
    return temp_data_path

def prepare_csv(csv_requirements,filename,resource):
    requirements = csv_requirements["response"]
    number_units = int(requirements["number"]) #Un número de 1 al numero de filas o columnas 
    sampling = requirements["sampling"] #random, first, last
    unit = requirements["unit"] # rows, title, file, columns
    raw = requirements["raw"]
    temp_data_path = filter_data(raw,unit,filename, sampling, number_units)
    return temp_data_path