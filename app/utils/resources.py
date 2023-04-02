import json
import platform
from pathlib import Path


def resource_local(_platform: str = platform.system(),
                   folder: str = '') -> str:
    file_path = Path(__file__).parts
    index_ = 0
    for x in range(len(file_path), 0, -1):
        if file_path[x - 1].lower() == 'app':
            index_ = x
            break
    file_path_final = ''
    for i in range(index_):
        if _platform == 'Darwin':
            if file_path[i] == '/':
                file_path_final += file_path[i]
            else:
                file_path_final += file_path[i] + '/'
        if _platform == 'Windows':
            if file_path[i].__contains__('\\'):
                file_path_final += file_path[i]
            else:
                file_path_final += file_path[i] + '\\'
    if folder != '':
        if _platform == 'Darwin':
            return file_path_final + folder + '/'
        if _platform == 'Windows':
            return file_path_final + folder + '\\'
    return file_path_final


def file_local(path_file: str = ''):
    if path_file == '':
        if platform.system() == 'Windows':
            endereco = resource_local(platform.system()) + \
                       'instance\\teste.json'
        else:
            endereco = resource_local(platform.system()) + \
                       'instance/teste.json'
    else:
        endereco = path_file
    with open(endereco, encoding='utf-8') as file:
        return json.load(file)
