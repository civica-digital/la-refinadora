import string
import random

TMP_DIR="tmp"

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

def filter_data(unit,filename,sampling,number_units = 0):
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

def prepare_csv(csv_requirements,filename,resource):
    requirements = csv_requirements["response"]
    number_units = int(requirements["number"]) #Un número de 1 al numero de filas o columnas 
    sampling = requirements["sampling"] #random, first, last
    unit = requirements["unit"] # rows, title, file, columns
    data = b''
    temp_data_path = filter_data(unit,filename, sampling, number_units)
    return temp_data_path