document.addEventListener('DOMContentLoaded', function() {
    const pegar_imagem = document.querySelector('.alt-image');
    const imagem = document.querySelector('.imagem_do_usuario_define')

    
    pegar_imagem.onchange = function() {
        imagem.src = URL.createObjectURL(pegar_imagem.files[0]);
    }


})