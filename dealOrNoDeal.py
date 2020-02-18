#! python 3
# Deal or No Deal Terminal Game created by James Robertson - github.com/jamesurobertson
import random, pprint, sys


# Shuffles the dollar amounts into random cases
def shuffle_cases():
    dollar_amounts = ['1', '5', '10', '25', '50', '75', '100', '200', '300', '400',
        '500', '750', '1000', '5000', '10000', '25000', '50000', '75000', '100000',
        '200000', '300000', '400000', '500000', '750000', '1000000']

    random.shuffle(dollar_amounts)
    for i in range(len(dollar_amounts)):
        cases[i + 1] = dollar_amounts[i]


# The banks offer after each round.
def bank_offer(remaining_amounts, round_number, players_case):
    print(remaining_amounts)

    # Amounts left that are <= 75,000
    remining_low_amounts_sum = 0
    # Amounts left that are >= 100,000
    remining_high_amounts_sum = 0


    additional_calculation_per_round = {1: .13, 2:.17, 3: .2, 4:.25, 5:.33, 5:.33, 6:.33, \
        7: .33, 8: .33, 9: .33, 10: .33, 11: .33}
    additiona_high_amount_calcuation_per_round = {1: .11, 2: .16, 3: .21, 4: .26, 5: .31, 6:.41, \
        7: .51, 8: .61, 9: .71, 10: .81, 11: .91}

    # Calculating the totals for low/high remaining_amounts left
    for value in remaining_amounts.values():
        if int(value) <= 75000:
            remining_low_amounts_sum += int(value)
        else:
            remining_high_amounts_sum += int(value)

    if int(players_case) < 75000:
        remining_low_amounts_sum += int(players_case)
    else:
        remining_high_amounts_sum += int(players_case)

    round_calc = additiona_high_amount_calcuation_per_round[round_number]
    high_round_calc = additiona_high_amount_calcuation_per_round[round_number]

    # The bank's offer calculation
    bank_offer = round((remining_low_amounts_sum * round_calc) \
        + (remining_high_amounts_sum * round_calc * high_round_calc))

    print(f'\nThe bank offers ${bank_offer} Do you want to make the deal?')
    print('DEAL OR NO DEAL? Press "enter" for NO DEAL! Type (d)eal for Deal.', end='')
    answer = input()

    while answer != '' and answer != 'd':
        print("Please press 'enter' or type 'd' for deal.", end='')
        answer = input()

    if answer == 'd':
        print(f'Congratulations! You won {bank_offer}!! Please play again soon :) ')
        sys.exit()
    else:
        print(f"\nNO DEAL! Time for round #{round_number + 1} ")

def print_remaining_cases(remaining_dict):
    remaining_cases = []

    for k in remaining_dict.keys():
        remaining_cases += [int(k)]

    remaining_cases = sorted(remaining_cases)
    remaining_cases_string = ''

    for i in remaining_cases:
        if i == remaining_cases[-1]:
            remaining_cases_string += str(i)
        else:
            remaining_cases_string += str(i) + ', '

    print(f'Remaining cases: {remaining_cases_string}')

def print_remaining_values(remaining_dict):
    remaining_values = []

    for v in remaining_dict.values():
        if len(remaining_dict) == 1:
            print(f'You won {v}. Thanks for playing')
            sys.exit()
        else:
            remaining_values += [int(v)]

    remaining_values = sorted(remaining_values)
    remaining_values_string = ''

    for i in remaining_values:
        if i == remaining_values[-1]:
            remaining_values_string += str(i)
        else:
            remaining_values_string += str(i) + ', '

    print(f'Remaining values: {remaining_values_string}')

# Main Game Loop

while True:
    print('''
    A termianl version of Deal or No Deal.
    The game rules:
    The game starts with 25 cases.
    Each case holds a value of $1 - $1,000,000
    1                  1,000
    1                  5,000
    5                  10,000
    10                 25,000
    25                 50,000
    50                 75,000
    75                 100,000
    100                200,000
    200                300,000
    300                400,000
    400                500,000
    500                750,000
    750                1,000,000

    At the start of the game you choose a case with a hidden value inside between $1 - $1,000,000
    After choosing a case, there are a series of rounds where you open the remainging cases, revealing the values.
    At the end of each round the banker will offer you a deal, you can either accept the deal or keep going until
    There is only 1 unopened case left besides your own. You then get the choice of taking your case or the remaining case.

    If you have any suggestions for the game please let me know. Thanks for playing! :)\n''')
    cases = {}
    shuffle_cases()
    hidden_cases = dict.copy(cases)
    print('Choose a case #(1-25): ', end='')
    player_choice = input()
    while not player_choice.isnumeric() or not (1 <= int(player_choice) <= 25):
        print('Please enter a postive integer in range of 1-25')
        player_choice = input()

    players_case = cases[int(player_choice)]
    print(players_case)

    used_cases = {}
    used_cases[player_choice] = players_case
    round_counter = 1

    # Number of cases to choose per round
    rounds = { 1:5, 2:5, 3:4, 4:2, 5:2, 6:1, 7:1, 8:1, 9:1, 10:1, 11:1}
    print('\n------------------------------------')
    print(f'\nGreat! You choose case #{player_choice}. I hope it has the 1,000,000!\n')
    del cases[int(player_choice)]
    while round_counter < len(rounds):
        number_of_cases_to_choose = rounds[round_counter]
        print_remaining_cases(cases)
        print_remaining_values(hidden_cases)
        print(f'\nIn round #{round_counter} you have to open {number_of_cases_to_choose} cases.')
        for i in range(1, number_of_cases_to_choose + 1):
            print(f'Choose a case to open from the remaining cases list: ', end='')
            guess = input()
            while (guess in  used_cases or guess == player_choice) or (not guess.isnumeric() or not (1 <= int(guess) <= 25)):
                while not guess.isnumeric() or not (1 <= int(guess) <= 25):
                    print('You must enter a positive whole number between 1 and 25.')
                    print('What case would you like to choose?: ', end='')
                    guess = input()
                print(f"Case #{guess} has already been chosen. Please choose another case: ", end = '')
                guess = input()

            used_cases[guess] = cases[int(guess)]

            print(f'Case #{guess} = {cases[int(guess)]}\n')
            del cases[int(guess)]
            del hidden_cases[int(guess)]

        bank_offer(cases, round_counter, players_case)
        print('-------------------------------------------')
        round_counter += 1
    if round_counter == len(rounds):
        print('\nWe are down to the last two!')
        print('Do you want to keep your original case or switch to the remaining case?')
        print('Press ENTER to keep your case. Type (s)witch to switch cases.')
        final = input()
        if final == '':
            print(f'Congratulations! You won ${players_case}! Thank you for playing!')
            sys.exit()
        else:
            del hidden_cases[int(player_choice)]
            print_remaining_values(hidden_cases)
