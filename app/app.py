from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app)

juego_iniciado = False
numeros_sorteados = []
numeros_registrados = []
tiempo_entre_balotas = 5

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

def generar_balota():
    if balotas:
        balota = random.choice(balotas)
        balotas.remove(balota)
        return balota
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tablero/', methods=['GET', 'POST'])
def tablero():
    global juego_iniciado
    global numeros_sorteados
    global tiempo_entre_balotas
    global balotas

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
            balotas = list(range(1, 76))
            return redirect(url_for('tablero'))
        elif request.form['action'] == 'ordenar':
            juego_iniciado = False
            return redirect(url_for('ordenar_numeros'))
    return render_template('tablero.html', juego_iniciado=juego_iniciado, numeros_sorteados=numeros_sorteados, tiempo_entre_balotas=tiempo_entre_balotas)

@app.route('/ordenar_numeros', methods=['POST'])
def ordenar_numeros():
    global numeros_sorteados
    if not juego_iniciado:
        numeros_sorteados.sort()
    return redirect(url_for('tablero'))

@app.route('/bingo')
def bingo():
    return render_template('bingo.html')

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
        if balota:
            numeros_sorteados.append(balota)
            numeros_registrados.append(balota)
            socketio.emit('update_balota', {'balota': balota})
            time.sleep(tiempo_entre_balotas)

if __name__ == '__main__':
    socketio.run(app, debug=True)
