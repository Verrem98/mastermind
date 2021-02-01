import random
import time
import itertools
from itertools import product



user_picks = []
options = ['A','B','C','D','E','F']
options_string = 'ABCDEF'
code = []
results = []
possible_combinations = []
rounds = []


for i in product(options_string, repeat=4):
    possible_combinations.append(list(i))

possible_combinations_copy = possible_combinations.copy()

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

    for i in range(len(user_picks), 0, -1):
        for x in user_picks[i - 1]:
            print(x, end = '')
        print(results[i-1], end='')

        print('')

def check_for_end(round_number):
    'kijkt of de eindconditie bereikt is'

    if([4,0] in results):
        print_board()
        print(f"round: {round_number}")
        print("You've guessed the code!")
        print(f"The code was: {code}")
        rounds.append(round_number)
        return False
    elif(len(results)==1000):
        print_board()
        print("You've lost!")
        print(f"The code was: {code}")
        return False
    else:
        return True

def reset():
    results = []
    possible_combinations_copy = possible_combinations.copy()
    user_picks = []


def player_vs_computer():
    'gameplayloop voor speler tegen computer'
    generate_code()
    while(check_for_end()):
        print_board()
        picks = player_turn()
        user_picks.append(picks)
        results.append(check_placement(picks))

#--------------------------------------------------------------------------------------------------------------

def computer_turn_random():
    picks = []
    for x in range(4):
        rand = random.randint(0, len(options) - 1)
        picks.append(options[rand])
    return picks


def computer_turn_simple(round_number):
    global possible_combinations_copy

    if(round_number==1):
        rand = random.randint(0, len(possible_combinations_copy) - 1)
        first_pick = possible_combinations[rand]
        possible_combinations_copy.remove(first_pick)

        return first_pick

    else:
        previous_result = results[round_number-2]
        previous_user_pick = user_picks[round_number-2]


        # als geen van de gegokte getallen voorkomen in de code delete dat x/6e van de opties
        if(previous_result[1] == 0 and previous_result[0] == 0):
            for x in set(previous_user_pick):
                for i in possible_combinations:
                    if x in i:
                        try:
                            possible_combinations_copy.remove(i)
                        except ValueError:
                            pass

        temp_list = []
        # als de feedback [0,x] is dan betekent dat dat je voor elke letter zeker weet dat ze niet in de huidige postie horen, ik elimneer hier die opties
        for i in possible_combinations_copy:
            counter = 0
            for x in range(len(previous_user_pick)):
                if (previous_user_pick[x] != i[x]):
                    counter += 1
            if counter == (4-previous_result[0]):
                temp_list.append(i)
        possible_combinations_copy = temp_list



        #als alle letters hetzelfde zijn en er komt er tenminste één van voor in de code, delete dan alle opties zonder die letter
        if(len(set(previous_user_pick))==1):
            if(previous_result[0]>=1):
                for i in possible_combinations:
                    if(previous_user_pick[0] not in i):
                        try:
                            possible_combinations_copy.remove(i)
                        except ValueError:
                            pass



        #als alle letters in de code voorkomen maar nog niet op de goede plek staan, delete dan alle andere opties
        if(previous_result[0] + previous_result[1] == 4):
            temp_list = []
            for i in range(0, len(possible_combinations_copy)):
                count = 0
                for x in previous_user_pick:
                    if (previous_user_pick.count(x) == possible_combinations_copy[i].count(x)):
                        count += 1
                if count == 4:
                    temp_list.append(possible_combinations_copy[i])

            possible_combinations_copy = temp_list

        rand = random.randint(0, len(possible_combinations_copy) - 1)
        guess = possible_combinations_copy[rand]
        possible_combinations_copy.remove(guess)


        return guess

def computer_vs_computer():

    generate_code()
    round_number = 0
    while (check_for_end(round_number)):
        round_number += 1
        print_board()
        print()
        picks = computer_turn_simple(round_number)
        user_picks.append(picks)
        results.append(check_placement(picks))
        time.sleep(0)
    reset()

def reset():
    global code
    global user_picks
    global results
    global possible_combinations_copy
    global possible_combinations
    user_picks = []
    results = []
    possible_combinations_copy = possible_combinations.copy()
    code = []




computer_vs_computer()























