from classes.db_classes import BolasDoBingoJson


def json_montado(bolas_do_bingo_json: BolasDoBingoJson = None,
                 conf_api: list = None,
                 lista_geral: list = None,
                 lista_visitante: list = None,
                 lista_menor: list = None,
                 lista_dinamica: list = None,
                 lista_niver_casamento: list = None,
                 lista_ensaio: list = None,
                 lista_ensaio_alameda: list = None,
                 lista_ensaio_jardim_copa_1: list = None,
                 lista_ensaio_jardim_copa_2: list = None,
                 lista_ensaio_nova_divineia_1: list = None,
                 lista_ensaio_nova_divineia_2: list = None,
                 lista_ensaio_piedade: list = None,
                 lista_ensaio_veneza_4: list = None,
                 habilitar_lista_alameda: list = None,
                 habilitar_lista_jardim_copa_1: list = None,
                 habilitar_lista_jardim_copa_2: list = None,
                 habilitar_lista_nova_divineia_1: list = None,
                 habilitar_lista_nova_divineia_2: list = None,
                 habilitar_lista_piedade: list = None,
                 habilitar_lista_veneza_4: list = None,
                 mes_sorteio: list = None,
                 lista_mes_sorteio: list = None,
                 nome_sorteado_anterior: list = None,
                 nome_sorteado: list = None,
                 ensaio: list = None,
                 habilitar_ensaio: list = None,
                 ):
    if bolas_do_bingo_json is None:
        if habilitar_ensaio is None:
            habilitar_ensaio = ['']
        if ensaio is None:
            ensaio = ['']
        if nome_sorteado is None:
            nome_sorteado = ['']
        if nome_sorteado_anterior is None:
            nome_sorteado_anterior = ['']
        if lista_mes_sorteio is None:
            lista_mes_sorteio = []
        if mes_sorteio is None:
            mes_sorteio = ['']
        if habilitar_lista_veneza_4 is None:
            habilitar_lista_veneza_4 = ['true']
        if habilitar_lista_piedade is None:
            habilitar_lista_piedade = ['true']
        if habilitar_lista_nova_divineia_2 is None:
            habilitar_lista_nova_divineia_2 = ['true']
        if habilitar_lista_nova_divineia_1 is None:
            habilitar_lista_nova_divineia_1 = ['true']
        if habilitar_lista_jardim_copa_2 is None:
            habilitar_lista_jardim_copa_2 = ['true']
        if habilitar_lista_jardim_copa_1 is None:
            habilitar_lista_jardim_copa_1 = ['true']
        if habilitar_lista_alameda is None:
            habilitar_lista_alameda = ['true']
        if lista_ensaio_veneza_4 is None:
            lista_ensaio_veneza_4 = []
        if lista_ensaio_piedade is None:
            lista_ensaio_piedade = []
        if lista_ensaio_nova_divineia_2 is None:
            lista_ensaio_nova_divineia_2 = []
        if lista_ensaio_nova_divineia_1 is None:
            lista_ensaio_nova_divineia_1 = []
        if lista_ensaio_jardim_copa_2 is None:
            lista_ensaio_jardim_copa_2 = []
        if lista_ensaio_jardim_copa_1 is None:
            lista_ensaio_jardim_copa_1 = []
        if lista_ensaio_alameda is None:
            lista_ensaio_alameda = []
        if lista_ensaio is None:
            lista_ensaio = []
        if lista_niver_casamento is None:
            lista_niver_casamento = []
        if lista_dinamica is None:
            lista_dinamica = []
        if lista_menor is None:
            lista_menor = []
        if lista_visitante is None:
            lista_visitante = []
        if lista_geral is None:
            lista_geral = []
        if conf_api is None:
            conf_api = ['']
    else:
        if habilitar_ensaio is None:
            habilitar_ensaio = bolas_do_bingo_json.HabilitarEnsaio
        if ensaio is None:
            ensaio = bolas_do_bingo_json.Ensaio
        if nome_sorteado is None:
            nome_sorteado = bolas_do_bingo_json.NomeSorteado
        if nome_sorteado_anterior is None:
            nome_sorteado_anterior = bolas_do_bingo_json.NomeSorteadoAnterior
        if lista_mes_sorteio is None:
            lista_mes_sorteio = bolas_do_bingo_json.ListaMesSorteio
        if mes_sorteio is None:
            mes_sorteio = bolas_do_bingo_json.MesSorteio
        if habilitar_lista_veneza_4 is None:
            habilitar_lista_veneza_4 = \
                bolas_do_bingo_json.HabilitarListaVeneza4
        if habilitar_lista_piedade is None:
            habilitar_lista_piedade = bolas_do_bingo_json.HabilitarListaPiedade
        if habilitar_lista_nova_divineia_2 is None:
            habilitar_lista_nova_divineia_2 = \
                bolas_do_bingo_json.HabilitarListaNovaDivineia2
        if habilitar_lista_nova_divineia_1 is None:
            habilitar_lista_nova_divineia_1 = \
                bolas_do_bingo_json.HabilitarListaNovaDivineia1
        if habilitar_lista_jardim_copa_2 is None:
            habilitar_lista_jardim_copa_2 = \
                bolas_do_bingo_json.HabilitarListaJardimCopa2
        if habilitar_lista_jardim_copa_1 is None:
            habilitar_lista_jardim_copa_1 = \
                bolas_do_bingo_json.HabilitarListaJardimCopa1
        if habilitar_lista_alameda is None:
            habilitar_lista_alameda = bolas_do_bingo_json.HabilitarListaAlameda
        if lista_ensaio_veneza_4 is None:
            lista_ensaio_veneza_4 = bolas_do_bingo_json.ListaEnsaioVeneza4
        if lista_ensaio_piedade is None:
            lista_ensaio_piedade = bolas_do_bingo_json.ListaEnsaioPiedade
        if lista_ensaio_nova_divineia_2 is None:
            lista_ensaio_nova_divineia_2 = \
                bolas_do_bingo_json.ListaEnsaioNovaDivineia2
        if lista_ensaio_nova_divineia_1 is None:
            lista_ensaio_nova_divineia_1 = \
                bolas_do_bingo_json.ListaEnsaioNovaDivineia1
        if lista_ensaio_jardim_copa_2 is None:
            lista_ensaio_jardim_copa_2 = \
                bolas_do_bingo_json.ListaEnsaioJardimCopa2
        if lista_ensaio_jardim_copa_1 is None:
            lista_ensaio_jardim_copa_1 = \
                bolas_do_bingo_json.ListaEnsaioJardimCopa1
        if lista_ensaio_alameda is None:
            lista_ensaio_alameda = bolas_do_bingo_json.ListaEnsaioAlameda
        if lista_ensaio is None:
            lista_ensaio = bolas_do_bingo_json.ListaEnsaio
        if lista_niver_casamento is None:
            lista_niver_casamento = bolas_do_bingo_json.ListaNiverCasamento
        if lista_dinamica is None:
            lista_dinamica = bolas_do_bingo_json.ListaDinamica
        if lista_menor is None:
            lista_menor = bolas_do_bingo_json.ListaMenor
        if lista_visitante is None:
            lista_visitante = bolas_do_bingo_json.ListaVisitante
        if lista_geral is None:
            lista_geral = bolas_do_bingo_json.ListaGeral
        if conf_api is None:
            conf_api = bolas_do_bingo_json.ConfAPI
    return {
        'ConfAPI': conf_api,
        'ListaGeral': lista_geral,
        'ListaVisitante': lista_visitante,
        'ListaMenor': lista_menor,
        'ListaDinamica': lista_dinamica,
        'ListaNiverCasamento': lista_niver_casamento,
        'ListaEnsaio': lista_ensaio,
        'ListaEnsaioAlameda': lista_ensaio_alameda,
        'ListaEnsaioJardimCopa1': lista_ensaio_jardim_copa_1,
        'ListaEnsaioJardimCopa2': lista_ensaio_jardim_copa_2,
        'ListaEnsaioNovaDivineia1': lista_ensaio_nova_divineia_1,
        'ListaEnsaioNovaDivineia2': lista_ensaio_nova_divineia_2,
        'ListaEnsaioPiedade': lista_ensaio_piedade,
        'ListaEnsaioVeneza4': lista_ensaio_veneza_4,
        'HabilitarListaAlameda': habilitar_lista_alameda,
        'HabilitarListaJardimCopa1': habilitar_lista_jardim_copa_1,
        'HabilitarListaJardimCopa2': habilitar_lista_jardim_copa_2,
        'HabilitarListaNovaDivineia1': habilitar_lista_nova_divineia_1,
        'HabilitarListaNovaDivineia2': habilitar_lista_nova_divineia_2,
        'HabilitarListaPiedade': habilitar_lista_piedade,
        'HabilitarListaVeneza4': habilitar_lista_veneza_4,
        'MesSorteio': mes_sorteio,
        'ListaMesSorteio': lista_mes_sorteio,
        'NomeSorteadoAnterior': nome_sorteado_anterior,
        'NomeSorteado': nome_sorteado,
        'Ensaio': ensaio,
        'HabilitarEnsaio': habilitar_ensaio
    }
