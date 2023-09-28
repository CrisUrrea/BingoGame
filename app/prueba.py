from flask import Flask, render_template, request, redirect, url_for
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Lista de balotas disponibles para el juego
balotas = list(range(1, 76))

# Estado del juego
juego_iniciado = False
numeros_sorteados = []
delay = 5  # Tiempo de espera predeterminado (5 segundos)

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
    global delay

    if request.method == 'POST':
        if request.form['action'] == 'start':
            juego_iniciado = True
            numeros_sorteados = []
            balotas = list(range(1, 76))
            delay = int(request.form['delay'])  # Configura el tiempo de espera
            return redirect(url_for('index'))
        elif request.form['action'] == 'stop':
            juego_iniciado = False
            return redirect(url_for('index'))
        elif request.form['action'] == 'reiniciar':
            juego_iniciado = False
            numeros_sorteados = []
            return redirect(url_for('index'))
        elif request.form['action'] == 'ordenar':
            numeros_sorteados.sort()  # Ordena los números seleccionados
            return redirect(url_for('index'))

    return render_template('bingo.html', juego_iniciado=juego_iniciado, numeros_sorteados=numeros_sorteados, delay=delay)

@app.route('/sortear')
def sortear():
    global juego_iniciado
    global numeros_sorteados
    global delay

    if juego_iniciado:
        balota = generar_balota()
        if balota:
            numeros_sorteados.append(balota)
            time.sleep(delay)  # Agregar una pausa de tiempo configurada antes de sortear el siguiente número

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
