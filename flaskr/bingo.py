from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)
from db import get_db
from auth import login_required
import random
import ast
import requests
import pandas as pd
import json
from datetime import datetime, date
import platform
from pathlib import Path

bp = Blueprint('bingo', __name__)
Cartelas = dict()
Vencedores = dict()
Premiacao = {"1": 100, "2": 50, "3": 25}


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index(imagem: str = 'images/globo.gif'):
    global BolaEscolhida, Cartelas, Vencedores, Premiacao
    # print(g.user['username'])
    # if len(BolasDoBingo) == 0:
    #     BolasDoBingo, _ = '', ''
    db = get_db()
    bolas = [dict(row)for row in db.execute(
        # 'SELECT p.id, author_id, bolasDoBingoJson, username'
        # 'SELECT p.id, title, body, created, author_id, username'
        # ' FROM post p JOIN user u ON p.author_id = u.id'
        # ' ORDER BY created DESC'
        f'SELECT p.id, author_id, bolasDoBingoJson, rankingJson, username'
        f' FROM bolasDoBingo p JOIN user u ON p.author_id = {g.user["id"]} AND u.id = {g.user["id"]}'
    ).fetchall()]

    if len(bolas) == 0:
        # bolas = [{'bolasDoBingoJson': {}, 'rankingJson': {}}]
        db.execute(
            'INSERT INTO bolasDoBingo (rankingJson, bolasDoBingoJson, author_id)'
            ' VALUES (?, ?, ?)',
            (str({}), str({}), g.user['id'])
        )
        db.commit()
        print()
        print()
        print(bolas)
        print()
        print()

    try:
        if type(bolas[0]['bolasDoBingoJson']) == str:
            bolas[0]['bolasDoBingoJson'] = json.loads(bolas[0]['bolasDoBingoJson'].replace("'", '"'))
    except:
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'geral' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        listaGeral = bolas[0]['bolasDoBingoJson']['ListaGeral']
        listaDinamica = bolas[0]['bolasDoBingoJson']['ListaDinamica']
        listaNiverCasamento = bolas[0]['bolasDoBingoJson']['ListaNiverCasamento']
        listaEnsaio = bolas[0]['bolasDoBingoJson']['ListaEnsaio']
        nomeSorteado = bolas[0]['bolasDoBingoJson']['NomeSorteado']
        proximo = bolas[0]['bolasDoBingoJson']['Proximo']
        if len(listaGeral) != 0:
            nomeSorteado = [random.choice(listaGeral)]
            db = get_db()
            # Remove o ganhador
            listaGeral.remove(nomeSorteado[0])
            proximo = ['True']
            try:
                listaDinamica.remove(nomeSorteado[0])
            except:
                pass
            try:
                listaNiverCasamento.remove(nomeSorteado[0])
            except:
                pass
            try:
                listaEnsaio.remove(nomeSorteado[0])
            except:
                pass

        jsonMontado = {
            'ConfAPI': bolas[0]['bolasDoBingoJson']['ConfAPI'],
            'ListaGeral': listaGeral,
            'ListaVisitante': bolas[0]['bolasDoBingoJson']['ListaVisitante'],
            'ListaMenor': bolas[0]['bolasDoBingoJson']['ListaMenor'],
            'ListaDinamica': listaDinamica,
            'ListaNiverCasamento': listaNiverCasamento,
            'ListaEnsaio': listaEnsaio,
            'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteado'],
            'NomeSorteado': nomeSorteado,
            'Opcao': ['adultos/casados'],
            'Proximo': proximo,
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
        }

        id = bolas[0]['id']
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()

        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'menores' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        listaMenor = bolas[0]['bolasDoBingoJson']['ListaMenor']
        nomeSorteado = bolas[0]['bolasDoBingoJson']['NomeSorteado']
        proximo = bolas[0]['bolasDoBingoJson']['Proximo']
        if len(listaMenor) != 0:
            nomeSorteado = [random.choice(listaMenor)]
            db = get_db()
            # Remove o ganhador
            listaMenor.remove(nomeSorteado[0])
            proximo = ['True']

        jsonMontado = {
            'ConfAPI': bolas[0]['bolasDoBingoJson']['ConfAPI'],
            'ListaGeral': bolas[0]['bolasDoBingoJson']['ListaGeral'],
            'ListaVisitante': bolas[0]['bolasDoBingoJson']['ListaVisitante'],
            'ListaMenor': listaMenor,
            'ListaDinamica': bolas[0]['bolasDoBingoJson']['ListaDinamica'],
            'ListaNiverCasamento': bolas[0]['bolasDoBingoJson']['ListaNiverCasamento'],
            'ListaEnsaio': bolas[0]['bolasDoBingoJson']['ListaEnsaio'],
            'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteado'],
            'NomeSorteado': nomeSorteado,
            'Opcao': ['menores'],
            'Proximo': proximo,
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
        }

        id = bolas[0]['id']
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()

        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'visitantes' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        listaVisitante = bolas[0]['bolasDoBingoJson']['ListaVisitante']
        nomeSorteado = bolas[0]['bolasDoBingoJson']['NomeSorteado']
        proximo = bolas[0]['bolasDoBingoJson']['Proximo']
        if len(listaVisitante) != 0:
            nomeSorteado = [random.choice(listaVisitante)]
            db = get_db()
            # Remove o ganhador
            listaVisitante.remove(nomeSorteado[0])
            proximo = ['True']

        jsonMontado = {
            'ConfAPI': bolas[0]['bolasDoBingoJson']['ConfAPI'],
            'ListaGeral': bolas[0]['bolasDoBingoJson']['ListaGeral'],
            'ListaVisitante': listaVisitante,
            'ListaMenor': bolas[0]['bolasDoBingoJson']['ListaMenor'],
            'ListaDinamica': bolas[0]['bolasDoBingoJson']['ListaDinamica'],
            'ListaNiverCasamento': bolas[0]['bolasDoBingoJson']['ListaNiverCasamento'],
            'ListaEnsaio': bolas[0]['bolasDoBingoJson']['ListaEnsaio'],
            'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteado'],
            'NomeSorteado': nomeSorteado,
            'Opcao': ['visitantes'],
            'Proximo': proximo,
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
        }

        id = bolas[0]['id']
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()

        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'aniversario' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        listaGeral = bolas[0]['bolasDoBingoJson']['ListaGeral']
        listaDinamica = bolas[0]['bolasDoBingoJson']['ListaDinamica']
        listaNiverCasamento = bolas[0]['bolasDoBingoJson']['ListaNiverCasamento']
        listaEnsaio = bolas[0]['bolasDoBingoJson']['ListaEnsaio']
        nomeSorteado = bolas[0]['bolasDoBingoJson']['NomeSorteado']
        proximo = bolas[0]['bolasDoBingoJson']['Proximo']
        if len(listaNiverCasamento) != 0:
            nomeSorteado = [random.choice(listaNiverCasamento)]
            db = get_db()
            # Remove o ganhador
            listaNiverCasamento.remove(nomeSorteado[0])
            proximo = ['True']
            try:
                listaDinamica.remove(nomeSorteado[0])
            except:
                pass
            try:
                listaGeral.remove(nomeSorteado[0])
            except:
                pass
            try:
                listaEnsaio.remove(nomeSorteado[0])
            except:
                pass

        jsonMontado = {
            'ConfAPI': bolas[0]['bolasDoBingoJson']['ConfAPI'],
            'ListaGeral': listaGeral,
            'ListaVisitante': bolas[0]['bolasDoBingoJson']['ListaVisitante'],
            'ListaMenor': bolas[0]['bolasDoBingoJson']['ListaMenor'],
            'ListaDinamica': listaDinamica,
            'ListaNiverCasamento': listaNiverCasamento,
            'ListaEnsaio': listaEnsaio,
            'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteado'],
            'NomeSorteado': nomeSorteado,
            'Opcao': ['aniversario'],
            'Proximo': proximo,
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
        }

        id = bolas[0]['id']
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()

        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'dinamica' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        listaGeral = bolas[0]['bolasDoBingoJson']['ListaGeral']
        listaDinamica = bolas[0]['bolasDoBingoJson']['ListaDinamica']
        listaNiverCasamento = bolas[0]['bolasDoBingoJson']['ListaNiverCasamento']
        listaEnsaio = bolas[0]['bolasDoBingoJson']['ListaEnsaio']
        nomeSorteado = bolas[0]['bolasDoBingoJson']['NomeSorteado']
        proximo = bolas[0]['bolasDoBingoJson']['Proximo']
        if len(listaDinamica) != 0:
            nomeSorteado = [random.choice(listaDinamica)]
            db = get_db()
            # Remove o ganhador
            listaDinamica.remove(nomeSorteado[0])
            proximo = ['True']
            try:
                listaNiverCasamento.remove(nomeSorteado[0])
            except:
                pass
            try:
                listaGeral.remove(nomeSorteado[0])
            except:
                pass
            try:
                listaEnsaio.remove(nomeSorteado[0])
            except:
                pass

        jsonMontado = {
            'ConfAPI': bolas[0]['bolasDoBingoJson']['ConfAPI'],
            'ListaGeral': listaGeral,
            'ListaVisitante': bolas[0]['bolasDoBingoJson']['ListaVisitante'],
            'ListaMenor': bolas[0]['bolasDoBingoJson']['ListaMenor'],
            'ListaDinamica': listaDinamica,
            'ListaNiverCasamento': listaNiverCasamento,
            'ListaEnsaio': listaEnsaio,
            'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteado'],
            'NomeSorteado': nomeSorteado,
            'Opcao': ['dinamica'],
            'Proximo': proximo,
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
        }

        id = bolas[0]['id']
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()

        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'ensaio' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        listaGeral = bolas[0]['bolasDoBingoJson']['ListaGeral']
        listaDinamica = bolas[0]['bolasDoBingoJson']['ListaDinamica']
        listaNiverCasamento = bolas[0]['bolasDoBingoJson']['ListaNiverCasamento']
        listaEnsaio = bolas[0]['bolasDoBingoJson']['ListaEnsaio']
        nomeSorteado = bolas[0]['bolasDoBingoJson']['NomeSorteado']
        proximo = bolas[0]['bolasDoBingoJson']['Proximo']
        if len(listaEnsaio) != 0:
            nomeSorteado = [random.choice(listaEnsaio)]
            db = get_db()
            # Remove o ganhador
            listaEnsaio.remove(nomeSorteado[0])
            proximo = ['True']
            try:
                listaNiverCasamento.remove(nomeSorteado[0])
            except:
                pass
            try:
                listaGeral.remove(nomeSorteado[0])
            except:
                pass
            try:
                listaDinamica.remove(nomeSorteado[0])
            except:
                pass

        jsonMontado = {
            'ConfAPI': bolas[0]['bolasDoBingoJson']['ConfAPI'],
            'ListaGeral': listaGeral,
            'ListaVisitante': bolas[0]['bolasDoBingoJson']['ListaVisitante'],
            'ListaMenor': bolas[0]['bolasDoBingoJson']['ListaMenor'],
            'ListaDinamica': listaDinamica,
            'ListaNiverCasamento': listaNiverCasamento,
            'ListaEnsaio': listaEnsaio,
            'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteado'],
            'NomeSorteado': nomeSorteado,
            'Opcao': ['ensaio'],
            'Proximo': proximo,
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
        }

        id = bolas[0]['id']
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()

        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'sim' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        listaGeral = bolas[0]['bolasDoBingoJson']['ListaGeral']
        listaDinamica = bolas[0]['bolasDoBingoJson']['ListaDinamica']
        listaNiverCasamento = bolas[0]['bolasDoBingoJson']['ListaNiverCasamento']
        listaEnsaio = bolas[0]['bolasDoBingoJson']['ListaEnsaio']
        nomeSorteado = bolas[0]['bolasDoBingoJson']['NomeSorteado']
        opcao = bolas[0]['bolasDoBingoJson']['Opcao']
        if opcao[0] in ['adultos/casados', 'dinamica', 'aniversario', 'ensaio']:
            # Remove o ganhador

            congregacao = nomeSorteado[0].split('|')[1]
            numCartao = nomeSorteado[0].split('|')[2]

            def removerPessoa(lista):
                for pessoa in lista:
                    if pessoa.split('|')[1] == congregacao and pessoa.split('|')[2] == numCartao:
                        lista.remove(pessoa)
                return lista

            try:
                listaEnsaio = removerPessoa(listaEnsaio)
            except:
                pass
            try:
                listaNiverCasamento = removerPessoa(listaNiverCasamento)
            except:
                pass
            try:
                listaGeral = removerPessoa(listaGeral)
            except:
                pass
            try:
                listaDinamica = removerPessoa(listaDinamica)
            except:
                pass

        db = get_db()
        jsonMontado = {
            'ConfAPI': bolas[0]['bolasDoBingoJson']['ConfAPI'],
            'ListaGeral': listaGeral,
            'ListaVisitante': bolas[0]['bolasDoBingoJson']['ListaVisitante'],
            'ListaMenor': bolas[0]['bolasDoBingoJson']['ListaMenor'],
            'ListaDinamica': listaDinamica,
            'ListaNiverCasamento': listaNiverCasamento,
            'ListaEnsaio': listaEnsaio,
            'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteadoAnterior'],
            'NomeSorteado': nomeSorteado,
            'Opcao': opcao,
            'Proximo': [''],
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
        }

        id = bolas[0]['id']
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()

        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'nao' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        db = get_db()
        jsonMontado = {
            'ConfAPI': bolas[0]['bolasDoBingoJson']['ConfAPI'],
            'ListaGeral': bolas[0]['bolasDoBingoJson']['ListaGeral'],
            'ListaVisitante': bolas[0]['bolasDoBingoJson']['ListaVisitante'],
            'ListaMenor': bolas[0]['bolasDoBingoJson']['ListaMenor'],
            'ListaDinamica': bolas[0]['bolasDoBingoJson']['ListaDinamica'],
            'ListaNiverCasamento': bolas[0]['bolasDoBingoJson']['ListaNiverCasamento'],
            'ListaEnsaio': bolas[0]['bolasDoBingoJson']['ListaEnsaio'],
            'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteadoAnterior'],
            'NomeSorteado': bolas[0]['bolasDoBingoJson']['NomeSorteado'],
            'Opcao': bolas[0]['bolasDoBingoJson']['Opcao'],
            'Proximo': [''],
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
        }

        id = bolas[0]['id']
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()

        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'reset' in request.form:
        confAPI = bolas[0]['bolasDoBingoJson']['ConfAPI'] if 'ConfAPI' in bolas[0]['bolasDoBingoJson'] else ['']
        db = get_db()
        jsonMontado = {
            'ConfAPI': confAPI,
            'ListaGeral': [],
            'ListaVisitante': [],
            'ListaMenor': [],
            'ListaDinamica': [],
            'ListaNiverCasamento': [],
            'ListaEnsaio': [],
            'MesSorteio': [''],
            'ListaMesSorteio': [],
            'NomeSorteadoAnterior': [''],
            'NomeSorteado': [''],
            'Opcao': [''],
            'Proximo': [''],
            'Ensaio': [''],
            'HabilitarEnsaio': ['']

        }
        id = (bolas[0]['id'] if 'id' in bolas[0] else g.user['id'])
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'config' in request.form:
        id = (bolas[0]['id'] if 'id' in bolas[0] else g.user['id'])
        return redirect(url_for(f'bingo.config', id=id))

    return render_template('bingo/index.html', bolas=bolas[0],
                           imagem=url_for('static', filename=imagem))


@bp.route('/<int:id>/configuracao', methods=('GET', 'POST'))
@login_required
def config(id):
    db = get_db()
    bolas = [dict(row) for row in db.execute(
        # 'SELECT p.id, author_id, bolasDoBingoJson, username'
        # 'SELECT p.id, title, body, created, author_id, username'
        # ' FROM post p JOIN user u ON p.author_id = u.id'
        # ' ORDER BY created DESC'
        f'SELECT p.id, author_id, bolasDoBingoJson, rankingJson, username'
        f' FROM bolasDoBingo p JOIN user u ON p.id = {id} AND u.id = {g.user["id"]}'
    ).fetchall()]
    if type(bolas[0]['bolasDoBingoJson']) == str:
        bolas[0]['bolasDoBingoJson'] = json.loads(bolas[0]['bolasDoBingoJson'].replace("'", '"'))
        # bolas[0]['bolasDoBingoJson'] = json.loads(bolas[0]['bolasDoBingoJson'])

    def carregarAPI(url: str):
        # if confAPI == ['']:
        connect = file_local()
        chaves = pd.DataFrame(connect['presenca']).keys().values
        listaChaves = [chave for chave in chaves]

        return listaChaves

    def file_local():
        if platform.system() == 'Windows':
            endereco = resource_local(platform.system()) + 'instance\\teste.json'
        else:
            endereco = resource_local(platform.system()) + 'instance/teste.json'
        print(endereco)
        with open(endereco, encoding='utf-8') as file:
            return json.load(file)

    def resource_local(_platform: str = platform.system(), folder: str = '') -> str:
        file_path = Path(__file__).parts
        index = 0
        for x in range(len(file_path), 0, -1):
            if file_path[x - 1].lower() == 'flaskr':
                index = x
                break
        file_path_final = ''
        for i in range(index):
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

    if 'ConfAPI' in bolas[0]['bolasDoBingoJson'] and 'ListaMesSorteio' in bolas[0]['bolasDoBingoJson']:
        if not bolas[0]['bolasDoBingoJson']['ListaMesSorteio']:
            listaChaves = carregarAPI(bolas[0]['bolasDoBingoJson']['ConfAPI'])
            bolas[0]['bolasDoBingoJson']['ListaMesSorteio'] = sorted(listaChaves)

    if request.method == 'POST' and 'carregar' in request.form:
        def pegarMes(mesAtual):
            if mesAtual == '':
                mesAtual = date.today().month
                if mesAtual in [1]:
                    mesAtual = 'janeiro'
                elif mesAtual in [2]:
                    mesAtual = 'fevereiro'
                elif mesAtual in [11]:
                    mesAtual = 'novembro'
                elif mesAtual in [12]:
                    mesAtual = 'dezembro'
                elif mesAtual in [3]:
                    mesAtual = 'março'
                elif mesAtual in [4]:
                    mesAtual = 'abril'
                elif mesAtual in [5]:
                    mesAtual = 'maio'
                elif mesAtual in [6]:
                    mesAtual = 'junho'
                elif mesAtual in [7]:
                    mesAtual = 'julho'
                elif mesAtual in [8]:
                    mesAtual = 'agosto'
                elif mesAtual in [9]:
                    mesAtual = 'setembro'
                else:
                    mesAtual = 'outubro'
            return mesAtual

        # Realizar chamada para o banco da API
        mes = [f"{pegarMes(request.form['carregar'].lower())}"]
        url = bolas[0]['bolasDoBingoJson']['ConfAPI'][0]
        # conect = requests.get(url + 'presenca/'+ meses + '.json')
        # conect = requests.get(url + '.json')
        # dados = pd.DataFrame(conect.json())

        connect = file_local()
        dados = pd.DataFrame(connect['presenca'][mes[0]])

        def juntar(df, coluna):
            df[coluna] = df[coluna].apply(str)
            return df

        def retornarIdade(nascimento):
            if nascimento != 'nan':
                nascimento = datetime.strptime(nascimento, "%d/%m/%Y").date()
                today = date.today()
                return str(today.year - nascimento.year - ((today.month,
                                                            today.day) < (nascimento.month,
                                                                          nascimento.day)))
            else:
                return nascimento

        def niverCasamento(casamento, mesTeste=0):
            if casamento not in ['nan', '']:
                if mesTeste == 0:
                    casamento = datetime.strptime(casamento, "%d/%m/%Y").date()
                    casamento = casamento.month
                    if casamento in [1, 2]:
                        casamento = 2
                    elif casamento in [11, 12]:
                        casamento = 11

                    if mes[0].lower().__contains__('janeiro') or\
                            mes[0].lower().__contains__('fevereiro'):
                        mesTeste = 2
                    elif mes[0].lower().__contains__('novembro') or \
                            mes[0].lower().__contains__('dezembro'):
                        mesTeste = 11
                    elif mes[0].lower().__contains__('marco'):
                        mesTeste = 3
                    elif mes[0].lower().__contains__('abril'):
                        mesTeste = 4
                    elif mes[0].lower().__contains__('maio'):
                        mesTeste = 5
                    elif mes[0].lower().__contains__('junho'):
                        mesTeste = 6
                    elif mes[0].lower().__contains__('julho'):
                        mesTeste = 7
                    elif mes[0].lower().__contains__('agosto'):
                        mesTeste = 8
                    elif mes[0].lower().__contains__('setembro'):
                        mesTeste = 9
                    elif mes[0].lower().__contains__('outubro'):
                        mesTeste = 10
                    else:
                        return niverCasamento(casamento, datetime.now().date().month)
                else:
                    if mesTeste in [1, 2]:
                        mesTeste = 2
                    elif mesTeste in [11, 12]:
                        mesTeste = 11
                if casamento == mesTeste:
                    return True
                else:
                    return False
            else:
                return False

        dados = dados.transpose()
        for column in dados:
            dados = juntar(dados, column)
        dados['numCartao'] = dados['idNumero'].apply(lambda x: x.split('/')[1])
        dados['congregacao'] = dados['idNumero'].apply(lambda x: x.split('/')[0])
        dados['juntosConjuge'] = (dados['nomeConjuge'] + '|' +
                                  dados['congregacao'] + '|' +
                                  dados['numCartao'] + '|' +
                                  dados['nascimentoConjuge'].apply(retornarIdade) + '|' +
                                  dados['dataCasamento'] + '|' +
                                  dados['nomeTitular'])
        dados['juntosTitular'] = (dados['nomeTitular'] + '|' +
                                  dados['congregacao'] + '|' +
                                  dados['numCartao'] + '|' +
                                  dados['nascimentoTitular'].apply(retornarIdade) + '|' +
                                  dados['dataCasamento'] + '|' +
                                  dados['nomeConjuge'])
        colunas = ['idNumero', 'nomeTitular', 'nomeConjuge', 'congregacao', 'numCartao', 'nascimentoConjuge',
                   'nascimentoTitular', 'dataCasamento']
        dados = dados.drop(columns=colunas)
        dados = dados.transpose()
        listaGeral = list()
        listaDinamica = list()
        listaVisitante = list()
        listaMenor = list()
        listaNiverCasamento = list()
        listaEnsaio = list()
        for column in dados:
            for index in dados[column]:
                index = str(index).removesuffix('nan')
                if str(index) != str(index).removesuffix('nan|'):
                    index = str(index).removesuffix('nan|') + '|'
                if str(index) == str(index).removeprefix('nan|'):
                    if str(index).split('|')[1].lower() == 'visitante':
                        listaVisitante.append(index)
                    elif int(str(index).split('|')[3]) < 18:
                        listaMenor.append(index)
                    else:
                        listaGeral.append(index)
                        if niverCasamento(str(index).split('|')[4]):
                            listaNiverCasamento.append(index)
                        if mes[0].lower().__contains__('ensaio'):
                            listaEnsaio.append(index)

        # Colocar os dados adquiridos na tabela correta
        db = get_db()
        jsonMontado = {
            'ConfAPI': bolas[0]['bolasDoBingoJson']['ConfAPI'],
            'ListaGeral': listaGeral,
            'ListaVisitante': listaVisitante,
            'ListaMenor': listaMenor,
            'ListaDinamica': listaDinamica,
            'ListaNiverCasamento': listaNiverCasamento,
            'ListaEnsaio': listaEnsaio,
            'MesSorteio': mes,
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': [''],
            'NomeSorteado': [''],
            'Opcao': [''],
            'Proximo': [''],
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
        }
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()

        return redirect(url_for('bingo.config', id=id))

    if request.method == 'POST' and 'dinamica' in request.form:
        # Realizar chamada para o banco da API
        congregacao = request.form['dinamica'].split('|')[0]
        NumCartao = request.form['dinamica'].split('|')[1]
        listaGeral = bolas[0]['bolasDoBingoJson']['ListaGeral']
        listaDinamica = set(bolas[0]['bolasDoBingoJson']['ListaDinamica'])
        ultimoItem = ''
        for item in listaGeral:
            if item.split('|')[1] == congregacao and item.split('|')[2] == NumCartao:
                listaDinamica.add(item)
                ultimoItem = item

        if len(listaDinamica) % 2 != 0:
            listaDinamica.remove(ultimoItem)

        # Colocar os dados adquiridos na tabela correta
        confAPI = bolas[0]['bolasDoBingoJson']['ConfAPI']
        db = get_db()
        jsonMontado = {
            'ConfAPI': confAPI,
            'ListaGeral': listaGeral,
            'ListaVisitante': bolas[0]['bolasDoBingoJson']['ListaVisitante'],
            'ListaMenor': bolas[0]['bolasDoBingoJson']['ListaMenor'],
            'ListaDinamica': list(listaDinamica),
            'ListaNiverCasamento': bolas[0]['bolasDoBingoJson']['ListaNiverCasamento'],
            'ListaEnsaio': bolas[0]['bolasDoBingoJson']['ListaEnsaio'],
            'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteadoAnterior'],
            'NomeSorteado': bolas[0]['bolasDoBingoJson']['NomeSorteado'],
            'Opcao': [''],
            'Proximo': [''],
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
        }
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()

        return redirect(url_for('bingo.config', id=id))

    # if request.method == 'POST' and 'ensaio' in request.form:
    #     # Realizar chamada para o banco da API
    #
    #     congregacao = request.form['ensaio'].split('|')[0]
    #     NumCartao = request.form['ensaio'].split('|')[1]
    #     listaGeral = bolas[0]['bolasDoBingoJson']['ListaGeral']
    #     listaEnsaio = set(bolas[0]['bolasDoBingoJson']['ListaEnsaio'])
    #     for item in listaGeral:
    #         if item.split('|')[1] == congregacao and item.split('|')[2] == NumCartao:
    #             listaEnsaio.add(item)
    #
    #     # Colocar os dados adquiridos na tabela correta
    #     confAPI = bolas[0]['bolasDoBingoJson']['ConfAPI']
    #     db = get_db()
    #     jsonMontado = {
    #         'ConfAPI': confAPI,
    #         'ListaGeral': listaGeral,
    #         'ListaVisitante': bolas[0]['bolasDoBingoJson']['ListaVisitante'],
    #         'ListaMenor': bolas[0]['bolasDoBingoJson']['ListaMenor'],
    #         'ListaDinamica': bolas[0]['bolasDoBingoJson']['ListaDinamica'],
    #         'ListaNiverCasamento': bolas[0]['bolasDoBingoJson']['ListaNiverCasamento'],
    #         'ListaEnsaio': list(listaEnsaio),
    #         'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
    #         'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
    #         'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteadoAnterior'],
    #         'NomeSorteado': bolas[0]['bolasDoBingoJson']['NomeSorteado'],
    #         'Opcao': [''],
    #         'Proximo': [''],
    #         'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
    #         'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
    #     }
    #     db.execute(
    #         'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
    #         ' WHERE id = ?',
    #         (str(jsonMontado),
    #          g.user['id'], id)
    #     )
    #     db.commit()
    #
    #     return redirect(url_for('bingo.config', id=id))

    if request.method == 'POST' and 'confAPI' in request.form:
        confAPI = request.form['confAPI']

        ### carregar chamada das chaves
        listaChaves = carregarAPI(confAPI)

        db = get_db()
        jsonMontado = {
            'ConfAPI': [confAPI],
            'ListaGeral': [],
            'ListaVisitante': [],
            'ListaMenor': [],
            'ListaDinamica': [],
            'ListaNiverCasamento': [],
            'ListaEnsaio': [],
            'MesSorteio': [''],
            'ListaMesSorteio': sorted(listaChaves),
            'NomeSorteadoAnterior': [''],
            'NomeSorteado': [''],
            'Opcao': [''],
            'Proximo': [''],
            'Ensaio': [''],
            'HabilitarEnsaio': ['']
        }
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()

        return redirect(url_for('bingo.config', id=id))

    if request.method == 'POST' and 'cancel' in request.form:
        db = get_db()
        list().__len__()
        jsonMontado = {
            'ConfAPI': bolas[0]['bolasDoBingoJson']['ConfAPI'],
            'ListaGeral': bolas[0]['bolasDoBingoJson']['ListaGeral'],
            'ListaVisitante': bolas[0]['bolasDoBingoJson']['ListaVisitante'],
            'ListaMenor': bolas[0]['bolasDoBingoJson']['ListaMenor'],
            'ListaDinamica': bolas[0]['bolasDoBingoJson']['ListaDinamica'],
            'ListaNiverCasamento': bolas[0]['bolasDoBingoJson']['ListaNiverCasamento'],
            'ListaEnsaio': bolas[0]['bolasDoBingoJson']['ListaEnsaio'],
            'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteadoAnterior'],
            'NomeSorteado': bolas[0]['bolasDoBingoJson']['NomeSorteado'],
            'Opcao': bolas[0]['bolasDoBingoJson']['Opcao'],
            'Proximo': bolas[0]['bolasDoBingoJson']['Proximo'],
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': bolas[0]['bolasDoBingoJson']['HabilitarEnsaio']
        }
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'habilitarEnsaio' in request.form:
        db = get_db()
        jsonMontado = {
            'ConfAPI': bolas[0]['bolasDoBingoJson']['ConfAPI'],
            'ListaGeral': bolas[0]['bolasDoBingoJson']['ListaGeral'],
            'ListaVisitante': bolas[0]['bolasDoBingoJson']['ListaVisitante'],
            'ListaMenor': bolas[0]['bolasDoBingoJson']['ListaMenor'],
            'ListaDinamica': bolas[0]['bolasDoBingoJson']['ListaDinamica'],
            'ListaNiverCasamento': bolas[0]['bolasDoBingoJson']['ListaNiverCasamento'],
            'ListaEnsaio': bolas[0]['bolasDoBingoJson']['ListaEnsaio'],
            'MesSorteio': bolas[0]['bolasDoBingoJson']['MesSorteio'],
            'ListaMesSorteio': bolas[0]['bolasDoBingoJson']['ListaMesSorteio'],
            'NomeSorteadoAnterior': bolas[0]['bolasDoBingoJson']['NomeSorteadoAnterior'],
            'NomeSorteado': bolas[0]['bolasDoBingoJson']['NomeSorteado'],
            'Opcao': bolas[0]['bolasDoBingoJson']['Opcao'],
            'Proximo': bolas[0]['bolasDoBingoJson']['Proximo'],
            'Ensaio': bolas[0]['bolasDoBingoJson']['Ensaio'],
            'HabilitarEnsaio': ['true'] if request.form['habilitarEnsaio'] == 'Habilitar' else ['']
        }
        db.execute(
            'UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ?'
            ' WHERE id = ?',
            (str(jsonMontado),
             g.user['id'], id)
        )
        db.commit()
        return redirect(url_for('bingo.config', id=id))

    print(bolas[0])
    return render_template('bingo/configuracao.html', bolas=bolas[0])


if __name__ == '__main__':
    # BolasDoBingo = list()
    # # IniciarBingo(BolasDoBingo)
    # # print(BolasDoBingo)
    # desejo = 'S'
    # BolasSorteadas = list()
    # BolaEscolhida = 0
    # while desejo.upper() == 'S':
    #     print('Quantidade de bolas restantes: ' + str(len(BolasDoBingo)))
    #     BolaEscolhida = random.choice(BolasDoBingo)
    #     print(BolaEscolhida)
    #     BolasSorteadas.append(BolaEscolhida)
    #     desejo = input('Deseja continuar(S/N)? ')
    #     while True:
    #         if desejo.upper() == 'S' or desejo.upper() == 'N':
    #             break
    #         else:
    #             desejo = input("Digite 'S' ou 'N':  ")
    #     # ImprimirQuadro(BolasSorteadas)
    #     BolasDoBingo.remove(BolaEscolhida)
    # print('O último número foi: ' + str(BolaEscolhida))
    def file_local():
        if platform.system() == 'Windows':
            endereco = resource_local(platform.system()) + 'instance\\teste.json'
        else:
            endereco = resource_local(platform.system()) + 'instance/teste.json'
        with open(endereco, encoding='utf-8') as file:
            return json.load(file)

    def resource_local(_platform: str = platform.system(), folder: str = '') -> str:
        file_path = Path(__file__).parts
        index = 0
        for x in range(len(file_path), 0, -1):
            if file_path[x - 1].lower() == 'flaskr':
                index = x
                break
        file_path_final = ''
        for i in range(index):
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
        if _platform == 'Darwin':
            file_path_final += '/../'
        if _platform == 'Windows':
            file_path_final += '\\..\\'
        print()
        print()
        print(file_path_final)
        print()
        print()
        if folder != '':
            if _platform == 'Darwin':
                return file_path_final + folder + '/'
            if _platform == 'Windows':
                return file_path_final + folder + '\\'
        return file_path_final

    print(resource_local())
