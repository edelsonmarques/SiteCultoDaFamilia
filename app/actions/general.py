from utils.connect import update_db
from utils.json_db import json_montado
from enums import actions
import random


def remove_people(g, bolas, option, _print=False):
    # print('Bolas do Bingo:', BolasDoBingo)
    bolasDoBingoJson = bolas[0].bolasDoBingoJson
    listaGeral = bolasDoBingoJson.ListaGeral
    listaDinamica = bolasDoBingoJson.ListaDinamica
    listaDinamicaMaePai = bolasDoBingoJson.ListaDinamicaMaePai
    listaDinamicaFilhosPais = bolasDoBingoJson.ListaDinamicaFilhosPais
    listaNiverCasamento = bolasDoBingoJson.ListaNiverCasamento
    listaEnsaio = bolasDoBingoJson.ListaEnsaio
    listaEnsaioAlameda = bolasDoBingoJson.ListaEnsaioAlameda
    listaEnsaioJardinCopa1 = bolasDoBingoJson.ListaEnsaioJardimCopa1
    listaEnsaioJardinCopa2 = bolasDoBingoJson.ListaEnsaioJardimCopa2
    listaEnsaioNovaDivineia1 = bolasDoBingoJson.ListaEnsaioNovaDivineia1
    listaEnsaioNovaDivineia2 = bolasDoBingoJson.ListaEnsaioNovaDivineia2
    listaEnsaioPiedade = bolasDoBingoJson.ListaEnsaioPiedade
    listaEnsaioVeneza4 = bolasDoBingoJson.ListaEnsaioVeneza4
    listaMenor = bolasDoBingoJson.ListaMenor
    listaVisitante = bolasDoBingoJson.ListaVisitante
    nomeSorteado = bolasDoBingoJson.NomeSorteado
    historicoSorteio = bolasDoBingoJson.HistoricoSorteio
    mesSorteio = bolasDoBingoJson.MesSorteio
    nomeSorteado_temp = ''

    if len(listaGeral) != 0 and option == actions.GERAL:
        nomeSorteado = [random.choice(listaGeral)]

    elif len(listaMenor) != 0 and option == actions.JOVENS:
        nomeSorteado = [random.choice(listaMenor)]
        
        # Remove o ganhador
        listaMenor.remove(nomeSorteado[0])

    elif len(listaVisitante) != 0 and option == actions.VISITANTES:
        nomeSorteado = [random.choice(listaVisitante)]
        
        # Remove o ganhador
        listaVisitante.remove(nomeSorteado[0])

    elif len(listaNiverCasamento) != 0 and option == actions.ANIVERSARIO:
        nomeSorteado = [random.choice(listaNiverCasamento)]
        
    elif len(listaDinamica) != 0 and option == actions.DINAMICA:
        nomeSorteado = [random.choice(listaDinamica)]

    elif len(listaDinamicaMaePai) != 0 and option == actions.DINAMICA_MAE_PAI:
        nomeSorteado = [random.choice(listaDinamicaMaePai)]

    elif len(listaDinamicaFilhosPais) != 0 and \
            option == actions.DINAMICA_FILHOS_PAIS:
        nomeSorteado = [random.choice(list(listaDinamicaFilhosPais))]
        nomeSorteado_temp = [
            random.choice(listaDinamicaFilhosPais[nomeSorteado[0]])]

    elif len(listaEnsaio) != 0 and option == actions.ENSAIO:
        nomeSorteado = [random.choice(listaEnsaio)]
        
    elif len(listaEnsaioAlameda) != 0 and option == actions.ALAMEDA:
        nomeSorteado = [random.choice(listaEnsaioAlameda)]
        
    elif len(listaEnsaioJardinCopa1) != 0 and option == actions.JDCOPA1:
        nomeSorteado = [random.choice(listaEnsaioJardinCopa1)]
        
    elif len(listaEnsaioJardinCopa2) != 0 and option == actions.JDCOPA2:
        nomeSorteado = [random.choice(listaEnsaioJardinCopa2)]
        
    elif len(listaEnsaioNovaDivineia1) != 0 and option == actions.ND1:
        nomeSorteado = [random.choice(listaEnsaioNovaDivineia1)]
        
    elif len(listaEnsaioNovaDivineia2) != 0 and option == actions.ND2:
        nomeSorteado = [random.choice(listaEnsaioNovaDivineia2)]
        
    elif len(listaEnsaioPiedade) != 0 and option == actions.PIEDADE:
        nomeSorteado = [random.choice(listaEnsaioPiedade)]
        
    elif len(listaEnsaioVeneza4) != 0 and option == actions.VENEZA4:
        nomeSorteado = [random.choice(listaEnsaioVeneza4)]

    if nomeSorteado != ['']:
        if mesSorteio[0] in historicoSorteio:
            if nomeSorteado[0] not in historicoSorteio[mesSorteio[0]]:
                historicoSorteio[mesSorteio[0]].append(nomeSorteado[0])
        else:
            historicoSorteio[mesSorteio[0]] = nomeSorteado

    listaGeral = remove_lista(listaGeral, nomeSorteado[0], 'Lista Geral')
    listaDinamica = remove_lista(listaDinamica, nomeSorteado[0],
                                 'Lista Dinâmica')
    listaDinamicaMaePai = remove_lista(listaDinamicaMaePai, nomeSorteado[0],
                                       'Lista Dinâmica Mãe/Pai')
    listaDinamicaFilhosPais = remove_lista(listaDinamicaFilhosPais,
                                           nomeSorteado[0],
                                           'Lista Dinâmica Filhos/Pais')
    listaNiverCasamento = remove_lista(listaNiverCasamento, nomeSorteado[0],
                                       'Lista Aniversário')
    listaEnsaio = remove_lista(listaEnsaio, nomeSorteado[0], 'Lista Ensaio')
    listaEnsaioAlameda = remove_lista(listaEnsaioAlameda, nomeSorteado[0],
                                      'Lista Ensaio Alameda')
    listaEnsaioJardinCopa1 = remove_lista(listaEnsaioJardinCopa1,
                                          nomeSorteado[0],
                                          'Lista Ensaio Jardim Copacabana 1')
    listaEnsaioJardinCopa2 = remove_lista(listaEnsaioJardinCopa2,
                                          nomeSorteado[0],
                                          'Lista Ensaio Jardim Copacabana 2')
    listaEnsaioNovaDivineia1 = remove_lista(listaEnsaioNovaDivineia1,
                                            nomeSorteado[0],
                                            'Lista Ensaio Nova Divinéia 1')
    listaEnsaioNovaDivineia2 = remove_lista(listaEnsaioNovaDivineia2,
                                            nomeSorteado[0],
                                            'Lista Ensaio Nova Divinéia 2')
    listaEnsaioPiedade = remove_lista(listaEnsaioPiedade,
                                      nomeSorteado[0],
                                      'Lista Ensaio Piedade')
    listaEnsaioVeneza4 = remove_lista(listaEnsaioVeneza4, nomeSorteado[0],
                                      'Lista Ensaio Veneza 4')

    if option in [actions.GERAL, actions.DINAMICA, actions.DINAMICA_MAE_PAI,
                  actions.DINAMICA_FILHOS_PAIS, actions.ANIVERSARIO,
                  actions.ENSAIO, actions.ALAMEDA, actions.JDCOPA1,
                  actions.JDCOPA2, actions.ND1, actions.ND2, actions.PIEDADE,
                  actions.VENEZA4]:
        # Remove o ganhador
        try:
            congregacao = nomeSorteado[0].split('|')[1]
            numCartao = nomeSorteado[0].split('|')[2]
        except IndexError:
            congregacao = ''
            numCartao = ''

        def remover_pessoa(lista, descricao):
            try:
                for pessoa in lista:
                    if pessoa.split('|')[1] == congregacao and \
                            pessoa.split('|')[2] == numCartao:
                        if type(lista) == dict:
                            lista.pop(pessoa)
                        else:
                            lista.remove(pessoa)
            except Exception as e:
                if _print:
                    print(f'{descricao} não tem o nome sorteado. Erro: ', e)
            return lista

        listaGeral = remover_pessoa(listaGeral, 'Lista Geral')
        listaDinamica = remover_pessoa(listaDinamica, 'Lista Dinâmica')
        listaDinamicaMaePai = remover_pessoa(listaDinamicaMaePai,
                                             'Lista Dinâmica Mãe/Pai')
        listaDinamicaFilhosPais = remover_pessoa(listaDinamicaFilhosPais,
                                                 'Lista Dinâmica Filhos/Pais')
        listaNiverCasamento = remover_pessoa(listaNiverCasamento,
                                             'Lista Aniversário')
        listaEnsaio = remover_pessoa(listaEnsaio, 'Lista Ensaio')
        listaEnsaioAlameda = remover_pessoa(listaEnsaioAlameda,
                                            'Lista Ensaio Alameda')
        listaEnsaioJardinCopa1 = remover_pessoa(listaEnsaioJardinCopa1,
                                                'Lista Ensaio Jardim '
                                                'Copacabana 1')
        listaEnsaioJardinCopa2 = remover_pessoa(listaEnsaioJardinCopa2,
                                                'Lista Ensaio Jardim '
                                                'Copacabana 2')
        listaEnsaioNovaDivineia1 = remover_pessoa(listaEnsaioNovaDivineia1,
                                                  'Lista Ensaio Nova '
                                                  'Divinéia 1')
        listaEnsaioNovaDivineia2 = remover_pessoa(listaEnsaioNovaDivineia2,
                                                  'Lista Ensaio Nova '
                                                  'Divinéia 2')
        listaEnsaioPiedade = remover_pessoa(listaEnsaioPiedade,
                                            'Lista Ensaio Piedade')
        listaEnsaioVeneza4 = remover_pessoa(listaEnsaioVeneza4,
                                            'Lista Ensaio Veneza 4')

    jsonMontado = json_montado(
        bolas_do_bingo_json=bolasDoBingoJson,
        lista_geral=listaGeral,
        lista_dinamica=listaDinamica,
        lista_dinamica_mae_pai=listaDinamicaMaePai,
        lista_dinamica_filhos_pais=listaDinamicaFilhosPais,
        lista_niver_casamento=listaNiverCasamento,
        lista_menor=listaMenor,
        lista_visitante=listaVisitante,
        lista_ensaio=listaEnsaio,
        lista_ensaio_alameda=listaEnsaioAlameda,
        lista_ensaio_jardim_copa_1=listaEnsaioJardinCopa1,
        lista_ensaio_jardim_copa_2=listaEnsaioJardinCopa2,
        lista_ensaio_nova_divineia_1=listaEnsaioNovaDivineia1,
        lista_ensaio_nova_divineia_2=listaEnsaioNovaDivineia2,
        lista_ensaio_piedade=listaEnsaioPiedade,
        lista_ensaio_veneza_4=listaEnsaioVeneza4,
        nome_sorteado_anterior=bolasDoBingoJson.NomeSorteado,
        nome_sorteado=nomeSorteado if
        nomeSorteado_temp == '' else nomeSorteado_temp,
        historico_sorteio=historicoSorteio
    )
    update_db(g, jsonMontado)


def remove_lista(lista, pessoa, descricao, _print=False):
    try:
        if type(lista) == dict:
            lista.pop(pessoa)
        else:
            lista.remove(pessoa)
    except Exception as e:
        if _print:
            print(f'{descricao} não tem o nome sorteado. Erro: ', e)
    return lista


def remove(bingo_json, people, _print=False):
    bingo_json.ListaGeral = remove_lista(bingo_json.ListaGeral, people,
                                         'Lista Geral')
    bingo_json.ListaDinamica = remove_lista(bingo_json.ListaDinamica, people,
                                            'Lista Dinâmica')
    bingo_json.ListaEnsaio = remove_lista(bingo_json.ListaEnsaio, people,
                                          'Lista Ensaio')
    bingo_json.listaDinamicaMaePai = remove_lista(
        bingo_json.listaDinamicaMaePai, people, 'Lista Dinâmica Mãe/Pai')
    return bingo_json


def add(bingo_json, people, _print=False):
    if people not in bingo_json.ListaGeral:
        bingo_json.ListaGeral.append(people)
    if people not in bingo_json.ListaEnsaio:
        bingo_json.ListaEnsaio.append(people)
    return bingo_json


def remove_congregacao(g, bolas, lista_congregacao, _print=False):
    # print('Bolas do Bingo:', BolasDoBingo)
    bolasDoBingoJson = bolas[0].bolasDoBingoJson
    listaEnsaioAlameda = bolasDoBingoJson.ListaEnsaioAlameda
    listaEnsaioJardimCopa1 = bolasDoBingoJson.ListaEnsaioJardimCopa1
    listaEnsaioJardimCopa2 = bolasDoBingoJson.ListaEnsaioJardimCopa2
    listaEnsaioNovaDivineia1 = bolasDoBingoJson.ListaEnsaioNovaDivineia1
    listaEnsaioNovaDivineia2 = bolasDoBingoJson.ListaEnsaioNovaDivineia2
    listaEnsaioPiedade = bolasDoBingoJson.ListaEnsaioPiedade
    listaEnsaioVeneza4 = bolasDoBingoJson.ListaEnsaioVeneza4

    if actions.ALAMEDA in lista_congregacao:
        habilitarListaAlameda = ['']
        for people in listaEnsaioAlameda:
            bolasDoBingoJson = remove(bolasDoBingoJson, people)
    else:
        habilitarListaAlameda = ['true']
        for people in listaEnsaioAlameda:
            bolasDoBingoJson = add(bolasDoBingoJson, people)
    if actions.JDCOPA1 in lista_congregacao:
        habilitarListaJardimCopa1 = ['']
        for people in listaEnsaioJardimCopa1:
            bolasDoBingoJson = remove(bolasDoBingoJson, people)
    else:
        habilitarListaJardimCopa1 = ['true']
        for people in listaEnsaioJardimCopa1:
            bolasDoBingoJson = add(bolasDoBingoJson, people)
    if actions.JDCOPA2 in lista_congregacao:
        habilitarListaJardimCopa2 = ['']
        for people in listaEnsaioJardimCopa2:
            bolasDoBingoJson = remove(bolasDoBingoJson, people)
    else:
        habilitarListaJardimCopa2 = ['true']
        for people in listaEnsaioJardimCopa2:
            bolasDoBingoJson = add(bolasDoBingoJson, people)
    if actions.ND1 in lista_congregacao:
        habilitarListaNovaDivineia1 = ['']
        for people in listaEnsaioNovaDivineia1:
            bolasDoBingoJson = remove(bolasDoBingoJson, people)
    else:
        habilitarListaNovaDivineia1 = ['true']
        for people in listaEnsaioNovaDivineia1:
            bolasDoBingoJson = add(bolasDoBingoJson, people)
    if actions.ND2 in lista_congregacao:
        habilitarListaNovaDivineia2 = ['']
        for people in listaEnsaioNovaDivineia2:
            bolasDoBingoJson = remove(bolasDoBingoJson, people)
    else:
        habilitarListaNovaDivineia2 = ['true']
        for people in listaEnsaioNovaDivineia2:
            bolasDoBingoJson = add(bolasDoBingoJson, people)
    if actions.PIEDADE in lista_congregacao:
        habilitarListaPiedade = ['']
        for people in listaEnsaioPiedade:
            bolasDoBingoJson = remove(bolasDoBingoJson, people)
    else:
        habilitarListaPiedade = ['true']
        for people in listaEnsaioPiedade:
            bolasDoBingoJson = add(bolasDoBingoJson, people)
    if actions.VENEZA4 in lista_congregacao:
        habilitarListaVeneza4 = ['']
        for people in listaEnsaioVeneza4:
            bolasDoBingoJson = remove(bolasDoBingoJson, people)
    else:
        habilitarListaVeneza4 = ['true']
        for people in listaEnsaioVeneza4:
            bolasDoBingoJson = add(bolasDoBingoJson, people)

    jsonMontado = json_montado(
        bolas_do_bingo_json=bolasDoBingoJson,
        lista_ensaio_alameda=listaEnsaioAlameda,
        lista_ensaio_jardim_copa_1=listaEnsaioJardimCopa1,
        lista_ensaio_jardim_copa_2=listaEnsaioJardimCopa2,
        lista_ensaio_nova_divineia_1=listaEnsaioNovaDivineia1,
        lista_ensaio_nova_divineia_2=listaEnsaioNovaDivineia2,
        lista_ensaio_piedade=listaEnsaioPiedade,
        lista_ensaio_veneza_4=listaEnsaioVeneza4,
        habilitar_lista_alameda=habilitarListaAlameda,
        habilitar_lista_jardim_copa_1=habilitarListaJardimCopa1,
        habilitar_lista_jardim_copa_2=habilitarListaJardimCopa2,
        habilitar_lista_nova_divineia_1=habilitarListaNovaDivineia1,
        habilitar_lista_nova_divineia_2=habilitarListaNovaDivineia2,
        habilitar_lista_piedade=habilitarListaPiedade,
        habilitar_lista_veneza_4=habilitarListaVeneza4
    )
    update_db(g, jsonMontado)


def remove_historico(g, bolas, mes_escolhido, _print=False):
    # print('Bolas do Bingo:', BolasDoBingo)
    bolasDoBingoJson = bolas[0].bolasDoBingoJson
    nomeSorteado = bolasDoBingoJson.NomeSorteado
    historicoSorteio = bolasDoBingoJson.HistoricoSorteio

    if mes_escolhido in historicoSorteio:
        historicoSorteio.pop(mes_escolhido)
    elif mes_escolhido == 'todos' and len(historicoSorteio) > 0:
        historicoSorteio = {}

    jsonMontado = json_montado(
        bolas_do_bingo_json=bolasDoBingoJson,
        nome_sorteado_anterior=bolasDoBingoJson.NomeSorteado,
        nome_sorteado=nomeSorteado,
        historico_sorteio=historicoSorteio
    )
    update_db(g, jsonMontado)
