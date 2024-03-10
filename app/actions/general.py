from utils.connect import update_db
from utils.json_db import json_montado
from enums import actions, events
import random


def remove_people(g, bolas, option, gj='', _print=False):
    # print('Bolas do Bingo:', BolasDoBingo)
    bolas_do_bingo_json = bolas[0].bolasDoBingoJson
    lista_geral = bolas_do_bingo_json.ListaGeral
    lista_dinamica = bolas_do_bingo_json.ListaDinamica
    lista_dinamica_mae_pai = bolas_do_bingo_json.ListaDinamicaMaePai
    lista_dinamica_filhos_pais = bolas_do_bingo_json.ListaDinamicaFilhosPais
    lista_niver_casamento = bolas_do_bingo_json.ListaNiverCasamento
    lista_ensaio = bolas_do_bingo_json.ListaEnsaio
    lista_ensaio_alameda = bolas_do_bingo_json.ListaEnsaioAlameda
    lista_ensaio_jardim_copa1 = bolas_do_bingo_json.ListaEnsaioJardimCopa1
    lista_ensaio_jardim_copa2 = bolas_do_bingo_json.ListaEnsaioJardimCopa2
    lista_ensaio_nova_divineia1 = bolas_do_bingo_json.ListaEnsaioNovaDivineia1
    lista_ensaio_nova_divineia2 = bolas_do_bingo_json.ListaEnsaioNovaDivineia2
    lista_ensaio_piedade = bolas_do_bingo_json.ListaEnsaioPiedade
    lista_ensaio_veneza4 = bolas_do_bingo_json.ListaEnsaioVeneza4
    lista_de_out_nov = bolas_do_bingo_json.ListaDeOutNov
    lista_set = bolas_do_bingo_json.ListaSet
    lista_menor = bolas_do_bingo_json.ListaMenor
    lista_visitante = bolas_do_bingo_json.ListaVisitante
    if len(bolas[0].bolasDoBingoJson.SelecaoEventoEspecial) > 0:
        selecao_evento_especial = bolas_do_bingo_json.SelecaoEventoEspecial[0]
    else:
        selecao_evento_especial = ''
    nome_sorteado = bolas_do_bingo_json.NomeSorteado
    historico_sorteio = bolas_do_bingo_json.HistoricoSorteio
    mes_sorteio = bolas_do_bingo_json.MesSorteio
    nome_sorteado_temp = ''

    def remove_name(_list, action):
        if len(_list) != 0 and option == action:
            name = [random.choice(list(_list))]

            # Remove o ganhador em listas específicas
            if option in [actions.JOVENS, actions.VISITANTES]:
                _list.remove(name[0])
                return name, _list
            elif option in [actions.DINAMICA_FILHOS_PAIS]:
                name_temp = [random.choice(_list[name[0]])]
                return name, name_temp
            return name
        else:
            if option in action:
                if selecao_evento_especial not in [events.SEMINARIO_3]:
                    name = [
                        random.choice(_list[gj][option])]
                    lista_set[gj][option] = lista_set[gj][option] - 1
                else:
                    lista_678 = _list[gj]['8'].copy()
                    lista_678.extend(_list[gj]['7'].copy())
                    lista_678.extend(_list[gj]['6'].copy())
                    name = [random.choice(lista_678)]
                return name
        return nome_sorteado

    nome_sorteado = remove_name(lista_geral, actions.GERAL)
    nome_sorteado, lista_menor = remove_name(lista_menor, actions.JOVENS)
    nome_sorteado, lista_visitante = remove_name(lista_visitante,
                                                 actions.VISITANTES)
    nome_sorteado = remove_name(lista_niver_casamento, actions.ANIVERSARIO)
    nome_sorteado = remove_name(lista_dinamica, actions.DINAMICA)
    nome_sorteado = remove_name(lista_dinamica_mae_pai,
                                actions.DINAMICA_MAE_PAI)
    nome_sorteado, nome_sorteado_temp = remove_name(
        lista_dinamica_filhos_pais, actions.DINAMICA_FILHOS_PAIS)
    nome_sorteado = remove_name(lista_ensaio, actions.ENSAIO)
    nome_sorteado = remove_name(lista_ensaio_alameda, actions.ALAMEDA)
    nome_sorteado = remove_name(lista_ensaio_jardim_copa1, actions.JDCOPA1)
    nome_sorteado = remove_name(lista_ensaio_jardim_copa2, actions.JDCOPA2)
    nome_sorteado = remove_name(lista_ensaio_nova_divineia1, actions.ND1)
    nome_sorteado = remove_name(lista_ensaio_nova_divineia2, actions.ND2)
    nome_sorteado = remove_name(lista_ensaio_piedade, actions.PIEDADE)
    nome_sorteado = remove_name(lista_ensaio_veneza4, actions.VENEZA4)
    nome_sorteado = remove_name(actions.SEMINARIO, actions.SEMINARIO)

    if nome_sorteado != ['']:
        if mes_sorteio[0] in historico_sorteio:
            if nome_sorteado[0] not in historico_sorteio[mes_sorteio[0]]:
                historico_sorteio[mes_sorteio[0]].append(nome_sorteado[0])
        else:
            historico_sorteio[mes_sorteio[0]] = nome_sorteado

    actions_escolha = [actions.GERAL, actions.VISITANTES,
                       actions.DINAMICA, actions.DINAMICA_MAE_PAI,
                       actions.DINAMICA_FILHOS_PAIS, actions.ANIVERSARIO,
                       actions.ENSAIO, actions.ALAMEDA, actions.JDCOPA1,
                       actions.JDCOPA2, actions.ND1, actions.ND2,
                       actions.PIEDADE, actions.VENEZA4]
    if option in actions_escolha or (
            option in actions.SEMINARIO and
            gj == actions.GERAL
    ):
        lista_geral = remove_lista(lista_geral, nome_sorteado[0],
                                   'Lista Geral')

        lista_dinamica = remove_lista(lista_dinamica, nome_sorteado[0],
                                      'Lista Dinâmica')
        lista_dinamica_mae_pai = remove_lista(lista_dinamica_mae_pai,
                                              nome_sorteado[0],
                                              'Lista Dinâmica Mãe/Pai')
        lista_dinamica_filhos_pais = remove_lista(lista_dinamica_filhos_pais,
                                                  nome_sorteado[0],
                                                  'Lista Dinâmica Filhos/Pais')
        lista_niver_casamento = remove_lista(lista_niver_casamento,
                                             nome_sorteado[0],
                                             'Lista Aniversário')
        lista_ensaio = remove_lista(lista_ensaio, nome_sorteado[0],
                                    'Lista Ensaio')
        lista_ensaio_alameda = remove_lista(lista_ensaio_alameda,
                                            nome_sorteado[0],
                                            'Lista Ensaio Alameda')
        lista_ensaio_jardim_copa1 = remove_lista(lista_ensaio_jardim_copa1,
                                                 nome_sorteado[0],
                                                 'Lista Ensaio '
                                                 'Jardim Copacabana 1')
        lista_ensaio_jardim_copa2 = remove_lista(lista_ensaio_jardim_copa2,
                                                 nome_sorteado[0],
                                                 'Lista Ensaio '
                                                 'Jardim Copacabana 2')
        lista_ensaio_nova_divineia1 = remove_lista(
            lista_ensaio_nova_divineia1, nome_sorteado[0],
            'Lista Ensaio Nova Divinéia 1')
        lista_ensaio_nova_divineia2 = remove_lista(
            lista_ensaio_nova_divineia2, nome_sorteado[0],
            'Lista Ensaio Nova Divinéia 2')
        lista_ensaio_piedade = remove_lista(lista_ensaio_piedade,
                                            nome_sorteado[0],
                                            'Lista Ensaio Piedade')
        lista_ensaio_veneza4 = remove_lista(lista_ensaio_veneza4,
                                            nome_sorteado[0],
                                            'Lista Ensaio Veneza 4')
        if option in actions.SEMINARIO:
            if selecao_evento_especial not in [events.SEMINARIO_3]:
                lista_de_out_nov[gj][option] = \
                    remove_lista(lista_de_out_nov[gj][option],
                                 nome_sorteado[0],
                                 'Lista Seminario')
            else:
                for presencas in lista_de_out_nov[actions.GERAL]:
                    lista_de_out_nov[actions.GERAL][presencas] = \
                        remove_lista(
                            lista_de_out_nov[actions.GERAL][presencas],
                            nome_sorteado[0], 'Lista Seminario')
            for presencas in lista_de_out_nov[actions.GERAL]:
                lista_de_out_nov[actions.GERAL][presencas] = \
                    remove_lista(lista_de_out_nov[actions.GERAL][presencas],
                                 nome_sorteado[0], 'Lista Seminario')
        else:
            if selecao_evento_especial in events.EVENTOSEMINARIO:
                for presencas in lista_de_out_nov[actions.GERAL]:
                    lista_de_out_nov[actions.GERAL][presencas] = \
                        remove_lista(
                            lista_de_out_nov[actions.GERAL][presencas],
                            nome_sorteado[0], 'Lista Seminario')
                for presencas in lista_de_out_nov[actions.GERAL]:
                    lista_de_out_nov[actions.GERAL][presencas] = \
                        remove_lista(
                            lista_de_out_nov[actions.GERAL][presencas],
                            nome_sorteado[0], 'Lista Seminario')
    else:
        if selecao_evento_especial in events.EVENTOSEMINARIO:
            for presencas in lista_de_out_nov[actions.JOVENS]:
                lista_de_out_nov[actions.JOVENS][presencas] = \
                    remove_lista(lista_de_out_nov[actions.JOVENS][presencas],
                                 nome_sorteado[0], 'Lista Seminario')

    # Remove o conjuge do ganhador
    try:
        congregacao = nome_sorteado[0].split('|')[1]
        num_cartao = nome_sorteado[0].split('|')[2]
    except IndexError:
        congregacao = ''
        num_cartao = ''

    if option in actions_escolha or (
            option in actions.SEMINARIO and
            gj == actions.GERAL
    ):

        lista_geral = remover_pessoa(lista_geral, 'Lista Geral',
                                     congregacao, num_cartao)
        lista_visitante = remover_pessoa(lista_visitante, 'Lista Visitante',
                                         congregacao, num_cartao)
        lista_dinamica = remover_pessoa(lista_dinamica, 'Lista Dinâmica',
                                        congregacao, num_cartao)
        lista_dinamica_mae_pai = remover_pessoa(lista_dinamica_mae_pai,
                                                'Lista Dinâmica Mãe/Pai',
                                                congregacao, num_cartao)
        lista_dinamica_filhos_pais = remover_pessoa(
            lista_dinamica_filhos_pais, 'Lista Dinâmica Filhos/Pais',
            congregacao, num_cartao)
        lista_niver_casamento = remover_pessoa(lista_niver_casamento,
                                               'Lista Aniversário',
                                               congregacao, num_cartao)
        lista_ensaio = remover_pessoa(lista_ensaio, 'Lista Ensaio',
                                      congregacao, num_cartao)
        lista_ensaio_alameda = remover_pessoa(lista_ensaio_alameda,
                                              'Lista Ensaio Alameda',
                                              congregacao, num_cartao)
        lista_ensaio_jardim_copa1 = remover_pessoa(lista_ensaio_jardim_copa1,
                                                   'Lista Ensaio Jardim '
                                                   'Copacabana 1',
                                                   congregacao, num_cartao)
        lista_ensaio_jardim_copa2 = remover_pessoa(lista_ensaio_jardim_copa2,
                                                   'Lista Ensaio Jardim '
                                                   'Copacabana 2',
                                                   congregacao, num_cartao)
        lista_ensaio_nova_divineia1 = remover_pessoa(
            lista_ensaio_nova_divineia1, 'Lista Ensaio Nova Divinéia 1',
            congregacao, num_cartao)
        lista_ensaio_nova_divineia2 = remover_pessoa(
            lista_ensaio_nova_divineia2, 'Lista Ensaio Nova Divinéia 2',
            congregacao, num_cartao)
        lista_ensaio_piedade = remover_pessoa(lista_ensaio_piedade,
                                              'Lista Ensaio Piedade',
                                              congregacao, num_cartao)
        lista_ensaio_veneza4 = remover_pessoa(lista_ensaio_veneza4,
                                              'Lista Ensaio Veneza 4',
                                              congregacao, num_cartao)
        if selecao_evento_especial in events.EVENTOSEMINARIO:
            for presencas in lista_de_out_nov[actions.GERAL]:
                lista_de_out_nov[actions.GERAL][presencas] = \
                    remover_pessoa(lista_de_out_nov[actions.GERAL][presencas],
                                   'Lista Seminario', congregacao, num_cartao)
            for presencas in lista_de_out_nov[actions.GERAL]:
                lista_de_out_nov[actions.GERAL][presencas] = \
                    remover_pessoa(lista_de_out_nov[actions.GERAL][presencas],
                                   'Lista Seminario', congregacao, num_cartao)
    elif option in actions.SEMINARIO:
        for presencas in lista_de_out_nov[gj]:
            lista_de_out_nov[gj][presencas] = \
                remover_pessoa(lista_de_out_nov[gj][presencas],
                               'Lista Seminario', congregacao, num_cartao)
        for presencas in lista_de_out_nov[gj]:
            lista_de_out_nov[gj][presencas] = \
                remover_pessoa(lista_de_out_nov[gj][presencas],
                               'Lista Seminario', congregacao, num_cartao)
        lista_dinamica = remover_pessoa(lista_dinamica, 'Lista Dinâmica',
                                        congregacao, num_cartao)
        lista_niver_casamento = remover_pessoa(lista_niver_casamento,
                                               'Lista Aniversário',
                                               congregacao, num_cartao)

    _json_montado = json_montado(
        bolas_do_bingo_json=bolas_do_bingo_json,
        lista_geral=lista_geral,
        lista_dinamica=lista_dinamica,
        lista_dinamica_mae_pai=lista_dinamica_mae_pai,
        lista_dinamica_filhos_pais=lista_dinamica_filhos_pais,
        lista_niver_casamento=lista_niver_casamento,
        lista_menor=lista_menor,
        lista_visitante=lista_visitante,
        lista_ensaio=lista_ensaio,
        lista_ensaio_alameda=lista_ensaio_alameda,
        lista_ensaio_jardim_copa_1=lista_ensaio_jardim_copa1,
        lista_ensaio_jardim_copa_2=lista_ensaio_jardim_copa2,
        lista_ensaio_nova_divineia_1=lista_ensaio_nova_divineia1,
        lista_ensaio_nova_divineia_2=lista_ensaio_nova_divineia2,
        lista_ensaio_piedade=lista_ensaio_piedade,
        lista_ensaio_veneza_4=lista_ensaio_veneza4,
        lista_de_out_nov=lista_de_out_nov,
        lista_set=lista_set,
        nome_sorteado_anterior=bolas_do_bingo_json.NomeSorteado,
        nome_sorteado=nome_sorteado if
        nome_sorteado_temp == '' else nome_sorteado_temp,
        historico_sorteio=historico_sorteio
    )
    update_db(g, _json_montado)


def remove_lista(lista, pessoa, descricao, _print=False):
    try:
        if lista is dict:
            lista.pop(pessoa)
        else:
            lista.remove(pessoa)
    except Exception as e:
        if _print:
            print(f'{descricao} não tem o nome sorteado. Erro: ', e)
    return lista


def remover_pessoa(lista, descricao, congregacao, num_cartao,
                   _print: bool = False):
    try:
        for pessoa in lista:
            if pessoa.split('|')[1] == congregacao and \
                    pessoa.split('|')[2] == num_cartao:
                if lista is dict:
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
    bingo_json.ListaDinamicaMaePai = remove_lista(
        bingo_json.ListaDinamicaMaePai, people, 'Lista Dinâmica Mãe/Pai')
    return bingo_json


def add(bingo_json, people, _print=False):
    if people not in bingo_json.ListaGeral:
        bingo_json.ListaGeral.append(people)
    if people not in bingo_json.ListaEnsaio:
        bingo_json.ListaEnsaio.append(people)
    return bingo_json


def remove_congregacao(g, bolas, lista_congregacao, _print=False):
    # print('Bolas do Bingo:', BolasDoBingo)
    bolas_do_bingo_json = bolas[0].bolasDoBingoJson
    lista_ensaio_alameda = bolas_do_bingo_json.ListaEnsaioAlameda
    lista_ensaio_jardim_copa1 = bolas_do_bingo_json.ListaEnsaioJardimCopa1
    lista_ensaio_jardim_copa2 = bolas_do_bingo_json.ListaEnsaioJardimCopa2
    lista_ensaio_nova_divineia1 = bolas_do_bingo_json.ListaEnsaioNovaDivineia1
    lista_ensaio_nova_divineia2 = bolas_do_bingo_json.ListaEnsaioNovaDivineia2
    lista_ensaio_piedade = bolas_do_bingo_json.ListaEnsaioPiedade
    lista_ensaio_veneza4 = bolas_do_bingo_json.ListaEnsaioVeneza4

    if actions.ALAMEDA in lista_congregacao:
        habilitar_lista_alameda = ['']
        for people in lista_ensaio_alameda:
            bolas_do_bingo_json = remove(bolas_do_bingo_json, people)
    else:
        habilitar_lista_alameda = ['true']
        for people in lista_ensaio_alameda:
            bolas_do_bingo_json = add(bolas_do_bingo_json, people)
    if actions.JDCOPA1 in lista_congregacao:
        habilitar_lista_jardim_copa1 = ['']
        for people in lista_ensaio_jardim_copa1:
            bolas_do_bingo_json = remove(bolas_do_bingo_json, people)
    else:
        habilitar_lista_jardim_copa1 = ['true']
        for people in lista_ensaio_jardim_copa1:
            bolas_do_bingo_json = add(bolas_do_bingo_json, people)
    if actions.JDCOPA2 in lista_congregacao:
        habilitar_lista_jardim_copa2 = ['']
        for people in lista_ensaio_jardim_copa2:
            bolas_do_bingo_json = remove(bolas_do_bingo_json, people)
    else:
        habilitar_lista_jardim_copa2 = ['true']
        for people in lista_ensaio_jardim_copa2:
            bolas_do_bingo_json = add(bolas_do_bingo_json, people)
    if actions.ND1 in lista_congregacao:
        habilitar_lista_nova_divineia11 = ['']
        for people in lista_ensaio_nova_divineia1:
            bolas_do_bingo_json = remove(bolas_do_bingo_json, people)
    else:
        habilitar_lista_nova_divineia11 = ['true']
        for people in lista_ensaio_nova_divineia1:
            bolas_do_bingo_json = add(bolas_do_bingo_json, people)
    if actions.ND2 in lista_congregacao:
        habilitar_lista_nova_divineia12 = ['']
        for people in lista_ensaio_nova_divineia2:
            bolas_do_bingo_json = remove(bolas_do_bingo_json, people)
    else:
        habilitar_lista_nova_divineia12 = ['true']
        for people in lista_ensaio_nova_divineia2:
            bolas_do_bingo_json = add(bolas_do_bingo_json, people)
    if actions.PIEDADE in lista_congregacao:
        habilitar_lista_piedade = ['']
        for people in lista_ensaio_piedade:
            bolas_do_bingo_json = remove(bolas_do_bingo_json, people)
    else:
        habilitar_lista_piedade = ['true']
        for people in lista_ensaio_piedade:
            bolas_do_bingo_json = add(bolas_do_bingo_json, people)
    if actions.VENEZA4 in lista_congregacao:
        habilitar_lista_veneza4 = ['']
        for people in lista_ensaio_veneza4:
            bolas_do_bingo_json = remove(bolas_do_bingo_json, people)
    else:
        habilitar_lista_veneza4 = ['true']
        for people in lista_ensaio_veneza4:
            bolas_do_bingo_json = add(bolas_do_bingo_json, people)

    _json_montado = json_montado(
        bolas_do_bingo_json=bolas_do_bingo_json,
        lista_ensaio_alameda=lista_ensaio_alameda,
        lista_ensaio_jardim_copa_1=lista_ensaio_jardim_copa1,
        lista_ensaio_jardim_copa_2=lista_ensaio_jardim_copa2,
        lista_ensaio_nova_divineia_1=lista_ensaio_nova_divineia1,
        lista_ensaio_nova_divineia_2=lista_ensaio_nova_divineia2,
        lista_ensaio_piedade=lista_ensaio_piedade,
        lista_ensaio_veneza_4=lista_ensaio_veneza4,
        habilitar_lista_alameda=habilitar_lista_alameda,
        habilitar_lista_jardim_copa_1=habilitar_lista_jardim_copa1,
        habilitar_lista_jardim_copa_2=habilitar_lista_jardim_copa2,
        habilitar_lista_nova_divineia_1=habilitar_lista_nova_divineia11,
        habilitar_lista_nova_divineia_2=habilitar_lista_nova_divineia12,
        habilitar_lista_piedade=habilitar_lista_piedade,
        habilitar_lista_veneza_4=habilitar_lista_veneza4
    )
    update_db(g, _json_montado)


def remove_historico(g, bolas, mes_escolhido, _print=False):
    # print('Bolas do Bingo:', BolasDoBingo)
    bolas_do_bingo_json = bolas[0].bolasDoBingoJson
    nome_sorteado = bolas_do_bingo_json.NomeSorteado
    historico_sorteio = bolas_do_bingo_json.HistoricoSorteio

    if mes_escolhido in historico_sorteio:
        historico_sorteio.pop(mes_escolhido)
    elif mes_escolhido == 'todos' and len(historico_sorteio) > 0:
        historico_sorteio = {}

    _json_montado = json_montado(
        bolas_do_bingo_json=bolas_do_bingo_json,
        nome_sorteado_anterior=bolas_do_bingo_json.NomeSorteado,
        nome_sorteado=nome_sorteado,
        historico_sorteio=historico_sorteio
    )
    update_db(g, _json_montado)
