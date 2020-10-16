import teams
import random
from tabulate import tabulate


class Game:
    def __init__(self, home_lineup, away_lineup, home_pitcher, away_pitcher, outs, innings):
        self.home_lineup = home_lineup
        self.away_lineup = away_lineup
        self.home_pitcher = home_pitcher
        self.away_pitcher = away_pitcher
        self.home_score = 0
        self.away_score = 0
        self.home_hits = 0
        self.away_hits = 0
        self.home_k = 0
        self.away_k = 0
        self.home_bb = 0
        self.away_bb = 0
        self.home_batter = 0
        self.away_batter = 0
        self.inning = 0
        self.max_innings = innings * 2
        self.outs = 0
        self.max_outs = outs
        self.first = None
        self.second = None
        self.third = None

    def add_out(self):
        if self.inning % 2 == 1:
            self.away_pitcher.game_outs += 1
        else:
            self.home_pitcher.game_outs += 1
        self.outs += 1
        if self.outs > 1:
            print("There are now {} outs".format(self.outs))
        else:
            print("There is now {} out".format(self.outs))
        if self.outs == self.max_outs:
            self.inning += 1
            if self.inning == self.max_innings - 1:
                if self.home_score > self.away_score:
                    self.inning += 1
            if self.inning == self.max_innings:
                if self.home_score == self.away_score:
                    self.max_innings += 2
                else:
                    return
            print("Switch sides!\n\n")
            if self.inning % 2 == 1:
                print("It is now the bottom of inning {}".format(int(self.inning / 2) + 1))
            else:
                print("It is now the top of inning {}".format(int(self.inning / 2) + 1))
            print("AWAY: {}  HOME: {}\n".format(self.away_score, self.home_score))
            self.outs = 0
            self.first = None
            self.second = None
            self.third = None
            if self.inning > 1:
                if self.inning % 2 == 1:
                    self.away_pitcher.game_innings += 1
                else:
                    self.home_pitcher.game_innings += 1

    def thrown_out(self, base):
        bases = {1: "first", 2: "second", 3: "third"}
        print("{} was thrown out advancing from {} base!".format(getattr(self, '{}'.format(bases[base])).name, bases[base]))
        setattr(self, '{}'.format(bases[base]), None)
        if self.outs == self.max_outs - 1:
            new_inning = True
        else:
            new_inning = False
        self.add_out()
        return new_inning

    def run_scored(self, runs):
        if runs > 1:
            print("{} RUNS SCORED!".format(runs))
        else:
            print("{} RUN SCORED!".format(runs))
        if self.inning % 2 == 1:
            self.home_score += runs
        else:
            self.away_score += runs
        print("AWAY: {}  HOME: {}".format(self.away_score, self.home_score))
        if self.inning == self.max_innings - 1:
            if self.home_score > self.away_score:
                self.inning += 1

    def advance_runner(self, start_base, end_base):
        bases = {1: "first", 2: "second", 3: "third"}
        if start_base == 0:
            if self.inning % 2 == 1:
                print("{} advanced to {} base".format(self.home_lineup[self.home_batter].name, bases[end_base]))
                setattr(self, '{}'.format(bases[start_base]), self.home_lineup[self.home_batter])
            else:
                print("{} advanced to {} base".format(self.away_lineup[self.away_batter].name, bases[end_base]))
                setattr(self, '{}'.format(bases[start_base]), self.away_lineup[self.away_batter])
        if end_base == 4:
            getattr(self, '{}'.format(bases[start_base])).game_runs += 1
            print("{} scored from {} base!".format(getattr(self, '{}'.format(bases[start_base])).name, bases[start_base]))
            setattr(self, '{}'.format(bases[start_base]), None)
            return 1
        elif start_base == end_base:
            print("{} stayed at {} base".format(getattr(self, '{}'.format(bases[start_base])).name, bases[start_base]))
            return 0
        else:
            print("{} advanced from {} to {}".format(getattr(self, '{}'.format(bases[start_base])).name, bases[start_base], bases[end_base]))
            setattr(self, '{}'.format(bases[end_base]), getattr(self, '{}'.format(bases[start_base])))
            setattr(self, '{}'.format(bases[start_base]), None)
            return 0

    def single(self, batter, pitcher):
        print("SINGLE!")
        runs = 0
        new_inning = False
        if self.third is not None:
            if random.choices([0, 1], [self.third.baserunning_out, 1 - self.third.baserunning_out])[0] == 0:
                new_inning = self.thrown_out(3)
            else:
                result = random.randint(3, 4) if self.second is None or self.first is None else 4
                runs += self.advance_runner(3, result)
        if self.second is not None and new_inning is False:
            if random.choices([0, 1], [self.second.baserunning_out, 1 - self.second.baserunning_out])[0] == 0:
                new_inning = self.thrown_out(2)
            else:
                max = 4 if self.third is None else 2
                min = 2 if self.first is None else 3
                result = random.randint(min, max)
                runs += self.advance_runner(2, result)
        if self.first is not None and new_inning is False:
            if random.choices([0, 1], [self.first.baserunning_out, 1 - self.first.baserunning_out])[0] == 0:
                new_inning = self.thrown_out(1)
            else:
                result = random.randint(2, 4) if self.third is None else 2
                runs += self.advance_runner(1, result)
        if new_inning is False:
            self.first = batter
            print("{} advanced to first\n".format(batter.name))
        if runs > 0:
            batter.game_rbi += runs
            pitcher.game_runs += runs
            self.run_scored(runs)


    def double(self, batter, pitcher):
        print("DOUBLE!!")
        runs = 0
        new_inning = False
        if self.third is not None:
            runs += self.advance_runner(3, 4)
        if self.second is not None:
            if random.choices([0, 1], [self.second.baserunning_out, 1 - self.second.baserunning_out])[0] == 0:
                new_inning = self.thrown_out(2)
            else:
                runs += self.advance_runner(2, 4)
        if self.first is not None and new_inning is False:
            if random.choices([0, 1], [self.first.baserunning_out, 1 - self.first.baserunning_out])[0] == 0:
                new_inning = self.thrown_out(1)
            else:
                result = random.randint(3, 4)
                runs += self.advance_runner(1, result)
        if new_inning is False:
            self.second = batter
            print("{} advanced to second\n".format(batter.name))
        if runs > 0:
            batter.game_rbi += runs
            pitcher.game_runs += runs
            self.run_scored(runs)

    def triple(self, batter, pitcher):
        print("TRIPLE!!")
        runs = 0
        new_inning = False
        if self.third is not None:
            runs += self.advance_runner(3, 4)
        if self.second is not None:
            runs += self.advance_runner(2, 4)
        if self.first is not None:
            if random.choices([0, 1], [self.first.baserunning_out, 1 - self.first.baserunning_out])[0] == 0:
                new_inning = self.thrown_out(1)
            else:
                runs += self.advance_runner(1, 4)
        if new_inning is False:
            self.third = batter
            print("{} advanced to third\n".format(batter.name))
        if runs > 0:
            batter.game_rbi += runs
            pitcher.game_runs += runs
            self.run_scored(runs)

    def homerun(self, batter, pitcher):
        print("HOME RUN!!!!!")
        runs = 1
        if self.third is not None:
            runs += self.advance_runner(3, 4)
        if self.second is not None:
            runs += self.advance_runner(2, 4)
        if self.first is not None:
            runs += self.advance_runner(1, 4)
        print("{} scored!\n".format(batter.name))
        batter.game_rbi += runs
        batter.game_runs += 1
        pitcher.game_runs += runs
        self.run_scored(runs)

    def walk(self, batter, pitcher):
        print("BASE ON BALLS")
        runs = 0
        if self.first is not None:
            if self.second is not None:
                if self.third is not None:
                    runs += self.advance_runner(3, 4)
                runs += self.advance_runner(2, 3)
            runs += self.advance_runner(1, 2)
        self.first = batter
        print("{} advanced to first\n".format(batter.name))
        if runs > 0:
            self.run_scored(1)
            batter.game_rbi += 1
            pitcher.game_runs += 1

    def groundout(self, batter, pitcher):
        print("{} grounded out".format(batter.name))
        if self.outs == self.max_outs - 1:
            self.add_out()
        else:
            runs = 0
            new_inning = False
            if self.third is not None and new_inning is False:
                if random.choices([0, 1], [self.third.baserunning_out * 3, 1 - self.third.baserunning_out * 3])[0] == 0:
                    new_inning = self.thrown_out(3)
                else:
                    result = random.randint(3, 4) if self.second is None or self.first is None else 4
                    runs += self.advance_runner(3, result)
            if self.second is not None and new_inning is False:
                if random.choices([0, 1], [self.second.baserunning_out * 4, 1 - self.second.baserunning_out * 4])[0] == 0:
                    new_inning = self.thrown_out(2)
                else:
                    max = 3 if self.third is None else 2
                    min = 2 if self.first is None else 3
                    result = random.randint(min, max)
                    runs += self.advance_runner(2, result)
            if self.first is not None and new_inning is False:
                if random.choices([0, 1], [self.first.baserunning_out * 5, 1 - self.first.baserunning_out * 5])[0] == 0:
                    new_inning = self.thrown_out(1)
                else:
                    runs += self.advance_runner(1, 2)
            if new_inning is False:
                self.add_out()
                if runs > 0:
                    batter.game_rbi += runs
                    pitcher.game_runs += runs
                    self.run_scored(runs)

    def flyout(self, batter, pitcher):
        print("{} flew out".format(batter.name))
        if self.outs == self.max_outs - 1:
            self.add_out()
        else:
            runs = 0
            new_inning = False
            if self.third is not None:
                tag = random.choices([0, 1], [0.25, 0.75])[0]
                if tag == 1:
                    if random.choices([0, 1], [self.third.baserunning_out * 2, 1 - self.third.baserunning_out * 2])[0] == 0:
                        new_inning = self.thrown_out(3)
                    else:
                        runs += self.advance_runner(3, 4)
                else:
                    runs += self.advance_runner(3, 3)
            if self.second is not None and self.third is None and new_inning is False:
                tag = random.choice([0, 1])
                if tag == 1:
                    if random.choices([0, 1], [self.second.baserunning_out * 3, 1 - self.second.baserunning_out * 3])[0] == 0:
                        new_inning = self.thrown_out(2)
                    else:
                        runs += self.advance_runner(2, 3)
                else:
                    runs += self.advance_runner(2, 2)
            if self.first is not None and self.second is None and new_inning is False:
                tag = random.choices([0, 1], [0.75, 0.25])
                if tag == 1:
                    if random.choices([0, 1], [self.first.baserunning_out * 3, 1 - self.first.baserunning_out * 3])[0] == 0:
                        new_inning = self.thrown_out(1)
                    else:
                        runs += self.advance_runner(1, 2)
                else:
                    runs += self.advance_runner(1, 1)
            if new_inning is False:
                self.add_out()
                if runs > 0:
                    batter.game_rbi += runs
                    pitcher.game_runs += runs
                    self.run_scored(runs)

    def at_bat(self):
        if self.inning % 2 == 1:
            batter = self.home_lineup[self.home_batter]
            pitcher = self.away_pitcher
            self.home_batter += 1
            if self.home_batter == len(self.home_lineup):
                self.home_batter = 0
        else:
            batter = self.away_lineup[self.away_batter]
            pitcher = self.home_pitcher
            self.away_batter += 1
            if self.away_batter == len(self.away_lineup):
                self.away_batter = 0
        batter.game_pa += 1
        pitcher.game_bf += 1
        hit_chance = (batter.hit_chance + pitcher.hit_chance) / 2
        bb_chance = (batter.bb_chance + pitcher.bb_chance) / 2
        out_chance = (batter.out_chance + pitcher.out_chance) / 2
        print("\n{} is now up to bat".format(batter.name))
        #print("HIT% = {}    BB% = {}    OUT% = {}".format(hit_chance, bb_chance, out_chance))
        outcome = random.choices(["hit", "walk", "out"], [hit_chance, bb_chance, out_chance])[0]
        if outcome == "hit":
            if self.inning % 2 == 1:
                self.home_hits += 1
            else:
                self.away_hits += 1
            batter.game_hits += 1
            pitcher.game_hits += 1
            #print("Single% = {}    Double% = {}    Triple% = {}    HR % = {}".format(batter.single, batter.double, batter.triple, batter.hr))
            hit = random.choices(["single", "double", "triple", "HR"],
                                 [batter.single,
                                  batter.double,
                                  batter.triple,
                                  batter.hr])[0]
            if hit == "single":
                self.single(batter, pitcher)
            elif hit == "double":
                self.double(batter, pitcher)
            elif hit == "triple":
                self.triple(batter, pitcher)
            else:
                self.homerun(batter, pitcher)
        elif outcome == "walk":
            if self.inning % 2 == 1:
                self.home_bb += 1
            else:
                self.away_bb += 1
            batter.game_bb += 1
            pitcher.game_bb += 1
            self.walk(batter, pitcher)
        else:
            k_chance = (batter.k + pitcher.k) / 2
            #print("Batter K% = {}   Pitcher K% = {}    k% = {}".format(batter.k, pitcher.k, k_chance))
            outcome = random.choices(["k", "other"], [k_chance, 1 - k_chance])[0]
            if outcome == "k":
                print("{} was struck out by {}".format(batter.name, pitcher.name))
                if self.inning % 2 == 1:
                    self.home_k += 1
                else:
                    self.away_k += 1
                batter.game_k += 1
                pitcher.game_k += 1
                self.add_out()
            else:
                outcome = random.choices(["ground", "fly"], [1 - batter.slg, batter.slg])[0]
                if outcome == "ground":
                    self.groundout(batter, pitcher)
                else:
                    self.flyout(batter, pitcher)

    def game_stats(self):
        game_table = [["AWAY", self.away_score, self.away_hits, self.away_bb, self.away_k],
                 ["HOME", self.home_score, self.home_hits, self.home_bb, self.home_k]]
        print(tabulate(game_table, headers=["TEAM", "SCORE", "HITS", "WALKS", "STRIKEOUTS"]) + "\n\n\n")
        away_batter_table = []
        for batter in self.away_lineup:
            batter_stats = [batter.name, batter.game_pa, batter.game_hits, batter.game_bb, batter.game_runs, batter.game_rbi, batter.game_k]
            away_batter_table.append(batter_stats)
        print(tabulate(away_batter_table, headers=["Batters - Away", "PA", "HITS", "WALKS", "RUNS", "RBI", "STRIKEOUTS"]) + "\n")
        away_pitcher_table = [[self.away_pitcher.name, self.away_pitcher.game_innings, self.away_pitcher.game_bf, self.away_pitcher.game_outs, self.away_pitcher.game_k, self.away_pitcher.game_hits, self.away_pitcher.game_bb, self.away_pitcher.game_runs]]
        print(tabulate(away_pitcher_table, headers=["Pitchers - Away", "INNINGS", "BF", "OUTS", "STRIKEOUTS", "HITS", "WALKS", "RUNS"]) + "\n\n\n")
        home_batter_table = []
        for batter in self.home_lineup:
            batter_stats = [batter.name, batter.game_pa, batter.game_hits, batter.game_bb, batter.game_runs, batter.game_rbi, batter.game_k]
            home_batter_table.append(batter_stats)
        print(tabulate(home_batter_table, headers=["Batters - Home", "PA", "HITS", "WALKS", "RUNS", "RBI", "STRIKEOUTS"]) + "\n")
        home_pitcher_table = [[self.home_pitcher.name, self.home_pitcher.game_innings, self.home_pitcher.game_bf, self.home_pitcher.game_outs, self.home_pitcher.game_k, self.home_pitcher.game_hits, self.home_pitcher.game_bb, self.home_pitcher.game_runs]]
        print(tabulate(home_pitcher_table, headers=["Pitchers - Home", "INNINGS", "BF", "OUTS", "STRIKEOUTS", "HITS", "WALKS", "RUNS"]) + "\n\n\n")

    def play(self):
        simulate = False
        while self.inning < self.max_innings:
            if simulate is False:
                if input("\nPress enter to continue to the next at bat, or enter any keys to simulate the rest of the game\n"):
                    simulate = True
            self.at_bat()
        print("\n\nGame Over!\n\n")
        self.game_stats()


def main():
    batter_count = int(input("Number of batters: "))
    inning_count = int(input("Number of innings: "))
    out_count = int(input("Number of outs per half inning: "))
    print("Begin inputting away lineup:")
    away_lineup = teams.create_lineup(batter_count)
    for batter in away_lineup:
        print("{}".format(batter.name))
        print("{} / {} / {}\n".format(batter.avg, batter.obp, batter.slg))
    print("Begin inputting home lineup:")
    home_lineup = teams.create_lineup(batter_count)
    for batter in home_lineup:
        print("{}".format(batter.name))
        print("{} / {} / {}\n".format(batter.avg, batter.obp, batter.slg))
    print("Input away team's pitcher:")
    away_pitcher = teams.get_pitcher()
    print("ERA = {}\n".format(away_pitcher.era))
    print("Input home team's pitcher:")
    home_pitcher = teams.get_pitcher()
    print("ERA = {}\n".format(home_pitcher.era))
    game = Game(home_lineup, away_lineup, home_pitcher, away_pitcher, out_count, inning_count)
    game.play()


if __name__ == "__main__":
    main()
