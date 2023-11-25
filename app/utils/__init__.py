from enums import actions, events, meses


def contar_presenca(x):
    return len(','.join(
        ('a' if p.__contains__('ensaio') else p)
        for p in x.removesuffix(',').split(',')).
               replace('a,', '').split(','))


def inserir_presenca(lista_princ, lista_temp, dados, lista_return, base,
                     qtd, hist, add: str = actions.GERAL, event: str = ''):
    try:
        n = lista_temp.index(dados[base])
        pessoa = lista_princ[n]
        tem_hist = -1

        # Verificar sorteios anteriores
        if event in [events.SEMINARIO_3, events.OUTUBRO]:
            columns = []
        elif event in [events.SEMINARIO_1]:
            columns = [meses.OUTUBRO]
        else:
            columns = [meses.OUTUBRO, meses.NOVEMBRO_1]

        for mes in columns:
            if mes in hist:
                histMes = hist[mes]
                histMes = list(
                    {'|'.join(x.split('|', 3)[1:3]) for x in histMes})
                try:
                    tem_hist = histMes.index(dados['idNumero'])
                except ValueError:
                    pass

        def include(numbers: list):
            for num in numbers:
                lista_return[add][f'{num}'].append(pessoa)

        if tem_hist == -1:
            if 4 <= dados[qtd] < 8:
                include([dados[qtd]])
            else:
                include([8])
        else:
            n = tem_hist
    except ValueError:
        n = -1
    return lista_return, n
