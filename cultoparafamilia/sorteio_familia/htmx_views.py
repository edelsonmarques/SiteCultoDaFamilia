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

@login_required(login_url=pages_links['LOGIN_PAGE'])
def reset_view(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if 'recarregar' in request.POST:
        from cultoparafamilia.sorteio_familia.functions import separar_pessoas_sorteio
        dados.listaMesSorteio = [x for x in load_lista_presenca().keys()]
        dados = separar_pessoas_sorteio.limpar_base(dados)
        # TODO: Implementar para carregar o mês do sorteio selecionado!
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'sorteiofamilia.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_geral(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.geral.listaGeral.lista) > 0:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosgeral(dados, 'listaGeral')
            
        # remover das listas
        dados = remover_pessoa_geral_filtro(dados, 'listaGeral')
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_menor(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.geral.listaMenor.lista) > 0:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosgeral(dados, 'listaMenor')
            
        # remover das listas
        dados = remover_pessoa_geral_filtro(dados, 'listaMenor')
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_niverCasamento(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.geral.listaNiverCasamento.lista) > 0:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosgeral(dados, 'listaNiverCasamento')
            
        # remover das listas
        dados = remover_pessoa_geral_filtro(dados, 'listaNiverCasamento')
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_visitante(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.geral.listaVisitante) > 0:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosgeral(dados, 'listaVisitante')
            
        # remover das listas
        dados = remover_pessoa_geral_lista(dados)
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_dinamica(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.geral.listaDinamica) > 0:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosgeral(dados, 'listaDinamica')
            
        # remover das listas
        dados = remover_pessoa_geral_lista(dados)
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


def sortear_dadosgeral(dados: DadosDict, lista: str):
    """
        Para Lista Geral, Lista Visitante, Lista Dinâmica, Lista Menor, Lista NiverCasamento
    """
    nome_sorteado = dados.geral.sortear(lista)
    if nome_sorteado is None:
        nome_sorteado = dados.historico.nomeSorteado
    if nome_sorteado not in dados.historico.historicoSorteio[dados.mesSorteio]:
        dados.historico.nomeSorteadoAnterior = dados.historico.nomeSorteado
        dados.historico.nomeSorteado = nome_sorteado
        dados.historico.historicoSorteio[dados.mesSorteio].append(nome_sorteado)
    return dados


def remover_pessoa_geral_filtro(dados: DadosDict, lista: str):
    nome_sorteado = dados.historico.nomeSorteado
    cartao = nome_sorteado.split('|')[1] + "|" + nome_sorteado.split('|')[2]
    if cartao in dados.geral[lista].filtro:
        filtro = dados.geral[lista].filtro[cartao]
        if cartao in dados.geral.listaGeral.filtro:
            for pessoa in filtro:
                dados.geral.listaGeral.lista.remove(pessoa)
            dados.geral.listaGeral.filtro.pop(cartao)
        if cartao in dados.geral.listaNiverCasamento.filtro:
            for pessoa in filtro:
                dados.geral.listaNiverCasamento.lista.remove(pessoa)
            dados.geral.listaNiverCasamento.filtro.pop(cartao)
        if cartao in dados.geral.listaMenor.filtro:
            for pessoa in filtro:
                dados.geral.listaMenor.lista.remove(pessoa)
            dados.geral.listaMenor.filtro.pop(cartao)
        for pessoa in filtro:
            if pessoa in dados.geral.listaVisitante:
                dados.geral.listaVisitante.remove(pessoa)
            if pessoa in dados.geral.listaDinamica:
                dados.geral.listaDinamica.remove(pessoa)
            
    return dados


def remover_pessoa_geral_lista(dados: DadosDict):
    nome_sorteado = dados.historico.nomeSorteado
    cartao = nome_sorteado.split('|')[1] + "|" + nome_sorteado.split('|')[2]
    if cartao in dados.geral.listaGeral.filtro:
        filtro = dados.geral.listaGeral.filtro[cartao]
    else:
        filtro = []
    if cartao in dados.geral.listaGeral.filtro:
        for pessoa in filtro:
            dados.geral.listaGeral.lista.remove(pessoa)
        dados.geral.listaGeral.filtro.pop(cartao)
    if cartao in dados.geral.listaNiverCasamento.filtro:
        for pessoa in filtro:
            dados.geral.listaNiverCasamento.lista.remove(pessoa)
        dados.geral.listaNiverCasamento.filtro.pop(cartao)
    if cartao in dados.geral.listaMenor.filtro:
        for pessoa in filtro:
            dados.geral.listaMenor.lista.remove(pessoa)
        dados.geral.listaMenor.filtro.pop(cartao)
    for pessoa in filtro:
        if pessoa in dados.geral.listaVisitante:
            dados.geral.listaVisitante.remove(pessoa)
        if pessoa in dados.geral.listaDinamica:
            dados.geral.listaDinamica.remove(pessoa)
    if len(filtro) == 0:
        if nome_sorteado in dados.geral.listaVisitante:
            dados.geral.listaVisitante.remove(nome_sorteado)
        if nome_sorteado in dados.geral.listaDinamica:
            dados.geral.listaDinamica.remove(nome_sorteado)
        
            
    return dados


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_ensaio(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.ensaio.listaEnsaio.lista) > 0:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosensaio(dados, 'listaEnsaio')
            
        # remover das listas
        dados = remover_pessoa_ensaio_filtro(dados, 'listaEnsaio')
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})

  
@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_alameda(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.ensaio.listaEnsaioAlameda.lista) > 0 and not dados.ensaio.habilitarListaAlameda:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosensaio(dados, 'listaEnsaioAlameda')
            
        # remover das listas
        dados = remover_pessoa_ensaio_filtro(dados, 'listaEnsaioAlameda')
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_jdcopacabana(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.ensaio.listaEnsaioJardimCopa1.lista) > 0 and not dados.ensaio.habilitarListaJardimCopa1:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        dados = sortear_dadosensaio(dados, 'listaEnsaioJardimCopa1')
            
        # remover das listas
        dados = remover_pessoa_ensaio_filtro(dados, 'listaEnsaioJardimCopa1')
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_jdcopacabana2(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.ensaio.listaEnsaioJardimCopa2.lista) > 0 and not dados.ensaio.habilitarListaJardimCopa2:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosensaio(dados, 'listaEnsaioJardimCopa2')
            
        # remover das listas
        dados = remover_pessoa_ensaio_filtro(dados, 'listaEnsaioJardimCopa2')
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_novadivineia(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.ensaio.listaEnsaioNovaDivineia1.lista) > 0 and not dados.ensaio.habilitarListaNovaDivineia1:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosensaio(dados, 'listaEnsaioNovaDivineia1')
            
        # remover das listas
        dados = remover_pessoa_ensaio_filtro(dados, 'listaEnsaioNovaDivineia1')
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_novadivineia2(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.ensaio.listaEnsaioNovaDivineia2.lista) > 0 and not dados.ensaio.habilitarListaNovaDivineia2:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosensaio(dados, 'listaEnsaioNovaDivineia2')
            
        # remover das listas
        dados = remover_pessoa_ensaio_filtro(dados, 'listaEnsaioNovaDivineia2')
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_piedade(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.ensaio.listaEnsaioPiedade.lista) > 0 and not dados.ensaio.habilitarListaPiedade:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosensaio(dados, 'listaEnsaioPiedade')
            
        # remover das listas
        dados = remover_pessoa_ensaio_filtro(dados, 'listaEnsaioPiedade')
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_veneza4(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.ensaio.listaEnsaioVeneza4.lista) > 0 and not dados.ensaio.habilitarListaVeneza4:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosensaio(dados, 'listaEnsaioVeneza4')
            
        # remover das listas
        dados = remover_pessoa_ensaio_filtro(dados, 'listaEnsaioVeneza4')
        
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_dinamica_ensaio(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.geral.listaDinamica) > 0:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosgeral(dados, 'listaDinamica')
        
        # remover das listas
        dados = remover_pessoa_ensaio_lista(dados)
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


def sortear_dadosensaio(dados: DadosDict, lista: str):
    """
        Para Lista Ensaio, Lista EnsaioAlameda, Lista EnsaioJardimCopa1, Lista EnsaioJardimCopa2, 
        Lista EnsaioNovaDivineia1, Lista EnsaioNovaDivineia2, Lista EnsaioPiedade, Lista EnsaioVeneza4
    """
    nome_sorteado = dados.ensaio.sortear(lista)
    if nome_sorteado is None:
        nome_sorteado = dados.historico.nomeSorteado
    if nome_sorteado not in dados.historico.historicoSorteio[dados.mesSorteio]:
        dados.historico.nomeSorteadoAnterior = dados.historico.nomeSorteado
        dados.historico.nomeSorteado = nome_sorteado
        dados.historico.historicoSorteio[dados.mesSorteio].append(nome_sorteado)
    return dados


def remover_pessoa_ensaio_filtro(dados: DadosDict, lista: str):
    nome_sorteado = dados.historico.nomeSorteado
    cartao = nome_sorteado.split('|')[1] + "|" + nome_sorteado.split('|')[2]
    if cartao in dados.ensaio[lista].filtro:
        filtro = dados.ensaio[lista].filtro[cartao]
        if cartao in dados.ensaio.listaEnsaio.filtro:
            for pessoa in filtro:
                dados.ensaio.listaEnsaio.lista.remove(pessoa)
            dados.ensaio.listaEnsaio.filtro.pop(cartao)
        if cartao in dados.ensaio.listaEnsaioAlameda.filtro:
            for pessoa in filtro:
                dados.ensaio.listaEnsaioAlameda.lista.remove(pessoa)
            dados.ensaio.listaEnsaioAlameda.filtro.pop(cartao)
        if cartao in dados.ensaio.listaEnsaioJardimCopa1.filtro:
            for pessoa in filtro:
                dados.ensaio.listaEnsaioJardimCopa1.lista.remove(pessoa)
            dados.ensaio.listaEnsaioJardimCopa1.filtro.pop(cartao)
        if cartao in dados.ensaio.listaEnsaioJardimCopa2.filtro:
            for pessoa in filtro:
                dados.ensaio.listaEnsaioJardimCopa2.lista.remove(pessoa)
            dados.ensaio.listaEnsaioJardimCopa2.filtro.pop(cartao)
        if cartao in dados.ensaio.listaEnsaioNovaDivineia1.filtro:
            for pessoa in filtro:
                dados.ensaio.listaEnsaioNovaDivineia1.lista.remove(pessoa)
            dados.ensaio.listaEnsaioNovaDivineia1.filtro.pop(cartao)
        if cartao in dados.ensaio.listaEnsaioNovaDivineia2.filtro:
            for pessoa in filtro:
                dados.ensaio.listaEnsaioNovaDivineia2.lista.remove(pessoa)
            dados.ensaio.listaEnsaioNovaDivineia2.filtro.pop(cartao)
        if cartao in dados.ensaio.listaEnsaioPiedade.filtro:
            for pessoa in filtro:
                dados.ensaio.listaEnsaioPiedade.lista.remove(pessoa)
            dados.ensaio.listaEnsaioPiedade.filtro.pop(cartao)
        if cartao in dados.ensaio.listaEnsaioVeneza4.filtro:
            for pessoa in filtro:
                dados.ensaio.listaEnsaioVeneza4.lista.remove(pessoa)
            dados.ensaio.listaEnsaioVeneza4.filtro.pop(cartao)
            
        if cartao in dados.geral.listaNiverCasamento.filtro:
            for pessoa in filtro:
                dados.geral.listaNiverCasamento.lista.remove(pessoa)
            dados.geral.listaNiverCasamento.filtro.pop(cartao)
            
        for pessoa in filtro:
            if pessoa in dados.geral.listaDinamica:
                dados.geral.listaDinamica.remove(pessoa)
            
    return dados


def remover_pessoa_ensaio_lista(dados: DadosDict):
    nome_sorteado = dados.historico.nomeSorteado
    cartao = nome_sorteado.split('|')[1] + "|" + nome_sorteado.split('|')[2]
    if cartao in dados.ensaio.listaEnsaio.filtro:
        filtro = dados.ensaio.listaEnsaio.filtro[cartao]
    else:
        filtro = []
        
    if cartao in dados.ensaio.listaEnsaio.filtro:
        for pessoa in filtro:
            dados.ensaio.listaEnsaio.lista.remove(pessoa)
        dados.ensaio.listaEnsaio.filtro.pop(cartao)
    if cartao in dados.ensaio.listaEnsaioAlameda.filtro:
        for pessoa in filtro:
            dados.ensaio.listaEnsaioAlameda.lista.remove(pessoa)
        dados.ensaio.listaEnsaioAlameda.filtro.pop(cartao)
    if cartao in dados.ensaio.listaEnsaioJardimCopa1.filtro:
        for pessoa in filtro:
            dados.ensaio.listaEnsaioJardimCopa1.lista.remove(pessoa)
        dados.ensaio.listaEnsaioJardimCopa1.filtro.pop(cartao)
    if cartao in dados.ensaio.listaEnsaioJardimCopa2.filtro:
        for pessoa in filtro:
            dados.ensaio.listaEnsaioJardimCopa2.lista.remove(pessoa)
        dados.ensaio.listaEnsaioJardimCopa2.filtro.pop(cartao)
    if cartao in dados.ensaio.listaEnsaioNovaDivineia1.filtro:
        for pessoa in filtro:
            dados.ensaio.listaEnsaioNovaDivineia1.lista.remove(pessoa)
        dados.ensaio.listaEnsaioNovaDivineia1.filtro.pop(cartao)
    if cartao in dados.ensaio.listaEnsaioNovaDivineia2.filtro:
        for pessoa in filtro:
            dados.ensaio.listaEnsaioNovaDivineia2.lista.remove(pessoa)
        dados.ensaio.listaEnsaioNovaDivineia2.filtro.pop(cartao)
    if cartao in dados.ensaio.listaEnsaioPiedade.filtro:
        for pessoa in filtro:
            dados.ensaio.listaEnsaioPiedade.lista.remove(pessoa)
        dados.ensaio.listaEnsaioPiedade.filtro.pop(cartao)
    if cartao in dados.ensaio.listaEnsaioVeneza4.filtro:
        for pessoa in filtro:
            dados.ensaio.listaEnsaioVeneza4.lista.remove(pessoa)
        dados.ensaio.listaEnsaioVeneza4.filtro.pop(cartao)
        
    if cartao in dados.geral.listaNiverCasamento.filtro:
        for pessoa in filtro:
            dados.geral.listaNiverCasamento.lista.remove(pessoa)
        dados.geral.listaNiverCasamento.filtro.pop(cartao)
        
    for pessoa in filtro:
        if pessoa in dados.geral.listaDinamica:
            dados.geral.listaDinamica.remove(pessoa)
    if len(filtro) == 0:
        if nome_sorteado in dados.geral.listaDinamica:
            dados.geral.listaDinamica.remove(nome_sorteado)
        
            
    return dados


# TODO: Fazer o complemento para visão ensaio_evento seminário
@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_dinamica_mae_pai(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.evento.listaDinamicaMaePai.lista) > 0:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosevento_nao_seminario(dados, 'listaDinamicaMaePai')
        
        # remover das listas
        dados = remover_pessoa_evento_mae_pai_lista(dados)
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_dinamica_filhos_pais(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if len(dados.evento.listaDinamicaFilhosPais.lista) > 0:
        if dados.mesSorteio not in dados.historico.historicoSorteio:
            dados.historico.historicoSorteio[dados.mesSorteio] = []
        
        dados = sortear_dadosevento_nao_seminario(dados, 'listaDinamicaFilhosPais')
            
        # remover das listas
        dados = remover_pessoa_evento_filho_pai_lista(dados)
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})


def sortear_dadosevento_nao_seminario(dados: DadosDict, lista: str):
    """
        Para Lista DinamicaFilhosPais, Lista DinamicaMaePai
    """
    nome_sorteado = dados.evento.sortear(lista)
    if type(nome_sorteado) == dict:
        nome_sorteado = [key for key in nome_sorteado][0]
    if nome_sorteado is None:
        nome_sorteado = dados.historico.nomeSorteado
    if nome_sorteado not in dados.historico.historicoSorteio[dados.mesSorteio]:
        dados.historico.nomeSorteadoAnterior = dados.historico.nomeSorteado
        dados.historico.nomeSorteado = nome_sorteado
        dados.historico.historicoSorteio[dados.mesSorteio].append(nome_sorteado)
    return dados


def remover_pessoa_evento_filho_pai_lista(dados: DadosDict):
    nome_sorteado = dados.historico.nomeSorteado
    cartao = nome_sorteado.split('|')[1] + "|" + nome_sorteado.split('|')[2]
    if cartao in dados.evento.listaDinamicaFilhosPais.filtro:
        filtro = dados.evento.listaDinamicaFilhosPais.filtro[cartao]
        for pessoa in filtro:
            if pessoa in dados.evento.listaDinamicaFilhosPais.lista:
                dados.evento.listaDinamicaFilhosPais.lista.pop(pessoa)
        dados.evento.listaDinamicaFilhosPais.filtro.pop(cartao)
        
    if cartao in dados.geral.listaGeral.filtro:
        filtro = dados.geral.listaGeral.filtro[cartao]
    else:
        filtro = []
        
    if cartao in dados.geral.listaGeral.filtro:
        for pessoa in filtro:
            dados.geral.listaGeral.lista.remove(pessoa)
        dados.geral.listaGeral.filtro.pop(cartao)
        
    if cartao in dados.geral.listaNiverCasamento.filtro:
        for pessoa in filtro:
            dados.geral.listaNiverCasamento.lista.remove(pessoa)
        dados.geral.listaNiverCasamento.filtro.pop(cartao)
        
    if cartao in dados.geral.listaMenor.filtro:
        for pessoa in filtro:
            dados.geral.listaMenor.lista.remove(pessoa)
        dados.geral.listaMenor.filtro.pop(cartao)
    
    if cartao in dados.evento.listaDinamicaMaePai.filtro:
        for pessoa in filtro:
            if pessoa in dados.evento.listaDinamicaMaePai.lista: 
                dados.evento.listaDinamicaMaePai.lista.remove(pessoa)
        dados.evento.listaDinamicaMaePai.filtro.pop(cartao)
        
    for pessoa in filtro:
        if pessoa in dados.geral.listaVisitante:
            dados.geral.listaVisitante.remove(pessoa)
            
        if pessoa in dados.geral.listaDinamica:
            dados.geral.listaDinamica.remove(pessoa)
        
    if len(filtro) == 0:
        if nome_sorteado in dados.geral.listaVisitante:
            dados.geral.listaVisitante.remove(nome_sorteado)
        if nome_sorteado in dados.geral.listaDinamica:
            dados.geral.listaDinamica.remove(nome_sorteado)
        
            
    return dados


def remover_pessoa_evento_mae_pai_lista(dados: DadosDict):
    nome_sorteado = dados.historico.nomeSorteado
    cartao = nome_sorteado.split('|')[1] + "|" + nome_sorteado.split('|')[2]
    if cartao in dados.evento.listaDinamicaMaePai.filtro:
        filtro = dados.evento.listaDinamicaMaePai.filtro[cartao]
    else:
        filtro = []
        
    if cartao in dados.geral.listaGeral.filtro:
        for pessoa in filtro:
            dados.geral.listaGeral.lista.remove(pessoa)
        dados.geral.listaGeral.filtro.pop(cartao)
        "Nova Divinéia|31"
    if cartao in dados.geral.listaNiverCasamento.filtro:
        for pessoa in filtro:
            dados.geral.listaNiverCasamento.lista.remove(pessoa)
        dados.geral.listaNiverCasamento.filtro.pop(cartao)
        
    if cartao in dados.geral.listaMenor.filtro:
        for pessoa in filtro:
            dados.geral.listaMenor.lista.remove(pessoa)
        dados.geral.listaMenor.filtro.pop(cartao)
    
    if cartao in dados.evento.listaDinamicaMaePai.filtro:
        for pessoa in filtro:
            dados.evento.listaDinamicaMaePai.lista.remove(pessoa)
        dados.evento.listaDinamicaMaePai.filtro.pop(cartao)
    
    if cartao in dados.evento.listaDinamicaFilhosPais.filtro:
        for pessoa in filtro:
            dados.evento.listaDinamicaFilhosPais.lista.pop(pessoa)
        dados.evento.listaDinamicaFilhosPais.filtro.pop(cartao)
        
    for pessoa in filtro:
        if pessoa in dados.geral.listaVisitante:
            dados.geral.listaVisitante.remove(pessoa)
            
        if pessoa in dados.geral.listaDinamica:
            dados.geral.listaDinamica.remove(pessoa)
        
    if len(filtro) == 0:
        if nome_sorteado in dados.geral.listaVisitante:
            dados.geral.listaVisitante.remove(nome_sorteado)
        if nome_sorteado in dados.geral.listaDinamica:
            dados.geral.listaDinamica.remove(nome_sorteado)
        
            
    return dados


# TODO: Fazer o complemento para visão evento
@login_required(login_url=pages_links['LOGIN_PAGE'])
def sort_teste_sem_salvar(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if dados.mesSorteio not in dados.historico.historicoSorteio:
        dados.historico.historicoSorteio[dados.mesSorteio] = []
    
    nome_temp = dados.historico.nomeSorteado
    dados = sortear_dadosevento_nao_seminario(dados, 'listaDinamicaMaePai')
    print(nome_temp)
    print(dados.historico.nomeSorteado)
    # remover das listas
    if nome_temp == dados.historico.nomeSorteado and dados.historico.nomeSorteado != '':
        print("entrou")
        dados = remover_pessoa_evento_mae_pai_lista(dados)
        dados.save()
    return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'partials', 'view_primary.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})
