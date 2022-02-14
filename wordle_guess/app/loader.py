import pkgutil
import json


def load_str(file: str):
    data = pkgutil.get_data("app.data", file)
    return data.decode("utf-8")

def load_json(file: str):
    file_string = load_str(file)
    return json.loads(file_string)