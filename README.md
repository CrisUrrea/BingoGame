# Bingo

## .venv Ambiente
Para trabajar con python se debe crear un ambiente para instalar las librerias y framework.

Se abre una terminal y se debe ir hasta donde se tiene alojado la carpeta dentro de la carpeta que tiene el proyecto.

Para windows, si el computador tiene sistema operativo macOS, entonces basarse en la documentacion de Flask https://flask.palletsprojects.com/en/2.3.x/installation/

### Crea ambiente
```bash
py -3 -m venv .venv
```

### Activar ambiente
```bash
.venv\Scripts\activate
```

## Librerias y Framework
Dentro de la activacion de ambiente se debe instalar lo siguiente

### Framework
```bash
pip install Flask
```

### Libreria
```bash
pip install flask-socketio
```

### Ejecutar
```bash
python app.py
```

## Push
La clausula se utiliza para mandar los cambios al repositorio, se realiza con el siguiente paso a paso:

```bash
git add .
```

Este comando añade todos los cambios al commit que sera enviado

```bash
git commit -m "mensaje que deseas"
```

Esto es para colocarle un mensaje a lo que se va a enviar para diferenciarlos ( La idea es que sea algo referente al cambio, por ejemplo si se hizo cambio en los colores de index se deberia colocar index Colors)

```bash
git push
```

El ultimo comando envia todos los cambios al repositorio, si tiene problema con este ultimo punto verifique el paso a paso, busque en internet o por ultimo pregunte al team leader

## Pull y Merge
Nota: Deben tener presente que para realizar este proceso ya debieron haber hecho un Push a sus ramas, sino el comando les pedirá que lo hagan.

Primero deben cambiar de rama, para ello utilizan el comando.

```bash
git checkout "Rama a la que va dirigida"
```

Despues de cambiar de rama deben traer lo que este contenido por lo que hacen

```bash
git pull
```

Con ello traen lo que esta almacenado, vuelven a tu rama usando "Checkout". Cuando ya esten en su rama colocan

```bash
git merge "Rama a la que quieren combinar"
```