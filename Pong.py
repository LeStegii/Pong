# Don't judge me for the code style please...

# Imports

import os
import random
import sys
import time
import importlib.util
import subprocess

spec = importlib.util.find_spec("pygame")
if spec is None:
    print("PyGame is not installed. Trying to install it automatically.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

try:
    import pygame
    import pygame.freetype
except ImportError as e:
    print("Automatic installation failed. Please install PyGame in order to run this game.\nBitte installiere PyGame, um dieses Spiel zu spielen.\n\npython3 -m pip install -U pygame --user")
    time.sleep(5)
    sys.exit()

# PyGame Setup

pygame.init()
clock = pygame.time.Clock()

game_state = "MENU"

# Images and Sounds
player_icon = pygame.image.load(sys.path[0] + "/stuff/player_icon.png")
bot_icon = pygame.image.load(sys.path[0] + "/stuff/bot_icon.png")
window_icon = pygame.image.load(sys.path[0] + "/stuff/icon.png")
logo = pygame.image.load(sys.path[0] + "/stuff/logo.png")
logo = pygame.transform.scale(logo, (500, 125))

hit_sound = pygame.mixer.Sound(sys.path[0] + "/stuff/hit.mp3")
hit_sound.set_volume(0.1)
score_sound = pygame.mixer.Sound(sys.path[0] + "/stuff/score.mp3")
score_sound.set_volume(0.1)

def play_sound(sound):
    pygame.mixer.Sound.play(sound)

# Static variables

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 128, 0)
GRAY = (64, 64, 64)

WIDTH = 1280
HEIGTH = 720

EDGE_DISTANCE = 50

PLAYER_WIDTH = 20
PLAYER_HEIGTH = 180

BALL_SIZE = 25

UP = -4
DOWN = 4

BALL_SPEED = 4

SELECTOR_SIZE = 64

START_TICKS = 120 

# Text

TEXT_TITLE = "Press SPACE to start"
TEXT_RESTART = "Press SPACE to restart the game."
TEXT_CONTROLS_1 = "Player 1: W/S"
TEXT_CONTROLS_2 = "Player 2: ↑/↓"
TEXT_WIN = "Player {} won the game!"
TEXT_BOT_CHANGE = "(Use ←/→ to change)" 
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

def get_formatted_winner(winner):
    return TEXT_WIN.format(winner)

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
display.set_icon(window_icon)
window = display.set_mode((WIDTH, HEIGTH))
display.set_caption("Pong")

# Ball

ball_move_x = BALL_SPEED
ball_move_y = BALL_SPEED

ticks = START_TICKS

def reset_ticks(): 
    global ticks 
    ticks = START_TICKS 

def move_ball():
    global ball_move_x, ball_move_y, ball, score_timer
    ball.x += ball_move_x
    ball.y += ball_move_y
    if ball.top <= 0 or ball.bottom >= HEIGTH:
        switch_direction("y")
    if ball.left <= 0:
        add_point(2)
        play_sound(score_sound)
        score_timer = pygame.time.get_ticks()
    if ball.right >= WIDTH:
        add_point(1)
        play_sound(score_sound)
        score_timer = pygame.time.get_ticks()

def check_ball_collision():
    if player1.colliderect(ball) and ball_move_x < 0:
        if abs(ball.left - player1.right) <= BALL_SPEED:
            switch_direction("x")
            play_sound(hit_sound)
        elif abs(ball.bottom - player1.top) <= BALL_SPEED or abs(ball.top - player1.bottom) <= BALL_SPEED:
            switch_direction("y")
            play_sound(hit_sound)
    if player2.colliderect(ball) and ball_move_x > 0:
        if abs(ball.right - player2.left) <= BALL_SPEED:
            switch_direction("x")
            play_sound(hit_sound)
        elif abs(ball.bottom - player2.top) <= BALL_SPEED or abs(ball.top - player2.bottom) <= BALL_SPEED:
            switch_direction("y")
            play_sound(hit_sound)


def switch_direction(dir):
    global ball_move_x, ball_move_y, ticks
    if dir == "x":
        ball_move_x *= -1 
        ticks += 3
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

# Bot 

bot_player = False
selector = pygame.Rect(WIDTH/2-SELECTOR_SIZE/2, HEIGTH/2-SELECTOR_SIZE/2, SELECTOR_SIZE, SELECTOR_SIZE)

def select(pos):
    if pos == 1:
        selector.center = (WIDTH/2 - 50, HEIGTH/2+90)
    elif pos == 2:
        selector.center = (WIDTH/2 + 50, HEIGTH/2+90)

# Player

winning_score = 5
winner = 0

pressed = {}
score = {}


player1 = pygame.Rect(get_start_x(1), get_start_y(), PLAYER_WIDTH, PLAYER_HEIGTH)
player2 = pygame.Rect(get_start_x(2), get_start_y(), PLAYER_WIDTH, PLAYER_HEIGTH)

score[1] = 0
score[2] = 0

def move_players():
    if pressed.get(pygame.K_UP) and not player2.top <= 0 and not bot_player:
        player2.y += UP
    elif pressed.get(pygame.K_DOWN) and not player2.bottom >= HEIGTH and not bot_player:
        player2.y += DOWN
    if pressed.get(pygame.K_w) and not player1.top <= 0:
        player1.y += UP
    elif pressed.get(pygame.K_s) and not player1.bottom >= HEIGTH:
        player1.y += DOWN
    
    if bot_player:
        if ball.x >= WIDTH/1.5 and int(round(ball.y+BALL_SIZE/2)) < int(round(player2.y+PLAYER_HEIGTH/2)) and not player2.top <= 0:
            player2.y += UP
        elif ball.x >= WIDTH/1.5 and int(round(ball.y+BALL_SIZE/2)) > int(round(player2.y+PLAYER_HEIGTH/2)) and not player2.bottom >= HEIGTH:
            player2.y += DOWN

def check_player_keys_down(event):
    if event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_s or event.key == pygame.K_w:
        pressed[event.key] = True

def check_player_keys_up(event):
    if event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_s or event.key == pygame.K_w:
        pressed[event.key] = False

def add_point(player):
    global winner, game_state
    reset_ticks() 
    score[player] = score[player] + 1
    if score[player] >= winning_score:
        winner = player
        game_state = "ENDED"

# Animation

def animate():
    window.fill(GRAY)
    if game_state == "STARTED":
        animate_obj()
        show_score()
    elif game_state == "MENU":
        show_start_menu()
    elif game_state == "ENDED":
        show_winner()

def animate_obj():
    pygame.draw.rect(window, WHITE, ball)
    pygame.draw.rect(window, WHITE, player1)
    if bot_player:
        color = RED
    else:
        color = WHITE
    pygame.draw.rect(window, color, player2)

    if score_timer:
        reset_ball()

    check_ball_collision()

    move_ball()
    move_players()

def show_start_menu():
    # renders the start menu text to x = (half of the screen - half of the lenght of the text rectangle)
    font_big.render_to(window, (WIDTH/2-(font_big.get_rect(TEXT_TITLE).width/2), HEIGTH/2-80), TEXT_TITLE, WHITE)
    font_middle.render_to(window, (WIDTH/2-(font_middle.get_rect(TEXT_CONTROLS_1).width/2), HEIGTH/2-35), TEXT_CONTROLS_1, WHITE)
    if not bot_player:
        select(1)
        font_middle.render_to(window, (WIDTH/2-(font_middle.get_rect(TEXT_CONTROLS_2).width/2), HEIGTH/2), TEXT_CONTROLS_2, WHITE)
    else:
        select(2)
    pygame.draw.rect(window, RED, selector)
    window.blit(player_icon, ((WIDTH/2-50-(player_icon.get_width()/2)),HEIGTH/2+90-(player_icon.get_width()/2)))
    window.blit(bot_icon, ((WIDTH/2+50-(bot_icon.get_width()/2)),HEIGTH/2+90-(bot_icon.get_width()/2)))
    window.blit(logo, ((WIDTH/2-(logo.get_width()/2)),(HEIGTH/2-300)))
    font_small.render_to(window, (WIDTH/2-(font_small.get_rect(TEXT_BOT_CHANGE).width/2), HEIGTH/2+150), TEXT_BOT_CHANGE, WHITE)

def show_score():
    font_middle.render_to(window, (WIDTH/2-(font_middle.get_rect(get_formatted_score()).width/2), 10), get_formatted_score(), WHITE)

def show_winner():
   font_big.render_to(window, (WIDTH/2-(font_big.get_rect(get_formatted_winner(winner)).width/2), HEIGTH/2-50), get_formatted_winner(winner), WHITE)
   font_small.render_to(window, (WIDTH/2-(font_small.get_rect(TEXT_RESTART).width/2), HEIGTH/2 + 10), TEXT_RESTART, WHITE)

# Events

def check_events():
    global game_state, winner, pressed, score, ball_move_x, ball_move_y, score_timer, bot_player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    game_state = "STARTED"
                    play_sound(hit_sound)
                    start_ball()
                if event.key == pygame.K_RIGHT:
                    if not bot_player:
                        bot_player = True
                        play_sound(hit_sound)
                if event.key == pygame.K_LEFT:
                    if bot_player:
                        bot_player = False
                        play_sound(hit_sound)
            elif game_state == "ENDED":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Resets all the variables
                    game_state = "MENU"
                    winner = 0
                    pressed = {}
                    score = {}
                    score[1] = 0
                    score[2] = 0
                    ball_move_x = BALL_SPEED
                    ball_move_y = BALL_SPEED
                    score_timer = None
                    reset_ticks()
                    player1.x, player1.y = get_start_x(1), get_start_y()
                    player2.x, player2.y = get_start_x(2), get_start_y()
                    start_ball()
            elif game_state == "STARTED":
                check_player_keys_down(event)
        if event.type == pygame.KEYUP:
            if game_state == "STARTED":
                check_player_keys_up(event)

# Game Thread

while True:
    check_events()
    animate()
    display.flip()
    clock.tick(ticks)