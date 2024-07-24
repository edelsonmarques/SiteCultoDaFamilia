from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import posixpath
from enums.pages_names import pages_names
from enums.pages_links import pages_links
from enums import nomes_colunas
from cultoparafamilia.sorteio_familia.models import DadosDict, is_superuser, return_info_user
from cultoparafamilia.db.firebase import load_lista_presenca, load_lista_usuarios
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Create your views here.
@login_required(login_url=pages_links['LOGIN_PAGE'])
def configuracoes_sorteio(request):
    dados = DadosDict(username=auth.get_user(request).username)
    _, dados = dados.load()
    if request.method == "GET" and is_superuser(str(auth.get_user(request))):
        return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'configuracoessorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})
    if request.method == "POST":
        import pandas as pd
        import io
        if 'report' in request.POST and 'mes_historico' in request.POST and request.POST['mes_historico'] != '':
            with io.BytesIO() as b:
                with pd.ExcelWriter(b, engine='openpyxl') as writer:
                    _mes = request.POST['mes_historico']
                    if _mes == 'todos':
                        for _mes in dados.historico.historicoSorteio.keys():
                            df = pd.DataFrame(data=dados.historico.historicoSorteio[_mes], columns=['field'])
                            df['congregacao'] = df['field'].apply(lambda x: x.split('|')[1])
                            df['idNumero'] = df['field'].apply(lambda x: x.split('|')[2])
                            df['nomeTitular'] = df['field'].apply(lambda x: x.split('|')[0])
                            df['dataCasamento'] = df['field'].apply(lambda x: x.split('|')[-3])
                            df['estadoCivil'] = df['field'].apply(lambda x: x.split('|')[-2])
                            df['nomeConjuge'] = df['field'].apply(lambda x: x.split('|')[-1])
                            df = df.drop(columns=['field'])
                            df.to_excel(writer, sheet_name=_mes)
                    else:
                        df = pd.DataFrame(data=dados.historico.historicoSorteio[_mes], columns=['field'])
                        df['congregacao'] = df['field'].apply(lambda x: x.split('|')[1])
                        df['idNumero'] = df['field'].apply(lambda x: x.split('|')[2])
                        df['nomeTitular'] = df['field'].apply(lambda x: x.split('|')[0])
                        df['dataCasamento'] = df['field'].apply(lambda x: x.split('|')[-3])
                        df['estadoCivil'] = df['field'].apply(lambda x: x.split('|')[-2])
                        df['nomeConjuge'] = df['field'].apply(lambda x: x.split('|')[-1])
                        df = df.drop(columns=['field'])
                        df.to_excel(writer, sheet_name=_mes)
            
                filename = 'output.xlsx'
                response = HttpResponse(
                    b.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename={filename}'
                return response
        
        if 'report' in request.POST and 'report_option' in request.POST and request.POST['report_option'] != '':
            escolha = request.POST['report_option']
            usuarios = load_lista_usuarios()
            presenca = load_lista_presenca()
            usuarios = pd.DataFrame(usuarios).T
            usuarios['idNumero'] = usuarios['idNumero'].apply(lambda x: x.split('/')[1])
            usuarios = usuarios.loc[:, nomes_colunas.COLUNAS_REPORT]
            
            def extract_months(_mes, _writer):
                presenca_temp = pd.DataFrame(presenca[_mes]).T
                presenca_temp['congregacao'] = presenca_temp['idNumero'].apply(lambda x: x.split('/')[0])
                presenca_temp['idNumero'] = presenca_temp['idNumero'].apply(lambda x: x.split('/')[1])
                presenca_temp = presenca_temp.loc[:, nomes_colunas.COLUNAS_MESES_REPORT]
                presenca_temp = presenca_temp.merge(usuarios, on=['congregacao', 'idNumero'], how='left', suffixes=('_left', '_right'))
                for index_, value in pd.DataFrame(presenca_temp).iterrows():
                    presenca_temp.loc[index_, ['estadoCivil']] = value['estadoCivil_right']
                    presenca_temp.loc[index_, ['dataCasamento']] = value['dataCasamento_right']
                    presenca_temp.loc[index_, ['nomeTitular']] = value['nomeTitular_left']
                    presenca_temp.loc[index_, ['nomeConjuge']] = value['nomeConjuge_left']
                    if str(value['nomeTitular_left']).lower() != 'nan':
                        presenca_temp.loc[index_, ['nascimentoTitular']] = value['nascimentoTitular_right']
                        presenca_temp.loc[index_, ['sexoTitular']] = value['sexoTitular']
                    else:
                        presenca_temp.loc[index_, ['nascimentoTitular']] = value['nascimentoTitular_left']
                        presenca_temp.loc[index_, ['sexoTitular']] = ''
                    if str(value['nomeConjuge_left']).lower() != 'nan':
                        presenca_temp.loc[index_, ['nascimentoConjuge']] = value['nascimentoConjuge_right']
                        presenca_temp.loc[index_, ['sexoConjuge']] = value['sexoConjuge']
                    else:
                        presenca_temp.loc[index_, ['nascimentoConjuge']] = value['nascimentoConjuge_left']
                        presenca_temp.loc[index_, ['sexoConjuge']] = ''
                presenca_temp = presenca_temp.loc[:, nomes_colunas.COLUNAS_MERGE_REPORT]
                presenca_temp.to_excel(_writer, sheet_name=_mes)
            
            with io.BytesIO() as b:
                with pd.ExcelWriter(b, engine='openpyxl') as writer:
                    if escolha in ['todos', 'usuarios']:
                        usuarios.to_excel(writer, sheet_name="Dados_usuarios")
                    if escolha in ['todos']:
                        for _mes in presenca:
                            extract_months(_mes, writer)
                    elif escolha not in ['usuarios']:
                        extract_months(escolha, writer)
            
                filename = 'output.xlsx'
                response = HttpResponse(
                    b.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename={filename}'
                return response
        return render(request, posixpath.join('cultoparafamilia', 'sorteiofamilia', 'configuracoessorteio', 'configuracoessorteio.html'), {'pages_names': pages_names, 'dados': dados.to_object(), **return_info_user(request)})
    return redirect('cultoparafamilia')
    # TODO: Realizar todos os passos de configurações