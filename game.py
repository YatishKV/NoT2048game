import json
import sys
import time
from copy import deepcopy


import pygame
from pygame.locals import *

from logic import *
import variables


# set up pygame for main gameplay
pygame.init()
c = json.load(open("constants.json", "r"))
screen = pygame.display.set_mode(
    (c["size"], c["size"]))
my_font = pygame.font.SysFont(c["font"], c["font_size"], bold=True)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def displayrules():
    """
    Display rules of the game when button is pressed.
    """
    rules_font = pygame.font.SysFont(c["font"], 20, bold=True)
    size = c["size"]
    # Fill the window with a transparent background
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    s.fill(c["colour"]["light"]["over"])
    screen.blit(s, (0, 0))

    text = '''The Player's objective is to divide the main block(2048) \
by combining it with the other blocks and bring it to 1. \
Whenever the player makes a move, a new block with the \
value of 3 or 5 will spawn. Any 2 blocks with different \
value can be combined and the new block created will have \
the value of difference of the 2 blocks(eg.5-3=2).'''

    collection = [word.split() for word in text.splitlines()]
    space = rules_font.size(' ')[0]
    xpos,ypos = (20, 20)
    for lines in collection:
        for words in lines:
            word_surface = rules_font.render(words,True,BLACK)
            word_width, word_height = word_surface.get_size()
            if xpos + word_width >= size-10:
                xpos = 20
                ypos += word_height + space
            screen.blit(word_surface,(xpos,ypos))
            xpos += word_width + space
        xpos = 20
        ypos += word_height 

    back = variables.Button(tuple(c["colour"]["light"]["2048"]),
                  220, 360, 65, 55, "BACK")

    while True:

            # set fonts for buttons
            font1 = pygame.font.SysFont(c["font"], 15, bold=True)

            # draw buttons on the screen
            back.draw(screen, BLACK, font1)
        
            pygame.display.update()

            # store mouse position (coordinates)
            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():

                # check if a button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.isOver(pos):
                        return 'back'    
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()                  


def winCheck(board, status, theme, text_col):
    """
    Check game status and display win/lose result.

    Parameters:
        board (list): game board
        status (str): game status
        theme (str): game interface theme
        text_col (tuple): text colour
    Returns:
        board (list): updated game board
        status (str): game status
    """
    if status != "PLAY":
        size = c["size"]
        # Fill the window with a transparent background
        s = pygame.Surface((size, size), pygame.SRCALPHA)
        s.fill(c["colour"][theme]["over"])
        screen.blit(s, (0, 0))

        # Display win/lose status
        if status == "WIN":
            msg = "YOU WIN!"
        else:
            msg = "GAME OVER!"

        screen.blit(my_font.render(msg, 1, text_col), (160, 180))
        # Ask user to play again
        screen.blit(my_font.render(
            "Play again?(Yes/No)", 1, text_col), (80, 255))

        # Create buttons
        YES = variables.Button(tuple(c["colour"]["light"]["2048"]),
                  180, 330, 65, 55, "YES")
        NO = variables.Button(tuple(c["colour"]["light"]["2048"]),
                  280, 330, 65, 55, "NO")    

        pygame.display.update()

        while True:

            # set fonts for buttons
            font1 = pygame.font.SysFont(c["font"], 15, bold=True)

            # draw buttons on the screen
            YES.draw(screen, BLACK, font1)
            NO.draw(screen, BLACK, font1)

            pygame.display.update()

            # store mouse position (coordinates)
            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():

                # check if a button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if YES.isOver(pos):
                        board = newGame(theme, text_col)
                        return (board, "PLAY")

                    if NO.isOver(pos):
                        pygame.quit()
                        sys.exit()

                if event.type == QUIT or \
                        (event.type == pygame.KEYDOWN and event.key == K_n):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == K_y:
                    # 'y' is pressed to start a new game
                    board = newGame(theme, text_col)
                    return (board, "PLAY")
    return (board, status)


def newGame(theme, text_col):
    """
    Start a new game by resetting the board.

    Parameters:
        theme (str): game interface theme
        text_col (tuple): text colour
    Returns:
        board (list): new game board
    """
    # clear the board to start a new game
    board = [[0] * 4 for _ in range(4)]
    display(board, theme)

    screen.blit(my_font.render("NEW GAME!", 1, text_col), (150, 225))
    pygame.display.update()
    # wait for 1 second before starting over
    time.sleep(1)
    variables.number = variables.difficulty
    board = fillTwoOrFour(board, iter=2)
    display(board, theme)
    return board


def restart(board, theme, text_col):
    """
    Ask user to restart the game if 'n' key is pressed.

    Parameters:
        board (list): game board
        theme (str): game interface theme
        text_col (tuple): text colour
    Returns:
        board (list): new game board
    """
    # Fill the window with a transparent background
    s = pygame.Surface((c["size"], c["size"]), pygame.SRCALPHA)
    s.fill(c["colour"][theme]["over"])
    screen.blit(s, (0, 0))

    screen.blit(my_font.render("RESTART? (y / n)", 1, text_col), (85, 225))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == K_n):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == K_y:
                board = newGame(theme, text_col)
                return board


def display(board, theme):
    """
    Display the board 'matrix' on the game window.

    Parameters:
        board (list): game board
        theme (str): game interface theme
    """
    screen.fill(tuple(c["colour"][theme]["background"]))
    box = c["size"] // 4
    padding = c["padding"]
    for i in range(4):
        for j in range(4):
            try:
                colour = tuple(c["colour"][theme][str(board[i][j])])
            except:
                colour = tuple(c["colour"][theme]["exception"])    
            pygame.draw.rect(screen, colour, (j * box + padding,
                                              i * box + padding,
                                              box - 2 * padding,
                                              box - 2 * padding), 0)
            if board[i][j] != 0:
                
                text_colour = tuple(c["colour"][theme]["dark"])
                # display the number at the centre of the tile
                screen.blit(my_font.render("{:>4}".format(
                    board[i][j]), 1, text_colour),
                    # 2.5 and 7.5 were obtained by trial and error
                    (j * box + 2.8 * padding, i * box + 7.5 * padding))
                    
    pygame.display.update()


def playGame(theme, difficulty):
    """
    Main game loop function.

    Parameters:
        theme (str): game interface theme
        difficulty (int): game difficulty, i.e., max. tile to get
    """
    # initialise game status
    status = "PLAY"
    xpos1=0
    ypos1=0
    
    # set text colour according to theme
    if theme == "light":
        text_col = tuple(c["colour"][theme]["dark"])
    else:
        text_col = WHITE
    board = newGame(theme, text_col)

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == pygame.KEYDOWN and event.key in (K_q,K_ESCAPE)):
                # exit if q is pressed
                pygame.quit()
                sys.exit()

            # a key has been pressed
            if event.type == pygame.KEYDOWN:
                # 'r' is pressed to restart the game
                if event.key == pygame.K_r:
                    board = restart(board, theme, text_col)

                if str(event.key) not in c["keys"]:
                    # no direction key was pressed
                    continue
                else:
                    # convert the pressed key to w/a/s/d
                    key = c["keys"][str(event.key)]

                # obtain new board by performing move on old board's copy
                new_board = move(key, deepcopy(board))

                # proceed if change occurs in the board after making move
                if new_board != board:
                    # fill 2/4 after every move
                    board = fillTwoOrFour(new_board)
                    display(board, theme)
                    # update game status
                    status = checkGameStatus(board, difficulty)
                    # check if the game is over
                    (board, status) = winCheck(board, status, theme, text_col)
            
            #touch controls
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    xpos1,ypos1 = pygame.mouse.get_pos()
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    xpos2,ypos2 = pygame.mouse.get_pos()
                    

            
                new_board = swipe(xpos1,xpos2,ypos1,ypos2,deepcopy(board))
                
                if new_board != board:
                    # fill 2/4 after every move
                    board = fillTwoOrFour(new_board)
                    display(board, theme)
                    # update game status
                    status = checkGameStatus(board, difficulty)
                    # check if the game is over
                    (board, status) = winCheck(board, status, theme, text_col)    
