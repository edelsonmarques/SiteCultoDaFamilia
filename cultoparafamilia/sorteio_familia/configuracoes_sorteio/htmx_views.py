from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import posixpath
from enums.congregacoes import congregacoes_names, congregacoes_lists_names
from enums.pages_names import pages_names
from enums.pages_links import pages_links
from enums.events import EVENTOSEMINARIO, evento
from cultoparafamilia.sorteio_familia.models import DadosDict, return_info_user
from cultoparafamilia.db.firebase import load_lista_presenca, load_lista_usuarios
from cultoparafamilia.sorteio_familia.functions.mover_congregacoes import retirar_congregacao, inserir_congregacao

# Create your views here.
@login_required(login_url=pages_links['LOGIN_PAGE'])
def config_list(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    atualizou = False
    if 'recarregar' in request.POST:
        set_mes_sorteio(request, save=True, recharge=True)
        # TODO: Recarregar a API para atualizar a lista de mês sorteio
        _, dados = dados.load()
        return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'part_configuracoes_sorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})
    if request.POST['confAPI'] not in [dados.confAPI]:
        set_api(request, save=True)
        _, dados = dados.load()
        return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'part_configuracoes_sorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})
    if request.POST['carregar'] not in [dados.mesSorteio, '']:
        set_mes_sorteio(request, save=True)
        # testar o que realmente vai precisar
        _, dados = dados.load()
        return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'part_configuracoes_sorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})
    
    if 'dinamica_mae_pai' in request.POST and (request.POST['dinamica_mae_pai'] != ''):
        selecao_mae_pai(request, save=True)
        
    if 'dinamica' in request.POST and (request.POST['dinamica'] != ''):
        set_dinamica(request, save=True)
    
    if 'menor_solteiro' in request.POST  and (request.POST['menor_solteiro'] != ''):
        move_to_geral(request, save=True)
    if atualizou:
        _, dados = dados.load()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'part_configuracoes_sorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})

@login_required(login_url=pages_links['LOGIN_PAGE'])
def habilitar_evento(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if 'voltar' in request.POST:
        habilitar_evento = False
    else:
        habilitar_evento = request.POST['habilitar_evento']
        if 'desabilitar' in habilitar_evento.lower():
            habilitar_evento = False
            dados.evento.selecaoEventoEspecial = ['']
        else:
            habilitar_evento = True
    dados.habilitarEvento = habilitar_evento
    dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'part_configuracoes_sorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), 'events': {'EVENTOSEMINARIO': EVENTOSEMINARIO}, **return_info_user(request)})

@login_required(login_url=pages_links['LOGIN_PAGE'])
def carregar_evento(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    dados.evento.selecaoEventoEspecial = evento(request.POST['carregar_evento'])
    dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'part_configuracoes_sorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), 'events': {'EVENTOSEMINARIO': EVENTOSEMINARIO}, **return_info_user(request)})

@login_required(login_url=pages_links['LOGIN_PAGE'])
def selecao_mae_pai(request, save=False):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    # inserir pessoa
    for cartao in  request.POST['dinamica_mae_pai'].split(','):
        if cartao in dados.geral.listaGeral.filtro and cartao not in dados.evento.listaDinamicaMaePai.filtro:
            dados.evento.selecaoListaMaePai[cartao] = dados.geral.listaGeral.filtro[cartao]
    
    # seleção
    selecao = []
    for key in request.POST.keys():
        if key.__contains__('selecao'):
            selecao.append(key)
    for select in selecao:
        cartao = select.split(',')[1]
        pos_pessoa = int(select.split(',')[2])
        if cartao not in dados.evento.listaDinamicaMaePai.filtro:
            dados.evento.listaDinamicaMaePai.filtro[f'{cartao}'] = []
            dados.evento.listaDinamicaMaePai.filtro[cartao].append(dados.evento.selecaoListaMaePai[cartao][pos_pessoa])
            dados.evento.listaDinamicaMaePai.lista.append(dados.evento.selecaoListaMaePai[cartao][pos_pessoa])
        dados.evento.selecaoListaMaePai.pop(cartao)
    
    dados.save()
    if not save:
        return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'dinamica_eventos.html'), {'pages_names': pages_names, 'dados': dados.to_object(), 'events': {'EVENTOSEMINARIO': EVENTOSEMINARIO}, **return_info_user(request)})
    return True

@login_required(login_url=pages_links['LOGIN_PAGE'])
def selecao_filhos_pais(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    # inserir pessoa
    if request.POST['dinamica_mae'] != '':
        for cartao in request.POST['dinamica_mae'].split(','):
            if cartao in dados.geral.listaGeral.filtro and cartao not in dados.evento.selecaoListaFilhosPais:
                dados.evento.selecaoListaFilhosPais[cartao] = {}
                dados.evento.selecaoListaFilhosPais[cartao]['pais'] = dados.geral.listaGeral.filtro[cartao]
            if 'filhos' not in dados.evento.selecaoListaFilhosPais[cartao]:
                dados.evento.selecaoListaFilhosPais[cartao]['filhos'] = []
            for filho in  request.POST['dinamica_filho'].split(','):
                if filho.__contains__('|'):
                    if filho in dados.geral.listaMenor.filtro:
                        dados.evento.selecaoListaFilhosPais[cartao]['filhos'].append(dados.geral.listaMenor.filtro[filho][0])
                    elif filho in dados.geral.listaGeral.filtro:
                        for adulto in dados.geral.listaGeral.filtro[filho]:
                            dados.evento.selecaoListaFilhosPais[cartao]['filhos'].append(adulto)
                else:
                    dados.evento.selecaoListaFilhosPais[cartao]['filhos'].append(filho)
            dados.evento.selecaoListaFilhosPais[cartao]['filhos'] = list(set(dados.evento.selecaoListaFilhosPais[cartao]['filhos']))
            
    # seleção
    selecao = []
    for key in request.POST.keys():
        if key.__contains__('selecao'):
            selecao.append(key)
    separacao = {}
    for select in selecao:
        cartao = select.split(',')[1]
        if cartao not in separacao:
            separacao[cartao] = {} 
        parente = select.split(',')[2]
        if (parente.lower().__contains__('filho') or parente.lower().__contains__('neto')) and 'filhos' not in separacao[cartao]:
            separacao[cartao]['filhos'] = []
        elif 'pais' not in separacao[cartao]:
            separacao[cartao]['pais'] = []
        pos_pessoa = int(select.split(',')[3])
        texto = ""
        if (parente.lower().__contains__('filho') or parente.lower().__contains__('neto')):
            texto = f'{parente}: {dados.evento.selecaoListaFilhosPais[cartao]["filhos"][pos_pessoa].split("|")[0]}|{cartao}'
            separacao[cartao]['filhos'].append(texto)
        else:
            if len(separacao[cartao]['pais']) == 0:
                texto = f'{parente}: |{dados.evento.selecaoListaFilhosPais[cartao]["pais"][pos_pessoa]}'
            if texto != '':
                separacao[cartao]['pais'].append(texto)
    
    for cartao in separacao:
        if cartao in dados.evento.listaDinamicaFilhosPais.filtro and separacao[cartao]['pais'] not in dados.evento.listaDinamicaFilhosPais.filtro[cartao]:
            separacao.pop(cartao)
        for index, pessoa in enumerate(separacao[cartao]['filhos']):
            pronome = separacao[cartao]['pais'][0].split('|')[0]
            nome = separacao[cartao]['pais'][0].split('|')[1]
            cartao = f"{separacao[cartao]['pais'][0].split('|')[2]}|{separacao[cartao]['pais'][0].split('|')[3]}"
            idade = separacao[cartao]['pais'][0].split('|')[4]
            casamento = separacao[cartao]['pais'][0].split('|')[5]
            estado_civil = separacao[cartao]['pais'][0].split('|')[6]
            separacao[cartao]['filhos'][index] = f'{pessoa}|{idade}|{casamento}|{estado_civil}|{pronome}{nome}'
            if cartao not in dados.evento.listaDinamicaFilhosPais.filtro:
                dados.evento.listaDinamicaFilhosPais.filtro[f'{cartao}'] = []
            dados.evento.listaDinamicaFilhosPais.filtro[cartao].append("|".join(separacao[cartao]['pais'][0].split('|')[1:]))
            dados.evento.listaDinamicaFilhosPais.filtro[cartao].append(f'{pessoa}|{idade}|{casamento}|{estado_civil}|{pronome}{nome}')
            dados.evento.listaDinamicaFilhosPais.filtro[cartao] = list(set(dados.evento.listaDinamicaFilhosPais.filtro[cartao]))
            dados.evento.listaDinamicaFilhosPais.lista[f'{pessoa}|{idade}|{casamento}|{estado_civil}|{pronome}{nome}'] = cartao
        dados.evento.selecaoListaFilhosPais.pop(cartao)
            
    dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'dinamica_eventos.html'), {'pages_names': pages_names, 'dados': dados.to_object(), 'events': {'EVENTOSEMINARIO': EVENTOSEMINARIO}, **return_info_user(request)})

@login_required(login_url=pages_links['LOGIN_PAGE'])
def set_sorteios(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    for key in request.POST.keys():
        if key.__contains__('set'):
            CJ = key.split('_')[1]
            qtd = key.split('_')[2]
            if len(dados.evento.listaDeOutNov[CJ][qtd]) <= int(request.POST[key][0]):
                dados.evento.listaSet[CJ][qtd] = len(dados.evento.listaDeOutNov[CJ][qtd])
            else:
                dados.evento.listaSet[CJ][qtd] = int(request.POST[key][0])
    dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'dinamica_eventos.html'), {'pages_names': pages_names, 'dados': dados.to_object(), 'events': {'EVENTOSEMINARIO': EVENTOSEMINARIO}, **return_info_user(request)})

@login_required(login_url=pages_links['LOGIN_PAGE'])
def set_dinamica_seminario(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    lista = set()
    for cartao in  request.POST['dinamica_seminario'].split(','):
        if cartao in dados.evento.listaDeOutNov.filtro:
            lista.update(dados.evento.listaDeOutNov.filtro[cartao])
    dados.geral.listaDinamica.extend(list(lista))
    dados.geral.listaDinamica = list(set(dados.geral.listaDinamica))
    dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'dinamica_eventos.html'), {'pages_names': pages_names, 'dados': dados.to_object(), 'events': {'EVENTOSEMINARIO': EVENTOSEMINARIO}, **return_info_user(request)})

@login_required(login_url=pages_links['LOGIN_PAGE'])
def set_dinamica(request, save=False):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    lista = set()
    for cartao in  request.POST['dinamica'].split(','):
        if cartao in dados.geral.listaGeral.filtro:
            if len(dados.geral.listaGeral.filtro[cartao]) % 2 == 0:
                lista.update(dados.geral.listaGeral.filtro[cartao])
    dados.geral.listaDinamica.extend(list(lista))
    dados.geral.listaDinamica = list(set(dados.geral.listaDinamica))
    dados.save()
    if not save:
        return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'dinamica_eventos.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})
    return True

@login_required(login_url=pages_links['LOGIN_PAGE'])
def set_api(request, save=False):
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if request.POST['confAPI'] != os.getenv('FIREBASE_URL'):
        dados.confAPI = request.POST['confAPI']
    else:
        dados.confAPI = ""
    
    # Futuramente implementar para carregar da API que quiser!!! ou resetar dados já existentes
    # TODO: carregar a API para poder funcionar direitinho
    dados.save()
    if not save:
        return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'part_configuracoes_sorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})

@login_required(login_url=pages_links['LOGIN_PAGE'])
def set_mes_sorteio(request, save=False, recharge=False):
    from cultoparafamilia.sorteio_familia.functions import separar_pessoas_sorteio
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if request.POST['carregar'] != dados.mesSorteio and 'recarregar' not in request.POST:
        dados.mesSorteio = request.POST['carregar']
        dados = separar_pessoas_sorteio.load_month(dados, request.POST['carregar'])
    elif 'recarregar' in request.POST:
        dados.listaMesSorteio = [x for x in load_lista_presenca().keys()]
        dados = separar_pessoas_sorteio.limpar_base(dados)
    # TODO: Implementar para carregar o mês do sorteio selecionado!
    dados.save()
    if not save and not recharge:
        return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'part_configuracoes_sorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})

@login_required(login_url=pages_links['LOGIN_PAGE'])
def move_to_geral(request, save=False):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    # 'menor_solteiro': ['']
    if request.POST['carregar'] != dados.mesSorteio and 'recarregar' not in request.POST:
        dados.mesSorteio = request.POST['carregar']
    lista = []
    for cartao in  request.POST['menor_solteiro'].split(','):
        if cartao in dados.geral.listaMenor.filtro:
            lista.update(dados.geral.listaMenor.filtro[cartao])
            dados.geral.listaGeral.filtro[cartao] = dados.geral.listaMenor.filtro[cartao]
            dados.geral.listaMenor.filtro.pop(cartao)
    for pessoa in lista:
        try:
            dados.geral.listaMenor.lista.remove(pessoa)
        except ValueError:
            continue
        
    dados.geral.listaGeral.lista.extend(lista)
    dados.geral.listaGeral.lista = list(set(dados.geral.listaGeral.lista))
    dados.save()
    if not save:
        return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'part_configuracoes_sorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})
    return True

@login_required(login_url=pages_links['LOGIN_PAGE'])
def habilitar_ensaio(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    habilitar_ensaio = request.POST['habilitar_ensaio']
    if 'desabilitar' in habilitar_ensaio.lower():
        habilitar_ensaio = False
    else:
        habilitar_ensaio = True
    dados.habilitarEnsaio = habilitar_ensaio
    dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'ensaios.html'), {'pages_names': pages_names, 'dados': dados.to_object(), 'events': {'EVENTOSEMINARIO': EVENTOSEMINARIO}, **return_info_user(request)})

@login_required(login_url=pages_links['LOGIN_PAGE'])
def desabilitar_congregacao(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    for congregacao in congregacoes_names:
        if f'des_{congregacao}' in request.POST:
            dados.ensaio[congregacoes_names[congregacao]] = True
            dados.ensaio = retirar_congregacao(dados.ensaio, dados.ensaio[congregacoes_lists_names[congregacao]])
        else:
            if dados.ensaio[congregacoes_names[congregacao]]:
                dados.ensaio[congregacoes_names[congregacao]] = False
                dados.ensaio = inserir_congregacao(dados.ensaio, dados.ensaio[congregacoes_lists_names[congregacao]])
    dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'part_configuracoes_sorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), 'events': {'EVENTOSEMINARIO': EVENTOSEMINARIO}, **return_info_user(request)})

@login_required(login_url=pages_links['LOGIN_PAGE'])
def historico(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if 'remove' in request.POST and request.POST['mes_historico'] != '':
        if request.POST['mes_historico'] != 'todos':
            dados.historico.historicoSorteio.pop(request.POST['mes_historico'])
        else:
            meses = dados.historico.historicoSorteio.copy().keys()
            for historico in meses:
                dados.historico.historicoSorteio.pop(historico)
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'partials',  'historicos.html'), {'pages_names': pages_names, 'dados': dados.to_object(), 'events': {'EVENTOSEMINARIO': EVENTOSEMINARIO}, **return_info_user(request)})

# TODO: Realizar carregar presença nos seminário
# TODO: Verificar se falta algum outro passo de configurações