import turtle
import time
import random
import threading
import winsound  # Solo funciona en Windows. En otros sistemas operativos, se debe usar una biblioteca diferente.

# Configuración inicial de la ventana
window = turtle.Screen()
window.title('Snake')
window.bgcolor('#353535')
window.setup(width=600, height=600)
window.tracer(0)

# Variables del juego
posponer = 0.1
puntaje = 0
maxPuntaje = 0
juego_pausado = False

# Cabeza de la serpiente
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape('square')
cabeza.color('#75C46D')
cabeza.penup()
cabeza.goto(0, 0)
cabeza.direction = 'stop'

# Comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape('circle')
comida.color('#D12D2D')
comida.penup()
comida.goto(0, 100)

# Texto para el puntaje
texto = turtle.Turtle()
texto.speed(0)
texto.color('white')
texto.penup()
texto.hideturtle()
texto.goto(0, 260)
texto.write('Puntaje: 0     Máximo puntaje: 0', align='center', font=('Courier', 20, 'normal'))

# Cuerpo de la serpiente
cuerpo = []
colores = [(109, 160, 104), (104, 142, 160)]

# Funciones del juego
def printText():
    global maxPuntaje
    if puntaje > maxPuntaje:
        maxPuntaje = puntaje
    texto.clear()
    texto.write(f'Puntaje: {puntaje}     Máximo puntaje: {maxPuntaje}', align='center', font=('Courier', 20, 'normal'))

def arriba():
    if cabeza.direction != 'down':
        cabeza.direction = 'up'

def abajo():
    if cabeza.direction != 'up':
        cabeza.direction = 'down'

def izquierda():
    if cabeza.direction != 'right':
        cabeza.direction = 'left'

def derecha():
    if cabeza.direction != 'left':
        cabeza.direction = 'right'

def pausa():
    global juego_pausado
    juego_pausado = not juego_pausado

def movimiento():
    if cabeza.direction == 'up':
        y = cabeza.ycor()
        cabeza.sety(y + 20)
    elif cabeza.direction == 'down':
        y = cabeza.ycor()
        cabeza.sety(y - 20)
    elif cabeza.direction == 'left':
        x = cabeza.xcor()
        cabeza.setx(x - 20)
    elif cabeza.direction == 'right':
        x = cabeza.xcor()
        cabeza.setx(x + 20)

def crearSegmento():
    global puntaje
    segmento = turtle.Turtle()
    turtle.colormode(255)
    segmento.speed(0)
    segmento.shape('square')
    segmento.color(random.choice(colores))
    segmento.penup()
    cuerpo.append(segmento)
    puntaje += 1
    printText()
   # reproducir_sonido("eat.wav")

def colisionComida():
    if cabeza.distance(comida) < 20:
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        comida.goto(x, y)
        crearSegmento()

def movCuerpo():
    totalSeg = len(cuerpo)
    for segmento in range(totalSeg - 1, 0, -1):
        x = cuerpo[segmento - 1].xcor()
        y = cuerpo[segmento - 1].ycor()
        cuerpo[segmento].goto(x, y)
    if totalSeg > 0:
        x = cabeza.xcor()
        y = cabeza.ycor()
        cuerpo[0].goto(x, y)

def colisionBorde():
    global puntaje
    if cabeza.xcor() < -280 or cabeza.xcor() > 280 or cabeza.ycor() < -280 or cabeza.ycor() > 280:
        reiniciarJuego()

def mordida():
    global puntaje
    for segmento in cuerpo:
        if cabeza.distance(segmento) < 20:
            reiniciarJuego()

def reiniciarJuego():
    global puntaje
    #reproducir_sonido("game_over.wav")
    time.sleep(0.5)
    cabeza.goto(0, 0)
    cabeza.direction = 'stop'
    for segmento in cuerpo:
        segmento.goto(1000, 1000)
    cuerpo.clear()
    puntaje = 0
    printText()

#def reproducir_sonido(archivo):
 #   threading.Thread(target=lambda: winsound.PlaySound(archivo, winsound.SND_FILENAME)).start()

# Conexión con teclado
window.listen()
window.onkeypress(arriba, 'Up')
window.onkeypress(abajo, 'Down')
window.onkeypress(izquierda, 'Left')
window.onkeypress(derecha, 'Right')
window.onkeypress(pausa, 'p')

# Dibuja el borde del juego
borde_juego = turtle.Turtle()
borde_juego.penup()
borde_juego.hideturtle()
borde_juego.color('white')
borde_juego.goto(-290, 290)
borde_juego.pendown()
for _ in range(4):
    borde_juego.forward(580)
    borde_juego.right(90)

# Ciclo permanente del juego
while True:
    window.update()
    if not juego_pausado:
        colisionBorde()
        colisionComida()
        mordida()
        movCuerpo()
        movimiento()
    time.sleep(posponer)
