function girar(lista){
    iniciarAnimacao(lista);
    // setTimeout(function() {
    // }, 3000);
}

function iniciarAnimacao(lista) {
    // Exemplo básico de animação
    var divTitulo = document.getElementById('titular');
    var divConjuge = document.getElementById('conjuge');
    var divCartao = document.getElementById('congregacao');
    var divLoading = document.getElementById('loading');
    var frames = ['Sorteando.', 'Sorteando..', 'Sorteando...'];
    var framesNulo = ['Sem pessoa, voltando.', 'Sem pessoa, voltando.', 'Sem pessoa, voltando.'];
    var i = 0;
    divTitulo.style.opacity = 0.3
    divCartao.style.opacity = 0.3
    divConjuge.style.opacity = 0.3

    // Função para atualizar o texto com os frames
    if(JSON.stringify(lista).includes(':')){
        lista = Object.keys(lista)
    }
    function animar() {
        nome = lista[Math.floor(Math.random() * lista.length)].split('|');
        titulo = nome.at(0);
        conjuge = nome.at(-1);
        congregacao = nome.at(1);
        numeroCartao = nome.at(2);
        cartao = 'Congregação:  ' + congregacao + ' - Cartão: ' + numeroCartao;
        divTitulo.textContent = titulo;
        divConjuge.textContent = conjuge;
        divCartao.textContent = cartao;
        divLoading.textContent = frames[i];
        i = (i + 1) % frames.length;
    }
    
    function animarNulo() {
        divTitulo.style.opacity = 0;
        divCartao.style.opacity = 0;
        divConjuge.style.opacity = 0;
        divTitulo.textContent = '';
        divConjuge.textContent = '';
        divCartao.textContent = '';
        divLoading.textContent = framesNulo[i];
        i = (i + 1) % framesNulo.length;
    }
    
    // Atualizar a cada 500ms (exemplo)
    if (lista.length){
        setInterval(animar, 100);
    } else {
        setInterval(animarNulo, 100);
    };
}