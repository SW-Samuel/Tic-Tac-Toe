import PySimpleGUI as sg
import random 
import os

#global variables
game = [
    [" "," "," "],
    [" "," "," "],
    [" "," "," "]
]
Plays = 0
PlayAgain = "s"
Who_is_play = 1      #1-Player   2-Cpu
play_limit = 9
win = "n"

#building the name windows
def name_screen():
    sg.theme('Dark')
    layout=[
        [sg.Text('Jogo da velha')],
        [sg.Text('Nome:'),sg.Input(key = 'name')],
        [sg.Button('Continuar')]
    ]
    return sg.Window('Login', layout = layout, finalize=True)

#building the game windows
def game_screen():
    sg.theme('Dark')
    layout = [
        [sg.Text('Jogo da Velha')],
        [sg.Text('Coluna:'),sg.Input(key = 'colunm',size = (10,1))],
        [sg.Text('Linha:'),sg.Input(key = 'line',size = (10,1))],
        [sg.Button('Play')],
        [sg.Output(size = (30,20), key = '___output___')]
    ]
    return sg.Window('Game', layout = layout, finalize = True)

#building the final windows
def f_screem():
    sg.theme('Dark')
    layout = [
        [sg.Text('Fim de jogo')],
        [sg.Text('Deseja jogar novamente?')],
        [sg.Button('sim'),sg.Button('nao')],
        [sg.Output()]
    ]
    return sg.Window('Fim', layout = layout, finalize = True)

#initializing the windows
windowsOne, windowsTwo, windowsThree = name_screen(), None, None

def player(l,c):
    global Plays
    global Who_is_play
    play_limit

    l=int(l)
    c=int(c)

    if Who_is_play == 1 and Plays < play_limit and game[l][c] == " ":
        game[l][c] = "X"
        Who_is_play = 2
        Plays+=1
    else:
        sg.popup('Valores inválidos')

#function to make the cpu movements and check if it is already filled
def cpu_move():
    global Plays
    global Who_is_play
    play_limit
    if Who_is_play == 2 and Plays < play_limit:
        l = random.randrange(0,3)
        c = random.randrange(0,3)
        while game[l][c] != " ":
            l = random.randrange(0,3)
            c = random.randrange(0,3)
        game[l][c] = "O"
        Plays+=1
        Who_is_play = 1

#function to print the table on the screen
def print_screem():
    global game
    windowsTwo.FindElement('___output___').Update('')
    print(f'Nome: {name}')
    print(f'')
    print(f'          0   |     1    |     2     ')
    print(f'0 :     {game[0][0]}     |     {game[0][1]}     |     {game[0][2]}')
    print("       ---------------------------------")
    print(f'1 :     {game[1][0]}     |     {game[1][1]}     |     {game[1][2]}')
    print("       ---------------------------------")
    print(f'2 :     {game[2][0]}     |     {game[2][1]}     |     {game[2][2]}')
    print(f'Jogadas: {Plays}')

#check the champion
def winner():
    global game
    champion = "n"
    symbols = ["X", "O"]
    for s in symbols:
        champion="n"

        #check the line
        il=ic=0
        while il < 3:
            soma=0
            ic=0
            while ic < 3:
                if(game[il][ic] == s):
                    soma +=1
                ic+=1
            if(soma == 3):
                champion = s
                break
            il+=1
        if(champion != "n"):
            break
        
        #check the columns
        il=ic=0
        while ic < 3:
            soma=0
            il=0
            while il < 3:
                if(game[il][ic] == s):
                    soma +=1
                il+=1
            ic+=1
            if(soma == 3):
                champion = s
                break
        if(champion != "n"):
            break

        #checks the main diagonal
        soma = 0
        diagonal_index = 0
        while diagonal_index < 3:
            if(game[diagonal_index][diagonal_index] == s):
                soma +=1
            diagonal_index+=1        
        if(soma == 3):
            champion = s
            break

        #checks the secondary diagonal
        soma = 0
        diagonal_index_line = 0
        diagonal_index_column = 2
        while diagonal_index_column >= 0:
            if(game[diagonal_index_line][diagonal_index_column] == s):
                soma +=1
            diagonal_index_line += 1
            diagonal_index_column -= 1        
        if(soma == 3):
            champion = s
            break
    return champion

#the function reset the varieble
def reset():
    global PlayAgain
    global Plays
    global Who_is_play
    global play_limit
    global win
    global game 
    PlayAgain = "s"
    Plays = 0
    Who_is_play = 1
    play_limit = 9
    win = "n"
    game =[
        [" "," "," "],
        [" "," "," "],
        [" "," "," "]
    ]

#loop for the program
while(PlayAgain == 's'):

    while(True):

        windows, event, values = sg.read_all_windows()

        #when the window is closed
        if windows == windowsOne and event == sg.WIN_CLOSED:
            break

        if windows == windowsTwo and event == sg.WIN_CLOSED:
            break
    
        if windows == windowsThree and event == sg.WIN_CLOSED:
            break
    
        # Calling the next screen
        if windows == windowsOne and event == 'Continuar':
            name = values['name']
            windowsTwo = game_screen()
            print_screem()
            windowsOne.hide()

        if windows == windowsTwo and event == 'Play':

            # Monitoring the inputs to see if they are empty
            if values['colunm'] != None and values['line'] != None:
                colunm = values['colunm']
                line = values['line']
            
                #player move
                player(line,colunm)
            
                #cpu move
                cpu_move()
                print_screem()

                win = winner()
                if win != "n" or Plays>=play_limit:
                    windowsThree = f_screem()
                    windowsTwo.hide()
                    break
            else:
                #in case there is an empty input (column or row)
                sg.popup('Não há valores para linha ou coluna')


    #finish message
    if win == "X" or win == "O":
        print(f"Resultado: Jogador {win} venceu")
    
    if Plays>=play_limit:
        print(f"Deu velha")

    windows, event, values = sg.read_all_windows()

    if windows == windowsThree and event == 'sim':
        PlayAgain = 's'
        reset()

        windowsTwo = game_screen()
        print_screem()
        windowsThree.hide()
        
    if windows == windowsThree and event == 'nao':
        PlayAgain = 'n'
        break

    #when the window is closed
    if windows == windowsOne and event == sg.WIN_CLOSED:
        break

    if windows == windowsTwo and event == sg.WIN_CLOSED:
        break
    
    if windows == windowsThree and event == sg.WIN_CLOSED:
        break