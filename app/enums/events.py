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
    else:
        baixo = {'singular': 'Mãe', 'plural': 'Mães'}
        cima = {'singular': 'Filho(a)', 'plural': 'Filhos(as)'}
    return [baixo, cima]
