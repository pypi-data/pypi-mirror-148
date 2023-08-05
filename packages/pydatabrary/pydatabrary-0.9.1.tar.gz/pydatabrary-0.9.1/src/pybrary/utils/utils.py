import os
import csv
import json
import pandas as pd
from .. import constants
# TODO: Finish unit tests


def replace_file_extension(file_path, file_format='json'):
    root = get_file_root(file_path)
    file_name = get_file_name_no_extension(file_path)
    return os.path.join(root, "{}{}{}".format(file_name, '.', file_format))


# TODO: Check unit test and fix edge cases
def get_file_extension(file_path):
    if file_path is None:
        return None

    file_name = get_file_name(file_path)

    file_name, file_extension = os.path.splitext(file_name)
    file_ext = file_extension[1:] if len(file_extension[1:]) > 0 else None
    return file_ext


# TODO: Check unit test and fix edge cases
def get_file_name_no_extension(file_path):
    file_name, file_extension = os.path.splitext(get_file_name(file_path))

    if len(file_name) == 0:
        return None

    return file_name


def get_file_root(file_path):
    if file_path is None:
        return None

    return os.path.dirname(os.path.abspath(file_path))


# TODO: Check unit test and fix edge cases
def get_file_name(file_path):
    if file_path is None:
        return None

    return os.path.basename(file_path)


def get_supported_formats():
    return constants.SUPPORTED_FORMATS.values()


def dump_into_csv(data_list, output, index=False):
    df = pd.read_json(json.dumps(data_list))
    df.to_csv(output, index=index, index_label='id', quoting=csv.QUOTE_ALL)


def dump_into_json(data_list, output, indent=4):
    with open(output, 'w') as outFile:
        json.dump(data_list, outFile, indent=indent)


def read_csv(file_path: str):
    df = pd.read_csv(file_path, keep_default_na=False)
    return df.to_dict('records')


def get_category_from_category_id(category_id: int) -> str:
    return constants.DATABRARY_VOLUME_CATEGORIES[category_id]


def get_databrary_ext_from_format(format_id: int) -> str:
    return constants.SUPPORTED_FORMATS[format_id]
