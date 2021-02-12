import random
import time
import itertools
import matplotlib.pyplot as plt

# variabelen die ik in meerdere van mijn functies gebruik/aanpas
user_picks = []
code = []
results = []
rounds = []

# 65-71 is A-F in ASCII
options = [chr(x) for x in range(65, 71)]

possible_combinations_static = [list(z) for z in itertools.product('ABCDEF', repeat=4)]
possible_combinations_mutable = possible_combinations_static.copy()


def generate_start_option():
    """maakt de eerste gok aan, een combinatie van [x,x,y,y] waar x en y, A t/m F kunnen zijn"""

    #  Als ik alleen maar met AABB start dan lost die,bijvoorbeeld, code CCCC altijd binnen
    #  x aantal moves op, door ook andere begin gokken toe te voegen wordt daar varandering
    # in aangebracht wat voor een beter gemiddelde zorgt.

    rand1 = 0
    rand2 = 0
    while rand1 == rand2:
        rand1 = random.randint(0, len(options)-1)
        rand2 = random.randint(0, len(options)-1)

    return [options[rand1], options[rand1], options[rand2], options[rand2]]


def generate_code():
    """maak een random code aan"""

    global code

    code = [options[random.randint(0, len(options) - 1)] for _ in range(4)]


def get_player_input():
    """returnt de code die de gebruiker wilt gokken"""

    while True:
        print('Please enter your code')
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


def check_placement(picks, local_code):
    """kijkt welke user picks correct zijn, geef feedback terug in een list in het format:
    [goede_letter_goede_postie,goede_letter_verkeerde_positie]

              Args:
                  picks: de gekozen gok
                  local_code: de code waarme de gok wordt vergeleken
          """
    # de correcte overige letters op de verkeerde plaats, geen index nodig
    good_placement = []
    # de index van de correcte letters op de correcte plaats
    perfect_placement = [x for x in range(len(picks)) if picks[x] == local_code[x]]

    picks_copy = picks.copy()
    code_copy = local_code.copy()

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

    for _ in range(10 - len(results)):
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
    """een volledig speler vs computer spel"""

    round_number = 0
    generate_code()
    while check_for_end(round_number, True):
        round_number += 1
        print_board()
        picks = get_player_input()
        user_picks.append(picks)
        results.append(check_placement(picks, code))


def pick_random_guess():
    """returnt een random guess uit de lijst van mogelijke opties"""

    rand = random.randint(0, len(possible_combinations_mutable) - 1)
    guess = possible_combinations_mutable[rand]
    possible_combinations_mutable.remove(guess)

    return guess


# =================================================================================================================
# 5 Verschillende algoritmes:
# =================================================================================================================


def computer_turn_heuristic(round_number):
    """dit algorithme elimineert 'onmogelijke gokken' uit een lijst van mogelijke gokken op verschillende manieren'

                    Args:
                       round_number: wat de huidige ronde in het spel is
            """
    global possible_combinations_mutable

    # eerste gok is random
    if round_number == 1:
        rand = random.randint(0, len(possible_combinations_mutable) - 1)
        first_pick = possible_combinations_static[rand]
        possible_combinations_mutable.remove(first_pick)

        return first_pick

    else:
        previous_result = results[round_number - 2]
        previous_user_pick = user_picks[round_number - 2]

        carry_over = previous_result[0] + previous_result[1]

        # als geen van de gegokte getallen voorkomen in de code delete dan alle opties met die getallen
        if previous_result[1] == 0 and previous_result[0] == 0:
            for x in set(previous_user_pick):
                for i in possible_combinations_static:
                    if x in i:
                        try:
                            possible_combinations_mutable.remove(i)
                        except ValueError:
                            pass

        temp_list = []

        # als de feedback [0,x] is dan betekent dat dat je voor elke letter zeker weet
        # dat ze niet in de huidige postie horen,
        # ik elimneer hier die opties
        for i in possible_combinations_mutable:
            counter = 0
            for x in range(len(previous_user_pick)):
                if previous_user_pick[x] != i[x]:
                    counter += 1
            if counter == (4 - previous_result[0]):
                temp_list.append(i)
        possible_combinations_mutable = temp_list

        # [x,y] x+y = z, split de 4 gokken van de speler in een lijst van lijsten z groot,
        # delete alle opties waar niet tenminste 1 sublijst in voorkomt

        if 4 > carry_over > 0:
            temp_list = []
            previous_user_pick_string = ''
            for x in previous_user_pick:
                previous_user_pick_string += x

            sub_possible_combinations = [i for i in itertools.combinations(previous_user_pick_string,
                                                                           previous_result[0] + previous_result[1])]

            for i in possible_combinations_mutable:
                count = 0
                for x in sub_possible_combinations:
                    count2 = 0
                    for j in x:
                        if j in i:
                            count2 += 1
                    if count2 == len(x):
                        count += 1
                if count > 0:
                    temp_list.append(i)

            possible_combinations_mutable = temp_list

        # als alle letters in de code voorkomen maar nog niet op de goede plek staan, delete dan alle andere opties
        if previous_result[0] + previous_result[1] == 4:
            temp_list = []
            for i in range(0, len(possible_combinations_mutable)):
                count = 0
                for x in previous_user_pick:
                    if previous_user_pick.count(x) == possible_combinations_mutable[i].count(x):
                        count += 1
                if count == 4:
                    temp_list.append(possible_combinations_mutable[i])

            possible_combinations_mutable = temp_list

        # van de 4 letters in een gok met [x,y]: x+y=z,
        # mogen er in de volgende gok nooit meer dan z van de 4 letters voorkomen.
        temp_list = []
        if len(possible_combinations_mutable) > 1:
            if (carry_over == 1 or carry_over == 2 or carry_over == 3) and len(set(previous_user_pick)) > 2:

                previous_user_pick_copy = previous_user_pick.copy()
                for x in previous_user_pick_copy:
                    if previous_user_pick.count(x) > 1:
                        previous_user_pick_copy.remove(x)

                for i in possible_combinations_mutable:
                    count = 0
                    if len(set(i)) == 4:
                        for x in previous_user_pick_copy:
                            if x in i:
                                count += 1
                    if count <= carry_over:
                        temp_list.append(i)
                possible_combinations_mutable = temp_list

        return pick_random_guess()


def core_simple_algorithm(round_number):
    """kijk voor elke resterende gok in possible_options_mutable welke gokkken consistent zijn met voorgaande gokken,
    pas de lijst met mogelijke gokken aan'

    gebaseerd op 2.1 in het artikel van de Universiteit van Groningen


                    Args:
                       round_number: wat de huidige ronde in het spel is
            """

    global possible_combinations_mutable
    previous_result = results[round_number - 2]
    previous_user_pick = user_picks[round_number - 2]

    temp_list = []
    for i in possible_combinations_mutable:
        if (check_placement(i, previous_user_pick)) == previous_result:
            temp_list.append(i)
    possible_combinations_mutable = temp_list


def computer_turn_simple(round_number):
    """start de eerste gok met [AABB],[CCDD] of [EEFF] in ronde 1,
     pak daarna een random gok uit de lijst met mogelijke gokken.

     gebaseerd op 2.1 (A Simple Strategy )in het artikel van de Universiteit van Groningen

                 Args:
                    round_number: wat de huidige ronde in het spel is
         """
    global possible_combinations_mutable

    if round_number == 1:
        return generate_start_option()
    else:
        core_simple_algorithm(round_number)

        return possible_combinations_mutable[0]


def computer_turn_ahead(round_number):
    """kijkt voor elke resterende gok welke gok het grootste aantal [x,y] combinaties aan mogelijke feedback kan geven

    dit was een 'misinterpetatie' van 2.2 in het artikel van de Universiteit van Groningen,
    maar werkt het beste van alle algoritmen
    die ik heb geïmplementeerd (relatief snel met het laagste aantal gemiddelde vragen voor een win).
    
               Args:
                  round_number: wat de huidige ronde in het spel is
       """
    global possible_combinations_mutable

    if round_number == 1:
        return generate_start_option()
    else:
        core_simple_algorithm(round_number)

        feedback_length_list = []
        highest = 0
        for i in possible_combinations_mutable:
            feedback_list = []

            # deze possible_feedback staat binnen de loop omdat het aangepast wordt en dan gereset moet worden
            possible_feedback = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2],
                                 [3, 0]]

            for j in possible_combinations_mutable:
                feedback = check_placement(j, i)

                if feedback in possible_feedback:
                    feedback_list.append(feedback)
                    possible_feedback.remove(feedback)

                    # als de feedback list 12/12 lang is betekent dat dat het een optimale gok is,
                    # je hoeft daarna dus niet verder te kijken
                    # dit versnelt het algorithme enorm

                    if len(feedback_list) == 12:
                        guess = i
                        possible_combinations_mutable.remove(guess)
                        return guess

            if len(feedback_list) >= highest:
                feedback_length_list.append([len(feedback_list), i])
                highest = len(feedback_list)

        possible_guesses = []
        for i in feedback_length_list:
            if int(i[0]) == max(feedback_length_list)[0]:
                possible_guesses.append(i[1])

        guess = possible_guesses[random.randint(0, len(possible_guesses) - 1)]
        possible_combinations_mutable.remove(guess)

    return guess


def computer_turn_worst_case(round_number):
    """kijk voor elke resterende gok welke gok de minst slechte worst case heeft'

    gebaseerd op 2.3(A Worst Case Strategy) in het artikel van de Universiteit van Groningen


               Args:
                  round_number: wat de huidige ronde in het spel is
       """
    global possible_combinations_mutable

    if round_number == 1:
        return generate_start_option()
    else:
        core_simple_algorithm(round_number)

        possible_feedback = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2],
                             [3, 0]]

        feedback_max_list = []
        for i in possible_combinations_mutable:
            feedback_list = []

            for j in possible_combinations_mutable:
                feedback = check_placement(j, i)
                feedback_list.append(feedback)

            possible_feedback_count = []
            for x in possible_feedback:
                possible_feedback_count.append(feedback_list.count(x))

            feedback_max_list.append([max(possible_feedback_count), i])

        final_guess_list = [i[1] for i in feedback_max_list if i[0] == min(feedback_max_list)[0]]

        guess = final_guess_list[random.randint(0, len(final_guess_list) - 1)]
        possible_combinations_mutable.remove(guess)

    return guess


def computer_turn_expected(round_number):
    """kijk voor elke resterende gok welke gok de laagste verwachtingswaarde heeft'

    gebaseerd op 2.4(An Expected Size Strategy) in het artikel van de Universiteit van Groningen


               Args:
                  round_number: wat de huidige ronde in het spel is
       """
    global possible_combinations_mutable

    if round_number == 1:
        return generate_start_option()
    else:
        core_simple_algorithm(round_number)
        expected_value_for_codes = []
        possible_feedback = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2],
                             [3, 0], [4, 0]]

        for i in possible_combinations_mutable:
            feedback_list = []

            for x in possible_combinations_mutable:
                feedback = check_placement(x, i)
                feedback_list.append(feedback)

            possible_feedback_count = []
            for x in possible_feedback:
                possible_feedback_count.append(feedback_list.count(x))

            expected_value = 0
            for x in possible_feedback_count:
                expected_value += x ** 2 / (sum(possible_feedback_count))
            expected_value_for_codes.append([expected_value, i])

        guess = (min(expected_value_for_codes)[1])
        possible_combinations_mutable.remove(guess)

    return guess


# =================================================================================================================

# =================================================================================================================

def computer_vs_computer(prints, mode, sleep, code_generate):
    """een volledig computer vs computer spel

        Args:

            prints: of het speelbord wel of niet geprint moet worden
            mode: het soort algorithme dat de bot gebruikt
            sleep: de tijd(s) de bot wacht tussen turns
            code_generate: of er wel of niet een code gegenereerd moet worden
    """

    picks = user_picks

    if code_generate:
        generate_code()
    round_number = 0
    while check_for_end(round_number, prints):
        round_number += 1
        if prints:
            print_board()
            print()
        if mode == 'ahead':
            picks = computer_turn_ahead(round_number)
        if mode == 'heuristic':
            picks = computer_turn_heuristic(round_number)
        if mode == 'simple':
            picks = computer_turn_simple(round_number)
        if mode == 'worst_case':
            picks = computer_turn_worst_case(round_number)
        if mode == 'expected':
            picks = computer_turn_expected(round_number)

        user_picks.append(picks)
        results.append(check_placement(picks, code))
        time.sleep(sleep)
    reset()


def reset():
    """gebruik geen classes/constructor dus moet mijn lists resetten"""

    global code
    global user_picks
    global results
    global possible_combinations_mutable
    global possible_combinations_static
    user_picks = []
    results = []
    possible_combinations_mutable = possible_combinations_static.copy()
    code = []


def reset_rounds():
    """resets the list that tracks the rounds"""

    global rounds
    rounds = []


def get_avg(limit, mode, save):
    """ geeft terug wat de gemiddelde ronde-duur is van elk spel, maakt ook een grafiek'

            Args:
                limit: hoe vaak je een volledige spel aanroept
                mode: van welk bot algorithme het gemiddelde moet worden berekend
                save: boolean, of je de image op wilt slaan of niet

    """
    reset()
    for _ in range(limit):
        computer_vs_computer(False, mode, 0, True)

    print(f'avg guesses before win: {sum(rounds) / limit} {mode}')

    round_catagories = list(set(rounds))

    round_catagories_freq = [rounds.count(x) for x in round_catagories]

    height = round_catagories_freq
    bars = round_catagories

    label_color = '#52575e'
    fig, ax = plt.subplots()
    fig.tight_layout()
    plt.title(f'Number of guesses until win | "{mode}"', loc='left', color=label_color)
    plt.title(f'avg: {sum(rounds) / limit}', loc='right', color=label_color)
    plt.bar(bars, height)
    plt.ylabel('Frequency', color=label_color)
    plt.xlabel('Guesses', color=label_color)
    plt.xticks(bars)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#c5cad1')
    ax.xaxis.grid(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#c5cad1')

    plt.show()
    if save:
        fig.savefig(f"efficiency charts/{mode}-algorithm_chart.png")
    plt.close()
    reset_rounds()


def save_efficiency_charts(limit):
    """maakt een efficiëntie chart voor elk algoritme en slaat deze op

            Args:
                limit: hoe vaak je een volledig spel aanroept
    """

    algorithms = ['heuristic', 'simple', 'ahead', 'worst_case', 'expected']

    for x in algorithms:
        get_avg(limit, x, True)


def play_game():
    """toont het gamemode selectie menu in de console"""

    mode_choices = ['computer vs computer', 'player vs computer', 'computer vs player']

    while True:
        user_input = input("Do you want to play 'computer vs computer' or 'player vs computer' "
                           "or 'computer vs player'\n")
        if user_input in mode_choices:
            break
    if user_input == 'computer vs computer' or user_input == 'computer vs player':
        computer_mode_choices = ['heuristic', 'simple', 'ahead', 'worst_case', 'expected']
        while True:
            user_input_2 = input(f"pick computer mode: {computer_mode_choices}'\n")
            if user_input_2 in computer_mode_choices:
                break

        if user_input == 'computer vs computer':
            computer_vs_computer(True, user_input_2, 1, True)

        elif user_input == 'computer vs player':
            global code
            code = get_player_input()
            computer_vs_computer(True, user_input_2, 1, False)

    elif user_input == 'player vs computer':
        player_vs_computer()

# ---------------------------------------------------------------------------------------------------------------

# verschillende functies die je aan kan roepen:

# het textmenu om een gamemode te kiezen


play_game()


# een directe computer vs computer match, waar je aangeeft welk algoritme de computer moet gebruiken
# alle bot algoritmes: 'heuristic', 'simple', 'ahead', 'worst_case', 'expected'

# computer_vs_computer(True, 'heuristic', 0.5, True)

# om te testen hoe efficiënt de algoritmes zijn, kan je deze functie aangroepen.
# Het genereert een diagram die toont na hoeveel rondes een game wordt gewonnen na x games gespeelt
# get_avg(500, 'heuristic', False)
