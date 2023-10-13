from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import time
import random
import os

ultimo_numero_emitido = None

# Declaracion Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app)

# Variables globales
juego_iniciado = False
numeros_sorteados = []
numeros_registrados = []
tiempo_entre_balotas = 20
balotas = list(range(1, 76))
markedNumbers = {}
a = 1103515245
c = 12345

class GeneradorLinealCongruente:
    def __init__(self, semilla, a, c, m):
        self.Xo = semilla
        self.a = a
        self.c = c
        self.m = m

    def generar_numero(self):
        self.state = (self.a * self.Xo + self.c) % self.m
        return self.state

generador = GeneradorLinealCongruente(semilla=int(time.time()), a=1103515245, c=12345, m=32768**32)

def generar_balota():
    global balotas
    if balotas:
        indice = generador.generar_numero() % len(balotas)
        balota = balotas.pop(indice)
        return balota
    return None

def generar_tabla_de_bingo(generador):
    bingo_table = []
    numeros_disponibles = {  
        # Rangos para cada columna
        'B': list(range(1, 16)),
        'I': list(range(16, 31)),
        'N': list(range(31, 46)),
        'G': list(range(46, 61)),
        'O': list(range(61, 76))
    }

    generador = GeneradorLinealCongruente(semilla=int(time.time()), a=1103515245, c=12345, m=32768**32)

    for _ in range(5):
        columna = []
        for letra in 'BINGO':
            # Elegir un número aleatorio dentro del rango correspondiente
            numero = generador.generar_numero()
            disponibles = numeros_disponibles[letra]
            if disponibles:  # Verificar si hay números disponibles en el rango
                numero_elegido = random.choice(disponibles)
                disponibles.remove(numero_elegido)
                columna.append(numero_elegido)
        bingo_table.append(columna)

    return bingo_table

# Rutas
# Pestaña Index
@app.route('/')
def index():
    return render_template('index.html')

# Pestaña Tablero
@app.route('/tablero/', methods=['GET', 'POST'])
def tablero():
    global juego_iniciado
    global numeros_sorteados
    global tiempo_entre_balotas
    global balotas
    global a
    global c
    global generador

    if request.method == 'POST':
        if request.form['action'] == 'start':
            if not juego_iniciado:
                juego_iniciado = True
                tiempo_entre_balotas = 1
                if not numeros_sorteados:
                    balotas = list(range(1, 76))
                    numeros_registrados = []
            return redirect(url_for('tablero'))
        elif request.form['action'] == 'stop':
            juego_iniciado = False
            return redirect(url_for('tablero'))
        elif request.form['action'] == 'reiniciar':
            juego_iniciado = False
            numeros_sorteados = []
            numeros_registrados = []
            tiempo_entre_balotas = 1
            a = a ** 2
            c = c ** 2
            generador = generador = GeneradorLinealCongruente(semilla=int(time.time()), a=1103515245, c=12345, m=32768**32)
            return redirect(url_for('tablero'))
        elif request.form['action'] == 'ordenar':
            juego_iniciado = False
            tiempo_entre_balotas = 1
            numeros_sorteados = sort_bingo_table(numeros_sorteados)
            return redirect(url_for('tablero'))
    return render_template('tablero.html', juego_iniciado=juego_iniciado, numeros_sorteados=numeros_sorteados, 
    tiempo_entre_balotas=tiempo_entre_balotas, markedNumbers=markedNumbers)


# Pestaña Bingo
@app.route('/bingo/')
def bingo():
    # Llama a la función para generar la tabla de bingo
    bingo_table = generar_tabla_de_bingo(generador)
    if request.method == 'POST':
        if request.form['action'] == 'verificar_bingo':
            redirect(url_for('verificar_bingo'))
    return render_template('bingo.html', bingo_table=bingo_table)

# Ordenador
@app.route('/ordenar_numeros', methods=['POST'])
def ordenar_numeros():
    global numeros_sorteados
    if not juego_iniciado:
        numeros_sorteados = sorted(numeros_sorteados)
    return redirect(url_for('tablero'))

def sort_bingo_table(numbers):
    sorted_table = {'B': [], 'I': [], 'N': [], 'G': [], 'O': []}

    for number in numbers:
        if 1 <= number <= 15:
            sorted_table['B'].append(number)
        elif 16 <= number <= 30:
            sorted_table['I'].append(number)
        elif 31 <= number <= 45:
            sorted_table['N'].append(number)
        elif 46 <= number <= 60:
            sorted_table['G'].append(number)
        elif 61 <= number <= 75:
            sorted_table['O'].append(number)

    for key in sorted_table:
        sorted_table[key].sort()

    sorted_numbers = []
    for key in ['B', 'I', 'N', 'G', 'O']:
        sorted_numbers.extend(sorted_table[key])

    return sorted_numbers

# Conexion Socket
@socketio.on('connect')
def handle_connect():
    if juego_iniciado:
        socketio.start_background_task(target=sortear_balotas)

def sortear_balotas():
    global juego_iniciado
    global numeros_sorteados
    global numeros_registrados

    while juego_iniciado:
        balota = generar_balota()
        if not juego_iniciado:
            break
        if balota:
            numeros_sorteados.append(balota)
            numeros_registrados.append(balota)
            socketio.emit('update_balota', {'balota': balota})
        
        time.sleep(tiempo_entre_balotas)

# Función para verificar el bingo
@app.route('/verificar_bingo', methods=['POST'])
def verificar_bingo():
    global numeros_sorteados
    global numeros_registrados
    global juego_iniciado

    numeros_marcados_str = request.form.get('numeros_marcados')
        
    # Dividir la cadena en una lista de números únicos
    numeros_marcados_lista = list(set(numeros_marcados_str.split(',')))
        
    # Convierte los números en enteros
    numeros_marcados_revision = [int(numero.strip()) for numero in numeros_marcados_lista]
        
    print('Números marcados recibidos:', numeros_marcados_revision)
    print("Longitud:", len(numeros_marcados_revision))
    print("Sorteados:", numeros_sorteados)
        
    if len(numeros_marcados_revision) == 25:  # Se han marcado todos los números del tablero
        if set(numeros_marcados_revision).issubset(set(numeros_sorteados)):
            juego_iniciado = False
            return "Ganaste el Bingo"
        else:
            return "No todos los números han sido anunciados"
    else:
        return "Aún no has marcado todos los números del tablero"


port = int(os.environ.get('PORT', 8080))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=port)
    #socketio.run(app, debug=True)
