import random
import csv

# AI class
class AI:
    def __init__(self, strat, two_dice, name):
        self.wanted_quantities = strat
        self.use_two_dice = two_dice
        self.name = name
        self.wins = 0
        self.turns = 0
        self.reset()
        

    def reset(self):
        self.money = 0
        self.owned_quantities = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def roll_two_dice(self):
        return self.use_two_dice and self.owned_quantities[Station] == 1 and \
               sum(self.owned_quantities[i] for i in [Cheese_Factory, Furniture_Factory, Mine, Apple_Orchard, Fruit_Veg_Market]) > 0

    def action(self):
        # Go through the list of wanted cards backwards to see what we can get
        pick = -1
        for i in range(18, -1, -1):
            if self.wanted_quantities[i] > self.owned_quantities[i] and costs[i] <= self.money and quantities[i] > 0:
                pick = i
                # If we don't own this yet, pick it! (if we do own it, we'll continue to see if there's another one we want but don't have)
                if self.owned_quantities[i] == 0:
                    break
        if pick >= 0:
            self.money -= costs[pick]
            quantities[pick] -= 1
            self.owned_quantities[pick] += 1
            if verbose_output:
                print(f"\tPlayer \"{self.name}\" bought a {names[pick]} for {costs[pick]} money")
        elif verbose_output:
            print(f"\tPlayer \"{self.name}\" bought nothing")

    def has_won(self):
        return sum(self.owned_quantities[i] for i in [Station, Shopping_Mall, Amusement_Park, Radio_Tower]) == 4

# Functions
def create_bots():
    card_baseline = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1]
    
    BotStrat0 = card_baseline[:]
    BotStrat0[Ranch] = 6
    BotStrat0[Cheese_Factory] = 2
    cheese_factory_bot = AI(BotStrat0, True, "Cheese Factory")

    BotStrat1 = card_baseline[:]
    BotStrat1[Convenience_Store] = 6
    BotStrat1[Bakery] = 3
    convenience_store_bot = AI(BotStrat1, False, "Convenience Store")

    BotStrat2 = card_baseline[:]
    BotStrat2[Wheat_Field] = 2
    BotStrat2[Ranch] = 2
    BotStrat2[Forest] = 1
    BotStrat2[Bakery] = 2
    BotStrat2[Convenience_Store] = 2
    BotStrat2[Cafe] = 2
    BotStrat2[Family_Restaurant] = 1
    BotStrat2[Stadium] = 1
    one_die_spread_bot = AI(BotStrat2, False, "1 Die Spread")

    BotStrat3 = card_baseline[:]
    BotStrat3[Bakery] = 6
    bakery_bot = AI(BotStrat3, False, "Bakery")

    BotStrat4 = card_baseline[:]
    BotStrat4[Forest] = 3
    BotStrat4[Mine] = 3
    BotStrat4[Furniture_Factory] = 2
    furniture_factory_bot = AI(BotStrat4, True, "Furniture Factory")

    BotStrat5 = card_baseline[:]
    BotStrat5[Wheat_Field] = 6
    BotStrat5[Fruit_Veg_Market] = 6
    fruit_bot = AI(BotStrat5, True, "Fruit & Veg Market")

    BotStrat6 = card_baseline[:]
    BotStrat6[Wheat_Field] = 1
    BotStrat6[Ranch] = 1
    BotStrat6[Forest] = 1
    BotStrat6[Mine] = 4
    BotStrat6[Apple_Orchard] = 1
    mine_bot = AI(BotStrat6, True, "Mines + Blue Spread")

    BotStrat7 = card_baseline[:]
    BotStrat7[Wheat_Field] = 6
    BotStrat7[Ranch] = 6
    BotStrat7[Forest] = 1
    blue_one_die_bot = AI(BotStrat7, False, "Blue 1 die")

    all_bots = [cheese_factory_bot, convenience_store_bot, one_die_spread_bot, bakery_bot, furniture_factory_bot, fruit_bot, mine_bot, blue_one_die_bot]
    return all_bots

def simulate_games(bots, number_of_games):
    for _ in range(number_of_games):
        # Play a game
        for bot in bots:
            bot.reset()
        global quantities
        quantities = [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
        
        while True:
            for player in range(len(bots)):
                if verbose_output:
                    print(f"{player}{bots[player].name} turn")
                # First roll the dice
                roll = random.randint(1, 6)
                if bots[player].roll_two_dice():
                    roll += random.randint(1, 6)

                if verbose_output:
                    print(f"\tPlayer \"{bots[player].name}\" rolled a {roll}")

                # If this player has a Radio Tower then see if they want to reroll
                if bots[player].owned_quantities[Radio_Tower] == 1:
                    # Get the list of buildings associated with this roll
                    for_this_roll = activated_by_roll[roll]
                    has_no_buildings = all(bots[player].owned_quantities[b] == 0 for b in for_this_roll)
                    if has_no_buildings:
                        roll = random.randint(1, 6)
                        if bots[player].roll_two_dice():
                            roll += random.randint(1, 6)

                        if verbose_output:
                            print(f"\tPlayer \"{bots[player].name}\" rerolled a {roll}")

                # Distribute income
                pay_out(bots, player, roll)

                # Finally, decide what the bot wants to do
                bots[player].action()

                #Bot counts its turn
                bots[player].turns += 1
                if verbose_output:
                    print("\tPlayer Money:")
                    for bot in bots:
                        print(f"\t\t{bot.name}: {bot.money}")

                # If a player won, then break out
                if bots[player].has_won():
                    bots[player].wins += 1
                    break
                
            if bots[player].has_won():
                break

def pay_out(bots, player, roll):
    player_money = bots[player].money

    # RED (special actions like Cafe or Family Restaurant)
    RedCafe = 3
    RedFamily_Restaurant1 = 9
    RedFamily_Restaurant2 = 10  
    if roll == RedCafe or roll == RedFamily_Restaurant1 or roll == RedFamily_Restaurant2:
        for p in range(len(bots)):
            if p != player:
                boost = bots[p].owned_quantities[Shopping_Mall]
                if roll == 3:
                    total_to_take = (1 + boost) * bots[p].owned_quantities[Cafe]
                else:
                    total_to_take = (2 + boost) * bots[p].owned_quantities[Family_Restaurant]

                if total_to_take > player_money:
                    total_to_take = player_money

                bots[p].money += total_to_take
                player_money -= total_to_take
    #Red card mod
        if Red_Card_mod:
            if roll == RedCafe:
                RedCafe = random.randrange(1,6) 
            if roll == RedFamily_Restaurant1 or roll == RedFamily_Restaurant2:
                RedFamily_Restaurant1 = random.randrange(7,11)
                RedFamily_Restaurant2 = RedFamily_Restaurant1 + 1

    # BLUE (Apple Orchard, Wheat Field, etc.)
    if roll == 1 or roll == 2 or roll == 5 or roll == 9 or roll == 10:
        amount = 1
        if roll == 10:
            amount = 3
        elif roll == 9:
            amount = 5

        card = Apple_Orchard if roll == 1 else Wheat_Field if roll == 2 else Ranch if roll == 5 else Forest if roll == 9 else Mine
        for bot in bots:
            bot.money += amount * bot.owned_quantities[card]
            
    # GREEN & PURPLE (Bakery, Convenience Store, Stadium, etc.)
    boost = bots[player].owned_quantities[Shopping_Mall]
    if roll == 2:
        player_money += (1 + boost) * bots[player].owned_quantities[Bakery]
    elif roll == 4:
        player_money += (3 + boost) * bots[player].owned_quantities[Convenience_Store]
    elif roll == 6:  # Stadium, TV Station, Business Center (ignoring the Business Center for now)
        if bots[player].owned_quantities[Stadium] == 1:
            for p in range(len(bots)):
                if p != player:
                    total_to_take = 2
                    if bots[p].money < 2:
                        total_to_take = bots[p].money
                    bots[p].money -= total_to_take
                    player_money += total_to_take
        if bots[player].owned_quantities[TV_Station] == 1:
            total_to_take = 5
            most_money = -1
            player_to_take_from = 0
            for p in range(len(bots)):
                if p != player and bots[p].money > most_money:
                    most_money = bots[p].money
                    player_to_take_from = p

            if bots[player_to_take_from].money < 5:
                total_to_take = bots[player_to_take_from].money

            player_money += total_to_take
            bots[player_to_take_from].money -= total_to_take
    elif roll == 7:
        if Cheese_Factory_Nerf:
            player_money += 2 * bots[player].owned_quantities[Cheese_Factory] * bots[player].owned_quantities[Ranch]
        else:
            player_money += 3 * bots[player].owned_quantities[Cheese_Factory] * bots[player].owned_quantities[Ranch]
    elif roll == 8:
        player_money += 3 * bots[player].owned_quantities[Furniture_Factory] * (bots[player].owned_quantities[Forest] + bots[player].owned_quantities[Mine])
    elif roll == 11 or roll == 12:
        player_money += 2 * bots[player].owned_quantities[Fruit_Veg_Market] * (bots[player].owned_quantities[Wheat_Field] + bots[player].owned_quantities[Apple_Orchard])

    bots[player].money = player_money
    bots[player].value = player_money

def cleanup_bots(bots):
    for bot in bots:
        del bot

# Main
if __name__ == "__main__":
    # Constants
    num_games = 10000
    verbose_output = False

    #Cheese Factory Nerf
    Cheese_Factory_Nerf = False
    #Red Card mod
    Red_Card_mod = True

    # Card enum for easy indexing
    Wheat_Field, Ranch, Bakery, Cafe, Convenience_Store, Fruit_Veg_Market, Forest, Furniture_Factory, Apple_Orchard, Family_Restaurant, Station, Cheese_Factory, Stadium, Mine, TV_Station, Business_Center, Amusement_Park, Radio_Tower, Shopping_Mall = range(19)

    # Game variables
    if Cheese_Factory_Nerf:
        costs = [1, 2, 1, 2, 2, 2, 3, 3, 3, 3, 4, 6, 6, 6, 7, 8, 16, 10, 22]
    else:
        costs = [1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 7, 8, 16, 10, 22]

    names = ["Wheat Field", "Ranch", "Bakery", "Cafe", "Convenience Store", "Fruit Veg Market", "Forest", "Furniture Factory", "Apple Orchard", "Family Restaurant", "Station", "Cheese Factory", "Stadium", "Mine", "TV Station", "Business Center", "Amusement Park", "Shopping Mall", "Radio Tower"]
    quantities = [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]
    activated_by_roll = [
        [],  # 0
        [Wheat_Field],  # 1
        [Ranch, Bakery],  # 2
        [Cafe, Bakery],  # 3
        [Convenience_Store],  # 4
        [Forest],  # 5
        [Stadium, TV_Station, Business_Center],  # 6
        [Cheese_Factory],  # 7
        [Furniture_Factory],  # 8
        [Mine, Family_Restaurant],  # 9
        [Apple_Orchard, Family_Restaurant],  # 10
        [Fruit_Veg_Market],  # 11
        [Fruit_Veg_Market]  # 12
    ]
    #Data Holders
    fields = ['Name','Wins','Avg.Turns','Win%']
    rows = []
    
    #Bot Allocation 
    primary_bot = 0
    opponent_bot_1 = 4
    opponent_bot_2 = 6
    opponent_bot_3 = 3
    
    # Create bots
    all_bots = create_bots()
    bots = [all_bots[0], all_bots[opponent_bot_1], all_bots[opponent_bot_2], all_bots[opponent_bot_3]]
    
    #Set Bot wins to zero          
    for bot in bots:
        bot.wins = 0
    
    # Simulate games
    simulate_games(bots, num_games)

    # Print out results to csv
    x = [f"{num_games} Games"]
    rows.append(x)
    x = [f"Cheese_Factory_Nerf: {Cheese_Factory_Nerf}"]
    rows.append(x)
    x = [f"Red_Card_mod: {Red_Card_mod}"]
    rows.append(x)
    for bot in bots:
        x = [f"{bot.name}",f"{bot.wins}",f"{bot.turns/num_games}",f"{(bot.wins/num_games)*100}%"]
        rows.append(x)
    
    filename = "GameOutput.csv"
    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(rows)
