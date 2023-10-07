//Declaracion
// var socket = io.connect('https://' + document.domain + ':' + location.port); //Local
var socket = io.connect('https://bingogame-e092ca37112d.herokuapp.com/socket.io'); //Heroku


        // Escucha la actualización de balotas desde el servidor
        socket.on('update_balota', function (data) {
            var balota = data.balota;
            var balotaElement = document.createElement('p');
            balotaElement.textContent = balota;
            var columnId = getBalotaColumn(balota);
            var column = document.getElementById(columnId);
            if (column) {
                column.appendChild(balotaElement);
            }
        });

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