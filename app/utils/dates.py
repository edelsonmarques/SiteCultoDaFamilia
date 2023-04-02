from datetime import datetime, date
from enums import meses


def pegar_mes(mes_atual):
    if mes_atual == '':
        mes_atual = date.today().month
        if mes_atual in [1]:
            mes_atual = meses.JANEIRO
        elif mes_atual in [2]:
            mes_atual = meses.FEVEREIRO
        elif mes_atual in [11]:
            mes_atual = meses.NOVEMBRO
        elif mes_atual in [12]:
            mes_atual = meses.DEZEMBRO
        elif mes_atual in [3]:
            mes_atual = meses.MARCO
        elif mes_atual in [4]:
            mes_atual = meses.ABRIL
        elif mes_atual in [5]:
            mes_atual = meses.MAIO
        elif mes_atual in [6]:
            mes_atual = meses.JUNHO
        elif mes_atual in [7]:
            mes_atual = meses.JULHO
        elif mes_atual in [8]:
            mes_atual = meses.AGOSTO
        elif mes_atual in [9]:
            mes_atual = meses.SETEMBRO
        else:
            mes_atual = meses.OUTUBRO
    return mes_atual


def retornar_idade(nascimento):
    if nascimento not in ['nan', '', '00/00/0000']:
        nascimento = datetime.strptime(nascimento, "%d/%m/%Y").date()
        today = date.today()
        return str(today.year -
                   nascimento.year - (
                           (today.month, today.day) <
                           (nascimento.month, nascimento.day)
                   )
                   )
    if nascimento not in ['nan', '00/00/0000']:
        nascimento = date.today()
        return retornar_idade(str(f"{nascimento.day}/"
                                  f"{nascimento.month}/"
                                  f"{nascimento.year}"))
    if nascimento in ['00/00/0000']:
        return str(30)
    else:
        return str(30)


def niver_casamento(casamento, mes, mes_teste=0):
    if casamento not in ['nan', '', '00/00/0000']:
        if mes_teste == 0:
            casamento = datetime.strptime(casamento, "%d/%m/%Y").date()
            casamento = casamento.month
            if casamento in [1, 2]:
                casamento = 2
            elif casamento in [11, 12]:
                casamento = 11

            if mes[0].lower().__contains__(meses.JANEIRO) or\
                    mes[0].lower().__contains__(meses.FEVEREIRO):
                mes_teste = 2
            elif mes[0].lower().__contains__(meses.NOVEMBRO) or \
                    mes[0].lower().__contains__(meses.DEZEMBRO):
                mes_teste = 11
            elif mes[0].lower().__contains__(meses.MARCO):
                mes_teste = 3
            elif mes[0].lower().__contains__(meses.ABRIL):
                mes_teste = 4
            elif mes[0].lower().__contains__(meses.MAIO):
                mes_teste = 5
            elif mes[0].lower().__contains__(meses.JUNHO):
                mes_teste = 6
            elif mes[0].lower().__contains__(meses.JULHO):
                mes_teste = 7
            elif mes[0].lower().__contains__(meses.AGOSTO):
                mes_teste = 8
            elif mes[0].lower().__contains__(meses.SETEMBRO):
                mes_teste = 9
            elif mes[0].lower().__contains__(meses.OUTUBRO):
                mes_teste = 10
            else:
                return niver_casamento(casamento, mes,
                                       datetime.now().date().month)
        else:
            if mes_teste in [1, 2]:
                mes_teste = 2
            elif mes_teste in [11, 12]:
                mes_teste = 11
        if casamento == mes_teste:
            return True
        else:
            return False
    else:
        return False
