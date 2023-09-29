const ordenar = () => {
    const btnOrdenar = document.getElementById('ordenarNumeros');

    btnOrdenar.addEventListener('click', function(e) {
        e.preventDefault();

        // Obtener todos los números en las columnas
        const columnas = document.querySelectorAll('.bingo-column p');
        const numeros = [];

        columnas.forEach((p) => {
            const numero = parseInt(p.textContent);
            if (!isNaN(numero)) {
                numeros.push(numero);
            }
        });

        // Ordenar los números de forma ascendente
        numeros.sort((a, b) => a - b);

        // Reemplazar los números en las columnas con los números ordenados
        columnas.forEach((p, index) => {
            p.textContent = numeros[index];
        });
    });
}

ordenar();
