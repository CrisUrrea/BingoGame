var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('update_balota', function(data) {
    let balota = data.balota;
    document.getElementById('highlightedNumber').textContent = balota;
    agregarNumeroTabla(balota);

    // Confirmar la recepción del número
    socket.emit('confirm_balota', { balota: balota });
});

function agregarNumeroTabla(balota) {
    var balotaElement = document.createElement('p');
    balotaElement.textContent = balota;
    var columnId = getBalotaColumn(balota);
    var column = document.getElementById(columnId);
    if (column) {
        column.appendChild(balotaElement);
    }
}

function getBalotaColumn(balota) {
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
