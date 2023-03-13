from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)
from auth import login_required
import random
import pandas as pd
import platform
from utils.connect import carregar_api, carregar_chaves_api, insert_db_vazio, \
    select_dict, update_db
from utils.dates import pegar_mes, retornar_idade, niver_casamento
from utils.json_db import json_montado
from utils.converter import converter_str
from enums import nomes_colunas, meses
from datetime import datetime
bp = Blueprint('bingo', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    # print(g.user['username'])
    # if len(BolasDoBingo) == 0:
    #     BolasDoBingo, _ = '', ''
    try:
        bolas = select_dict(g)
    except Exception as e:
        print('Problema encontrado em: ', e)
        insert_db_vazio(g)
        update_db(g, json_montado())
        bolas = select_dict(g)
        # return render_template('bingo/index.html')

    # if len(bolas) == 0:
    #     insert_db_vazio(db, g)
    #     print()
    #     print()
    #     print(bolas)
    #     print()
    #     print()

    if request.method == 'POST' and 'geral' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaGeral = bolasDoBingoJson.ListaGeral
        listaDinamica = bolasDoBingoJson.ListaDinamica
        listaNiverCasamento = bolasDoBingoJson.ListaNiverCasamento
        listaEnsaio = bolasDoBingoJson.ListaEnsaio
        nomeSorteado = bolasDoBingoJson.NomeSorteado
        proximo = bolasDoBingoJson.Proximo
        if len(listaGeral) != 0:
            nomeSorteado = [random.choice(listaGeral)]
            # Remove o ganhador
            listaGeral.remove(nomeSorteado[0])
            proximo = ['True']
            try:
                listaDinamica.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Dinâmica não tem o nome sorteado. Erro: ', e)
                pass
            try:
                listaNiverCasamento.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Aniversário não tem o nome sorteado. Erro: ', e)
                pass
            try:
                listaEnsaio.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Ensaio não tem o nome sorteado. Erro: ', e)
                pass

        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_geral=listaGeral,
            lista_dinamica=listaDinamica,
            lista_niver_casamento=listaNiverCasamento,
            lista_ensaio=listaEnsaio,
            nome_sorteado_anterior=bolasDoBingoJson.NomeSorteado,
            nome_sorteado=nomeSorteado,
            opcao=['adultos/casados'],
            proximo=proximo
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'jovens' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaMenor = bolasDoBingoJson.ListaMenor
        nomeSorteado = bolasDoBingoJson.NomeSorteado
        proximo = bolasDoBingoJson.Proximo
        if len(listaMenor) != 0:
            nomeSorteado = [random.choice(listaMenor)]
            # Remove o ganhador
            listaMenor.remove(nomeSorteado[0])
            proximo = ['True']

        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_menor=listaMenor,
            nome_sorteado_anterior=bolasDoBingoJson.NomeSorteado,
            nome_sorteado=nomeSorteado,
            opcao=['jovens'],
            proximo=proximo
        )

        update_db(g, jsonMontado)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'visitantes' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaVisitante = bolasDoBingoJson.ListaVisitante
        nomeSorteado = bolasDoBingoJson.NomeSorteado
        proximo = bolasDoBingoJson.Proximo
        if len(listaVisitante) != 0:
            nomeSorteado = [random.choice(listaVisitante)]
            # Remove o ganhador
            listaVisitante.remove(nomeSorteado[0])
            proximo = ['True']

        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_visitante=listaVisitante,
            nome_sorteado_anterior=bolasDoBingoJson.NomeSorteado,
            nome_sorteado=nomeSorteado,
            opcao=['visitantes'],
            proximo=proximo
        )

        update_db(g, jsonMontado)

        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'aniversario' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaGeral = bolasDoBingoJson.ListaGeral
        listaDinamica = bolasDoBingoJson.ListaDinamica
        listaNiverCasamento = bolasDoBingoJson.ListaNiverCasamento
        listaEnsaio = bolasDoBingoJson.ListaEnsaio
        nomeSorteado = bolasDoBingoJson.NomeSorteado
        proximo = bolasDoBingoJson.Proximo
        if len(listaNiverCasamento) != 0:
            nomeSorteado = [random.choice(listaNiverCasamento)]
            # Remove o ganhador
            listaNiverCasamento.remove(nomeSorteado[0])
            proximo = ['True']
            try:
                listaDinamica.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Dinâmica não tem o nome sorteado. Erro: ', e)
                pass
            try:
                listaGeral.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Geral não tem o nome sorteado. Erro: ', e)
                pass
            try:
                listaEnsaio.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Ensaio não tem o nome sorteado. Erro: ', e)
                pass

        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_geral=listaGeral,
            lista_dinamica=listaDinamica,
            lista_niver_casamento=listaNiverCasamento,
            lista_ensaio=listaEnsaio,
            nome_sorteado_anterior=bolasDoBingoJson.NomeSorteado,
            nome_sorteado=nomeSorteado,
            opcao=['aniversario'],
            proximo=proximo
        )

        update_db(g, jsonMontado)

        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'dinamica' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaGeral = bolasDoBingoJson.ListaGeral
        listaDinamica = bolasDoBingoJson.ListaDinamica
        listaNiverCasamento = bolasDoBingoJson.ListaNiverCasamento
        listaEnsaio = bolasDoBingoJson.ListaEnsaio
        nomeSorteado = bolasDoBingoJson.NomeSorteado
        proximo = bolasDoBingoJson.Proximo
        if len(listaDinamica) != 0:
            nomeSorteado = [random.choice(listaDinamica)]
            # Remove o ganhador
            listaDinamica.remove(nomeSorteado[0])
            proximo = ['True']
            try:
                listaNiverCasamento.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Aniversário não tem o nome sorteado. Erro: ', e)
                pass
            try:
                listaGeral.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Geral não tem o nome sorteado. Erro: ', e)
                pass
            try:
                listaEnsaio.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Ensaio não tem o nome sorteado. Erro: ', e)
                pass

        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_geral=listaGeral,
            lista_dinamica=listaDinamica,
            lista_niver_casamento=listaNiverCasamento,
            lista_ensaio=listaEnsaio,
            nome_sorteado_anterior=bolasDoBingoJson.NomeSorteado,
            nome_sorteado=nomeSorteado,
            opcao=['dinamica'],
            proximo=proximo
        )

        update_db(g, jsonMontado)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'ensaio' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaGeral = bolasDoBingoJson.ListaGeral
        listaDinamica = bolasDoBingoJson.ListaDinamica
        listaNiverCasamento = bolasDoBingoJson.ListaNiverCasamento
        listaEnsaio = bolasDoBingoJson.ListaEnsaio
        nomeSorteado = bolasDoBingoJson.NomeSorteado
        proximo = bolasDoBingoJson.Proximo
        if len(listaEnsaio) != 0:
            nomeSorteado = [random.choice(listaEnsaio)]
            # Remove o ganhador
            listaEnsaio.remove(nomeSorteado[0])
            proximo = ['True']
            try:
                listaNiverCasamento.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Aniversário não tem o nome sorteado. Erro: ', e)
                pass
            try:
                listaGeral.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Geral não tem o nome sorteado. Erro: ', e)
                pass
            try:
                listaDinamica.remove(nomeSorteado[0])
            except Exception as e:
                print('Lista Dinâmica não tem o nome sorteado. Erro: ', e)
                pass

        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_geral=listaGeral,
            lista_dinamica=listaDinamica,
            lista_niver_casamento=listaNiverCasamento,
            lista_ensaio=listaEnsaio,
            nome_sorteado_anterior=bolasDoBingoJson.NomeSorteado,
            nome_sorteado=nomeSorteado,
            opcao=['ensaio'],
            proximo=proximo
        )

        update_db(g, jsonMontado)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'sim' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaGeral = bolasDoBingoJson.ListaGeral
        listaDinamica = bolasDoBingoJson.ListaDinamica
        listaNiverCasamento = bolasDoBingoJson.ListaNiverCasamento
        listaEnsaio = bolasDoBingoJson.ListaEnsaio
        nomeSorteado = bolasDoBingoJson.NomeSorteado
        opcao = bolasDoBingoJson.Opcao
        if opcao[0] in ['adultos/casados',
                        'dinamica', 'aniversario', 'ensaio']:
            # Remove o ganhador

            congregacao = nomeSorteado[0].split('|')[1]
            numCartao = nomeSorteado[0].split('|')[2]

            def remover_pessoa(lista):
                for pessoa in lista:
                    if pessoa.split('|')[1] == congregacao and \
                            pessoa.split('|')[2] == numCartao:
                        lista.remove(pessoa)
                return lista

            try:
                listaEnsaio = remover_pessoa(listaEnsaio)
            except Exception as e:
                print('Lista Ensaio não tem o nome sorteado. Erro: ', e)
                pass
            try:
                listaNiverCasamento = remover_pessoa(listaNiverCasamento)
            except Exception as e:
                print('Lista Aniversário não tem o nome sorteado. Erro: ', e)
                pass
            try:
                listaGeral = remover_pessoa(listaGeral)
            except Exception as e:
                print('Lista Geral não tem o nome sorteado. Erro: ', e)
                pass
            try:
                listaDinamica = remover_pessoa(listaDinamica)
            except Exception as e:
                print('Lista Dinâmica não tem o nome sorteado. Erro: ', e)
                pass

        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_geral=listaGeral,
            lista_dinamica=listaDinamica,
            lista_niver_casamento=listaNiverCasamento,
            lista_ensaio=listaEnsaio,
            nome_sorteado_anterior=bolasDoBingoJson.NomeSorteadoAnterior,
            nome_sorteado=nomeSorteado,
            proximo=['']
        )

        update_db(g, jsonMontado)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'nao' in request.form:
        # print('Bolas do Bingo:', BolasDoBingo)
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            proximo=['']
        )

        update_db(g, jsonMontado)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'reset' in request.form:
        confAPI = bolas[0].bolasDoBingoJson.ConfAPI
        jsonMontado = json_montado(conf_api=confAPI)
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'config' in request.form:
        _id = (bolas[0].id if 'id' in bolas[0] else g.user['id'])
        return redirect(url_for(f'bingo.config', _id=_id))

    print(bolas[0])
    return render_template('bingo/index.html', bolas=bolas[0])


@bp.route('/<int:_id>/configuracao', methods=('GET', 'POST'))
@login_required
def config(_id):
    bolas = select_dict(g)

    bolasDoBingoJson = bolas[0].bolasDoBingoJson
    if not bolasDoBingoJson.ListaMesSorteio:
        listaChaves = carregar_chaves_api(bolasDoBingoJson.ConfAPI[0])
        bolasDoBingoJson.ListaMesSorteio = sorted(listaChaves)

    if request.method == 'POST' and 'carregar' in request.form:

        # Realizar chamada para o banco da API
        mes = [f"{pegar_mes(request.form['carregar'].lower())}"]
        ConfAPI = bolasDoBingoJson.ConfAPI[0]
        ConfAPI = carregar_api(ConfAPI)
        try:
            dados = pd.DataFrame(ConfAPI['presenca'][mes[0]])
        except KeyError:
            return redirect(url_for('bingo.config', _id=_id))

        # print('dados: ', dados)
        # print('keys: ', dados.keys())
        # print('dados.transpose: ', dados.transpose())
        dados = dados.transpose()
        colunas = ['idNumero', 'nomeTitular', 'nomeConjuge', 'congregacao',
                   'numCartao', 'nascimentoConjuge', 'nascimentoTitular',
                   'dataCasamento', 'estadoCivil']
        for column in colunas:
            if column not in dados:
                dados[column] = ''
        # print('keys: ', dados.keys())
        for column in dados:
            dados = converter_str(dados, column)
        # print(dados)
        dados['numCartao'] = dados['idNumero'].apply(
            lambda x: x.split('/')[1])
        dados['congregacao'] = dados['idNumero'].apply(
            lambda x: x.split('/')[0])
        # dados.to_excel('pessoas.xlsx')
        dados['juntosConjuge'] = (dados['nomeConjuge'] + '|' +
                                  dados['congregacao'] + '|' +
                                  dados['numCartao'] + '|' +
                                  dados['nascimentoConjuge'].apply(
                                      retornar_idade) + '|' +
                                  dados['dataCasamento'] + '|' +
                                  dados['estadoCivil'] + '|' +
                                  dados['nomeTitular'])
        dados['juntosConjuge'] = dados['juntosConjuge'].apply(
            lambda x: f'nan{x}' if x.split('|')[0] == '' else x)
        dados['juntosTitular'] = (dados['nomeTitular'] + '|' +
                                  dados['congregacao'] + '|' +
                                  dados['numCartao'] + '|' +
                                  dados['nascimentoTitular'].apply(
                                      retornar_idade) + '|' +
                                  dados['dataCasamento'] + '|' +
                                  dados['estadoCivil'] + '|' +
                                  dados['nomeConjuge'])
        dados['juntosTitular'] = dados['juntosTitular'].apply(
            lambda x: f'nan{x}' if x.split('|')[0] == '' else x)
        dados = dados.drop(columns=colunas)
        dados = dados.transpose()
        listaGeral = list()
        listaDinamica = list()
        listaVisitante = list()
        listaMenor = list()
        listaNiverCasamento = list()
        listaEnsaio = list()
        for column in dados:
            for _index in dados[column]:
                _index = str(_index).removesuffix('nan')
                if str(_index) != str(_index).removesuffix('nan|'):
                    _index = str(_index).removesuffix('nan|') + '|'
                if str(_index) == str(_index).removeprefix('nan|'):
                    if str(_index).split('|')[1].lower().__contains__(
                            'visitante'):
                        listaVisitante.append(_index)
                    elif int(str(_index).split('|')[3]) < 18 or \
                            (int(str(_index).split('|')[3]) < 35 and
                             str(_index).split('|')[5].lower() == 'solteiro'):
                        listaMenor.append(_index)
                    else:
                        listaGeral.append(_index)
                        if niver_casamento(str(_index).split('|')[4], mes):
                            listaNiverCasamento.append(_index)
                        if mes[0].lower().__contains__('ensaio'):
                            listaEnsaio.append(_index)

        # Colocar os dados adquiridos na tabela correta
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_geral=listaGeral,
            lista_visitante=listaVisitante,
            lista_menor=listaMenor,
            lista_dinamica=listaDinamica,
            lista_niver_casamento=listaNiverCasamento,
            lista_ensaio=listaEnsaio,
            mes_sorteio=mes,
            nome_sorteado_anterior=[''],
            nome_sorteado=[''],
            opcao=[''],
            proximo=['']
        )

        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'dinamica' in request.form:
        # Realizar chamada para o banco da API
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        congregacao = request.form['dinamica'].split('|')[0]
        NumCartao = request.form['dinamica'].split('|')[1]
        listaGeral = bolasDoBingoJson.ListaGeral
        listaDinamica = set(bolasDoBingoJson.ListaDinamica)
        ultimoItem = ''
        for item in listaGeral:
            if item.split('|')[1] == congregacao and \
                    item.split('|')[2] == NumCartao:
                listaDinamica.add(item)
                ultimoItem = item

        if len(listaDinamica) % 2 != 0:
            listaDinamica.remove(ultimoItem)

        # Colocar os dados adquiridos na tabela correta
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_geral=listaGeral,
            lista_dinamica=list(listaDinamica),
            opcao=[''],
            proximo=['']
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'menor_solteiro' in request.form:
        # Realizar chamada para o banco da API
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        congregacao = request.form['menor_solteiro'].split('|')[0]
        NumCartao = request.form['menor_solteiro'].split('|')[1]
        listaGeral = bolasDoBingoJson.ListaGeral
        listaMenor = bolasDoBingoJson.ListaMenor
        ultimoItem = ''
        for item in listaMenor:
            if item.split('|')[1] == congregacao and \
                    item.split('|')[2] == NumCartao:
                listaGeral.append(item)
                ultimoItem = item

        listaMenor.remove(ultimoItem)

        # Colocar os dados adquiridos na tabela correta
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_geral=listaGeral,
            lista_menor=list(listaMenor),
            opcao=[''],
            proximo=['']
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'report' in request.form:
        ConfAPI = bolas[0].bolasDoBingoJson.ConfAPI[0]
        caminho = request.form['report']
        ConfAPI = carregar_api(ConfAPI)
        usuarios = ConfAPI['usuarios']
        presenca = ConfAPI['presenca']
        # print(pd.DataFrame(usuarios))
        dados = pd.DataFrame(usuarios).transpose()
        # dados = dados.loc[:, ['idNumero', 'nomeTitular', 'nomeConjuge']]
        dados['congregacao'] = dados['idNumero'].apply(
            lambda x: x.split('/')[0])
        dados['idNumero'] = dados['idNumero'].apply(
            lambda x: x.split('/')[1])
        dados = dados.loc[:, nomes_colunas.COLUNAS_REPORT]

        dados_presenca = pd.DataFrame(presenca)
        if platform.system() == 'Windows':
            caminho = caminho + '\\'
        else:
            caminho = caminho + '/'

        def pdf_writer(_writer=caminho + 'report.xlsx'):
            pd.DataFrame(dados).to_excel(_writer,
                                         sheet_name="Dados_usuarios")
            mes_maximo = list()

            for indice in meses.DICT_NUM_MES:
                if indice <= datetime.now().month and indice not in [1, 12]:
                    mes_maximo.append(meses.DICT_NUM_MES[indice])

            for _mes in dados_presenca:
                if _mes in mes_maximo:
                    presenca_transp = pd.DataFrame(presenca[_mes]).transpose()
                    presenca_transp['congregacao'] = \
                        presenca_transp['idNumero'].apply(
                            lambda x: x.split('/')[0])
                    presenca_transp['idNumero'] = \
                        presenca_transp['idNumero'].apply(
                            lambda x: x.split('/')[1])
                    presenca_transp = presenca_transp.loc[
                                      :, nomes_colunas.COLUNAS_MESES_REPORT]
                    presenca_transp = presenca_transp.merge(dados,
                                                            on=['congregacao',
                                                                'idNumero'],
                                                            how='left',
                                                            suffixes=(
                                                                '_left',
                                                                '_right')
                                                            )
                    for index, value in pd.DataFrame(presenca_transp).iterrows():
                        presenca_transp.loc[index, ['estadoCivil']] = \
                            value['estadoCivil_right']
                        presenca_transp.loc[index, ['dataCasamento']] = \
                            value['dataCasamento_right']
                        presenca_transp.loc[index, ['nomeTitular']] = \
                            value['nomeTitular_left']
                        presenca_transp.loc[index, ['nomeConjuge']] = \
                            value['nomeConjuge_left']
                        if str(value['nomeTitular_left']).lower() != 'nan':
                            presenca_transp.loc[index,
                                                ['nascimentoTitular']] = \
                                value['nascimentoTitular_right']
                            presenca_transp.loc[index,
                                                ['sexoTitular']] = \
                                value['sexoTitular']
                        else:
                            presenca_transp.loc[
                                index, ['nascimentoTitular']] = \
                                value['nascimentoTitular_left']
                            presenca_transp.loc[
                                index, ['sexoTitular']] = ''
                        if str(value['nomeConjuge_left']).lower() != 'nan':
                            presenca_transp.loc[index,
                                                ['nascimentoConjuge']] = \
                                value['nascimentoConjuge_right']
                            presenca_transp.loc[index,
                                                ['sexoConjuge']] = \
                                value['sexoConjuge']
                        else:
                            presenca_transp.loc[
                                index, ['nascimentoConjuge']] = \
                                value['nascimentoConjuge_left']
                            presenca_transp.loc[index,
                                                ['sexoConjuge']] = ''
                        # if index == 161:
                        #     print(presenca_transp.loc[index])
                    presenca_transp = presenca_transp.loc[
                                      :, nomes_colunas.COLUNAS_MERGE_REPORT]
                    presenca_transp.to_excel(_writer, sheet_name=_mes)
        try:
            with pd.ExcelWriter(caminho + 'report.xlsx', mode='a',
                                if_sheet_exists="replace") as writer:
                pdf_writer(writer)
        except FileNotFoundError:
            with pd.ExcelWriter(caminho + 'report.xlsx') as writer:
                pdf_writer(writer)
            # with pd.ExcelWriter(caminho + 'report.xlsx', mode='a',
            #                     if_sheet_exists="replace") as writer:
            #     pdf_writer(writer)

        print()
        print(f'Arquivo exportado em: {caminho}report.xlsx')
        print()
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'confAPI' in request.form:
        confAPI = request.form['confAPI']

        # # carregar chamada das chaves
        listaChaves = carregar_chaves_api(confAPI)

        jsonMontado = json_montado(
            conf_api=[confAPI],
            lista_mes_sorteio=sorted(listaChaves)
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'cancel' in request.form:
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson
        )

        update_db(g, jsonMontado)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'habilitarEnsaio' in request.form:
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            habilitar_ensaio=['true' if
                              request.form['habilitarEnsaio'] ==
                              'Habilitar' else '']
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    print(bolas[0])
    return render_template('bingo/configuracao.html', bolas=bolas[0])


if __name__ == '__main__':
    print()
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
    # def file_local():
    #     if platform.system() == 'Windows':
    #         endereco = resource_local(platform.system()) +
    #         'instance\\teste.json'
    #     else:
    #         endereco = resource_local(platform.system()) +
    #         'instance/teste.json'
    #     with open(endereco, encoding='utf-8') as file:
    #         return json.load(file)
    #
    # def resource_local(_platform: str = platform.system(),
    #                    folder: str = '') -> str:
    #     file_path = Path(__file__).parts
    #     index = 0
    #     for x in range(len(file_path), 0, -1):
    #         if file_path[x - 1].lower() == 'flaskr':
    #             index = x
    #             break
    #     file_path_final = ''
    #     for i in range(index):
    #         if _platform == 'Darwin':
    #             if file_path[i] == '/':
    #                 file_path_final += file_path[i]
    #             else:
    #                 file_path_final += file_path[i] + '/'
    #         if _platform == 'Windows':
    #             if file_path[i].__contains__('\\'):
    #                 file_path_final += file_path[i]
    #             else:
    #                 file_path_final += file_path[i] + '\\'
    #     if _platform == 'Darwin':
    #         file_path_final += '/../'
    #     if _platform == 'Windows':
    #         file_path_final += '\\..\\'
    #     print()
    #     print()
    #     print(file_path_final)
    #     print()
    #     print()
    #     if folder != '':
    #         if _platform == 'Darwin':
    #             return file_path_final + folder + '/'
    #         if _platform == 'Windows':
    #             return file_path_final + folder + '\\'
    #     return file_path_final
    #
    # print(resource_local())
