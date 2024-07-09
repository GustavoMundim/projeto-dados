document.addEventListener('DOMContentLoaded', function() {
    const abrir_anotacao = document.querySelectorAll('.open-notepad');
    const fechar_anotacao = document.querySelectorAll('.close-button');

    fechar_anotacao.forEach((card_close) => {
        card_close.addEventListener('click', function(event) {
            const anotacoes = document.querySelectorAll('.abrir-anotacao.open-note');
            anotacoes.forEach((notepad_close) => {
                notepad_close.classList.remove('open-note');
            });
            const notepad = event.currentTarget.closest('.card-dados').querySelector('.abrir-anotacao');
            notepad.classList.remove('open-note');
        })
    })

    abrir_anotacao.forEach((card) => {
        card.addEventListener('click', function(event) {
            const anotacoes = document.querySelectorAll('.abrir-anotacao.open-note');
            anotacoes.forEach((notepad) => {
                notepad.classList.remove('open-note');
            });
            const notepad = event.currentTarget.closest('.card-dados').querySelector('.abrir-anotacao');
            notepad.classList.add('open-note');
        });
    });
});
