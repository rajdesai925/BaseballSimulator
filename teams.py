import sqlite3


class Team:
    def __init__(self, lineup, pitcher):
        self.lineup = lineup
        self.pitchers = [pitcher]
            

class Batter:
    def __init__(self, id, name, db):
        self.id = id
        self.name = name
        db.execute('SELECT SUM(AB), SUM(H), SUM("2B"), SUM("3B"), SUM("HR"), SUM(BB + HBP), SUM(SO), MAX(SB) FROM batting WHERE playerID = "{}"'.format(self.id))
        stats = db.fetchone()
        if stats[0] == 0:
            stats[0] = 1
        if stats[1] > 0:
            self.hit_chance = stats[1] / (stats[0] + stats[5])
            self.single = (stats[1] - stats[2] - stats[3] - stats[4]) / stats[1]
            self.double = stats[2] / stats[1]
            self.triple = stats[3] / stats[1]
            self.hr = stats[4] / stats[1]
        else:
            self.hit_chance = 0.1
            self.single = 0.75
            self.double = 0.15
            self.triple = 0.05
            self.hr = 0.1
        if stats[5] > 0:
            self.bb_chance = stats[5] / (stats[0] + stats[5])
        else:
            self.bb_chance = 0.05
        self.out_chance = 1 - self.hit_chance - self.bb_chance
        self.avg = round(stats[1] / stats[0], 3)
        self.obp = round((stats[1] + stats[5]) / (stats[0] + stats[5]), 3)
        self.slg = round(((stats[1] - stats[2] - stats[3] - stats[4]) + (2 * stats[2]) + (3 * stats[3]) + (4 * stats[4])) / stats[0], 3)
        if stats[6] > 0:
            self.k = stats[6] / (stats[0] - stats[1])
        else:
            self.k = 0.5
        if stats[7] >= 30:
            self.baserunning_out = 0.05
            self.speed = 5
        elif stats[7] in range(20, 30):
            self.baserunning_out = 0.075
            self.speed = 4
        elif stats[7] in range(10, 20):
            self.baserunning_out = 0.1
            self.speed = 3
        elif stats[7] in range(5, 10):
            self.baserunning_out = 0.125
            self.speed = 2
        else:
            self.baserunning_out = 0.15
            self.speed = 1
        self.game_pa = 0
        self.game_hits = 0
        self.game_bb = 0
        self.game_k = 0
        self.game_runs = 0
        self.game_rbi = 0

    def reset(self):
        self.game_pa = 0
        self.game_hits = 0
        self.game_bb = 0
        self.game_k = 0
        self.game_runs = 0
        self.game_rbi = 0


class Pitcher:
    def __init__(self, id, name, db):
        self.id = id
        self.name = name
        db.execute("SELECT SUM(BFP), SUM(H), SUM(BB + HBP), SUM(SO), SUM(ER), SUM(IPOuts) FROM pitching WHERE playerID = '{}'".format(self.id))
        stats = db.fetchone()
        self.era = round((stats[4] / (stats[5] / 3) * 9), 2)
        self.hit_chance = stats[1] / (stats[0] + stats[2])
        self.bb_chance = stats[2] / (stats[0] + stats[2])
        self.out_chance = 1 - self.hit_chance - self.bb_chance
        self.k = stats[3] / (stats[0] - stats[1] - stats[2])
        self.game_innings = 1
        self.game_bf = 0
        self.game_outs = 0
        self.game_k = 0
        self.game_hits = 0
        self.game_bb = 0
        self.game_runs = 0

    def reset(self):
        self.game_pa = 0
        self.game_hits = 0
        self.game_bb = 0
        self.game_k = 0
        self.game_runs = 0
        self.game_rbi = 0

def create_lineup(batter_count):
    with sqlite3.connect("stats.sqlite") as connection:
        db = connection.cursor()
        lineup = []
        lineup_number = 0
        while lineup_number < batter_count:
            name = input("Input Batter {}: ".format(lineup_number + 1))
            if " " in name:
                first = name[0:name.index(" ")]
                last = name[name.index(" ") + 1:]
                db.execute("SELECT people.playerID, people.nameFirst, people.nameLast, people.debut, people.finalGame FROM people INNER JOIN batting ON people.playerID = batting.playerID WHERE (people.nameFirst LIKE '{}%' COLLATE NOCASE AND people.nameLast LIKE '{}%' COLLATE NOCASE) OR (people.nameFirst LIKE '{}%' COLLATE NOCASE AND people.nameLast LIKE '{}%' COLLATE NOCASE) GROUP BY people.playerID".format(first, last, last, first))
            else:
                db.execute("SELECT people.playerID, people.nameFirst, people.nameLast, people.debut, people.finalGame FROM people INNER JOIN batting ON people.playerID = batting.playerID WHERE people.nameFirst LIKE '{}%' COLLATE NOCASE OR people.nameLast LIKE '{}%' COLLATE NOCASE GROUP BY people.playerID".format(name, name))
            players = db.fetchall()
            player_count = 0
            for player in players:
                player_count += 1
            if player_count == 0:
                print("No players found")
                continue
            else:
                for num, player in enumerate(players):
                    if player[3] is not None and player[4] is not None:
                        print("[ {} ]   {} {} ( {} - {} )".format(num, player[1], player[2], player[3][0:4], player[4][0:4]))
                player_choice = int(input("Input a number: "))
                selected = Batter(players[player_choice][0], players[player_choice][1] + " " + players[player_choice][2], db)
                lineup.append(selected)
            lineup_number += 1
        return lineup


def get_pitcher():
    with sqlite3.connect("stats.sqlite") as connection:
        db = connection.cursor()
        found = False
        while found is False:
            name = input()
            if " " in name:
                first = name[0:name.index(" ")]
                last = name[name.index(" ") + 1:]
                db.execute("SELECT people.playerID, people.nameFirst, people.nameLast, people.debut, people.finalGame FROM people INNER JOIN pitching ON people.playerID = pitching.playerID WHERE (people.nameFirst LIKE '{}%' COLLATE NOCASE AND people.nameLast LIKE '{}%' COLLATE NOCASE) OR (people.nameFirst LIKE '{}%' COLLATE NOCASE AND people.nameLast LIKE '{}%' COLLATE NOCASE) GROUP BY people.playerID".format(first, last, last, first))
            else:
                db.execute("SELECT people.playerID, people.nameFirst, people.nameLast, people.debut, people.finalGame FROM people INNER JOIN pitching ON people.playerID = pitching.playerID WHERE people.nameFirst LIKE '{}%' COLLATE NOCASE OR people.nameLast LIKE '{}%' COLLATE NOCASE GROUP BY people.playerID".format(name, name))
            players = db.fetchall()
            player_count = 0
            for player in players:
                player_count += 1
            if player_count == 0:
                print("No players found, try again")
            else:
                found = True
        for num, player in enumerate(players):
            if player[3] is not None and player[4] is not None:
                print("[ {} ]   {} {} ( {} - {} )".format(num, player[1], player[2], player[3][0:4], player[4][0:4]))
        player_choice = int(input("Input a number: "))
        selected = Pitcher(players[player_choice][0], players[player_choice][1] + " " + players[player_choice][2], db)
        return selected
