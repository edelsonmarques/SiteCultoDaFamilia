from flask import (
    Blueprint, g, redirect, render_template, request, url_for, send_file
)
from auth import login_required
import pandas as pd
import platform
from actions.general import remove_people, remove_congregacao, \
    remove_historico, remove_lista
from utils.connect import carregar_api, carregar_chaves_api, insert_db_vazio, \
    select_dict, update_db
from utils.dates import pegar_mes, retornar_idade, niver_casamento
from utils.json_db import json_montado
from utils.converter import converter_str
from enums import nomes_colunas, meses, congregacoes, actions, events
from utils.print_class import print_class
from datetime import datetime
import io
bp = Blueprint('bingo', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    # print(g.user['username'])
    # if len(BolasDoBingo) == 0:
    #     BolasDoBingo, _ = '', ''
    _print = False
    try:
        bolas = select_dict(g)
    except Exception as e:
        if _print:
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
        remove_people(g, bolas, actions.GERAL)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.JOVENS in request.form:
        remove_people(g, bolas, actions.JOVENS)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.VISITANTES in request.form:
        remove_people(g, bolas, actions.VISITANTES)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.ANIVERSARIO in request.form:
        remove_people(g, bolas, actions.ANIVERSARIO)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.DINAMICA in request.form:
        if request.form[actions.DINAMICA] == 'Dinâmica':
            remove_people(g, bolas, actions.DINAMICA)
        elif request.form[actions.DINAMICA] == \
                f'Dinâmica - {events.evento()[0]["plural"]}':
            remove_people(g, bolas, actions.DINAMICA_MAE_PAI)
        elif request.form[actions.DINAMICA] == \
                f'Dinâmica - {events.evento("Pais")[0]["plural"]}':
            remove_people(g, bolas, actions.DINAMICA_MAE_PAI)
        elif request.form[actions.DINAMICA] == \
                f'Dinâmica - {events.evento()[1]["plural"]}' or \
                request.form[actions.DINAMICA] == \
                f'Dinâmica - {events.evento("Avós")[1]["plural"]}':
            remove_people(g, bolas, actions.DINAMICA_FILHOS_PAIS)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.ENSAIO in request.form:
        remove_people(g, bolas, actions.ENSAIO)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.ALAMEDA in request.form:
        remove_people(g, bolas, actions.ALAMEDA)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.JDCOPA1 in request.form:
        remove_people(g, bolas, actions.JDCOPA1)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.JDCOPA2 in request.form:
        remove_people(g, bolas, actions.JDCOPA2)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.ND1 in request.form:
        remove_people(g, bolas, actions.ND1)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.ND2 in request.form:
        remove_people(g, bolas, actions.ND2)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.PIEDADE in request.form:
        remove_people(g, bolas, actions.PIEDADE)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and actions.VENEZA4 in request.form:
        remove_people(g, bolas, actions.VENEZA4)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'reset' in request.form:
        confAPI = bolas[0].bolasDoBingoJson.ConfAPI
        historicoSorteio = bolas[0].bolasDoBingoJson.HistoricoSorteio
        jsonMontado = json_montado(conf_api=confAPI,
                                   historico_sorteio=historicoSorteio)
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.index'))

    if request.method == 'POST' and 'config' in request.form:
        _id = (bolas[0].id if 'id' in bolas[0] else g.user['id'])
        return redirect(url_for(f'bingo.config', _id=_id))

    # print_class(bolas[0])
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
        except (KeyError, TypeError):
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
        listaVisitante = list()
        listaMenor = list()
        listaNiverCasamento = list()
        listaEnsaio = list()
        listaEnsaioAlameda = list()
        listaEnsaioJardimCopa1 = list()
        listaEnsaioJardimCopa2 = list()
        listaEnsaioNovaDivineia1 = list()
        listaEnsaioNovaDivineia2 = list()
        listaEnsaioPiedade = list()
        listaEnsaioVeneza4 = list()
        for column in dados:
            for _index in dados[column]:
                _index = str(_index).removesuffix('nan')
                if str(_index) != str(_index).removesuffix('nan|'):
                    _index = str(_index).removesuffix('nan|') + '|'
                if str(_index) == str(_index).removeprefix('nan|'):
                    if str(_index).split('|')[1].lower().__contains__(
                            congregacoes.VISITANTE):
                        listaVisitante.append(_index)
                    elif not mes[0].lower().__contains__('ensaio') and \
                        (str(_index).split('|')[5].lower() not in [
                            'casado', 'outro(união estável)', 'viúvo'] and
                            int(str(_index).split('|')[3]) < 35):
                        listaMenor.append(_index)
                    else:
                        listaGeral.append(_index)
                        if niver_casamento(str(_index).split('|')[4], mes):
                            listaNiverCasamento.append(_index)
                        if mes[0].lower().__contains__('ensaio'):
                            listaEnsaio.append(_index)
                            if str(_index).split('|')[1].lower() == \
                                    congregacoes.ALAMEDA:
                                listaEnsaioAlameda.append(_index)
                            elif str(_index).split('|')[1].lower() == \
                                    congregacoes.JARDIMCOPACABANA1:
                                listaEnsaioJardimCopa1.append(_index)
                            elif str(_index).split('|')[1].lower() == \
                                    congregacoes.JARDIMCOPACABANA2:
                                listaEnsaioJardimCopa2.append(_index)
                            elif str(_index).split('|')[1].lower() == \
                                    congregacoes.NOVADIVINEIA1:
                                listaEnsaioNovaDivineia1.append(_index)
                            elif str(_index).split('|')[1].lower() == \
                                    congregacoes.NOVADIVINEIA2:
                                listaEnsaioNovaDivineia2.append(_index)
                            elif str(_index).split('|')[1].lower() == \
                                    congregacoes.PIEDADE:
                                listaEnsaioPiedade.append(_index)
                            elif str(_index).split('|')[1].lower() == \
                                    congregacoes.VENEZA4:
                                listaEnsaioVeneza4.append(_index)

        # Colocar os dados adquiridos na tabela correta
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_geral=listaGeral,
            lista_visitante=listaVisitante,
            lista_menor=listaMenor,
            lista_dinamica=list(),
            lista_dinamica_mae_pai=list(),
            selecao_lista_mae_pai=dict(),
            lista_dinamica_filhos_pais=dict(),
            selecao_lista_filhos_pais=dict(),
            selecao_evento_especial=list(),
            lista_niver_casamento=listaNiverCasamento,
            lista_ensaio=listaEnsaio,
            lista_ensaio_alameda=listaEnsaioAlameda,
            lista_ensaio_jardim_copa_1=listaEnsaioJardimCopa1,
            lista_ensaio_jardim_copa_2=listaEnsaioJardimCopa2,
            lista_ensaio_nova_divineia_1=listaEnsaioNovaDivineia1,
            lista_ensaio_nova_divineia_2=listaEnsaioNovaDivineia2,
            lista_ensaio_piedade=listaEnsaioPiedade,
            lista_ensaio_veneza_4=listaEnsaioVeneza4,
            habilitar_filhos_para_pais=[''],
            mes_sorteio=mes,
            nome_sorteado_anterior=[''],
            nome_sorteado=['']
        )

        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'carregar_evento' in request.form:
        # Realizar chamada para o banco da API
        bolasDoBingoJson = bolas[0].bolasDoBingoJson

        selecao = events.evento(request.form['carregar_evento'])
        # Colocar os dados adquiridos na tabela correta
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            selecao_evento_especial=selecao,
        )

        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'dinamica' in request.form:
        # Realizar chamada para o banco da API
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaGeral = bolasDoBingoJson.ListaGeral
        listaDinamica = set(bolasDoBingoJson.ListaDinamica)
        ultimoItem = ''

        for cartao in request.form['dinamica'].split(','):
            if cartao.__contains__('|'):
                congregacao = cartao.split('|')[0]
                NumCartao = cartao.split('|')[1]
                for item in listaGeral:
                    if item.split('|')[1] == congregacao and \
                            item.split('|')[2] == NumCartao:
                        listaDinamica.add(item)
                        ultimoItem = item

                if len(listaDinamica) % 2 != 0:
                    listaDinamica = remove_lista(listaDinamica, ultimoItem,
                                                 'Lista Dinâmica')

        # Colocar os dados adquiridos na tabela correta
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_geral=listaGeral,
            lista_dinamica=list(listaDinamica)
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'dinamica_mae_pai' in request.form:
        # Realizar chamada para o banco da API
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaGeral = bolasDoBingoJson.ListaGeral
        selecaoListaMaePai = bolasDoBingoJson.SelecaoListaMaePai

        for cartao in request.form['dinamica_mae_pai'].split(','):
            if cartao.__contains__('|'):
                congregacao = cartao.split('|')[0]
                NumCartao = cartao.split('|')[1]
                lista = list()
                for item in listaGeral:
                    if item.split('|')[1] == congregacao and \
                            item.split('|')[2] == NumCartao:
                        lista.append(item)
                if len(lista) > 0:
                    selecaoListaMaePai[cartao] = lista

        # Colocar os dados adquiridos na tabela correta
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            selecao_lista_mae_pai=selecaoListaMaePai
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'dinamica_filho' in request.form:
        # Realizar chamada para o banco da API
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaGeral = bolasDoBingoJson.ListaGeral
        listaMenor = bolasDoBingoJson.ListaMenor
        selecaoListaFilhosPais = bolasDoBingoJson.SelecaoListaFilhosPais
        for cartao in request.form['dinamica_mae'].split(','):
            if cartao.__contains__('|'):
                congregacao = cartao.split('|')[0]
                NumCartao = cartao.split('|')[1]
                lista = list()
                for item in listaGeral:
                    if item.split('|')[1] == congregacao and \
                            item.split('|')[2] == NumCartao:
                        lista.append(item)
                if len(lista) > 0:
                    if cartao not in selecaoListaFilhosPais:
                        selecaoListaFilhosPais[cartao] = dict()
                        selecaoListaFilhosPais[cartao]['pais'] = set()
                        selecaoListaFilhosPais[cartao]['filhos'] = set()
                    else:
                        if type(selecaoListaFilhosPais[cartao]['pais']) != \
                                set():
                            selecaoListaFilhosPais[cartao]['pais'] = \
                                set(selecaoListaFilhosPais[cartao]['pais'])
                        if type(selecaoListaFilhosPais[cartao]['filhos']) != \
                                set():
                            selecaoListaFilhosPais[cartao]['filhos'] = \
                                set(selecaoListaFilhosPais[cartao]['filhos'])
                    selecaoListaFilhosPais[cartao]['pais'] = \
                        selecaoListaFilhosPais[cartao]['pais'].union(lista)

        for cartao in request.form['dinamica_filho'].split(','):
            lista = list()
            if cartao.__contains__('|'):
                congregacao = cartao.split('|')[0]
                NumCartao = cartao.split('|')[1]
                for item in listaGeral:
                    if item.split('|')[1] == congregacao and \
                            item.split('|')[2] == NumCartao:
                        lista.append(item)
                for item in listaMenor:
                    if item.split('|')[1] == congregacao and \
                            item.split('|')[2] == NumCartao:
                        lista.append(item)
            else:
                if cartao.strip() != '':
                    lista.append(cartao)
            if len(lista) > 0:
                for cartao_pais in request.form['dinamica_mae'].split(','):
                    if cartao_pais.__contains__('|') and \
                            cartao_pais in selecaoListaFilhosPais:
                        selecaoListaFilhosPais[cartao_pais][
                            'filhos'] = \
                            selecaoListaFilhosPais[cartao_pais][
                                'filhos'].union(lista)

        for cartao in request.form['dinamica_mae'].split(','):
            if cartao in selecaoListaFilhosPais and \
                    len(selecaoListaFilhosPais[cartao]['filhos']) == 0:
                selecaoListaFilhosPais.pop(cartao)

        for cartao in selecaoListaFilhosPais:
            for parente in selecaoListaFilhosPais[cartao]:
                temp = selecaoListaFilhosPais[cartao][parente]
                selecaoListaFilhosPais[cartao][parente] = list(temp)

        # Colocar os dados adquiridos na tabela correta
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            selecao_lista_filhos_pais=selecaoListaFilhosPais
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'menor_solteiro' in request.form:
        # Realizar chamada para o banco da API
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaGeral = bolasDoBingoJson.ListaGeral
        listaMenor = bolasDoBingoJson.ListaMenor
        ultimoItem = ''
        _print = False

        for cartao in request.form['menor_solteiro'].split(','):
            if cartao.__contains__('|'):
                congregacao = cartao.split('|')[0]
                NumCartao = cartao.split('|')[1]
                for item in listaMenor:
                    if item.split('|')[1] == congregacao and \
                            item.split('|')[2] == NumCartao:
                        listaGeral.append(item)
                        ultimoItem = item

                listaMenor = \
                    remove_lista(listaMenor, ultimoItem, 'Lista Jovens')

        # Colocar os dados adquiridos na tabela correta
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            lista_geral=listaGeral,
            lista_menor=list(listaMenor)
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'report' in request.form:
        ConfAPI = bolas[0].bolasDoBingoJson.ConfAPI[0]
        # caminho = request.form['report']
        ConfAPI = carregar_api(ConfAPI)
        # try:
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
            caminho = '.\\report\\'
        else:
            caminho = './report/'

        def pdf_writer(_writer: pd.ExcelWriter =
                       caminho + 'report.xlsx'):
            pd.DataFrame(dados).to_excel(_writer,
                                         sheet_name="Dados_usuarios")
            mes_maximo = list()

            for indice in meses.DICT_NUM_MES:
                if indice <= datetime.now().month and \
                        indice not in [1, 12]:
                    mes_maximo.append(meses.DICT_NUM_MES[indice])
                    mes_maximo.append(
                        f'ensaio_{meses.DICT_NUM_MES[indice]}')
            # print('mes_maximo:', mes_maximo, '\n')
            # print('dados_presenca - chaves: \n', dados_presenca.keys())
            # print('dados_presenca: \n', dados_presenca)
            for _mes in dados_presenca:
                if _mes in mes_maximo:
                    # print('mes teste: ', _mes)
                    presenca_transp = pd.DataFrame(
                        presenca[_mes]).transpose()
                    # print('chaves da presenca do mês em teste: ',
                    # presenca_transp.keys())
                    # print('presenca do mês em teste: \n',
                    # presenca_transp)
                    presenca_transp['congregacao'] = \
                        presenca_transp['idNumero'].apply(
                            lambda x: x.split('/')[0])
                    presenca_transp['idNumero'] = \
                        presenca_transp['idNumero'].apply(
                            lambda x: x.split('/')[1])
                    presenca_transp = presenca_transp.loc[
                                      :,
                                      nomes_colunas.COLUNAS_MESES_REPORT]
                    presenca_transp = presenca_transp.merge(
                        dados, on=['congregacao', 'idNumero'],
                        how='left', suffixes=('_left', '_right')
                                                            )
                    for index_, value in \
                            pd.DataFrame(presenca_transp).iterrows():
                        presenca_transp.loc[index_, ['estadoCivil']] = \
                            value['estadoCivil_right']
                        presenca_transp.loc[index_, ['dataCasamento']] = \
                            value['dataCasamento_right']
                        presenca_transp.loc[index_, ['nomeTitular']] = \
                            value['nomeTitular_left']
                        presenca_transp.loc[index_, ['nomeConjuge']] = \
                            value['nomeConjuge_left']
                        if str(value['nomeTitular_left']).lower() != 'nan':
                            presenca_transp.loc[index_,
                                                ['nascimentoTitular']] = \
                                value['nascimentoTitular_right']
                            presenca_transp.loc[index_,
                                                ['sexoTitular']] = \
                                value['sexoTitular']
                        else:
                            presenca_transp.loc[
                                index_, ['nascimentoTitular']] = \
                                value['nascimentoTitular_left']
                            presenca_transp.loc[
                                index_, ['sexoTitular']] = ''
                        if str(value['nomeConjuge_left']).lower() != 'nan':
                            presenca_transp.loc[index_,
                                                ['nascimentoConjuge']] = \
                                value['nascimentoConjuge_right']
                            presenca_transp.loc[index_,
                                                ['sexoConjuge']] = \
                                value['sexoConjuge']
                        else:
                            presenca_transp.loc[
                                index_, ['nascimentoConjuge']] = \
                                value['nascimentoConjuge_left']
                            presenca_transp.loc[index_,
                                                ['sexoConjuge']] = ''
                        # if index == 161:
                        #     print(presenca_transp.loc[index])
                    presenca_transp = presenca_transp.loc[
                                      :,
                                      nomes_colunas.COLUNAS_MERGE_REPORT]
                    presenca_transp.to_excel(_writer, sheet_name=_mes)

        out = io.BytesIO()
        writer = pd.ExcelWriter(out, engine='openpyxl')
        pdf_writer(writer)
        writer.save()
        out.seek(0)
        add = send_file(out, download_name='output.xlsx', as_attachment=True)
        return add

    if request.method == 'POST' and 'confAPI' in request.form:
        confAPI = request.form['confAPI']
        if confAPI.strip() == '':
            confAPI = bolasDoBingoJson.ConfAPI[0]

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

    if request.method == 'POST' and 'removeHistorico' in request.form:
        mesEscolhido = f"{request.form['removeHistorico'].lower()}"
        remove_historico(g, bolas, mesEscolhido)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'reportHistorico' in request.form:
        historico = bolas[0].bolasDoBingoJson.HistoricoSorteio
        dados = dict()
        for mes in historico:
            if mes not in dados:
                dados[mes] = []
            temp = {'congregacao': [],
                    'idNumero': [],
                    'nomeTitular': [],
                    'dataCasamento': [],
                    'estadoCivil': [],
                    'nomeConjuge': []}
            for pessoa in historico[mes]:
                pessoa = pessoa.split('|')
                temp['congregacao'] = pessoa[1]
                temp['idNumero'] = pessoa[2]
                temp['nomeTitular'] = pessoa[0]
                temp['dataCasamento'] = pessoa[4]
                temp['estadoCivil'] = pessoa[5]
                temp['nomeConjuge'] = pessoa[6]
                dados[mes].append(temp.copy())
        # print('dados:')
        # for mes in dados:
        #     print(f'{mes}:')
        #     for pessoa in dados[mes]:
        #         print(pessoa)
        if platform.system() == 'Windows':
            caminho = '.\\report\\'
        else:
            caminho = './report/'

        def pdf_writer(_writer: pd.ExcelWriter =
                       caminho + 'report_historico.xlsx'):
            mes_maximo = list()

            for indice in meses.DICT_NUM_MES:
                if indice <= datetime.now().month and \
                        indice not in [1, 12]:
                    mes_maximo.append(meses.DICT_NUM_MES[indice])
                    mes_maximo.append(
                        f'ensaio_{meses.DICT_NUM_MES[indice]}')
            for _mes in dados:
                if _mes in mes_maximo:
                    # print('mes teste: ', _mes)
                    dados_temp = pd.DataFrame(dados[_mes])
                    # print('chaves da presenca do mês em teste: ',
                    # presenca_transp.keys())
                    # print('presenca do mês em teste: \n',
                    # presenca_transp)
                    dados_temp.to_excel(_writer, sheet_name=_mes)

        out = io.BytesIO()
        writer = pd.ExcelWriter(out, engine='openpyxl')
        pdf_writer(writer)
        writer.save()
        out.seek(0)
        add = send_file(out, download_name='output.xlsx', as_attachment=True)
        return add

    if request.method == 'POST' and 'habilitarEnsaio' in request.form:
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            habilitar_ensaio=['true' if
                              request.form['habilitarEnsaio'].__contains__(
                                  'Habilitar') else '']
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'habilitarFilhosParaPais' in request.form:
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        selecaoEventoEspecial = bolasDoBingoJson.SelecaoEventoEspecial
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            habilitar_filhos_para_pais=['true' if
                                        request.form[
                                            'habilitarFilhosParaPais'].
                                        __contains__('Habilitar') else ''],
            selecao_evento_especial=list() if request.form[
                'habilitarFilhosParaPais'].__contains__('Desabilitar') else
            selecaoEventoEspecial
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'desabilitar_congregacao' in request.form:
        lista_desabilitar = list()
        for item in request.form:
            if item.__contains__('des_'):
                lista_desabilitar.append(request.form[item])
        remove_congregacao(g, bolas, lista_desabilitar)
        # jsonMontado = json_montado(
        #     bolas_do_bingo_json=bolasDoBingoJson,
        #     # habilitar_ensaio=['true' if
        #     #                   request.form['habilitarEnsaio'].__contains__(
        #     #                       'Habilitar') else '']
        # )
        # update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and 'salvar_mae_pai' in request.form:
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaDinamicaMaePai = set(bolasDoBingoJson.ListaDinamicaMaePai)
        selecaoListaMaePai = bolasDoBingoJson.SelecaoListaMaePai
        lista_habilitar = dict()
        lista_selecao = set()

        for item in request.form:
            if not item.__contains__('salvar'):
                if item[:-2] in lista_habilitar:
                    lista_habilitar[item[:-2]].append(request.form[item])
                else:
                    lista_habilitar[item[:-2]] = [request.form[item]]

        for item in lista_habilitar:
            for numero in lista_habilitar[item]:
                try:
                    pessoa = selecaoListaMaePai[item][int(numero)]
                    listaDinamicaMaePai.add(pessoa)
                    lista_selecao.add(item)
                except IndexError:
                    lista_selecao.add(item)

        for item in lista_selecao:
            try:
                selecaoListaMaePai.pop(item)
            except KeyError:
                pass
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            selecao_lista_mae_pai=selecaoListaMaePai,
            lista_dinamica_mae_pai=list(listaDinamicaMaePai)
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    if request.method == 'POST' and \
            'salvar_filhos_pais' in request.form:
        bolasDoBingoJson = bolas[0].bolasDoBingoJson
        listaDinamicaFilhosPais = bolasDoBingoJson.ListaDinamicaFilhosPais
        selecaoListaFilhosPais = bolasDoBingoJson.SelecaoListaFilhosPais
        selecaoEventoEspecial = bolasDoBingoJson.SelecaoEventoEspecial
        lista_habilitar = dict()
        lista_selecao = set()

        for item in request.form:
            if not item.__contains__('salvar'):
                quebra = item.split('|-|')
                cartao = quebra[0]
                parente = quebra[1].split('|')[0]
                if cartao in lista_habilitar:
                    if parente in lista_habilitar[cartao]:
                        lista_habilitar[cartao][parente].append(
                            request.form[item])
                    else:
                        lista_habilitar[cartao][parente] = [request.form[item]]
                else:
                    lista_habilitar[cartao] = dict()
                    lista_habilitar[cartao][parente] = [request.form[item]]

        for cartao in lista_habilitar:
            if 'pais' in lista_habilitar[cartao] and \
                    'filhos' in lista_habilitar[cartao]:
                for num_pais in lista_habilitar[cartao]['pais']:
                    pai = selecaoListaFilhosPais[cartao]['pais'][
                        int(num_pais)]
                    listaDinamicaFilhosPais[pai] = set()
                    for num_filho in lista_habilitar[cartao]['filhos']:
                        try:
                            quebra_pai = pai.split('|')[0:-1]
                            filho = selecaoListaFilhosPais[cartao]['filhos'][
                                int(num_filho)].split('|')[0]
                            juntar = ''
                            PREFIXO_EVENTO = selecaoEventoEspecial
                            for num_item in range(len(quebra_pai) - 1, -1, -1):
                                if num_item == 0:
                                    juntar = \
                                        juntar + \
                                        f'|{PREFIXO_EVENTO[0]["singular"]}: ' \
                                        + quebra_pai[num_item]
                                else:
                                    juntar = '|' + quebra_pai[num_item] + \
                                             juntar
                            filho = \
                                f'{PREFIXO_EVENTO[1]["singular"]}: {filho}' + \
                                juntar
                            if pai not in listaDinamicaFilhosPais:
                                listaDinamicaFilhosPais[pai] = {filho}
                            else:
                                listaDinamicaFilhosPais[pai].add(filho)
                            lista_selecao.add(cartao)
                        except IndexError:
                            lista_selecao.add(cartao)
        for item in lista_selecao:
            try:
                selecaoListaFilhosPais.pop(item)
            except KeyError:
                pass
        for pais in listaDinamicaFilhosPais:
            listaDinamicaFilhosPais[pais] = list(listaDinamicaFilhosPais[pais])
        jsonMontado = json_montado(
            bolas_do_bingo_json=bolasDoBingoJson,
            selecao_lista_filhos_pais=selecaoListaFilhosPais,
            lista_dinamica_filhos_pais=listaDinamicaFilhosPais
        )
        update_db(g, jsonMontado)
        return redirect(url_for('bingo.config', _id=_id))

    # print_class(bolas[0])
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
    #         if file_path[x - 1].lower() == 'app':
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
