from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import posixpath
from enums.pages_names import pages_names
from enums.pages_links import pages_links
from cultoparafamilia.db.firebase import load_postagens, load_lista_cultos
from cultoparafamilia.sorteio_familia.models import is_logged, is_superuser

# Create your views here.
@login_required(login_url=pages_links['LOGIN_PAGE'])
def arearestritafamilia(request):
    if request.method == "GET" and is_superuser(str(auth.get_user(request))):
        postagens = load_postagens()
        lista_cultos = load_lista_cultos()
        return render(request, posixpath.join('cultoparafamilia', 'arearestritafamilia', 'arearestritafamilia.html'), {'pages_names': pages_names, 'postagens': postagens, 'lista_cultos': lista_cultos, 'logged': is_superuser(auth.get_user(request))})
    return redirect('cultoparafamilia')
    
