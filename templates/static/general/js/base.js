let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
// let searchBtn = document.querySelector(".bx-search");

closeBtn.addEventListener("click", ()=>{
    sidebar.classList.toggle("open");
    menuBtnChange();
});

/* searchBtn.addEventListener("click", ()=>{
    sidebar.classList.toggle("open");
    menuBtnChange();
}); */

function menuBtnChange() {
if(sidebar.classList.contains("open")){
    closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
}else {
    closeBtn.classList.replace("bx-menu-alt-right","bx-menu");
}
}

// Função para verificar se o usuário está logado
function usuarioLogado(nome) {
  // Simulando que o usuário está logado
  if (nome){
    return true
  }
  return false;
}

// Função para verificar se a imagem do usuário existe
function imagemUsuarioExiste(nome) {
  var imgSrc = 'avatar-' + nome + '.png';
  
  // Verifica se o arquivo existe
  var img = new Image();
  img.src = imgSrc;
  
  return img.complete && img.naturalWidth !== 0;
}

// Função para mudar o avatar
function mudarAvatar(nome) {
  if (usuarioLogado(nome)) {
    var avatar = document.getElementById('avatar');
    var novoSrc = 'avatar-' + nome + '.png'; // Nome do arquivo baseado nas duas primeiras letras do nome
    // Verifica se o arquivo existe
    if (imagemUsuarioExiste(nome)) {
      avatar.src = novoSrc;
    } else {
      // Se não existe, troca para um círculo com as duas primeiras letras do nome
      avatar.src = criarAvatarPadrao(nome);
    }
  }
}

// Função para criar um avatar padrão com as duas primeiras letras do nome
function criarAvatarPadrao(nome) {
  var canvas = document.createElement('canvas');
  var ctx = canvas.getContext('2d');
  var tamanho = 100; // Tamanho do avatar
  canvas.width = tamanho;
  canvas.height = tamanho;

  // Estilos para o círculo
  ctx.fillStyle = '#ccc'; // Cor de fundo
  ctx.beginPath();
  ctx.arc(tamanho / 2, tamanho / 2, tamanho / 2, 0, Math.PI * 2);
  ctx.fill();

  // Texto com as duas primeiras letras do nome
  ctx.fillStyle = '#fff'; // Cor do texto
  ctx.font = '40px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(nome.substr(0, 2).toUpperCase(), tamanho / 2, tamanho / 2);

  return canvas.toDataURL(); // Retorna a imagem como base64
}

// Exemplo de uso:
var nomeUsuario = $(document.getElementById("username")).text(); // Substitua pelo nome de usuário real após o login
mudarAvatar(nomeUsuario);