from cultoparafamilia.sorteio_familia.models import Ensaio, Lista

def retirar_congregacao(ensaio:Ensaio, lista: Lista):
    for cartao in lista.filtro:
        if cartao in ensaio.listaEnsaio.filtro:
            for pessoa in lista.filtro[cartao]:
                try:
                    ensaio.listaEnsaio.lista.remove(pessoa)
                except ValueError:
                    continue
            ensaio.listaEnsaio.filtro.pop(cartao)
    return ensaio
    
def inserir_congregacao(ensaio:Ensaio, lista: Lista):
    ensaio.listaEnsaio.filtro.update(lista.filtro)
    ensaio.listaEnsaio.lista.extend(lista.lista)
    ensaio.listaEnsaio.lista = list(set(ensaio.listaEnsaio.lista))
    return ensaio