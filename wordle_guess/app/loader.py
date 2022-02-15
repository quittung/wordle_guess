from ntpath import join
import pkgutil
import json


def load_str(file: str):
    module_path = __name__.split(".")
    module_path[-1] = "data"
    data_module = ".".join(module_path)

    data = pkgutil.get_data(data_module, file)
    return data.decode("utf-8")

def load_json(file: str):
    file_string = load_str(file)
    return json.loads(file_string)