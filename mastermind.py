import random

board = []
options = ['A','B','C','D','E','F','G','H']
code = []
results = []

def generate_code():
    for x in range(4):
        rand = random.randint(0, len(options)-1)
        code.append(options[rand])

def player_turn():
    while(True):
            pick = input().upper()

            picks = (list(pick))
            pick_count = 0
            for pick in picks:
                if pick in options:
                    pick_count+=1
            if pick_count == 4:
                break
            else:
                print(f'Please enter 4 of the following in a row: {options}')

    return picks

def check_placement(picks):
    'kijkt welke user picks correct zijn, geeft het terug in een list in het format: [goede_letter_goede_postie,goede_letter]'

    perfect_placement = [] # de index van de correcte letters op de correcte plaats, heb index nodig voor een list.pop later
    good_placement = [] # de correcte overige letters op de verkeerde plaats, geen index nodig
    picks_copy = picks.copy()
    code_copy = code.copy()

    for x in range(len(picks)):
        if picks[x] == code[x]:
            perfect_placement.append(x)

    for x in range(len(perfect_placement)):
        picks_copy.pop(perfect_placement[x]-x)
        code_copy.pop(perfect_placement[x]-x)

    for pick in picks_copy:
        if(pick in code_copy):
            good_placement.append(pick)
            code_copy.remove(pick)

    result = [len(perfect_placement),len(good_placement)]
    return result

def print_board():
    'print hoeveel pogingen je nog hebt en je gokgeschiedenis'
    for i in range(10-len(results)):
        for x in range(4):
            print('-', end = '')
        print('')

    for i in range(len(board),0,-1):
        for x in board[i-1]:
            print(x, end = '')
        print(results[i-1], end='')

        print('')

def check_for_end():
    'kijkt of de eindconditie bereikt is'

    if([4,0] in results):
        print("You've guessed the code!")
        print(f"The code was: {code}")
        return False
    elif(len(results)==10):
        print_board()
        print("You've lost!")
        print(f"The code was: {code}")
        return False
    else:
        return True


def player_vs_computer():
    'gameplayloop voor speler tegen computer'
    generate_code()
    while(check_for_end()):
        print_board()
        picks = player_turn()
        board.append(picks)
        results.append(check_placement(picks))



player_vs_computer()