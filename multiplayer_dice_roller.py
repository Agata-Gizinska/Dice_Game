# This program is a multiplayer (2 - 10 players) dice game. User provides teams' and
# players' names. Players are set into two teams randomly, choose dice size and number,
# roll dice and get results in a table. After 10 rounds the program sums up results
# and prints the outcome.

import random
import pandas as pd

team_name_1 = ''
team_name_2 = ''
team_1 = []
team_2 = []


def wait():
    input('Press enter to continue...')


def play_again():
    question = input('Do you want to play again? (yes / no): ')
    if question == 'yes':
        main()
    elif question == 'no':
        print('Thank you for playing!')
        exit()
    else:
        print('Invalid input')
        exit()


def set_teams():
    global team_1
    global team_2
    global team_name_1
    global team_name_2
    team_name_1 = input('Name the first team: ')
    team_name_2 = input('Name the second team: ')
    while True:
        try:
            players = input('Enter names: ').split()
            if len(players) in range(2, 11):
                random.shuffle(players)
                break
            if len(players) < 2:
                print('Minimum number of players is 2. Please provide valid number')
            if len(players) > 10:
                print('Maximum number of players is 10. Please provide valid number')
        except Exception as e:
            print(e)
    mid_id = len(players) // 2
    team_1 = (players[:mid_id])
    team_2 = (players[mid_id:])
    print(f'{team_name_1} players: {team_1} \n{team_name_2} players: {team_2}')
    return team_1, team_2, team_name_1, team_name_2


def game():
    list_of_rounds = []
    for number in range(1, 11):
        list_of_rounds.append(str(number))
    dice_rolls = int(input('How many dice would you like to roll? '))
    dice_size = int(input('How many sides are the dice? '))
    wait()
    df = pd.DataFrame(index=list_of_rounds, columns=[team_name_1, team_name_2], data=0)
    for round_number in list_of_rounds:
        print(df)
        print(f'round number {round_number} - start'.upper())
        result_team_1 = 0
        result_team_2 = 0
        for player in team_1:
            print(f'Player {player} - roll dice!')
            wait()
            dice_sum = 0
            for i in range(0, dice_rolls):
                roll = random.randint(1, dice_size)
                dice_sum += roll
                if roll == 1:
                    print(f'You rolled a {roll}! Critical Fail!')
                elif roll == dice_size:
                    print(f'You rolled a {roll}! Critical Success!')
                else:
                    print(f'You rolled a {roll}')
            print(f'You have rolled a total of {dice_sum}')
            result_team_1 += dice_sum
        print(f'The result for {team_name_1} in round {round_number} is {result_team_1}!')
        for player in team_2:
            print(f'Player {player} - roll dice!')
            wait()
            dice_sum = 0
            for i in range(0, dice_rolls):
                roll = random.randint(1, dice_size)
                dice_sum += roll
                if roll == 1:
                    print(f'You rolled a {roll}! Critical Fail!')
                elif roll == dice_size:
                    print(f'You rolled a {roll}! Critical Success!')
                else:
                    print(f'You rolled a {roll}')
            print(f'You have rolled a total of {dice_sum}')
            result_team_2 += dice_sum
        print(f'The result for {team_name_2} in round {round_number} is {result_team_2}!')
        df.at[round_number, team_name_1] = result_team_1
        df.at[round_number, team_name_2] = result_team_2
    results = list(df.sum(axis=0).values)
    final_result_team_1 = results[0]
    final_result_team_2 = results[1]
    print(f'Final results:\n{team_name_1} - {final_result_team_1}\n'
          f'{team_name_2} - {final_result_team_2}')
    if final_result_team_1 > final_result_team_2:
        print(f'{team_name_1} won!')
    elif final_result_team_1 == final_result_team_2:
        print('It\'s a tie!')
    else:
        print(f'{team_name_2} won!')
    play_again()


def main():
    set_teams()
    game()


if __name__ == "__main__":
    main()
