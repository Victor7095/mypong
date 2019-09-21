# Jucimar Jr 2019
# pong em turtle python https://docs.python.org/3.3/library/turtle.html
# baseado em http://christianthompson.com/node/51
# fonte Press Start 2P https://www.fontspace.com/codeman38/press-start-2p
# fonte DS-Digital https://www.dafont.com/pt/ds-digital.font
# som pontuação https://freesound.org/people/Kodack/sounds/258020/

import turtle
import os
import sys
import random

# modos de jogo player vs player / player vs bot / bot vs bot
player_mode = sys.argv[1]  # "-2" "-1" "-0"

# desenhar tela
screen = turtle.Screen()
screen.title("My Pong")
screen.bgcolor("#377352")
screen.setup(width=800, height=600)
screen.tracer(100)

# desenhar raquete 1
paddle_1 = turtle.Turtle()
paddle_1.speed(0)
paddle_1.shape("square")
paddle_1.color("black", "#5ca3ff")
paddle_1.shapesize(stretch_wid=5, stretch_len=1)
paddle_1.penup()
paddle_1.goto(-350, 0)

# desenhar raquete 2
paddle_2 = turtle.Turtle()
paddle_2.speed(0)
paddle_2.shape("square")
paddle_2.color("black", "#ff6161")
paddle_2.shapesize(stretch_wid=5, stretch_len=1)
paddle_2.penup()
paddle_2.goto(350, 0)

# desenhar bola
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("#e8971e")
ball.penup()
ball.goto(0, 0)
ball.dx = 2
ball.dy = 2

# pontuação
score_1 = 0
score_2 = 0

# head-up display da pontuação
board_1 = turtle.Turtle()
board_1.speed(0)
board_1.shape("square")
board_1.color("#5ca3ff")
board_1.penup()
board_1.hideturtle()
board_1.goto(-100, 250)
board_1.write("0", align="center", font=("DS-Digital", 35, "normal"))

board_2 = turtle.Turtle()
board_2.speed(0)
board_2.shape("square")
board_2.color("#ff6161")
board_2.penup()
board_2.hideturtle()
board_2.goto(100, 250)
board_2.write("0", align="center", font=("DS-Digital", 35, "normal"))


# rede (tracejados do centro)
dashed = turtle.Turtle()
dashed.color("white")
dashed.penup()
dashed.hideturtle()
axis_y = 0
while axis_y >= -600:
    dashed.goto(0, 276+axis_y)
    dashed.write("|", align="center", font=("DS-Digital", 15, "bold"))
    axis_y -= 30


# linhas da mesa
def create_line(x1, y1, x2, y2):
    line = turtle.Turtle()
    line.penup()
    line.setpos(x1, y1)
    line.color("white")
    line.pendown()
    line.setpos(x2, y2)
    line.hideturtle()


create_line(-405, 245, 405, 245)
create_line(-405, -245, 405, -245)
create_line(-250, -245, -250, 245)
create_line(250, -245, 250, 245)
create_line(250, 0, -250, 0)


# mover raquete 1
def paddle_1_up():
    y = paddle_1.ycor()
    if y < 250:
        y += 20
    else:
        y = 250
    paddle_1.sety(y)


def paddle_1_down():
    y = paddle_1.ycor()
    if y > -250:
        y += -20
    else:
        y = -250
    paddle_1.sety(y)


def paddle_2_up():
    y = paddle_2.ycor()
    if y < 250:
        y += 20
    else:
        y = 250
    paddle_2.sety(y)


def paddle_2_down():
    y = paddle_2.ycor()
    if y > -250:
        y += -20
    else:
        y = -250
    paddle_2.sety(y)


# Ajustar velocidade da bola
def update_ball_speed(paddle):
    ball.dx = ball.dx + 1 if ball.dx > 0 else ball.dx - 1
    segment = int(abs(paddle.ycor()-ball.ycor()) / 8)
    ball.dy = 2 + segment if ball.dy > 0 else -2 - segment


# mapeando as teclas
screen.listen()
if player_mode == '-2' or player_mode == '-1':
    screen.onkeypress(paddle_1_up, "w")
    screen.onkeypress(paddle_1_down, "s")
if player_mode == '-2':
    screen.onkeypress(paddle_2_up, "Up")
    screen.onkeypress(paddle_2_down, "Down")

while True:
    screen.update()

    # movimentação da bola
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # colisão com parede superior
    if ball.ycor() > 290:
        os.system("aplay bounce.wav&")
        ball.sety(290)
        ball.dy *= -1

    # colisão com parede inferior
    if ball.ycor() < -280:
        os.system("aplay bounce.wav&")
        ball.sety(-280)
        ball.dy *= -1

    # colisão com parede esquerda
    if ball.xcor() < -390:
        score_2 += 1
        board_2.clear()
        board_2.write(score_2, align="center",
                      font=("DS-Digital", 35, "normal"))
        os.system("aplay 258020__kodack__arcade-bleep-sound.wav&")
        ball.dx = ball.dy = 2
        ball.goto(0, 0)
        ball.dx *= -1

    # colisão com parede direita
    if ball.xcor() > 390:
        score_1 += 1
        board_1.clear()
        board_1.write(score_1, align="center",
                      font=("DS-Digital", 35, "normal"))
        os.system("aplay 258020__kodack__arcade-bleep-sound.wav&")
        ball.dx = ball.dy = 2
        ball.goto(0, 0)
        ball.dx *= -1

    # colisão com raquete 1
    if(ball.xcor() < -330 and
       ball.ycor() < paddle_1.ycor() + 50 and
       ball.ycor() > paddle_1.ycor() - 50):
        ball.dx *= -1
        os.system("aplay bounce.wav&")
        update_ball_speed(paddle_1)

    # colisão com raquete 2
    if(ball.xcor() > 330 and
       ball.ycor() < paddle_2.ycor() + 50 and
       ball.ycor() > paddle_2.ycor() - 50):
        ball.dx *= -1
        os.system("aplay bounce.wav&")
        update_ball_speed(paddle_2)

    # raquetes em modo de jogo
    if player_mode == '-1' or player_mode == '-0':
        if paddle_2.ycor() < ball.ycor():
            a = paddle_2.ycor()
            paddle_2.sety(a + 2)
        if paddle_2.ycor() > ball.ycor():
            a = paddle_2.ycor()
            paddle_2.sety(a - 2)
    if player_mode == '-0':
        if paddle_1.ycor() < ball.ycor():
            a = paddle_1.ycor()
            paddle_1.sety(a + 2)
        if paddle_1.ycor() > ball.ycor():
            a = paddle_1.ycor()
            paddle_1.sety(a - 2)
