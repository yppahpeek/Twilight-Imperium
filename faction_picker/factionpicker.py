import csv, sys

from operator import itemgetter



def main():

    # checks correct number of args

    if len(sys.argv) != 3:

        sys.exit('Usage: "python factionpicker.py <name of votes file>.csv factions.txt')



    players = create_players(sys.argv[1])



    factions = get_factions(sys.argv[2])



    table = make_table(players, factions)



    print(table)





def create_players(c):

    """

    The create_players() function:

    - validates that the player_choices.csv argument is a CSV

    - returns a list of dicts of player_choices

    """



    # validate file formats of the arguments

    if c.endswith(".csv") == False:

        sys.exit('Usage: "python project.py <name of votes file>.csv factions.txt')



    # list to save choices for each player

    player_choices = []



    # load player choices

    with open(c) as file:

        # skip the header row

        next(file)

        reader = csv.reader(file)

        for row in reader:

            timestamp, priority, name, *choices = row

            player_choices.append({"Priority": priority, "Name": name, "Choices": choices})



        return player_choices





def get_factions(f):

    """

    The get_factions() function:

    - validates that the factions.txt argument is a TXT

    - returns a list of factions

    """



    # validate file formats of the arguments

    if f.endswith(".txt") == False:

        sys.exit('Usage: "python project.py <name of votes file>.csv factions.txt')



    # list saves factions

    factions = []



    # load factions

    with open(f) as file:

        lines  = file.readlines()

        for line in lines:

            factions.append(line.strip())



    return factions





def make_table(p, f):

    """

    The make_table() function:

    - takes the player choices dict and the factions list as input

    - assigns a faction to each player

    - returns a new list of dicts detailing which faction each player has

    """



    table_players = []



    """

    This section iterates through the player choices.

    Players should get their highest choice which is still available.

    First we itereate through the first choices.

    If a faction is still available for that player, they get that faction and the faction is removed from factions list.

    If faction is not available, then the program looks to that player's second choice.

    (But only after all first choices are assigned).

    """

    for n in range(6):

        for player in sorted(p, key=itemgetter('Priority')):

            faction = player["Choices"][n]

            if faction in f:

                # add player and their faction pick to final list of players

                table_players.append({"Name": player["Name"], "Faction": faction})



                # remove faction and player from the draw, since these have both been used

                f.remove(faction)

                p.remove(player)

            else:

                continue



        # break out of loop once all players have a faction

        if len(table_players) == 6:

            return table_players



# TODO - Assign start position and colour to each player

# TODO - Print PDF with table position, colour and



if __name__ == "__main__":

    main()