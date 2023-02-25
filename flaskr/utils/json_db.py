from flaskr.classes.db_classes import BolasDoBingoJson


def json_montado(bolas_do_bingo_json: BolasDoBingoJson = None,
                 conf_api: list = None,
                 lista_geral: list = None,
                 lista_visitante: list = None,
                 lista_menor: list = None,
                 lista_dinamica: list = None,
                 lista_niver_casamento: list = None,
                 lista_ensaio: list = None,
                 mes_sorteio: list = None,
                 lista_mes_sorteio: list = None,
                 nome_sorteado_anterior: list = None,
                 nome_sorteado: list = None,
                 opcao: list = None,
                 proximo: list = None,
                 ensaio: list = None,
                 habilitar_ensaio: list = None,
                 ):
    if bolas_do_bingo_json is None:
        if habilitar_ensaio is None:
            habilitar_ensaio = ['']
        if ensaio is None:
            ensaio = ['']
        if proximo is None:
            proximo = ['']
        if opcao is None:
            opcao = ['']
        if nome_sorteado is None:
            nome_sorteado = ['']
        if nome_sorteado_anterior is None:
            nome_sorteado_anterior = ['']
        if lista_mes_sorteio is None:
            lista_mes_sorteio = []
        if mes_sorteio is None:
            mes_sorteio = ['']
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
        return {
            'ConfAPI': conf_api,
            'ListaGeral': lista_geral,
            'ListaVisitante': lista_visitante,
            'ListaMenor': lista_menor,
            'ListaDinamica': lista_dinamica,
            'ListaNiverCasamento': lista_niver_casamento,
            'ListaEnsaio': lista_ensaio,
            'MesSorteio': mes_sorteio,
            'ListaMesSorteio': lista_mes_sorteio,
            'NomeSorteadoAnterior': nome_sorteado_anterior,
            'NomeSorteado': nome_sorteado,
            'Opcao': opcao,
            'Proximo': proximo,
            'Ensaio': ensaio,
            'HabilitarEnsaio': habilitar_ensaio
        }
    else:
        if habilitar_ensaio is None:
            habilitar_ensaio = bolas_do_bingo_json.HabilitarEnsaio
        if ensaio is None:
            ensaio = bolas_do_bingo_json.Ensaio
        if proximo is None:
            proximo = bolas_do_bingo_json.Proximo
        if opcao is None:
            opcao = bolas_do_bingo_json.Opcao
        if nome_sorteado is None:
            nome_sorteado = bolas_do_bingo_json.NomeSorteado
        if nome_sorteado_anterior is None:
            nome_sorteado_anterior = bolas_do_bingo_json.NomeSorteadoAnterior
        if lista_mes_sorteio is None:
            lista_mes_sorteio = bolas_do_bingo_json.ListaMesSorteio
        if mes_sorteio is None:
            mes_sorteio = bolas_do_bingo_json.MesSorteio
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
            'MesSorteio': mes_sorteio,
            'ListaMesSorteio': lista_mes_sorteio,
            'NomeSorteadoAnterior': nome_sorteado_anterior,
            'NomeSorteado': nome_sorteado,
            'Opcao': opcao,
            'Proximo': proximo,
            'Ensaio': ensaio,
            'HabilitarEnsaio': habilitar_ensaio
        }
