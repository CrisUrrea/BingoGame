// Objeto para rastrear números marcados
var markedNumbers = {};

// Objeto para rastrear números marcados
var contadorNumerosMarcados = 0;

// Función para marcar o desmarcar un número
function marcarNumero(cell) {
    var number = cell.textContent;
    if (markedNumbers[number]) {
        cell.style.backgroundColor = '';
        markedNumbers[number] = false;
        contadorNumerosMarcados--; // Resta 1 al contador
    } else {
        cell.style.backgroundColor = 'lightblue';
        markedNumbers[number] = true;
        contadorNumerosMarcados++; // Suma 1 al contador
    }

    // Actualiza el valor del campo oculto con la lista de números marcados
    let numerosMarcados = Object.keys(markedNumbers).filter(numero => markedNumbers[numero]);
    document.getElementById('numerosMarcados').value = numerosMarcados;

    // Actualiza el texto del párrafo de contador
    document.getElementById('contadorNumerosMarcados').textContent = contadorNumerosMarcados + ' de 25 números marcados';
    // No emitimos el número seleccionado al servidor aquí; lo hacemos al verificar el Bingo
}

// Agregar un evento al botón "Bingo" para verificar el Bingo
const btnVerificarBingo = document.querySelector('#btnVerificarBingo');
btnVerificarBingo.addEventListener('click', function (e) {
    e.preventDefault();
    // Comprobar si se han marcado todos los números (contador igual a 25)
    if (contadorNumerosMarcados === 25) {
        fetch("/verificar_bingo", {
            method: "POST",
            body: new URLSearchParams({ "numeros_marcados": document.getElementById('numerosMarcados').value }),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
            .then(response => response.text())
            .then(message => {
                Swal.fire({
                     icon: 'info',
                     text: message,
                })
            })
            .catch(error => {
                console.error("Error:", error);
            });
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Debes marcar todos los números del tablero antes de verificar el Bingo.',
          });
        // alert('Debes marcar todos los números del tablero antes de verificar el Bingo.');
    }
});


// Declarar socket como variable global
//const socket = io.connect('https://' + document.domain + ':' + location.port); //Local
var socket = io.connect('https://bingogame-e092ca37112d.herokuapp.com/bingo/'); // Heroku


document.addEventListener("DOMContentLoaded", function () {
    // Manejar la conexión al servidor Socket.IO
    socket.on('connect', function () {
        console.log('Conectado al servidor de Socket.IO');
    });

    // Obtener el botón de reinicio
    const btnreinicio = document.querySelector("#btnNewCard");

    // Función para reiniciar la página
    const reinicioPagina = () => {
        btnreinicio.addEventListener('click', (e) => {
            e.preventDefault();
            location.reload();
        });
    }

    // Funciones
    reinicioPagina();
});
