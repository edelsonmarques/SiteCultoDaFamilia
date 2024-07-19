from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import posixpath
from enums.pages_names import pages_names
from enums.pages_links import pages_links
from cultoparafamilia.sorteio_familia.models import DadosDict, is_logged, is_staff, is_superuser

# Create your views here.
@login_required(login_url=pages_links['LOGIN_PAGE'])
def sorteio_familia(request):
    if request.method == "GET" and is_superuser(str(auth.get_user(request))):
        dados = DadosDict(username=auth.get_user(request).username)
        _, dados = dados.load()
        return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'sorteiofamilia.html'), {'pages_names': pages_names, 'dados': dados.to_object(), 'logged': is_logged(auth.get_user(request))})
    return redirect('cultoparafamilia')
    