import json
import platform
from pathlib import Path
import os


def resource_local(folder: str = '') -> str:
    file_path = Path(__file__).parts
    index_ = 0
    for x in range(len(file_path), 0, -1):
        if file_path[x - 1].lower() == 'app':
            index_ = x
            break
    file_path_final = ''
    for i in range(index_):
        file_path_final = os.path.join(file_path_final, file_path[i])
    file_path_final = os.path.join(file_path_final)
    if folder != '':
        return os.path.join(file_path_final, folder)
    return file_path_final


def file_local(path_file: str = ''):
    if path_file == '':
        endereco = os.path.join(resource_local(), 'instance', 'teste.json')
    else:
        endereco = path_file
    with open(endereco, encoding='utf-8') as file:
        return json.load(file)
