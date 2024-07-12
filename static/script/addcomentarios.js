

document.addEventListener('DOMContentLoaded', function(){


const anotacao_usuarios = document.querySelectorAll('textarea#pegar-anotacao');

const botao_adicionar = document.querySelectorAll('.custom-button-anotacao');


botao_adicionar.forEach(function(btn) {
    btn.addEventListener('click', function(event){
        event.preventDefault();
        let notepad = ''
        anotacao_usuarios.forEach(function(note_user) {
            let anotacao = note_user.value;
            notepad += anotacao;
        })
        const section_comentarios = document.querySelector('.comentarios')
        const postar_comentario = document.createElement('div');

        postar_comentario.innerHTML = `
        <div class="card-comentarios">
                                    <div class="card-username">
                                        <div class="info-username">
                                            <h3>@Usuário</h3>
                                            </div>
                                            <div class="deletar-comentario">
                                                <form method="POST" action="{% url 'projeto:delete' comentario.id %}">
                                                    {% csrf_token %}
                                                    <button id="delete-trash"><i class='bx bx-trash'></i></button>
                                                </form>
                                            </div>
                                            </form>
                                        </div>
                                        <div class="card-infos">
                                            <div class="card-image-create">
                                                <div class="card-image">
                                                    <img src="" alt="user-ico">
                                                </div>
                                            </div>
                                            <div class="comentario-usuario">
                                                <p>${notepad}</p>
                                            </div>
                                        </div>
                                    </div>
        `
        section_comentarios.appendChild(postar_comentario);

    })})
})