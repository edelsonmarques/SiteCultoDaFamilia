from enums.mes import meses_name
def sorted_mes(data):
    new_dict = dict()
    for mes in meses_name:
        if mes in data:
            new_dict[mes]= data[mes]
    return new_dict