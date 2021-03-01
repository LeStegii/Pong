# Imports

import functools
import os
import sys
from tkinter import PhotoImage

import pygame
import pygame.freetype

# PyGame Setup

pygame.init()
clock = pygame.time.Clock()

game_started = False

# Static variables

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (64, 64, 64)

width = 1280
height = 720

edge_distance = 50

player_width = 20
player_hight = 180

ball_size = 25

UP = -(height/64)
DOWN = height/64

# Text

TEXT_TITLE = "Press SPACE to start"
TEXT_CONTROLS_1 = "Player 1: W/S"
TEXT_CONTROLS_2 = "Player 2: ↑/↓"
TEXT_WIN = "Player %s won the game!"
TEXT_SCORE = "%s | %s"

TITLE_WIDTH = 434

pygame.font.init()
font_title = pygame.freetype.SysFont("Consolas", 40) # width = 434
font_controls = pygame.freetype.SysFont("Consolas", 30)


# Math

def get_start_x(player):
    if player == 1:
        return edge_distance - player_width/2 
    elif player == 2:
        return width - edge_distance - player_width/2

def get_start_y():
    return height/2 - player_hight/2

# Window

display = pygame.display
window = display.set_mode((width,height))
display.set_caption("Pong")

# Ball - pygame.Rect(x,y,w,h)

ball_move_x = 7
ball_move_y = 7

def switch_direction(dir):
    global ball_move_x, ball_move_y
    if dir == "x":
        ball_move_x *= -1 
    elif dir == "y":
        ball_move_y *= -1 

ball = pygame.Rect(width/2-15,height/2-15,30,30)

# Player

player1 = pygame.Rect(get_start_x(1), get_start_y(), player_width, player_hight)
player2 = pygame.Rect(get_start_x(2), get_start_y(), player_width, player_hight)

# Draw


# Game Thread

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True
            if event.key == pygame.K_DOWN and game_started:
                player2.y += DOWN
            if event.key == pygame.K_UP and game_started:
                player2.y += UP
            if event.key == pygame.K_s and game_started:
                player1.y += DOWN
            if event.key == pygame.K_w and game_started:
                player1.y += UP
    
    window.fill(GRAY)
    if not game_started:
        # renders the start menu text to x = (half of the screen - half of the lenght of the text rectangle)
        font_title.render_to(window, (width/2-(font_title.get_rect(TEXT_TITLE).width/2), height/2-70), TEXT_TITLE, WHITE)
        font_controls.render_to(window, (width/2-(font_controls.get_rect(TEXT_CONTROLS_1).width/2), height/2-25), TEXT_CONTROLS_1, WHITE)
        font_controls.render_to(window, (width/2-(font_controls.get_rect(TEXT_CONTROLS_2).width/2), height/2+10), TEXT_CONTROLS_2, WHITE)
    else:  
        pygame.draw.rect(window, WHITE, ball)
        pygame.draw.rect(window, WHITE, player1)
        pygame.draw.rect(window, WHITE, player2)

    display.flip()
    clock.tick(60)

#    title 434 pixel
