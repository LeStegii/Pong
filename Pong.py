# Imports and static Variables

import turtle
import sys, os
import functools 
from tkinter import PhotoImage

BLACK = (0, 0, 0)
WHITE = (1, 1, 1)
GRAY = (64/255, 64/255, 64/255)

height = 1280
width = 720

UP = height/64
DOWN = -(height/64)

# Math

def get_start_x(player):
    if player == 1:
        return -width + 120
    elif player == 2:
        return width - 120

# Window

window = turtle.Screen()
window.title("Pong")
window.bgcolor(GRAY)
window.setup(width=height, height=width)
window.tracer(0)
window.cv._rootwindow.resizable(False, False)
program_directory=sys.path[0]
window.cv._rootwindow.iconphoto(True, PhotoImage(file=os.path.join(program_directory, "icon.png")))

# Player 
player_1 = turtle.Turtle()
player_1.speed(0)
player_1.shapesize(stretch_wid=5, stretch_len=1)
player_1.shape("square")
player_1.color(WHITE)
player_1.penup()
player_1.goto(get_start_x(1), 0)

# Player 2
player_2 = turtle.Turtle()
player_2.shapesize(stretch_wid=5, stretch_len=1)
player_2.speed(0)
player_2.shape("square")
player_2.color(WHITE)
player_2.penup()
player_2.goto(get_start_x(2), 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color(WHITE)
ball.penup()
ball.goto(0, 0)

# Movement

def move_player(direction, player):
    if player == 1:
        player_1.sety(player_1.ycor()+direction)
    elif player == 2:
        player_2.sety(player_2.ycor()+direction)
    print(direction, player)

# Keyboard

window.listen()
window.onkeypress(functools.partial(move_player, UP, 1), "w")
window.onkeypress(functools.partial(move_player, DOWN, 1), "s")
window.onkeypress(functools.partial(move_player, UP, 2), "Up")
window.onkeypress(functools.partial(move_player, DOWN, 2), "Down")

# Game Thread

while True:
    window.update()