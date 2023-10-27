from enums.meses import OUTUBRO

OUTUBRO = OUTUBRO.capitalize()
SEMINARIO_1 = 'Seminário Dia 1'
SEMINARIO_2 = 'Seminário Dia 2'
SEMINARIO_3 = 'Seminário Dia 3'
EVENTOSEMINARIO = [OUTUBRO, SEMINARIO_1, SEMINARIO_2,
                   SEMINARIO_3]
EVENTOFILHOSNETOS = [OUTUBRO, SEMINARIO_1, SEMINARIO_2,
                   SEMINARIO_3]
EVENTOSEMINARIOBLANK = ['']
EVENTOSEMINARIOBLANK.extend(EVENTOSEMINARIO)


def evento(festa='Mães'):
    if festa.__contains__('Pais'):
        baixo = {'singular': 'Pai', 'plural': 'Pais'}
        cima = {'singular': 'Filho(a)', 'plural': 'Filhos(as)'}
    elif festa.__contains__('Namorados'):
        baixo = {'singular': 'Namorado(a)', 'plural': 'Namorados'}
        cima = {'singular': 'Namorado(a)', 'plural': 'Namorados'}
    elif festa.__contains__('Avós'):
        baixo = {'singular': 'Avô/Avó', 'plural': 'Avós'}
        cima = {'singular': 'Neto(a)', 'plural': 'Netos(as)'}
    elif festa.__contains__('Mães'):
        baixo = {'singular': 'Mãe', 'plural': 'Mães'}
        cima = {'singular': 'Filho(a)', 'plural': 'Filhos(as)'}
    else:
        return [festa]
    return [baixo, cima]
