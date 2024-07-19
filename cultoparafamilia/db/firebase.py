import os
import requests
import json
import posixpath
from enums.env_deta import FIREBASE_URL
from utils.sorted_utils import sorted_mes

def ajust_path(path):
    pos = pos = posixpath.join(FIREBASE_URL)
    if type(path) is list:
        for _path in path:
            pos = posixpath.join(pos, _path)
        pos += '.json'
    else:
        pos = posixpath.join(pos, path + '.json')
    return pos
    
def load_firebase(path, _print: bool = False):
    _print = False
    pos = ajust_path(path)
    try:
        connect = requests.get(pos).json()
    except Exception as e:
        if _print:
            print('Falha na conexão com a API. Erro: ', e)
        connect = None
    return connect


def load_postagens():
    postagens = load_firebase('postagem')
    while None in postagens:
        postagens.remove(None)
    return postagens

def load_lista_cultos():
    lista_cultos = load_firebase('listaCulto')
    # lista_cultos = lista_de_culto
        
    lista_cultos = sorted_mes(lista_cultos)
    return lista_cultos

def load_lista_presenca():
    lista_presenca = load_firebase('presenca')
    # lista_presenca = presenca_json
    return lista_presenca

def load_lista_usuarios():
    lista_usuarios = load_firebase('usuarios')
    # lista_usuarios = usuarios_json
    return lista_usuarios

def insert_data(path, id_post, data, _print: bool = False):
    sent = json.dumps({id_post: data})
    pos = ajust_path(path)
    
    try:
        connect = requests.patch(pos, sent)
    except Exception as e:
        if _print:
            print('Falha na conexão com a API. Erro: ', e)
        connect = None
    return connect

def insert_postagens(path, id_post, data, _print: bool = False):
    return insert_data(path, id_post, data, _print)

def update_postagens(path, id_post, data, _print: bool = False):
    return insert_data(path, id_post, data, _print)

def update_lista_cultos(path, id_post, data, _print: bool = False):
    return insert_data(path, id_post, data, _print)

def delete_postagens(path, id_post, _print: bool = True):
    if type(path) is list:
        path.append(id_post)
        pos = ajust_path(path)
    else:
        pos = ajust_path([path, id_post])
    
    try:
        connect = requests.delete(pos)
    except Exception as e:
        if _print:
            print('Falha na conexão com a API. Erro: ', e)
        connect = None
    return connect