import json
import sys

import pygame
from pygame.locals import *

import game
import variables

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



def showMenu():
    """
    Display the start screen
    """
    # create light theme button
    light_theme = variables.Button(
        tuple(c["colour"]["light"]["2048"]), 200-70, 275, 45, 45, "light")
    # create dark theme button
    dark_theme = variables.Button(
        tuple(c["colour"]["dark"]["2048"]), 270-70, 275, 45, 45, "dark")
    
    # initialise theme
    theme = ""
    theme_selected = False
    
    # create difficulty buttons
    _2048 = variables.Button(tuple(c["colour"]["light"]["64"]),
                  130, 330, 45, 45, "2048")
    _4096 = variables.Button(tuple(c["colour"]["light"]["2048"]),
                  200, 330, 45, 45, "4096")
    _8192 = variables.Button(tuple(c["colour"]["light"]["2048"]),
                  270, 330, 45, 45, "8192")
    _16384 = variables.Button(tuple(c["colour"]["light"]["2048"]),
                  340, 330, 45, 45, "16384")

    # default difficulty
    difficulty = 0
    diff_selected = False
    
    # create play button
    play = variables.Button(tuple(c["colour"]["light"]["2048"]),
                  235, 400, 45, 45, "Play")

    # create rules button
    rules = variables.Button(tuple(c["colour"]["light"]["2048"]),
                  150, 400, 45, 45, "Rules")              

    # pygame loop for start screen
    while True:
        screen.fill(BLACK)

        screen.blit(pygame.transform.scale(
            pygame.image.load("icon01.png"), (200, 200)), (155, 50))

        font = pygame.font.SysFont(c["font"], 15, bold=True)

        theme_text = font.render("Theme: ", 1, WHITE)
        screen.blit(theme_text, (55, 285))

        diff_text = font.render("Difficulty: ", 1, WHITE)
        screen.blit(diff_text, (40, 345))

        # set fonts for buttons
        font1 = pygame.font.SysFont(c["font"], 15, bold=True)
        font2 = pygame.font.SysFont(c["font"], 14, bold=True)

        # draw all buttons on the screen
        light_theme.draw(screen, BLACK, font1)
        dark_theme.draw(screen, (197, 255, 215), font1)
        _2048.draw(screen, BLACK, font2)
        _4096.draw(screen, BLACK, font2)
        _8192.draw(screen, BLACK, font2)
        _16384.draw(screen, BLACK, font2)
        play.draw(screen, BLACK, font1)
        rules.draw(screen, BLACK,font1)

        pygame.display.update()

        for event in pygame.event.get():
            # store mouse position (coordinates)
            pos = pygame.mouse.get_pos()

            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_q):
                # exit if q is pressed 
                pygame.quit()
                sys.exit()

            # check if a button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # select light theme
                if light_theme.isOver(pos):
                    dark_theme.colour = tuple(c["colour"]["dark"]["2048"])
                    light_theme.colour = tuple(c["colour"]["light"]["64"])
                    theme = "light"
                    theme_selected = True

                # select dark theme
                if dark_theme.isOver(pos):
                    dark_theme.colour = tuple(c["colour"]["dark"]["background"])
                    light_theme.colour = tuple(c["colour"]["light"]["2048"])
                    theme = "dark"
                    theme_selected = True
                
                if _2048.isOver(pos):
                    _2048.colour = tuple(c["colour"]["light"]["64"])
                    _4096.colour = tuple(c["colour"]["light"]["2048"])
                    _8192.colour = tuple(c["colour"]["light"]["2048"])
                    _16384.colour = tuple(c["colour"]["light"]["2048"])
                    difficulty = 2048
                    variables.number = difficulty
                    variables.difficulty = difficulty
                    diff_selected = True
                
                if _4096.isOver(pos):
                    _4096.colour = tuple(c["colour"]["light"]["64"])
                    _2048.colour = tuple(c["colour"]["light"]["2048"])
                    _8192.colour = tuple(c["colour"]["light"]["2048"])
                    _16384.colour = tuple(c["colour"]["light"]["2048"])
                    difficulty = 4096
                    variables.number = difficulty
                    variables.difficulty = difficulty
                    diff_selected = True
                
                if _8192.isOver(pos):
                    _8192.colour = tuple(c["colour"]["light"]["64"])
                    _4096.colour = tuple(c["colour"]["light"]["2048"])
                    _2048.colour = tuple(c["colour"]["light"]["2048"])
                    _16384.colour = tuple(c["colour"]["light"]["2048"])
                    difficulty = 8192
                    variables.number = difficulty
                    variables.difficulty = difficulty
                    diff_selected = True
                
                if _16384.isOver(pos):
                    _16384.colour = tuple(c["colour"]["light"]["64"])
                    _4096.colour = tuple(c["colour"]["light"]["2048"])
                    _8192.colour = tuple(c["colour"]["light"]["2048"])
                    _2048.colour = tuple(c["colour"]["light"]["2048"])
                    difficulty = 16384
                    variables.number = difficulty
                    variables.difficulty = difficulty
                    diff_selected = True

                if rules.isOver(pos):
                    back = game.displayrules()
                    if back == 'back':
                        showMenu()

                # play game with selected theme
                if play.isOver(pos):
                    if theme != "" and difficulty != 0:
                        game.playGame(theme, difficulty)

                # reset theme & diff choice if area outside buttons is clicked
                if not play.isOver(pos) and \
                    not dark_theme.isOver(pos) and \
                    not light_theme.isOver(pos) and \
                    not _2048.isOver(pos) and \
                    not _4096.isOver(pos) and \
                    not _8192.isOver(pos) and \
                    not _16384.isOver(pos):

                    theme = ""
                    theme_selected = False
                    diff_selected = False

                    light_theme.colour = tuple(c["colour"]["light"]["2048"])
                    dark_theme.colour = tuple(c["colour"]["dark"]["2048"])
                    _2048.colour = tuple(c["colour"]["light"]["2048"])
                    _4096.colour = tuple(c["colour"]["light"]["2048"])
                    _8192.colour = tuple(c["colour"]["light"]["2048"])
                    _16384.colour = tuple(c["colour"]["light"]["2048"])
                    

            # change colour on hovering over buttons
            if event.type == pygame.MOUSEMOTION:
                if not theme_selected:
                    if light_theme.isOver(pos):
                        light_theme.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        light_theme.colour = tuple(c["colour"]["light"]["2048"])
                    
                    if dark_theme.isOver(pos):
                        dark_theme.colour = tuple(c["colour"]["dark"]["background"])
                    else:
                        dark_theme.colour = tuple(c["colour"]["dark"]["2048"])
                
                if not diff_selected:
                    if _2048.isOver(pos):
                        _2048.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        _2048.colour = tuple(c["colour"]["light"]["2048"])
                    
                    if _4096.isOver(pos):
                        _4096.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        _4096.colour = tuple(c["colour"]["light"]["2048"])
                    
                    if _8192.isOver(pos):
                        _8192.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        _8192.colour = tuple(c["colour"]["light"]["2048"])
                    
                    if _16384.isOver(pos):
                        _16384.colour = tuple(c["colour"]["light"]["64"])
                    else:
                        _16384.colour = tuple(c["colour"]["light"]["2048"])
                
                if play.isOver(pos):
                    play.colour = tuple(c["colour"]["light"]["64"])
                else:
                    play.colour = tuple(c["colour"]["light"]["2048"])


if __name__ == "__main__":
    # load json data
    c = json.load(open("constants.json", "r"))

    # set up pygame
    pygame.init()
    # set up screen
    screen = pygame.display.set_mode(
        (c["size"], c["size"]))
    pygame.display.set_caption("NoT2048")

    # display game icon in window
    icon = pygame.transform.scale(
        pygame.image.load("images/icon2.ico"), (32, 32))
    pygame.display.set_icon(icon)

    # set font according to json data specifications
    my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)

    # display the start screen 
    showMenu()
