from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app)

# Lista de balotas disponibles para el juego
balotas = list(range(1, 76))

# Estado del juego
juego_iniciado = False
numeros_sorteados = []
tiempo_entre_balotas = 5  # Tiempo en segundos entre balotas

def generar_balota():
    if balotas:
        balota = random.choice(balotas)
        balotas.remove(balota)
        return balota
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    global juego_iniciado
    global numeros_sorteados
    global tiempo_entre_balotas

    if request.method == 'POST':
        if request.form['action'] == 'start':
            juego_iniciado = True
            numeros_sorteados = []
            balotas = list(range(1, 76))
            tiempo_entre_balotas = 5  # Mantener el tiempo fijo en 5 segundos
            return redirect(url_for('index'))
        elif request.form['action'] == 'stop':
            juego_iniciado = False
            return redirect(url_for('index'))
        elif request.form['action'] == 'reiniciar':
            juego_iniciado = False
            numeros_sorteados = []
            return redirect(url_for('index'))
        elif request.form['action'] == 'seleccionar':
            if juego_iniciado:
                numeros_sorteados.sort()
            return redirect(url_for('index'))

    return render_template('index.html', juego_iniciado=juego_iniciado, numeros_sorteados=numeros_sorteados, tiempo_entre_balotas=tiempo_entre_balotas)

@socketio.on('connect')
def handle_connect():
    if juego_iniciado:
        socketio.start_background_task(target=sortear_balotas)

def sortear_balotas():
    global juego_iniciado
    global numeros_sorteados

    while juego_iniciado:
        balota = generar_balota()
        if balota:
            numeros_sorteados.append(balota)
            socketio.emit('update_balota', {'balota': balota})
            time.sleep(tiempo_entre_balotas)

if __name__ == '__main__':
    socketio.run(app, debug=True)
