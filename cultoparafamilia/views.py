from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth, sessions
from django.contrib.auth.decorators import login_required
import posixpath
from enums.pages_names import pages_names
from enums.pages_links import pages_links
from cultoparafamilia.sorteio_familia.models import User_field, is_logged, is_superuser, return_info_user
from cultoparafamilia.db.firebase import load_lista_cultos, load_postagens

# Create your views here.
def cultoparafamilia(request):
    if request.method == "GET":
        if is_superuser(str(auth.get_user(request))):
            return redirect('arearestritafamilia')
        postagens = load_postagens()
        lista_cultos = load_lista_cultos()
        # return HttpResponse('Página cultoparafamilia')
        return render(request, posixpath.join('cultoparafamilia', 'cultoparafamilia.html'), {'pages_names': pages_names, 'postagens': postagens, 'lista_cultos': lista_cultos, **return_info_user(request)})

def login_area_restrita(request, _print=False):
    if request.method == "GET" and not is_logged(str(auth.get_user(request))):
        return render(request, posixpath.join('cultoparafamilia', 'login_area_restrita.html'), {'pages_names': pages_names, 'next': request.GET.get('next'), **return_info_user(request)})
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        congregacao = request.POST.get('congregacao')
        cartao = request.POST.get('cartao')
        
        if username is None:
            # TODO: Habilitar login por congregação e cartão, acredito que vai procurar no firebase tbm.
            if _print:
                print(f'congregacao: {congregacao}')
                print(f'congrecartaoacao: {cartao}')
        else:
            user = User_field(username=username, password=password)
            user.login(request)
        if request.POST.get('next') is not None:
            return redirect(request.POST.get('next'))
    return redirect('cultoparafamilia')

def logout_area_restrita(request):
    if request.method == "GET" and is_logged(str(auth.get_user(request))):
        # return HttpResponse('Página cultoparafamilia')
        user = User_field(username=str(auth.get_user(request)))
        user.logout(request)
    return redirect('cultoparafamilia')
    
@login_required(login_url=pages_links['LOGIN_PAGE'])
def cadastrar_user(request, _print=False):
    if request.method == "GET" and is_superuser(str(auth.get_user(request))):
        return render(request, posixpath.join('cultoparafamilia', 'cadastrar_user.html'), {'pages_names': pages_names, 'next': request.GET.get('next'), **return_info_user(request)})
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        congregacao = request.POST.get('congregacao')
        cartao = request.POST.get('cartao')
        
        if username is None:
            # TODO: Habilitar login por congregação e cartão, acredito que vai procurar no firebase tbm.
            if _print:
                print(f'congregacao: {congregacao}')
                print(f'congrecartaoacao: {cartao}')
        else:
            user = User_field(username=username, password=password)
            user.save()
        if request.POST.get('next') is not None:
            return redirect(request.POST.get('next'))
        return redirect('home')
    return redirect('cultoparafamilia')