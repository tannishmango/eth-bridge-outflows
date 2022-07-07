from concurrent.futures import ThreadPoolExecutor
import json
import os

#################
## CONCURRENCY ##
#################


def run_multithreader(function, *args):
    pool = ThreadPoolExecutor(10)
    thread = pool.map(function,*args)
    result = [i for i in thread]
    return result


#####################
## DATA FORMATTING ##
#####################

def flatten_list(data_list):
    result_list = []
    for item in data_list:
        if isinstance(item,list) and len(item):
            result_list.extend(item)
    if not result_list:
        result_list=data_list
    return result_list

def read_json_file(file_path):
    f = open(file_path)
    file = json.load(f)
    f.close()
    return file


def write_json_file(file_path, json_data):
    with open(file_path, "w") as outfile:
        outfile.write(json_data)
