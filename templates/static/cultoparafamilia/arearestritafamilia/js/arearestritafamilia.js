function add_aviso(id_form){
    container = document.getElementById(id_form);
    console.log(container.getElementsByClassName('postagem'));
    i = container.getElementsByClassName('postagem').length;

    html = "<p class='postagem form_aviso" + i + "'> <input type='text' placeholder='Título(pode ser vazio)' class='form-control' name='titulo'> <textarea type='text' placeholder='Aviso(não pode ser vazio)' class='form-control' name='texto'></textarea> </p>";
    container.insertAdjacentHTML('beforeend', html);
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

function ajuste_aviso(id_form){
    container = document.getElementById(id_form);
    delay(500).then(() => container.innerHTML = "<br>");
}