def convert_str_mes(num):
    return str(num).zfill(2)

JANEIRO = 'janeiro'
FEVEREIRO = 'fevereiro'
MARCO = 'marco'
ABRIL = 'abril'
MAIO = 'maio'
JUNHO = 'junho'
JULHO = 'julho'
AGOSTO = 'agosto'
SETEMBRO = 'setembro'
OUTUBRO = 'outubro'
NOVEMBRO = 'novembro'
NOVEMBRO_1 = 'novembro_1'
NOVEMBRO_2 = 'novembro_2'
NOVEMBRO_3 = 'novembro_3'
DEZEMBRO = 'dezembro'

NUM_JANEIRO = 1
NUM_FEVEREIRO = 2
NUM_MARCO = 3
NUM_ABRIL = 4
NUM_MAIO = 5
NUM_JUNHO = 6
NUM_JULHO = 7
NUM_AGOSTO = 8
NUM_SETEMBRO = 9
NUM_OUTUBRO = 10
NUM_NOVEMBRO = 11
NUM_NOVEMBRO_1 = 11.1
NUM_NOVEMBRO_2 = 11.2
NUM_NOVEMBRO_3 = 11.3
NUM_DEZEMBRO = 12

meses_name = [
    JANEIRO, FEVEREIRO, MARCO, ABRIL, MAIO,
    JUNHO, JULHO, AGOSTO, SETEMBRO, OUTUBRO, 
    NOVEMBRO, DEZEMBRO
]

meses_number = [
    convert_str_mes(NUM_JANEIRO), convert_str_mes(NUM_FEVEREIRO), convert_str_mes(NUM_MARCO), 
    convert_str_mes(NUM_ABRIL), convert_str_mes(NUM_MAIO), convert_str_mes(NUM_JUNHO), 
    convert_str_mes(NUM_JULHO), convert_str_mes(NUM_AGOSTO), convert_str_mes(NUM_SETEMBRO), 
    convert_str_mes(NUM_OUTUBRO), convert_str_mes(NUM_NOVEMBRO), convert_str_mes(NUM_DEZEMBRO)
]

mes_num_dict = {
    JANEIRO: convert_str_mes(NUM_JANEIRO), 
    FEVEREIRO: convert_str_mes(NUM_FEVEREIRO),  
    MARCO: convert_str_mes(NUM_MARCO),  
    ABRIL: convert_str_mes(NUM_ABRIL),  
    MAIO: convert_str_mes(NUM_MAIO), 
    JUNHO: convert_str_mes(NUM_JUNHO),  
    JULHO: convert_str_mes(NUM_JULHO),  
    AGOSTO: convert_str_mes(NUM_AGOSTO),  
    SETEMBRO: convert_str_mes(NUM_SETEMBRO),  
    OUTUBRO: convert_str_mes(NUM_OUTUBRO),  
    NOVEMBRO: convert_str_mes(NUM_NOVEMBRO),  
    DEZEMBRO: convert_str_mes(NUM_DEZEMBRO)
}
