from utils.connect import update_db
from utils.json_db import json_montado
from enums import actions
import random


def remove_people(g, bolas, option, _print=False):
    # print('Bolas do Bingo:', BolasDoBingo)
    bolasDoBingoJson = bolas[0].bolasDoBingoJson
    listaGeral = bolasDoBingoJson.ListaGeral
    listaDinamica = bolasDoBingoJson.ListaDinamica
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
        

    try:
        listaGeral.remove(nomeSorteado[0])
    except Exception as e:
        if _print:
            print('Lista Geral não tem o nome sorteado. Erro: ', e)
        pass
    try:
        listaDinamica.remove(nomeSorteado[0])
    except Exception as e:
        if _print:
            print('Lista Dinâmica não tem o nome sorteado. Erro: ', e)
        pass
    try:
        listaNiverCasamento.remove(nomeSorteado[0])
    except Exception as e:
        if _print:
            print('Lista Aniversário não tem o nome sorteado. Erro: ', e)
        pass
    try:
        listaEnsaio.remove(nomeSorteado[0])
    except Exception as e:
        if _print:
            print('Lista Ensaio não tem o nome sorteado. Erro: ', e)
        pass
    try:
        listaEnsaioAlameda.remove(nomeSorteado[0])
    except Exception as e:
        print('Lista Ensaio Alameda '
              'não tem o nome sorteado. Erro: ', e)
        pass
    try:
        listaEnsaioJardinCopa1.remove(nomeSorteado[0])
    except Exception as e:
        print('Lista Ensaio Jardim Copacabana 1 '
              'não tem o nome sorteado. Erro: ', e)
        pass
    try:
        listaEnsaioJardinCopa2.remove(nomeSorteado[0])
    except Exception as e:
        print('Lista Ensaio Jardim Copacabana 2 '
              'não tem o nome sorteado. Erro: ', e)
        pass
    try:
        listaEnsaioNovaDivineia1.remove(nomeSorteado[0])
    except Exception as e:
        print('Lista Ensaio Nova Divinéia 1 '
              'não tem o nome sorteado. Erro: ', e)
        pass
    try:
        listaEnsaioNovaDivineia2.remove(nomeSorteado[0])
    except Exception as e:
        print('Lista Ensaio Nova Divinéia 2 '
              'não tem o nome sorteado. Erro: ', e)
        pass
    try:
        listaEnsaioPiedade.remove(nomeSorteado[0])
    except Exception as e:
        print('Lista Ensaio Piedade '
              'não tem o nome sorteado. Erro: ', e)
        pass
    try:
        listaEnsaioVeneza4.remove(nomeSorteado[0])
    except Exception as e:
        print('Lista Ensaio Veneza 4 '
              'não tem o nome sorteado. Erro: ', e)
        pass
    
    if option in [actions.GERAL, actions.DINAMICA, actions.ANIVERSARIO,
                  actions.ENSAIO, actions.ALAMEDA, actions.JDCOPA1,
                  actions.JDCOPA2, actions.ND1, actions.ND2,
                  actions.PIEDADE, actions.VENEZA4]:
        # Remove o ganhador
        try:
            congregacao = nomeSorteado[0].split('|')[1]
            numCartao = nomeSorteado[0].split('|')[2]
        except IndexError:
            congregacao = ''
            numCartao = ''

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
        try:
            listaEnsaioAlameda = remover_pessoa(listaEnsaioAlameda)
        except Exception as e:
            print('Lista Ensaio Alameda '
                  'não tem o nome sorteado. Erro: ', e)
            pass
        try:
            listaEnsaioJardinCopa1 = remover_pessoa(listaEnsaioJardinCopa1)
        except Exception as e:
            print('Lista Ensaio Jardim Copacabana 1 '
                  'não tem o nome sorteado. Erro: ', e)
            pass
        try:
            listaEnsaioJardinCopa2 = remover_pessoa(listaEnsaioJardinCopa2)
        except Exception as e:
            print('Lista Ensaio Jardim Copacabana 2 '
                  'não tem o nome sorteado. Erro: ', e)
            pass
        try:
            listaEnsaioNovaDivineia1 = remover_pessoa(
                listaEnsaioNovaDivineia1)
        except Exception as e:
            print('Lista Ensaio Nova Divinéia 1 '
                  'não tem o nome sorteado. Erro: ', e)
            pass
        try:
            listaEnsaioNovaDivineia2 = remover_pessoa(
                listaEnsaioNovaDivineia2)
        except Exception as e:
            print('Lista Ensaio Nova Divinéia 2 '
                  'não tem o nome sorteado. Erro: ', e)
            pass
        try:
            listaEnsaioPiedade = remover_pessoa(listaEnsaioPiedade)
        except Exception as e:
            print('Lista Ensaio Piedade '
                  'não tem o nome sorteado. Erro: ', e)
            pass
        try:
            listaEnsaioVeneza4 = remover_pessoa(listaEnsaioVeneza4)
        except Exception as e:
            print('Lista Ensaio Veneza 4 '
                  'não tem o nome sorteado. Erro: ', e)
            pass

    jsonMontado = json_montado(
        bolas_do_bingo_json=bolasDoBingoJson,
        lista_geral=listaGeral,
        lista_dinamica=listaDinamica,
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
        nome_sorteado=nomeSorteado,
    )
    update_db(g, jsonMontado)


def remove(bingo_json, people, _print=False):
    try:
        bingo_json.ListaGeral.remove(people)
    except Exception as e:
        if _print:
            print('Lista Geral não tem o nome sorteado. Erro: ', e)
        pass
    try:
        bingo_json.ListaDinamica.remove(people)
    except Exception as e:
        if _print:
            print('Lista Dinâmica não tem o nome sorteado. Erro: ', e)
        pass
    try:
        bingo_json.ListaEnsaio.remove(people)
    except Exception as e:
        if _print:
            print('Lista Ensaio não tem o nome sorteado. Erro: ', e)
        pass
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
