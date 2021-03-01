# Imports

import os
import sys

import pygame
import pygame.freetype

import time

import random

# PyGame Setup

pygame.init()
clock = pygame.time.Clock()

game_started = False

# Static variables

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (64, 64, 64)

WIDTH = 1280
HEIGTH = 720

EDGE_DISTANCE = 50

PLAYER_WIDTH = 20
PLAYER_HEIGTH = 180

BALL_SIZE = 25

UP = -3
DOWN = 3

BALL_SPEED = 3

# Text

TEXT_TITLE = "Press SPACE to start"
TEXT_CONTROLS_1 = "Player 1: W/S"
TEXT_CONTROLS_2 = "Player 2: ↑/↓"
TEXT_WIN = "Player {} won the game!"
TEXT_SCORE = "{} | {}"
TEXT_TIMER = "{}"

pygame.font.init()
font_big = pygame.freetype.SysFont("Consolas", 40)
font_middle = pygame.freetype.SysFont("Consolas", 30)
font_small = pygame.freetype.SysFont("Consolas", 20)

def get_formatted_score():
    return TEXT_SCORE.format(score[1], score[2])

def get_formatted_timer(counter):
    return TEXT_TIMER.format(counter)

# Math

def get_start_x(player):
    if player == 1:
        return EDGE_DISTANCE - PLAYER_WIDTH/2 
    elif player == 2:
        return WIDTH - EDGE_DISTANCE - PLAYER_WIDTH/2

def get_start_y():
    return HEIGTH/2 - PLAYER_HEIGTH/2

# Window

display = pygame.display
window = display.set_mode((WIDTH, HEIGTH))
display.set_caption("Pong")
image = pygame.image.load(sys.path[0] + "/stuff/icon.png")
display.set_icon(image)

# Ball

ball_move_x = BALL_SPEED
ball_move_y = BALL_SPEED

def move_ball():
    global ball_move_x, ball_move_y, ball, score_timer
    ball.x += ball_move_x
    ball.y += ball_move_y
    if ball.top <= 0 or ball.bottom >= HEIGTH:
        switch_direction("y")
    if ball.left <= 0:
        add_point(2)
        score_timer = pygame.time.get_ticks()
    if ball.right >= WIDTH:
        add_point(1)
        score_timer = pygame.time.get_ticks()

def switch_direction(dir):
    global ball_move_x, ball_move_y
    if dir == "x":
        ball_move_x *= -1 
    elif dir == "y":
        ball_move_y *= -1 

def start_ball():
    global score_timer
    score_timer = pygame.time.get_ticks()
    reset_ball()

def reset_ball():
    global ball_move_x, ball_move_y, score_timer
    ball.center = (WIDTH/2, HEIGTH/2)
    difference = pygame.time.get_ticks() - score_timer
    counter = 1
    if difference <= 3000:
        if difference < 1000:
            counter = 3
        elif difference < 2000:
            counter = 2
        font_small.render_to(window, ((WIDTH/2 - (font_small.get_rect(get_formatted_timer(counter)).width)/2), HEIGTH/2+30), get_formatted_timer(counter), WHITE)
        ball_move_x, ball_move_y = 0,0
    else:
        ball_move_x = BALL_SPEED * random.choice((1,-1))
        ball_move_y = BALL_SPEED * random.choice((1,-1))
        score_timer = None

ball = pygame.Rect(WIDTH/2-BALL_SIZE/2, HEIGTH/2-BALL_SIZE/2, BALL_SIZE, BALL_SIZE)

# Score timer

score_timer = None

# Player

pressed = {}
score = {}

player1 = pygame.Rect(get_start_x(1), get_start_y(), PLAYER_WIDTH, PLAYER_HEIGTH)
player2 = pygame.Rect(get_start_x(2), get_start_y(), PLAYER_WIDTH, PLAYER_HEIGTH)

score[1] = 0
score[2] = 0

def move_players():
    if pressed.get(pygame.K_UP) and not player2.top <= 0:
        player2.y += UP
    elif pressed.get(pygame.K_DOWN) and not player2.bottom >= HEIGTH:
        player2.y += DOWN
    if pressed.get(pygame.K_w) and not player1.top <= 0:
        player1.y += UP
    elif pressed.get(pygame.K_s) and not player1.bottom >= HEIGTH:
        player1.y += DOWN

def check_player_keys_down(event):
    if event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_s or event.key == pygame.K_w:
        pressed[event.key] = True

def check_player_keys_up(event):
    if event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_s or event.key == pygame.K_w:
        pressed[event.key] = False

def add_point(player):
    score[player] = score[player] + 1

# Animation

def animate():
    window.fill(GRAY)
    if game_started:
        animate_obj()
        show_score()
    else:
        show_start_menu()

def animate_obj():
    pygame.draw.rect(window, WHITE, ball)
    pygame.draw.rect(window, WHITE, player1)
    pygame.draw.rect(window, WHITE, player2)

    if score_timer:
        reset_ball()

    if (player1.colliderect(ball) or player2.colliderect(ball)):
        switch_direction("x")

    move_ball()
    move_players()

def show_start_menu():
    # renders the start menu text to x = (half of the screen - half of the lenght of the text rectangle)
    font_big.render_to(window, (WIDTH/2-(font_big.get_rect(TEXT_TITLE).width/2), HEIGTH/2-70), TEXT_TITLE, WHITE)
    font_middle.render_to(window, (WIDTH/2-(font_middle.get_rect(TEXT_CONTROLS_1).width/2), HEIGTH/2-25), TEXT_CONTROLS_1, WHITE)
    font_middle.render_to(window, (WIDTH/2-(font_middle.get_rect(TEXT_CONTROLS_2).width/2), HEIGTH/2+10), TEXT_CONTROLS_2, WHITE)

def show_score():
    font_middle.render_to(window, (WIDTH/2-(font_middle.get_rect(get_formatted_score()).width/2), 10), get_formatted_score(), WHITE)

# Events

def check_events():
    global game_started
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True
                start_ball()
            if game_started:
                check_player_keys_down(event)
        if event.type == pygame.KEYUP:
            if game_started:
                check_player_keys_up(event)

# Game Thread

while True:
    check_events()
    animate()
    display.flip()
    clock.tick(120)
