document.addEventListener('DOMContentLoaded', function() {
    var dataElement = document.querySelector('.data-get p');
    var botao_clicado = document.querySelectorAll('.container-buttons-2 button');


    const empresa = dataElement.getAttribute('data-dados-empresa');
    const dataString = dataElement.getAttribute('data-dados-data');
    const aberturaString = dataElement.getAttribute('data-dados-abertura');
    const altaString = dataElement.getAttribute('data-dados-alta');
    const baixaString = dataElement.getAttribute('data-dados-baixa');
    const fechamentoString = dataElement.getAttribute('data-dados-fechamento');

    const data = dataString.split(' ').map(function(item) {
                return item.trim(); 
            });

    const abertura = aberturaString.split(' ').map(function(item) {
                return parseFloat(item.trim()); 
            });
    const alta = altaString.split(' ').map(function(item) {
                return parseFloat(item.trim()); 
            });
    const baixa = baixaString.split(' ').map(function(item) {
                return parseFloat(item.trim()); 
            });
    const fechamento = fechamentoString.split(' ').map(function(item) {
                return parseFloat(item.trim());  
            });





    const dataInicial = {
        labels: ['08/07/2024', '08/06/2024', '08/05/2024', '08/03/2024', '08/01/2024'],
        datasets: [{
            label: 'Ativos',
            data: [0, 0, 0, 0, 0], 
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
        }]
    };

    const options = {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    };

    const container = document.getElementById('line-chart').getContext('2d');

    let chart = new Chart(container, {
        type: 'bar',
        data: dataInicial,
        options: options
    });

    botao_clicado.forEach(function(btn){
        btn.addEventListener('click', function(event){
            event.preventDefault();
            coluna_selecionada = btn.getAttribute('data-coluna');

            var dados;
            if(coluna_selecionada === 'Abertura') {
                dados = abertura;
                labels = data;
                nomeLabel = `${empresa} - ${coluna_selecionada}`

            } else if(coluna_selecionada === 'Baixa') {
                dados = baixa;
                labels = data;
                nomeLabel = `${empresa} - ${coluna_selecionada}`

            } else if(coluna_selecionada === 'Alta') {
                dados = alta;
                labels = data;
                nomeLabel = `${empresa} - ${coluna_selecionada}`

            } else if (coluna_selecionada === 'Fechamento') {
                dados = fechamento;
                labels = data;
                nomeLabel = `${empresa} - ${coluna_selecionada}`
            }
            chart.data.datasets[0].label = nomeLabel

            chart.data.datasets[0].data = dados;
            chart.data.labels =  labels;
            chart.update();
        });
    });
});
