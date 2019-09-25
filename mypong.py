# Jucimar Jr 2019
# pong em turtle python https://docs.python.org/3.3/library/turtle.html
# baseado em http://christianthompson.com/node/51
# fonte Press Start 2P https://www.fontspace.com/codeman38/press-start-2p
# fonte DS-Digital https://www.dafont.com/pt/ds-digital.font
# som pontuação https://freesound.org/people/Kodack/sounds/258020/


import os
import time
import turtle


# escrever mensagens e texos
def write_message(sprite, text, tamanho):
    sprite.write(text, align='center', font=('DS-Digital', tamanho, 'normal'))


# criar a tela inicial do jogo (inicializar)
def start_game(screen):

    # desenhando a tela
    screen.clear()
    screen.title('My Pong')
    screen.bgcolor('#2E6145')
    screen.setup(width=800, height=600)
    screen.tracer(100)

    # mensagens e configurações iniciais
    mensagens = [
        'Welcome to Pong!',
        'Are you ready?', 'GO!',
        '''Choose your game mode \n
    0 - Bot VS Bot \n
    1 - Player VS Bot \n
    2 - Player VS Player \n
    3 - Exit \n''']

    start = turtle.Turtle()
    start.color('white')
    start.penup()
    start.hideturtle()
    for i in range(3):
        write_message(start, mensagens[i], 30)
        time.sleep(1.5)
        start.clear()
        if i == 0:
            # usuário escolhendo o modo de jogo
            start.penup()
            start.goto(0, -220)
            write_message(start, mensagens[3], 30)
            global game_mode
            game_mode = 0
            while (game_mode != '0' and
                   game_mode != '1' and
                   game_mode != '2' and
                   game_mode != '3'):
                game_mode = screen.textinput(
                    'Game mode', 'Choose 0, 1, 2 or 3')
            if(game_mode == '3'):
                screen.bye()
            start.clear()
        start.penup()
        start.goto(0, 0)


# desenhar raquetes e bola (e alguns outros sprites)
def drawn_sprites(sprite, shape, color, x):
    sprite.speed(0)
    sprite.shape(shape)
    sprite.penup()
    sprite.goto(x, 0)
    if shape == 'square':
        sprite.color('black', color)
        sprite.shapesize(stretch_wid=5, stretch_len=1)
    else:
        sprite.color(color)


# desenhar o display da pontuação
def create_boards(board, color, x):
    board.speed(0)
    board.shape('square')
    board.color(color)
    board.penup()
    board.hideturtle()
    board.goto(x, 250)
    write_message(board, 0, 35)


# desenhar a rede (tracejados do centro)
def create_dashed():
    dashed = turtle.Turtle()
    dashed.color('white')
    dashed.penup()
    dashed.hideturtle()
    axis_y = 0
    while axis_y >= -600:
        dashed.goto(0, 276+axis_y)
        write_message(dashed, '|', 15)
        axis_y -= 30


# desenhar as linhas da mesa
def create_line(x1, y1, x2, y2):
    line = turtle.Turtle()
    line.penup()
    line.setpos(x1, y1)
    line.color('white')
    line.pendown()
    line.setpos(x2, y2)
    line.hideturtle()


# mover a raquete 1
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


# mover a raquete 2
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


# mapear as teclas
def map_keys():
    screen.listen()
    if game_mode == '2' or game_mode == '1':
        screen.onkeypress(paddle_1_up, 'w')
        screen.onkeypress(paddle_1_down, 's')
    if game_mode == '2':
        screen.onkeypress(paddle_2_up, 'Up')
        screen.onkeypress(paddle_2_down, 'Down')


# ajustar a velocidade da bola
def update_ball_speed(paddle):
    print(ball.dx, ball.dy)
    ball.dx = ball.dx + 0.1 if ball.dx > 0 else ball.dx - 0.1
    segment = int(abs(paddle.ycor()-ball.ycor()) / 8)/10
    ball.dy = 0.5 + segment if ball.dy > 0 else -0.5 - segment


# resetar a velocidade e posição da raquete e bola
def reset_positions():
    ball.dx = ball.dy = 0.5
    ball.goto(0, 0)
    ball.dx *= -1
    paddle_1.goto(-350, 0)
    paddle_2.goto(350, 0)
    time.sleep(1)


# criar a tela principal do jogo
def game():

    # criando as raquetes
    # as paddles precisam ser globais por causa das funções move_paddle
    global paddle_1
    paddle_1 = turtle.Turtle()
    drawn_sprites(paddle_1, 'square', '#5ca3ff', -350)
    global paddle_2
    paddle_2 = turtle.Turtle()
    drawn_sprites(paddle_2, 'square', '#ff6161', 350)

    # criando a bola
    # a bola precisa ser global por causa da função update_ball_speed
    global ball
    ball = turtle.Turtle()
    drawn_sprites(ball, 'circle', '#e8971e', 0)
    ball.dx = 0.5
    ball.dy = 0.5

    # criando o display da pontuação
    board_1 = turtle.Turtle()
    create_boards(board_1, '#5ca3ff', -100)
    board_2 = turtle.Turtle()
    create_boards(board_2, '#ff6161', 100)

    # criando as linhas e a rede
    create_dashed()
    create_line(-405, 245, 405, 245)
    create_line(-405, -245, 405, -245)
    create_line(-250, -245, -250, 245)
    create_line(250, -245, 250, 245)
    create_line(250, 0, -250, 0)

    # mapeando as teclas
    map_keys()

    # pontuação inicial
    score_1 = score_2 = 0

    # gameplay
    GameOn = True
    while GameOn:
        screen.update()

        # movimentação da bola
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # colisão com a parede superior
        if ball.ycor() > 287:
            os.system('aplay bounce.wav&')
            ball.sety(287)
            ball.dy *= -1

        # colisão com a parede inferior
        if ball.ycor() < -277:
            os.system('aplay bounce.wav&')
            ball.sety(-277)
            ball.dy *= -1

        # colisão com a parede esquerda
        if ball.xcor() < -385:
            score_2 += 1
            board_2.clear()
            write_message(board_2, score_2, 35)
            os.system('aplay 258020__kodack__arcade-bleep-sound.wav&')
            reset_positions()

        # colisão com a parede direita
        if ball.xcor() > 385:
            score_1 += 1
            board_1.clear()
            write_message(board_1, score_1, 35)
            os.system('aplay 258020__kodack__arcade-bleep-sound.wav&')
            reset_positions()

        # colisão com a raquete 1
        if (ball.xcor() < -330 and
            ball.ycor() < paddle_1.ycor() + 50 and
                ball.ycor() > paddle_1.ycor() - 50):
            ball.dx *= -1
            os.system('aplay bounce.wav&')
            update_ball_speed(paddle_1)

        # colisão com a raquete 2
        if (ball.xcor() > 330 and
            ball.ycor() < paddle_2.ycor() + 50 and
                ball.ycor() > paddle_2.ycor() - 50):
            ball.dx *= -1
            os.system('aplay bounce.wav&')
            update_ball_speed(paddle_2)

        # raquetes em modo de jogo 0 e 1
        if game_mode == '1' or game_mode == '0':
            if (paddle_2.ycor() < ball.ycor() and
                paddle_2.ycor() < 250 and
                    paddle_2.ycor() > -250):
                a = paddle_2.ycor()
                paddle_2.sety(a + 2)
            else:
                paddle_2.sety(a - 2)
            if (paddle_2.ycor() > ball.ycor() and
                paddle_2.ycor() < 250 and
                    paddle_2.ycor() > -250):
                a = paddle_2.ycor()
                paddle_2.sety(a - 2)
            else:
                paddle_2.sety(a + 2)

        if game_mode == '0':
            if (paddle_1.ycor() < ball.ycor() and
                paddle_1.ycor() < 250 and
                    paddle_1.ycor() > -250):
                a = paddle_1.ycor()
                paddle_1.sety(a + 2)
            else:
                paddle_1.sety(a - 2)
            if (paddle_1.ycor() > ball.ycor() and
                paddle_1. ycor() < 250 and
                    paddle_1.ycor() > -250):
                a = paddle_1.ycor()
                paddle_1.sety(a - 2)
            else:
                paddle_1.sety(a + 2)

        # fim de jogo: determinando o vencedor
        if (score_1 >= 5) or (score_2 >= 5):
            GameOn = False
            final = turtle.Turtle()
            if score_1 >= 5:
                drawn_sprites(final, 'turtle', '#5ca3ff', 0)
                write_message(final, 'Player 1 Wins!', 30)
            else:
                drawn_sprites(final, 'turtle', '#ff6161', 0)
                write_message(final, 'Player 2 Wins!', 30)
        else:
            GameOn = True


# loop para o jogo sempre reiniciar
while True:
    # chamando a tela inicial
    screen = turtle.Screen()
    start_game(screen)
    # chamando a tela principal
    game()
    # pequena pausa antes de iniciar outra partida
    time.sleep(4)
