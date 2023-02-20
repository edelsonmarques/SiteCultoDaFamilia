const form = {
    telaPrincipal: () => document.getElementsByClassName("tela_principal"),
    animation1: () => "flip-in-hor-bottom 1s cubic-bezier(.445,.05,.55,.95) 1s alternate both",
    animation2: () => "flip-out-hor-bottom 1s cubic-bezier(.445,.05,.55,.95) 1s alternate both",
}

function abc(){
    const telaPrincipal = form.telaPrincipal().value;
    form.telaPrincipal().style.animation = telaPrincipal ? form.animation1() : form.animation2();
    setTimeout(console.log("Mudança de animação."), 3000);
}