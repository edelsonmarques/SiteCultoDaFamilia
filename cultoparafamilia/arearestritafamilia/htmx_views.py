from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import posixpath
import ast
from datetime import datetime
from time import sleep
from enums.mes import mes_num_dict
from enums.pages_links import pages_links
from django.views.decorators.csrf import csrf_exempt
from cultoparafamilia.sorteio_familia.models import is_logged, is_superuser
from cultoparafamilia.db.firebase import load_postagens, insert_postagens, delete_postagens, update_postagens, load_lista_cultos

# Create your views here.
@login_required(login_url=pages_links['LOGIN_PAGE'])
def insert_list(request):
    postagens = load_postagens()

    titulos = request.POST.getlist('titulo')
    textos = request.POST.getlist('texto')
    avisos_join = zip(titulos, textos)
    usuario = auth.get_user(request)
    # print('postagem antes:\n', postagens)
    for ti, te in avisos_join:
        # print('titulo: ', ti, ' | texto: ', te)
        if te != '':
            sleep(0.5)
            id_post = f"{usuario}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}"
            postagens[id_post] = {'titulo': ti, 'texto': te}
            insert_postagens("postagem", id_post, {'titulo': ti, 'texto': te})
    return render(request, posixpath.join('cultoparafamilia', 'partials', 'postagem_list.html'), {'postagens': postagens, 'logged': is_superuser(auth.get_user(request))})
    
@csrf_exempt
@login_required(login_url=pages_links['LOGIN_PAGE'])
def exclude_post(request, id_post):
    delete_postagens("postagem", id_post)
    return render(request, posixpath.join('cultoparafamilia', 'partials', 'postagem_list.html'), {'logged': is_superuser(auth.get_user(request))})

@login_required(login_url=pages_links['LOGIN_PAGE'])
def save_post(request, id_post):
    postagens = load_postagens()
    titulo = request.POST.get('titulo')
    texto = request.POST.get('texto')
    postagens[id_post]['titulo'] = titulo
    postagens[id_post]['texto'] = texto
    update_postagens("postagem", id_post, {'titulo': titulo, 'texto': texto})
    postagem = {str(id_post): postagens[id_post]}
    edit_post = ast.literal_eval(request.POST.get('edit_post'))
    edit_post = set(edit_post)
    try:
        edit_post.remove(id_post)
    except KeyError:
        pass
    edit_post = list(edit_post)
    return render(request, posixpath.join('cultoparafamilia', 'partials', 'postagem_list.html'), {'postagens': postagem, 'logged': is_superuser(auth.get_user(request)), 'edit_post': edit_post})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def edit_post(request, id_post):
    postagens = load_postagens()
    postagem = {str(id_post): postagens[id_post]}
    if 'edit_post' in request.POST and request.POST.get('edit_post') != '':
        edit_post = ast.literal_eval(request.POST.get('edit_post'))
        edit_post = set(edit_post)
        edit_post.add(id_post)
        edit_post = list(edit_post)
    else:
        edit_post = [id_post]
    return render(request, posixpath.join('cultoparafamilia', 'partials', 'postagem_list.html'), {'postagens': postagem, 'logged': is_superuser(auth.get_user(request)), 'edit_post': edit_post})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def save_list_post(request, id_post):
    lista_cultos = load_lista_cultos()
    mes = f"_/{id_post.capitalize()}"
    tema = '-'
    if request.POST.get('mes') != '':
        mes = f"{request.POST.get('mes')}/{id_post.capitalize()}"
        lista_cultos[id_post]['mes'] = mes
    else:
        lista_cultos[id_post]['mes'] = mes
    if request.POST.get('tema') != '':
        tema = request.POST.get('tema')
        lista_cultos[id_post]['tema'] = tema
    else:
        lista_cultos[id_post]['tema'] = tema
    update_postagens("listaCulto", id_post, {'mes': mes, "numeromes": mes_num_dict[id_post], 'tema': tema})
    lista_culto = {str(id_post): lista_cultos[id_post]}
    edit_list_post = ast.literal_eval(request.POST.get('edit_list_post'))
    edit_list_post = set(edit_list_post)
    try:
        edit_list_post.remove(id_post)
    except KeyError:
        pass
    edit_list_post = list(edit_list_post)
    return render(request, posixpath.join('cultoparafamilia', 'partials', 'lista_culto_list.html'), {'lista_cultos': lista_culto, 'logged': is_superuser(auth.get_user(request)), 'edit_list_post': edit_list_post})


@login_required(login_url=pages_links['LOGIN_PAGE'])
def edit_list_post(request, id_post):
    lista_cultos = load_lista_cultos()
    
    lista_culto = {str(id_post): lista_cultos[id_post]}
    if 'edit_list_post' in request.POST and request.POST.get('edit_list_post') != '':
        edit_list_post = ast.literal_eval(request.POST.get('edit_list_post'))
        edit_list_post = set(edit_list_post)
        edit_list_post.add(id_post)
        edit_list_post = list(edit_list_post)
    else:
        edit_list_post = [id_post]
    return render(request, posixpath.join('cultoparafamilia', 'partials', 'lista_culto_list.html'), {'lista_cultos': lista_culto, 'logged': is_superuser(auth.get_user(request)), 'edit_list_post': edit_list_post})

def none_page(request):
    return HttpResponse('Nenhuma página será retornada.')