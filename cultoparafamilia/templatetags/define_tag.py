from django import template
from enums.events import EVENTOSEMINARIOBLANK, EVENTOSEMINARIO
register = template.Library()


@register.filter(name="define_dia_culto")
def define_dia_culto(val):
    val = val.split('/')[0]
    return val

@register.inclusion_tag("cultoparafamilia/sorteiofamilia/configuracoessorteio/partials/mes_sorteio.html", takes_context=True, name='mes_include')
def mes_include(context, pages_names, dados, logged):
    november = ['novembro_1', 'novembro_2', 'novembro_3']
    return {'pages_names': pages_names, 'dados': dados, 'logged': logged, 'mes_nov': november}


@register.inclusion_tag("cultoparafamilia/sorteiofamilia/configuracoessorteio/partials/dinamica_eventos.html", takes_context=True, name='dinamica_include')
def dinamica_include(context, pages_names, dados, logged):
    return {'pages_names': pages_names, 'dados': dados, 'logged': logged, 'events': {'EVENTOSEMINARIO': EVENTOSEMINARIO}}


@register.filter(name="sum_values")
def sum_values(dictval, listval=''):
    sum_values = 0
    for listname in listval.split(','):
        if listname in dictval['geral']:
            if listname.lower().__contains__('visitante'):
                sum_values += len(dictval['geral'][listname])
            else:
                sum_values += len(dictval['geral'][listname]['lista'])
        elif listname == '':
            pass
        else:
            sum_values = 'Error Value: ' + listname
            break
    return sum_values


@register.filter(name="selecao")
def selecao(selecaoEventoEspecial, enum=''):
    if enum == 'EVENTOSEMINARIOBLANK' and selecaoEventoEspecial[0] not in EVENTOSEMINARIOBLANK:
        return 1
    if enum == 'EVENTOSEMINARIO' and selecaoEventoEspecial[0] in EVENTOSEMINARIO:
        return 1
    if enum == 'NOTEVENTOSEMINARIO' and selecaoEventoEspecial[0] not in EVENTOSEMINARIO:
        return 1
    return 0

@register.filter(name="plural")
def plural(selecaoEventoEspecial, enum='0,singular'):
    num = int(enum.split(',')[0])
    enum = enum.split(',')[1]
    if enum == 'plural':
        return selecaoEventoEspecial[num]['plural']
    return selecaoEventoEspecial[num]['singular']

@register.filter(name="maepai")
def maepai(selecaoEventoEspecial, enum=0):
    if type(enum) is int:
        return selecaoEventoEspecial[0].split('|')[enum]
    if str(enum).isdigit():
        return selecaoEventoEspecial.split('|')[int(enum)]
    return selecaoEventoEspecial[enum]

@register.filter
def get_index(value, value_to_index):
    index = value.index(value_to_index)
    return index

@register.filter
def get_conteins(selecaoEventoEspecial, enum='0,'):
    num = int(enum.split(',')[0])
    enum = enum.split(',')[1]
    if enum == '':
        return 'Value empty: "' + enum + '"'
    if str(selecaoEventoEspecial[num]).__contains__(enum):
        return 1
    return 0

@register.filter
def get_string(value, index=0):
    return value[index]

@register.filter
def get_strip(value, index='|,0'):
    sep = index.split(',')[0]
    index = int(index.split(',')[1])
    return value.split(sep)[index]
