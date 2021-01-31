board = []
options = ['A','B','C','D','E','F','G','H']
code = ['A','A','B','C']
results = []

def turn():
    print('Your turn')

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

    print(f'{len(perfect_placement)} correct letters were places in the right spot\n{len(good_placement)} correct letters were places in the wrong spot')

    result = [len(perfect_placement),len(good_placement)]
    return result

picks = turn()
board.append(picks)
results.append(check_placement(picks))
print(results)
print(board)




