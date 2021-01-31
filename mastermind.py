board = []
options = ['A','B','C','D','E','F','G','H']
code = ['A','A','B','C']
results = []

def player_turn():
    picks = []
    for x in range(4):
        while(True):
            pick = input().capitalize()
            if(pick in options):
                picks.append(pick)
                break
            else:
                print('please enter one of A,B,C,D,E,F,G,H')
    return picks

def check_placement(picks):
    'kijkt welke user picks correct zijn, geeft het terug in een list in het format: [goede_letter_goede_postie,goede_letter]'

    perfect_placement = [] # de index van de correcte letters op de correcte plaats
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
    for i in range(10-len(results)):
        for x in range(4):
            print('-', end = '')
        print('')

    for i in range(len(board),0,-1):
        for x in board[i-1]:
            print(x, end = '')
        print(results[i-1], end='')

        print('')

def check_for_win():

    if([4,0] in results):
        print("You've guessed the code!")
        print(f"The code was: {code}")
        return False
    elif(len(results)==10):
        print_board()
        print("You've lost!")
        return False
    else:
        return True


while(check_for_win()):
    print_board()
    picks = player_turn()
    board.append(picks)
    results.append(check_placement(picks))






