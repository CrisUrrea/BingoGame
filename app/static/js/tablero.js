// Declaración
// const socket = io.connect('https://bingogame-e092ca37112d.herokuapp.com', {
//     path: '/socket.io',
//     transports: ['websocket'], // Utiliza WebSocket como transporte
//     secure: true, // Indica que es una conexión segura (HTTPS)
// });

var socket = io.connect('http://' + document.domain + ':' + location.port); // Local

// Escucha la actualización de balotas desde el servidor
socket.on('update_balota', function (data) {
    let balota = data.balota;
    let balotaElement = document.createElement('p');
    balotaElement.textContent = balota;
    let columnId = getBalotaColumn(balota);
    let column = document.getElementById(columnId);
    if (column) {
        column.appendChild(balotaElement);
    }
    document.getElementById('highlightedNumber').textContent = balota;

    anunciarNumero(balota);
});

//Decir balotas
const anunciarNumero = (numero) => {
    const synth = window.speechSynthesis;
    const mensajeBalota = new SpeechSynthesisUtterance(`Balota número ${numero}`);

    synth.speak(mensajeBalota);
}

// Balotas por columna
const getBalotaColumn = (balota) => {
    if (1 <= balota && balota <= 15) {
        return 'column-b';
    } else if (16 <= balota && balota <= 30) {
        return 'column-i';
    } else if (31 <= balota && balota <= 45) {
        return 'column-n';
    } else if (46 <= balota && balota <= 60) {
        return 'column-g';
    } else {
        return 'column-o';
    }
}

function ordenarBalotas() {
    const columnas = ['column-b', 'column-i', 'column-n', 'column-g', 'column-o'];

    for (const columnaId of columnas) {
        const columna = document.getElementById(columnaId);
        const numeros = Array.from(columna.getElementsByTagName('p'));
        
        // Ordena los números dentro de la columna
        numeros.sort((a, b) => parseInt(a.textContent) - parseInt(b.textContent));
        
        // Elimina los números desordenados de la columna
        numeros.forEach(numero => columna.removeChild(numero));
        
        // Agrega los números ordenados nuevamente a la columna
        numeros.forEach(numero => columna.appendChild(numero));
    }
}

// Luego, puedes activar esta función cuando se haga clic en el botón "Ordenar" utilizando un evento onClick
const botonOrdenar = document.getElementById('ordenarNumeros');
botonOrdenar.addEventListener('click', ordenarBalotas());