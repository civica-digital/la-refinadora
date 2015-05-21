import os.path
from os import getcwd
import json
import subprocess
import random
import string
import sys

FILE = sys.argv[1]
RESOURCES_FILE="resources.json"
RESOURCES_DIR="resources"
COMPILER_FILE = "compilers.json"
TMP_DIR="tmp"

CURRENT_DIRECTORY = os.getcwd()
RESOURCES_FULLPATH = CURRENT_DIRECTORY + "/" + RESOURCES_DIR
TEMP_FULLPATH = CURRENT_DIRECTORY + "/" + TMP_DIR

def load_json(filename):
    with open(filename) as data_file:    
        data = json.load(data_file)
    return data

def response_status(response_dict):
    status = "Pass"
    for response in response_dict.keys():
        if response_dict[response]['status'] == "Fail": status = "Fail"
    return status

def extract_extension(filename):
    extension = os.path.splitext(filename)[1][1:]
    return extension

def verify_morethan11ine(filename):
    count = 0
    valor = 0
    with open(filename) as fp:
        for line in fp:
            count = count + 1
            if count > 1: valor = 1
    return valor

def csv_validation(filename):
    extension = extract_extension(filename)
    if extension == "csv": 
        status = "Pass"
        reason = "Se detectó la codificación csv"
    else:
        status = "Fail"
        reason = extension   
    response = {"status":status,"reason":reason}
    return response

def morethan1line_validation(filename):
    test_result = verify_morethan11ine(filename)
    if test_result == 1 : 
        status = "Pass"
        reason = "El archivo cuenta con más de una fila"
    else:
        status = "Fail"
        reason = "El archivo no cuenta con contenido suficiente, verificar que al menos tenga una fila de valores"
    response = {"status":status,"reason":reason}
    return response

def base_validation(filename):
    csv_response = csv_validation(filename)
    morethan1line_response = morethan1line_validation(filename)
    response_dict = {"csv": csv_response, "morethan1line":morethan1line_response}
    status = response_status(response_dict)
    output_dict = {"status":status,"validators":response_dict}
    return output_dict

def load_resources(resources_filename):
    data = load_json(resources_filename)
    return data['resources']

def detect_api(resource):
    if resource[0:3] == "http": return "1"
    return "0"

def detect_compiler(resource):
    resource_extension = extract_extension(resource)
    compiler = compiler_dictionary[resource_extension]
    return compiler

def call_local_resource(resource,filename = None):
    resource_path = RESOURCES_DIR + "/" + resource
    compiler = detect_compiler(resource)
    if filename is None: 
        output = subprocess.check_output([compiler,resource_path])
    else:
        output = subprocess.check_output([compiler,resource_path,filename])
    output_dict = json.loads(output.decode("utf-8"))
    return output_dict

def get_requirements(resource,id_api):
    if id_api == 1: return None
    requirements = call_local_resource(resource)
    return requirements

def read_file(filepath):
    with open (filepath, "rb") as myfile:
        data=myfile.read()
    return data

def detect_lines(filename):
    count = 0
    with open(filename) as fp:
        for line in fp:
            count = count + 1
    return int(count)

def read_top_lines(filename, N):
    with open(filename,'rb') as fp:
        head = fp.readlines(N)
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
    return data

def write_data(data):
    sample_filename = generate_random_filename()
    file_path= TMP_DIR + "/" + sample_filename
    f = open(file_path, 'wb')
    f.write(data)
    f.close()
    return file_path

def prepare_csv(csv_requirements,filename,resource):
    requirements = csv_requirements["response"]
    number_units = int(requirements["number"]) #Un número de 1 al numero de filas o columnas 
    sampling = requirements["sampling"] #random, first, last
    unit = requirements["unit"] # rows, title, file, columns
    data = b''
    if unit == "file":
        data = read_file(filename)
    elif unit == "title":
        data = read_top_lines(filename,1)
    elif unit == "row":
        n_lines = detect_lines(filename)
        if n_lines < number_units:
            number_units = n_lines
            print('Warning: Less lines than required by resource '+ resource)
        if sampling == "top":
            data = read_top_lines(filename,number_units)
        elif sampling == "random":
            data = read_random_lines(filename,number_units,n_lines)
    temp_data_path = write_data(data)
    return temp_data_path

def get_resource_results(resource,filename, id_api):
    if id_api == 1: return None
    response = call_local_resource(resource,filename)
    return response

def call_resource(resource,filename):
    id_api = detect_api(resource)
    resource_requirements = get_requirements(resource,id_api)
    filtered_csv = prepare_csv(resource_requirements,filename,resource)
    resource_return = get_resource_results(resource,filtered_csv,id_api)
    return resource_return

compiler_dictionary = load_json(COMPILER_FILE)

base_response_dict = base_validation(FILE)
base_status = base_response_dict['status']
if base_status == "Fail": 
    print(base_response_dict)
    sys.exit() 
resource_list = load_resources(RESOURCES_FILE)
response_dict = {}
status = "Pass"
for resource in resource_list:
    response_dict[resource]= call_resource(resource,FILE)
    if response_dict[resource]['status'] != "Pass": status = "Fail"
return_dict = {"status":status,"detail":response_dict}
print(return_dict)