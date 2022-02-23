#!/usr/bin/env python3

# This program is a multiplayer (2 - 10 players) dice game. User provides
# teams' and players' names. Players are set into two teams randomly, choose
# dice size and number, roll dice and get results in a table. After 10 rounds
# the program sums up results and prints the outcome.

import random
import pandas


class Player:

    def __init__(self, name):
        self.player_name = name
        self.team = None

    def __repr__(self):
        return self.player_name

    def assign_team(self, team):
        self.team = team

    @staticmethod
    def roll_dice(dice):
        dice_sum = 0
        for i in range(0, dice.number):
            roll = random.randint(1, dice.size)
            dice_sum += roll
            if roll == 1:
                print(f'You rolled a {roll}! Critical Fail!')
            elif roll == dice.size:
                print(f'You rolled a {roll}! Critical Success!')
            else:
                print(f'You rolled a {roll}')
        print(f'You have rolled a total of {dice_sum}')
        return dice_sum


class Team:

    def __init__(self, name):
        self.team_name = name
        self.team_members = []
        self.score = 0

    def __repr__(self):
        return self.team_name

    def get_members(self, players):
        players_ = players
        for player in players_:
            player.assign_team(self)
            self.team_members.append(player)


class Dice:

    def __init__(self, number, size):
        self.number = number
        self.size = size


# function to slow down gameplay to user-friendly level
def wait():
    input('Press enter to continue...')


def set_teams(team1, team2, players_):
    # create team objects
    team_1 = Team(team1)
    team_2 = Team(team2)
    # get players' names and check if number of players is within range
    players = players_
    while True:
        if len(players) in range(2, 11):
            random.shuffle(players)
            break
        if len(players) < 2:
            print('Minimum number of players is 2. Please provide a valid '
                  'number')
        if len(players) > 10:
            print('Maximum number of players is 10. Please provide a valid '
                  'number')
    # create player objects for each prompted name
    player_objects = []
    for player_name in players:
        player = Player(player_name)
        player_objects.append(player)
    # shuffle created players into teams
    mid_id = len(player_objects) // 2
    team_1.get_members(player_objects[:mid_id])
    team_2.get_members(player_objects[mid_id:])

    print(f'{team_1.team_name} players: '
          f'{str(team_1.team_members).strip("[]")} \n'
          f'{team_2.team_name} players: '
          f'{str(team_2.team_members).strip("[]")}')

    return team_1, team_2


def game(team1, team2):
    # create list of rounds for output table rows
    rounds = []
    for number in range(1, 11):
        rounds.append(str(number))
    # set dice number and size
    dice_rolls = int(input('How many dice would you like to roll? '))
    dice_size = int(input('How many sides are the dice? '))
    dice = Dice(dice_rolls, dice_size)
    wait()
    # create Dataframe for output table
    df = pandas.DataFrame(index=rounds, columns=[team1, team2], data=0)
    # iterate over rounds
    for round_number in rounds:
        # show current scores and start next round
        print(df)
        print(f'Round number {round_number} - start'.upper())
        # team 1 members roll dice
        score_team1 = 0
        for player in team1.team_members:
            print(f'Player {player} - roll dice!')
            wait()
            score_team1 += player.roll_dice(dice)
        print(f'The score for {team1.team_name} in round {round_number} is '
              f'{score_team1}!')
        # team 2 members roll dice
        score_team2 = 0
        for player in team2.team_members:
            print(f'Player {player} - roll dice!')
            wait()
            score_team2 += player.roll_dice(dice)
        print(f'The score for {team2.team_name} in round {round_number} is '
              f'{score_team2}!')
        # append results for the round to Dataframe table
        df.at[round_number, team1] = score_team1
        df.at[round_number, team2] = score_team2
    # get final results for both teams
    results = list(df.sum(axis=0).values)
    final_result_team1 = results[0]
    final_result_team2 = results[1]
    print(f'Final results:\n{team1} - {final_result_team1}\n'
          f'{team2} - {final_result_team2}')
    if final_result_team1 > final_result_team2:
        print(f'{team1} won!')
    elif final_result_team1 == final_result_team2:
        print('It\'s a tie!')
    else:
        print(f'{team2} won!')


def main():
    team_name_1 = input('Name the first team: ')
    team_name_2 = input('Name the second team: ')
    players = input('Enter space-separated players\' names: ').split()
    teams = list(set_teams(team_name_1, team_name_2, players))
    game(teams[0], teams[1])


if __name__ == "__main__":
    main()
