import game
import teams

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
    new_game = game.Game(home_lineup, away_lineup, home_pitcher, away_pitcher, out_count, inning_count)
    new_game.play()


if __name__ == "__main__":
    main()
