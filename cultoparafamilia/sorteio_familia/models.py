from abc import ABCMeta
import os
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from pydantic import BaseModel, RootModel
from typing import List, Dict, Union, Optional, Any
from deta import Deta
from enums.env_deta import projeto_key, DETA_SORTEIO, DETA_USER
from sqlite3 import IntegrityError
from utils.dates import retornar_idade
from werkzeug.security import generate_password_hash, check_password_hash

db = Deta(project_key=projeto_key)

# Create your models here.
class Base():
    def len(self):
        return self.model_dump().keys().__len__()
    
    def str(self):
        return str(self.model_dump())
    
    def dict_key(self):
        return self.model_dump().keys()
    
    def to_json(self):
        return self.model_dump_json()
    
    def to_object(self):
        return self.model_dump()
    
    def __getitem__(self, item):
        return getattr(self, item)
    
    def __setitem__(self, item, value):
        setattr(self, item, value)


class Lista(BaseModel, Base):
    lista: Union[List[str], Dict] = []
    filtro: Dict = {}
    
    def __str__(self):
        return self.str()
    
    def sortear(self):
        import random
        
        # sorteia em self.lista
        if type(self.lista) == dict:
            escolha = random.choice([item for item in self.lista.keys()])
            return {escolha: self.lista[escolha] }
        if len(self.lista) > 0:
            return random.choice(self.lista)
        

class Ensaio(BaseModel, Base):
    habilitarListaAlameda: bool = False
    habilitarListaJardimCopa1: bool = False
    habilitarListaJardimCopa2: bool = False
    habilitarListaNovaDivineia1: bool = False
    habilitarListaNovaDivineia2: bool = False
    habilitarListaPiedade: bool = False
    habilitarListaVeneza4: bool = False
    listaEnsaio: Lista = Lista()
    listaEnsaioAlameda: Lista = Lista()
    listaEnsaioJardimCopa1: Lista = Lista()
    listaEnsaioJardimCopa2: Lista = Lista()
    listaEnsaioNovaDivineia1: Lista = Lista()
    listaEnsaioNovaDivineia2: Lista = Lista()
    listaEnsaioPiedade: Lista = Lista()
    listaEnsaioVeneza4: Lista = Lista()
    
    def __str__(self):
        return self.str()
    
    def reset(self):
        ensaio = Ensaio()
        return ensaio, 'Ensaios Resetados'
    
    def sortear(self, lista):
        return self[lista].sortear()
    
    
class Sorteio(BaseModel, Base):
    listaGeral: Lista = Lista()
    listaVisitante: List[str] = []
    listaMenor: Lista = Lista()
    listaDinamica: List[str] = []
    listaNiverCasamento: Lista = Lista()
    
    def __str__(self):
        return self.str()
    
    def reset(self):
        sorteio = Sorteio()
        return sorteio, 'Geral Resetado'
    
    def sortear(self, lista):
        import random
        
        # sorteia em self.[lista]
        if type(self[lista]) is not Lista:
            if len(self[lista]) > 0:
                return random.choice(self[lista])
        else:
            return self[lista].sortear()
 
 
class ListaDeOutNov(BaseModel, Base):
    geral: Dict = {
			"4": [],
			"5": [],
			"6": [],
			"7": [],
			"8": []
		}
    jovens: Dict = {
			"4": [],
			"5": [],
			"6": [],
			"7": [],
			"8": []
		}
    filtro: Dict = {}
    
    def __str__(self):
        return self.str()


class ListaSet(BaseModel, Base):
    geral: Dict = {
			"4": 0,
			"5": 0,
			"6": 0,
			"7": 0,
			"8": 0
		}
    jovens: Dict = {
			"4": 0,
			"5": 0,
			"6": 0,
			"7": 0,
			"8": 0
		}
    
    def __str__(self):
        return self.str()
    
       
class Evento(BaseModel, Base):
    listaDinamicaMaePai: Lista = Lista()
    listaDinamicaFilhosPais: Lista = Lista(lista={})
    listaDeOutNov: ListaDeOutNov = ListaDeOutNov()
    listaSet: ListaSet = ListaSet()
    selecaoEventoEspecial: Union[List[Dict], List[str]] = []
    selecaoListaMaePai: Dict = dict()
    selecaoListaFilhosPais: Dict = dict()
    
    def __str__(self):
        return self.str()
    
    def sortear(self, lista:str, presenca: str = ""):
        if lista == 'geral':
            return self.listaDeOutNov.geral[presenca]
        elif lista == 'jovens':
            return self.listaDeOutNov.jovens[presenca]
        return self[lista].sortear()
    
    def reset(self):
        evento = Evento()
        return evento, 'Eventos Resetados'
    
    
class Historico(BaseModel, Base):
    nomeSorteadoAnterior: str = ''
    nomeSorteado: str = ''
    historicoSorteio: Dict = dict()
    
    def __str__(self):
        return self.str()


class DadosDict(BaseModel, Base):
    confAPI: str = ''
    username: str
    mesSorteio: str = ''
    ensaio: Ensaio = Ensaio()
    evento: Evento = Evento()
    historico: Historico = Historico()
    geral: Sorteio = Sorteio()
    listaMesSorteio: List[str] = []
    habilitarEvento: bool = False # HabilitarFilhosParaPais: List[str]
    habilitarEnsaio: bool = False
    
    _loaded = False
    
    def __str__(self):
        return self.username
    
    @property
    def is_loaded(self):
        return self._loaded
    
    def _connect_base(self):
        return db.Base(DETA_SORTEIO)
    
    def load(self):
        db_load = self._connect_base()
        db_load_user = db_load.get(self.username)
        if db_load_user is None:
            tamanho = len(db_load.fetch().items)
            try:
                teste_login = self._connect_database(self.username)
                if teste_login is not None:
                    raise ConnectionError
                if teste_login is not None and len(teste_login) > 0:
                    raise ValueError("Many values for username")
                db_load.insert(
                    data={'username': self.username,
                    'confAPI': self.confAPI,
                    "id": tamanho + 1,
                    "mesSorteio": self.mesSorteio,
                    "ensaio": self.ensaio.to_object(),
                    "evento": self.evento.to_object(),
                    "historico": self.historico.to_object(),
                    "geral": self.geral.to_object(),
                    "listaMesSorteio": self.listaMesSorteio,
                    "habilitarEvento": self.habilitarEvento,
                    "habilitarEnsaio": self.habilitarEnsaio
                    }, key=self.username
                )
            except TypeError as e:
                raise TypeError(e)
            except Exception as e:
                print(e)
                raise ConnectionError("Connection Failed")
            return 'Dados Iniciados', DadosDict(username=self.username).load()[1]
        self._loaded = True
        return 'Dados carregados', DadosDict(**db_load_user)
    
    def save(self, _print=False):
        db_load = self._connect_base()
        try:
            teste_login = self._connect_database(self.username)
            if _print:
                print('save:', teste_login)
                print('tamanho:', len(teste_login))
            if teste_login is None:
                raise ConnectionError
            if len(teste_login) > 1:
                raise ValueError(f"Many values for username, len: {len(teste_login)}")
            db_load.put(
                    data={'username': self.username,
                    'confAPI': self.confAPI,
                    "mesSorteio": self.mesSorteio,
                    "ensaio": self.ensaio.to_object(),
                    "evento": self.evento.to_object(),
                    "historico": self.historico.to_object(),
                    "geral": self.geral.to_object(),
                    "listaMesSorteio": self.listaMesSorteio,
                    "habilitarEvento": self.habilitarEvento,
                    "habilitarEnsaio": self.habilitarEnsaio
                    }, key=self.username
                )
        except TypeError as e:
            raise TypeError(e)
        except Exception:
            raise ConnectionError("Connection Failed")
        return 'Dados Salvos'
    
    def _connect_database(self, username=None):
        items = self._connect_base().fetch({"key": username}).items
        if len(items) == 0:
            return None
        return items
    
    def reset_API(self):
        dados = DadosDict(username=self.username, historico=self.historico, confAPI=self.confAPI)
        dados.historico.nomeSorteado = ''
        dados.historico.nomeSorteadoAnterior = ''
        dados._loaded = self.is_loaded
        dados.save()
        return dados, 'Dados Resetados'
    
    def reset_mes(self):
        self.geral, _ = self.geral.reset()
        self.ensaio, _ = self.ensaio.reset()
        self.evento, _ = self.evento.reset()
        self.historico.nomeSorteado = ''
        self.historico.nomeSorteadoAnterior = ''
        self.habilitarEnsaio = False
        self.habilitarEvento = False
        self.mesSorteio = ''


class Caracteristicas(BaseModel, Base):
    congregacao: str = ''
    dataCasamento: str = ''
    estadoCivil: str = ''
    idNumero: str = ''
    numeroCartao: str = ''
    nascimentoConjuge: str = ''
    nascimentoTitular: str = ''
    nomeConjuge: str = ''
    nomeTitular: str = ''
    perfil: str = ''
    cargoEclesiastico: str = ''
    juntosConjuge: str = ''
    juntosTitular: str = ''
    idadeTitular: int = 0
    idadeConjuge: int = 0
    
    def __str__(self):
        return self.str()
    
    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.congregacao = self.idNumero.split('/')[0]
        self.numeroCartao = self.idNumero.split('/')[1]
        self.nomeTitular = self.nomeTitular.strip()
        self.nomeConjuge = self.nomeConjuge.strip()
        self.idadeTitular = int(retornar_idade(self.nascimentoTitular))
        self.idadeConjuge = int(retornar_idade(self.nascimentoConjuge))
        self.juntosTitular = '' if self. nomeTitular == '' else (
            self.nomeTitular + '|' + self.congregacao + '|' +  self.numeroCartao + '|' +
            str(self.idadeTitular) + '|' + self.dataCasamento + '|' +
            self.estadoCivil + '|' + self.nomeConjuge)
        self.juntosConjuge = '' if self.nomeConjuge == '' else (
            self.nomeConjuge + '|' + self.congregacao + '|' + self.numeroCartao + '|' +
            str(self.idadeConjuge) + '|' + self.dataCasamento + '|' +
            self.estadoCivil + '|' + self.nomeTitular)
    
    
class Presencas(RootModel, Base):
    root: Dict[str, Caracteristicas]
    
    def __str__(self):
        return self.str()
    
    def __iter__(self):
        return iter(self.root)
    
    def __getitem__(self, item):
        return self.root[item]
    
    def __setitem__(self, item, value):
        self.root[item] = value
    
    def insert_lists(self, dados: DadosDict, mes: str):
        from enums import congregacoes
        from utils.dates import niver_casamento
        
        def juntar_lista(lista, titular, conjuge):
            if titular != '':
                lista.append(titular)
            if conjuge != '':
                lista.append(conjuge)
            return lista
        
        def juntar_filtro(filtro, key: str, titular, conjuge):
            if titular != '' or conjuge != '':
                filtro[key] = []
            if titular != '':
                filtro[key].append(titular)
            if conjuge != '':
                filtro[key].append(conjuge)
            return filtro
    
        def zerar_listas():
            dados.geral.listaGeral.lista = []
            dados.geral.listaGeral.filtro = {}
            dados.geral.listaMenor.lista = []
            dados.geral.listaMenor.filtro = {}
            dados.geral.listaNiverCasamento.lista = []
            dados.geral.listaNiverCasamento.filtro = {}
            dados.geral.listaVisitante = []
            dados.ensaio.listaEnsaioAlameda.lista = []
            dados.ensaio.listaEnsaioAlameda.filtro = {}
            for cong in congregacoes.congregacoes_lists_full_names:
                dados.ensaio[congregacoes.congregacoes_lists_full_names[cong]].lista = []
                dados.ensaio[congregacoes.congregacoes_lists_full_names[cong]].filtro = {}
        
        zerar_listas()
        
        for id_cartao in self.__iter__():
            cartao: Caracteristicas = self.root[id_cartao]
            titular = cartao.juntosTitular
            conjuge = cartao.juntosConjuge
        
            if cartao.congregacao.lower().__contains__(congregacoes.VISITANTE):
                dados.geral.listaVisitante = juntar_lista(dados.geral.listaVisitante, titular, conjuge)
                continue
            if not mes.lower().__contains__('ensaio') and cartao.estadoCivil.lower() == 'solteiro' and cartao.idadeTitular < 35:
                dados.geral.listaMenor.lista = juntar_lista(dados.geral.listaMenor.lista, titular, conjuge)
                dados.geral.listaMenor.filtro = juntar_filtro(dados.geral.listaMenor.filtro, f'{cartao.congregacao}|{cartao.numeroCartao}', titular, conjuge)
                continue
            dados.geral.listaGeral.lista = juntar_lista(dados.geral.listaGeral.lista, titular, conjuge)
            dados.geral.listaGeral.filtro = juntar_filtro(dados.geral.listaGeral.filtro, f'{cartao.congregacao}|{cartao.numeroCartao}', titular, conjuge)
            if niver_casamento(cartao.dataCasamento, mes):
                dados.geral.listaNiverCasamento.lista = juntar_lista(dados.geral.listaNiverCasamento.lista, titular, conjuge)
                dados.geral.listaNiverCasamento.filtro = juntar_filtro(dados.geral.listaNiverCasamento.filtro, f'{cartao.congregacao}|{cartao.numeroCartao}', titular, conjuge)
            if mes.lower().__contains__('ensaio'):
                dados.ensaio.listaEnsaio.lista = juntar_lista(dados.ensaio.listaEnsaio.lista, titular, conjuge)
                dados.ensaio.listaEnsaio.filtro = juntar_filtro(dados.ensaio.listaEnsaio.filtro, f'{cartao.congregacao}|{cartao.numeroCartao}', titular, conjuge)
                dados.ensaio[congregacoes.congregacoes_lists_full_names[cartao.congregacao.lower()]].lista = juntar_lista(
                    dados.ensaio[congregacoes.congregacoes_lists_full_names[cartao.congregacao.lower()]].lista, titular, conjuge)
                dados.ensaio[congregacoes.congregacoes_lists_full_names[cartao.congregacao.lower()]].filtro = juntar_filtro(
                    dados.ensaio[congregacoes.congregacoes_lists_full_names[cartao.congregacao.lower()]].filtro, f'{cartao.congregacao}|{cartao.numeroCartao}', titular, conjuge)
        
        return dados
        
        
    # def insert_lists(self, i, dados: DadosDict, mes: str):
        

class User_field(BaseModel):
    username: str = None
    password: str = ''
    congregacao: str = ''
    num_cartao: int = None
    
    _logged = False
    
    @property
    def is_logged(self):
        return self._logged
    
    def __str__(self):
        return self.username
    
    def _connect_base(self):
        return db.Base(DETA_USER)
    
    def save(self):
        db_user = self._connect_base()
        try:
            teste_login = self._connect_database(self.username, save=True)
            # print('save:', teste_login)
            if teste_login is None:
                raise ConnectionError
            if len(teste_login) == 0:
                self.create()
                return 'Criado novo usuário'
            if len(teste_login) > 1:
                raise ValueError("Many values for username")
            db_user.update(
                updates={'username': self.username,
                'password': generate_password_hash(self.password)
                }, key=self.username
            )
            users = User.objects.filter(username=self.username)
            if not users.exists():
                teste_login
                _ = User.objects.create_user(
                    username=self.username, 
                    password=self.password
                )
            else:
                users = User.objects.get(username=self.username)
                users.password=make_password(self.password)
                users.save()
        except Exception:
            raise ConnectionError("Connection Failed")
    
    def create(self):
        db_user = self._connect_base()
        tamanho = len(db_user.fetch().items)
        try:
            teste_login = self._connect_database(self.username)
            if teste_login is not None:
                raise ValueError(f"Many values for username: {len(teste_login)}")
            db_user.insert(
                data={'username': self.username,
                'password': generate_password_hash(self.password),
                "id": tamanho + 1}, key=self.username
            )
            users = User.objects.filter(username=self.username)
            if not users.exists():
                _ = User.objects.create_user(
                    username=self.username, 
                    password=self.password
                )
            else:
                users = User.objects.get(username=self.username)
                users.password=make_password(self.password)
                users.save()
        except ConnectionError:
            raise ConnectionError("Connection Failed")
        except Exception as e:
            raise NotImplementedError(f"Exception Error: {e}")
        
    def _connect_database(self, username=None, save=False):
        items = self._connect_base().fetch({"key": username}).items
        if len(items) == 0:
            if save:
                return []
            return None
        return items
    
    def login(self, request, _print: bool = False):
        teste_login = self._connect_database(self.username)
        if teste_login is None or len(teste_login) == 0:
            raise ValueError("Username not exists")
        if len(teste_login) > 1:
            raise ValueError("Many values for username")
        if not check_password_hash(teste_login[0]['password'], self.password):
            raise ValueError("Wrong password")
        users = User.objects.filter(username=self.username)
        if _print:
            print('self.username:', self.username)
            print('self.password:', self.password)
            print('users.exists():', users.exists())
        if not users.exists():
            _ = User.objects.create_user(
                username=self.username, 
                password=self.password,
            )
        user = auth.authenticate(request, username=self.username, password=self.password)
        if _print:
            print('user:', user)
        if user is not None:
            auth.login(request, user)
            self._logged=True
        else:
            raise ValueError("User is not authenticated")
        
    def logout(self, request):
        auth.logout(request)
        self.password = None
        self.username = None
        self._logged = False
        
    def delete(self):
        try:
            users = User.objects.get(username=self.username)
            users.delete()
        except User.DoesNotExist: 
            users = User.objects.get(username=self.username)


def is_logged(username):
    return User.objects.filter(username=username).exists()


def is_staff(username):
    try:
        return User.objects.get(username=username).is_staff
    except User.DoesNotExist:
        return False


def is_superuser(username):
    try:
        return User.objects.get(username=username).is_superuser
    except User.DoesNotExist:
        return False


def return_username(username):
    try:
        user = User.objects.get(username=username).first_name
        if user == "":
            user = User.objects.get(username=username).username
        return user
    except User.DoesNotExist:
        return False
    

def return_info_user(request):
    return {
        'logged': is_superuser(str(auth.get_user(request))), 
        'connected': is_logged(str(auth.get_user(request))), 
        'username': return_username(str(auth.get_user(request)))
        }

if __name__ == '__main__':
    user = User_field(username='eudes', password='123')
    user.create()