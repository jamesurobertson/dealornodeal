#! python 3
# Deal or No Deal Terminal Game created by James Robertson


import random
import sys


# Shuffles the dollar amounts into random cases
def shuffled_cases():
    dollar_amounts = [.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400,
                      500, 750, 1000, 5000, 10000, 25000, 50000, 75000, 100000,
                      200000, 300000, 400000, 500000, 750000, 1000000]

    random.shuffle(dollar_amounts)
    for i in range(len(dollar_amounts)):
        cases[i + 1] = dollar_amounts[i]

    return cases


# The banks offer after each round.
def bank_offer(remaining_amounts, round_number):
    rounds = {1: 5, 2: 5, 3: 4, 4: 2, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1}

    remaining_low_amounts_sum = sum(v for v in remaining_amounts.values()
                                    if v <= 75000)
    remaining_high_amounts_sum = sum(v for v in remaining_amounts.values()
                                     if v >= 100000)

    # Additional parameters per round for banker to calculate offer
    calculation_per_round = [.13, .17, .2, .25, .33,
                             .33, .33, .5, .5, .5, .5]
    high_amount_calculation_per_round = [.11, .16, .21, .26, .31,
                                         .41, .51, .61, .71, .81, .91]

    round_calc = calculation_per_round[round_number - 1]
    high_round_calc = high_amount_calculation_per_round[round_number - 1]

    bank_offer = round((remaining_low_amounts_sum * round_calc) +
                       (remaining_high_amounts_sum * round_calc * high_round_calc))

    print(f'\nThe bank offers ${bank_offer} Do you want to make the deal?')
    if round_number < len(rounds) - 1:
        print(f'You have to choose {rounds[round_number + 1]} cases before your next offer.')
    print("DEAL OR NO DEAL? Press 'enter' for NO DEAL! Type 'D' for Deal: ", end='')
    answer = input()

    while answer != '' and answer.lower() != 'd':
        print("Please press 'enter' for NO DEAL! or type 'D' for deal: ", end='')
        answer = input()

    if answer.lower() == 'd':
        print(f'Congratulations! You won {bank_offer}!! Please play again soon :) ')
        sys.exit()
    else:
        print('\n-------------------------------------------')
        print(f"NO DEAL! Time for round #{round_number + 1}\n")


def print_remaining_cases_and_values(for_cases_dict, for_values_dict):
    remaining_cases_string = ', '.join([str(k) for k in sorted(for_cases_dict.keys())])
    remaining_values_string = ', '.join(str(v) for v in sorted(for_values_dict.values()))
    print(f'Remaining cases: {remaining_cases_string}')
    print(f'Remaining values: {remaining_values_string}')

# Main Game Loop
while True:
    print('''
    A termianl version of NBC's Deal or No Deal.
    The game rules:
    The game starts with 26 cases.
    Each case holds a value of $.01 - $1,000,000:

    .01                1,000
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

    At the start of the game you choose a case that will have a hidden value inside between $.01 - $1,000,000.
    This case is set aside. There are then a series of rounds where you open the remaining cases, revealing the values.
    These values and case numbers are then removed from the remaining pool of cases and values.
    At the end of each round the banker will offer you a deal, you can either accept the deal or keep going until
    there is only 1 unopened case left besides your own. If you make it this far,
    you then get the choice of taking your case or the remaining case.

    Goodluck and thanks for playing! :)\n''')
    cases = {}
    cases = shuffled_cases()
    hidden_cases = dict.copy(cases)
    print('Choose a case #(1-26): ', end='')
    player_choice = input()
    while not player_choice.isnumeric() or not (1 <= int(player_choice) <= 26):
        print('Please enter a postive integer in range of 1-26')
        player_choice = input()
    player_choice = int(player_choice)

    players_case = cases[player_choice]

    used_cases = {}
    used_cases[player_choice] = players_case
    round_counter = 1

    # Number of cases to choose per round
    rounds = {1: 5, 2: 5, 3: 4, 4: 2, 5: 2, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1}
    print('\n------------------------------------')
    print(f'\nGreat! You choose case #{player_choice}. I hope it has the 1,000,000!\n')
    del cases[player_choice]
    for round_counter in range(1, len(rounds)):

        number_of_cases_to_choose = rounds[round_counter]
        print_remaining_cases_and_values(cases, hidden_cases)
        print(f'\nIn round #{round_counter} you have to open {number_of_cases_to_choose} cases.')

        for i in range(1, number_of_cases_to_choose + 1):
            print(f'Choose a case to open from the remaining cases list: ', end='')
            guess = input()
            # TODO This check on guess seems like it could be shortened.
            while (not guess.isnumeric() or not (1 <= int(guess) <= 26)) or \
                  (int(guess) in used_cases or int(guess) == player_choice):
                if not guess.isnumeric() or not (1 <= int(guess) <= 26):
                    print('You must enter a positive whole number between 1 and 26.')
                    print('What case would you like to choose?: ', end='')
                    guess = input()
                else:
                    print('That cases has already been chosen. Please choose a new case')
                    print('What case would you like to choose?: ', end='')
                    guess = input()
            guess = int(guess)
            used_cases[guess] = cases[guess]
            print(f'Case #{guess} = {cases[guess]}\n')
            del cases[guess]
            del hidden_cases[guess]
        print('-------------------------------------------')
        print_remaining_cases_and_values(cases, hidden_cases)
        bank_offer(hidden_cases, round_counter)
        round_counter += 1

    print('\nWe are down to the last two!')
    print_remaining_cases_and_values(cases, hidden_cases)
    print('\nDo you want to keep your original case or switch to the remaining case?')
    print('Press ENTER to keep your case. Type (s)witch to switch cases.')
    final = input()

    while final != '' and final != 's':
        print('Wrong input received. Press ENTER to keep your case. Type (s)witch to switch cases.')
        final = input()

    if final == '':
        print(f'Congratulations! You won ${players_case}! Thank you for playing!')
        sys.exit()
    else:
        del hidden_cases[player_choice]
        # TODO: a better way to print the value in a 1 length
        hidden = ''.join(str(v) for v in hidden_cases.values())
        print(f'Congratulations! You won ${hidden}. Thank you for playing!')
        sys.exit()
