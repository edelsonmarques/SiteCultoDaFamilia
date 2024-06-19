//const form = {
//    telaPrincipal: () => document.getElementsByClassName("tela_principal"),
//    animation1: () => "flip-in-hor-bottom 1s cubic-bezier(.445,.05,.55,.95) 1s alternate both",
//    animation2: () => "flip-out-hor-bottom 1s cubic-bezier(.445,.05,.55,.95) 1s alternate both",
//}

//function abc(){
//    const telaPrincipal = form.telaPrincipal().value;
//    form.telaPrincipal().style.animation = telaPrincipal ? form.animation1() : form.animation2();
//    setTimeout(console.log("Mudança de animação."), 3000);
//}

function girar(lista){
    iniciarAnimacao(lista);
    console.log(lista)
//    setTimeout(function() {
//
//    }, 3000);
}

function iniciarAnimacao(lista) {
    // Exemplo básico de animação
    var divTitulo = document.getElementById('titulo');
    var divConjuge = document.getElementById('conjuge');
    var divCartao = document.getElementById('congregacao');
    var divLoading = document.getElementById('loading');
    var frames = ['Sorteando.', 'Sorteando..', 'Sorteando...'];
    var i = 0;
    divTitulo.style.opacity = 0.3
    divCartao.style.opacity = 0.3
    divConjuge.style.opacity = 0.3

    // Função para atualizar o texto com os frames
    function animar() {
        nome = lista[Math.floor(Math.random() * lista.length)].split('|');
        titulo = nome[0];
        conjuge = nome.at(-1);
        congregacao = nome[1];
        numeroCartao = nome[2];
        cartao = 'Congregação:  ' + congregacao + ' - Cartão: ' + numeroCartao;
        opacity : 0.5;
        divTitulo.textContent = titulo;
        divConjuge.textContent = conjuge;
        divCartao.textContent = cartao;
        divLoading.textContent = frames[i];
         i = (i + 1) % frames.length;
    }

    // Atualizar a cada 500ms (exemplo)
    setInterval(animar, 100);
}