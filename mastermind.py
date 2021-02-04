import random
import time
import itertools
import matplotlib.pyplot as plt

options = ['A', 'B', 'C', 'D', 'E', 'F']
options_string = 'ABCDEF'

user_picks = []
code = []
results = []
possible_combinations = []
rounds = []

for i in itertools.product(options_string, repeat=4):
    possible_combinations.append(list(i))

possible_combinations_copy = possible_combinations.copy()


def generate_code():
    """maak een random code aan"""
    for x in range(4):
        rand = random.randint(0, len(options) - 1)
        code.append(options[rand])


def player_turn():
    """returnt de code die de gebruiker wilt gokken"""
    while True:
        pick = input().upper()

        picks = (list(pick))
        pick_count = 0
        for pick in picks:
            if pick in options:
                pick_count += 1
        if pick_count == 4:
            break
        else:
            print(f'Please enter 4 of the following in a row: {options}')

    return picks


def check_placement(picks, code):
    """kijkt welke user picks correct zijn, geef feedback terug in een list in het format:
        [goede_letter_goede_postie,goede_letter_verkeerde_positie]

              Args:
                  picks: de gekozen gok
                  code: de code waarme de gok wordt vergeleken
          """

    perfect_placement = []  # de index van de correcte letters op de correcte plaats
    # heb index nodig voor een list.pop later

    good_placement = []  # de correcte overige letters op de verkeerde plaats, geen index nodig
    picks_copy = picks.copy()
    code_copy = code.copy()

    for x in range(len(picks)):
        if picks[x] == code[x]:
            perfect_placement.append(x)

    for x in range(len(perfect_placement)):
        picks_copy.pop(perfect_placement[x] - x)
        code_copy.pop(perfect_placement[x] - x)

    for pick in picks_copy:
        if pick in code_copy:
            good_placement.append(pick)
            code_copy.remove(pick)

    result = [len(perfect_placement), len(good_placement)]
    return result


def print_board():
    """print hoeveel pogingen je nog hebt, je feedback, en je gokgeschiedenis in de vorm van een bord"""

    for i in range(10 - len(results)):
        for x in range(4):
            print('-', end='')
        print('')

    for i in range(len(user_picks), 0, -1):
        for x in user_picks[i - 1]:
            print(x, end='')
        print(results[i - 1], end='')

        print('')


def check_for_end(round_number, prints):
    """kijkt of een van de eindcondities bereikt is

           Args:
               prints: of het speelbord wel of niet geprint moet worden
               round_number: wat de huidige ronde in het spel is
       """

    if [4, 0] in results:
        if prints:
            print_board()
            print(f"round: {round_number}")
            print("You've guessed the code!")
            print(f"The code was: {code}")
        rounds.append(round_number)
        return False
    elif len(results) == 10:
        print_board()
        print("You've lost!")
        print(f"The code was: {code}")
        return False
    else:
        return True


def player_vs_computer():
    'een volledig speler vs computer spel'

    round_number = 0
    generate_code()
    while (check_for_end(round_number, True)):
        round_number += 1
        print_board()
        picks = player_turn()
        user_picks.append(picks)
        results.append(check_placement(picks, code))


# --------------------------------------------------------------------------------------------------------------
def pick_random_guess():
    'returnt een random guess uit de lijst van mogelijke opties'
    rand = random.randint(0, len(possible_combinations_copy) - 1)
    guess = possible_combinations_copy[rand]
    possible_combinations_copy.remove(guess)

    return guess


def computer_turn_heuristic(round_number):
    """dit algorithme elimineert 'onmogelijke gokken' uit een lijst van mogelijke gokken op verschillende manieren'

                    Args:
                       round_number: wat de huidige ronde in het spel is
            """
    global possible_combinations_copy

    # eerste gok is random
    if (round_number == 1):
        rand = random.randint(0, len(possible_combinations_copy) - 1)
        first_pick = possible_combinations[rand]
        possible_combinations_copy.remove(first_pick)

        return first_pick

    else:
        previous_result = results[round_number - 2]
        previous_user_pick = user_picks[round_number - 2]

        carry_over = previous_result[0] + previous_result[1]

        # als geen van de gegokte getallen voorkomen in de code delete dan alle opties met die getallen
        if (previous_result[1] == 0 and previous_result[0] == 0):
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
            if counter == (4 - previous_result[0]):
                temp_list.append(i)
        possible_combinations_copy = temp_list

        # [x,y] x+y = z, split de 4 gokken van de speler in een lijst van lijsten z groot, delete alle opties waar niet tenminste 1 sublijst in voorkomt

        if (4 > carry_over > 0):
            temp_list = []
            previous_user_pick_string = ''
            for x in previous_user_pick:
                previous_user_pick_string += x

            sub_possible_combinations = []
            for i in itertools.combinations(previous_user_pick_string, previous_result[0] + previous_result[1]):
                sub_possible_combinations.append(list(i))

            for i in possible_combinations_copy:
                count = 0
                for x in sub_possible_combinations:
                    count2 = 0
                    for j in x:
                        if j in i:
                            count2 += 1
                    if (count2 == len(x)):
                        count += 1
                if (count > 0):
                    temp_list.append(i)

            possible_combinations_copy = temp_list

        # als alle letters in de code voorkomen maar nog niet op de goede plek staan, delete dan alle andere opties
        if (previous_result[0] + previous_result[1] == 4):
            temp_list = []
            for i in range(0, len(possible_combinations_copy)):
                count = 0
                for x in previous_user_pick:
                    if (previous_user_pick.count(x) == possible_combinations_copy[i].count(x)):
                        count += 1
                if count == 4:
                    temp_list.append(possible_combinations_copy[i])

            possible_combinations_copy = temp_list

        # van de 4 letters in een gok met [x,y] x+y=z, mogen er in de volgende gok nooit meer dan z van de 4 letters voorkomen.
        temp_list = []
        if (len(possible_combinations_copy) > 1):
            if ((carry_over == 1 or carry_over == 2 or carry_over == 3) and len(set(previous_user_pick)) > 2):

                previous_user_pick_copy = previous_user_pick.copy()
                for x in previous_user_pick_copy:
                    if (previous_user_pick.count(x) > 1):
                        previous_user_pick_copy.remove(x)

                for i in possible_combinations_copy:
                    count = 0
                    if (len(set(i)) == 4):
                        for x in previous_user_pick_copy:
                            if (x in i):
                                count += 1
                    if (count <= carry_over):
                        temp_list.append(i)
                possible_combinations_copy = temp_list

        return pick_random_guess()


def core_simple_algorithm(round_number):
    """kijk voor elke resterende gok in possible_options_copy welke gokkken consistent zijn met voorgaande gokken, pas de lijst met mogelijke gokken aan'

                    Args:
                       round_number: wat de huidige ronde in het spel is
            """


    global possible_combinations_copy
    previous_result = results[round_number - 2]
    previous_user_pick = user_picks[round_number - 2]

    temp_list = []
    for i in possible_combinations_copy:
        if (check_placement(i, previous_user_pick)) == previous_result:
            temp_list.append(i)
        possible_combinations_copy = temp_list


def computer_turn_simple(round_number):
    """start de eerste gok met [AABB] in ronde 1, pak daarna een random gok uit de lijst met mogelijke gokken'

                 Args:
                    round_number: wat de huidige ronde in het spel is
         """
    global possible_combinations_copy

    if (round_number == 1):
        return ['A', 'A', 'B', 'B']
    else:
        core_simple_algorithm(round_number)

        return pick_random_guess()


def computer_turn_ahead(round_number):
    """kijkt voor elke resterende gok welke gok de meest waardevolle feedback geeft (het grootste aantal [x,y] combinaties)'

               Args:
                  round_number: wat de huidige ronde in het spel is
       """
    global possible_combinations_copy

    if (round_number == 1):
        return ['A', 'A', 'B', 'B']
    else:
        core_simple_algorithm(round_number)

        feedback_length_list = []
        highest = 0
        for i in possible_combinations_copy:
            feedback_list = []
            possible_feedback = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2],
                                 [3, 0]]

            for j in possible_combinations_copy:
                feedback = check_placement(j, i)

                if (feedback in possible_feedback):
                    feedback_list.append(feedback)
                    possible_feedback.remove(feedback)

                    # als de feedback list 12/12 lang is betekent dat dat het een optimale gok is, je hoeft daarna dus niet verder te kijken
                    # dit versnelt het algorithme enorm
                    if (len(feedback_list) == 12):
                        guess = i
                        possible_combinations_copy.remove(guess)
                        return guess

            if (len(feedback_list) >= highest):
                feedback_length_list.append([len(feedback_list), i])
                highest = len(feedback_list)

        possible_guesses = []
        for i in feedback_length_list:
            if int(i[0]) == max(feedback_length_list)[0]:
                possible_guesses.append(i[1])

        guess = possible_guesses[random.randint(0, len(possible_guesses) - 1)]
        possible_combinations_copy.remove(guess)

    return guess


def computer_vs_computer(prints, mode, sleep):
    """een volledig computer vs computer spel

        Args:
            prints: of het speelbord wel of niet geprint moet worden
            mode: het soort algorithme dat de bot gebruikt
            sleep: de tijd de bot wacht tussen turns
    """
    picks = user_picks
    generate_code()
    round_number = 0
    while (check_for_end(round_number, prints)):
        round_number += 1
        if (prints):
            print_board()
            print()
        if (mode == 'ahead'):
            picks = computer_turn_ahead(round_number)
        if (mode == 'heuristic'):
            picks = computer_turn_heuristic(round_number)
        if (mode == 'simple'):
            picks = computer_turn_simple(round_number)
        user_picks.append(picks)
        results.append(check_placement(picks, code))
        time.sleep(sleep)
    reset()


def reset():
    'gebruik geen classes/constructor dus moet mijn lists resetten'
    global code
    global user_picks
    global results
    global possible_combinations_copy
    global possible_combinations
    global previous_user_pick
    previous_user_pick = []
    user_picks = []
    results = []
    possible_combinations_copy = possible_combinations.copy()
    code = []


def reset_rounds():
    'resets the list that tracks the rounds'
    global rounds
    rounds = []


def get_avg(limit, mode):
    """ geeft terug wat de gemiddelde ronde-duur is van elk spel, maakt ook een grafiek'

            Args:
                limit: hoe vaak je een volledige game rotatie aanroept voordat je het gemiddelde berekent
                mode: van welk bot algorithme het gemiddelde moet worden berekend

    """
    reset()
    for x in range(limit):
        computer_vs_computer(False, mode,0)

    print(f'avg rounds before win: {sum(rounds) / limit} {mode}')

    round_catagories = list(set(rounds))
    round_catagories_freq = []

    for x in round_catagories:
        round_catagories_freq.append(rounds.count(x))

    height = round_catagories_freq
    bars = round_catagories

    plt.title(f'Frequency of rounds played untill win | "{mode}"', loc='left')
    plt.title(f'avg: {sum(rounds) / limit}', loc='right')
    plt.bar(bars, height)
    plt.ylabel('frequency')
    plt.xlabel('rounds')
    plt.xticks(bars)
    plt.show()
    plt.close()
    reset_rounds()


def play_game():
    mode_choices = ['computer vs computer', 'player vs computer']

    while(True):
        user_input = input("Do you want to play 'computer vs computer' or 'player vs computer'\n")
        if(user_input in mode_choices):
            break
    if(user_input == 'computer vs computer'):
        computer_mode_choices = ['heuristic','simple','ahead']
        while(True):
            user_input = input("pick computer mode: 'heuristic','simple,'ahead'\n")
            if(user_input in computer_mode_choices):
                break
        computer_vs_computer(True, user_input,1)

    elif(user_input == 'player vs computer'):

        player_vs_computer()


# ---------------------------------------------------------------------------------------------------------------------
get_avg(500,'ahead')

play_game()
#computer_vs_computer(True, 'simple')

# speel tegen de computer
# player_vs_computer()

# computer speelt tegen de computer
# computer_vs_computer(True,'simple')
# computer_vs_computer(True,'heuristic')
# computer_vs_computer(True,'ahead')
