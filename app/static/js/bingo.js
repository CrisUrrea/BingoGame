var markedNumbers = {};

function marcarNumero(cell) {
    var number = cell.textContent;
    if (markedNumbers[number]) {
        cell.style.backgroundColor = '';
        delete markedNumbers[number];
    } else {
        cell.style.backgroundColor = 'lightblue';
        markedNumbers[number] = true;
    }
}

function verificarBingo() {
    var rows = document.querySelectorAll('tr');
    var bingo = true;
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        var cells = row.querySelectorAll('td');
        for (var j = 0; j < cells.length; j++) {
            var cell = cells[j];
            var number = cell.textContent;
            if (markedNumbers[number] !== true) {
                bingo = false;
                break;
            }
        }
        if (!bingo) {
            break;
        }
    }
    if (bingo) {
        document.getElementById('bingo-message').textContent = '¡Ganaste! ¡Es un Bingo!';
    } else {
        document.getElementById('bingo-message').textContent = 'Sigue intentando...';
    }
}