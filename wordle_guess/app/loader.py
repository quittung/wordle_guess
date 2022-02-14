import pkgutil
import json


data_package = "{}.data".format(__package__)

def load_str(file: str):
    data = pkgutil.get_data(data_package, file)
    return data.decode("utf-8")

def load_json(file: str):
    file_string = load_str(file)
    return json.loads(file_string)