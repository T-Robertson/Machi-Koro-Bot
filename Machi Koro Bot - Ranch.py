#Machi Koro Bot
#By Thomas Robertson

#Assumption 1: Bot buys Landmarks if it has enough money
#Assumption 2: Bot buys randomly
#Assumption 3: There's no other players against the bot
#Assumption 4: Bot roll one dice , until it has the train station
#Assumption 5: Business Center trades a random card and recives a random card

import random
from os.path import exists
from openpyxl import Workbook
from openpyxl import load_workbook
import os
import pandas as pd
import numpy as np

class MachiBot:
    def __init__(self, games, players):
        self.dest_filename = 'T:\Documents\Python\Machi Koro\Machi_bot_data.xlsx'
        self.file_created = False
        self.id_value = 1
        self.number_of_games = games
        self.number_of_players = players
        self._game_number = 1
        
    def game(self):
        '''
        This is the main method of the program. This will reset the game' data trackers
        and setup.
        
        '''
        for x in range(0,self.number_of_games):
            print(f"Running game # {self._game_number}")
            self.game_stat_tracker = {}
            
            for x in range(1,self.number_of_players + 1):
                player_name = "Player "+ str(x) 
                self.game_stat_tracker[f"{player_name}"] = x
                self.game_stat_tracker[f"{player_name}: Coins"] = 0
                self.game_stat_tracker[f"{player_name}: Cards"] = ['Wheat field','Bakery']
                self.game_stat_tracker[f"{player_name}: Spending"] = 0
                self.game_stat_tracker[f"{player_name}: Trades"] = 0
                self.game_stat_tracker[f"{player_name}: Player Holds"] = 0
                self.game_stat_tracker[f"{player_name}: Buy Train"] = 0
                self.game_stat_tracker[f"{player_name}: Buy Shopping"] = 0
                self.game_stat_tracker[f"{player_name}: Buy Amusement"] = 0
                self.game_stat_tracker[f"{player_name}: Buy Radio"] = 0
                self.game_stat_tracker[f"{player_name}: Buy Sequence"] = []
                self.game_stat_tracker[f"{player_name}: Train doubles"] = False
                self.game_stat_tracker[f"{player_name}: Shopping Mall Buff"] = False
                self.game_stat_tracker[f"{player_name}: Amusement Park Buff"] = False
                self.game_stat_tracker[f"{player_name}: Landmark Build"] = False
              
            #Data Trackers (reset at the start of ever game)
            self.rolls = []
            #Game Setup (reset at the start of ever game)
            self.game_cards = [
                'Wheat field',
                'Ranch',
                'Forest',
                'Mine',
                'Apple Orchard',
                'Bakery',
                'Convenience Store',
                'Cheese Factory',
                'Furniture Factory',
                'Fruit and Vegetable',
                'Cafe',
                'Family Restunrant',
                'Stadium',
                'TV Station',
                'Business Center',
            ]
            self.card_pool = []
            self.player_turn = 1
            self.round = 1
            self.game_active = True

            for x in range(6):
                for x in self.game_cards:
                    self.card_pool.append(x)
                    
            player_name = "Player 1" 
            
            #Game Running
            while True:
                self.roll(player_name)
                self.landmark(player_name)
                if self.game_stat_tracker[f"{player_name}: Landmark Build"] == False:
                    self.build(player_name)
                self.end_of_player_round()
                if self.game_active == False:
                    break 
                player_name = self.turn_change(player_name)
                
            print(f"Recording Game # {self._game_number}")   
            self._game_number += 1

    def turn_change(self,player_name):
        self.player_turn += 1
        new_player_name = "Player "+ str(self.player_turn)
        if self.player_turn > self.number_of_players:
            self.player_turn = 1
            new_player_name = "Player "+ str(self.player_turn)
            self.round += 1
        print(f"{new_player_name} Turn")
        return new_player_name
    
    def roll(self, player_name):
        '''
        The Rolling function is the first function called ever round and adds to the players coins according 
        to the random roll. Without buying Train station card the bot can only roll one dice.
        
        Added the ability to randomly select one or two dice, when train station is bought to increase the probability of lower rolls

        '''
        #Staring roll
        if self.game_stat_tracker[f"{player_name}: Train doubles"]:
            if random.randrange(1,3) == 2:
                roll1 = random.randrange(1,7)
                roll2 = random.randrange(1,7)
                value = roll1 + roll2
            else:
                value = random.randrange(1,7)
        else:
            value = random.randrange(1,7)
        self.rolls.append(value)
        
        print(f"{player_name} rolls {value}")
        
        card = ""
        card_value = 0
        blue_card = False
        shopping_mall_buff = False
            
        if value == 1:
            card = "Wheat field"
            card_value = 1
            blue_card = True
        if value == 2:
            card = "Ranch"
            card_value = 1
            blue_card = True
        if value == 2:
            card = "Bakery"
            card_value = 1
            shopping_mall_buff = True
        if value == 3:
            card = "Bakery"
            card_value = 1
            shopping_mall_buff = True
        if value == 3:
            card = "Cafe"
            loss = self.Machi_red_cards("Cafe", 2)
            self.game_stat_tracker[f"{player_name}: Coins"] -= loss
            Gain = self.Machi_red_cards("Cafe", 2)
            self.game_stat_tracker[f"{player_name}: Coins"] += Gain
        if value == 4:
            card = "Convenience Store"
            card_value = 3
            shopping_mall_buff = True
        if value == 5:
            card = "Forest"
            card_value = 3
            blue_card = True
        if value == 6:
            if "Stadium" in self.game_stat_tracker[f"{player_name}: Cards"]:
                amount = self.number_of_players * 2
                self.game_stat_tracker[f"{player_name}: Coins"] += amount
        if value == 6:
            if "TV Station" in self.game_stat_tracker[f"{player_name}: Cards"]: #Need to fix take amounts
                self.game_stat_tracker[f"{player_name}: Coins"] += 5
        if value == 6:
            if "Business Center" in self.game_stat_tracker[f"{player_name}: Cards"]:
                self.business_center(player_name)
        if value == 7:
            count = self.game_stat_tracker[f"{player_name}: Cards"].count("Cheese Factory")
            count2 = self.game_stat_tracker[f"{player_name}: Cards"].count("Ranch")
            self.game_stat_tracker[f"{player_name}: Coins"] += count * (count2 * 3)
        if value == 8:
            count = self.game_stat_tracker[f"{player_name}: Cards"].count("Furniture Factory")
            count2 = self.game_stat_tracker[f"{player_name}: Cards"].count("Forest")
            count3 = self.game_stat_tracker[f"{player_name}: Cards"].count("Mine")
            self.game_stat_tracker[f"{player_name}: Coins"] += count * ((count2 * 3) + (count3 * 3))
        if value == 9:
            card = "Mine"
            card_value = 5
            blue_card = True
        if value == 9:
            loss = self.Machi_red_cards("Family Restunrant", 2) 
            self.game_stat_tracker[f"{player_name}: Coins"] -= loss
            Gain = self.Machi_red_cards("Family Restunrant",2)
            self.game_stat_tracker[f"{player_name}: Coins"] += Gain
        if value == 10:
            loss = self.Machi_red_cards("Family Restunrant",2)
            self.game_stat_tracker[f"{player_name}: Coins"] -= loss
            Gain = self.Machi_red_cards("Family Restunrant",2)
            self.game_stat_tracker[f"{player_name}: Coins"] += Gain
        if value == 10:
            card = "Apple Orchard"
            card_value = 3
            blue_card = True
        if value == 11:
            count = self.game_stat_tracker[f"{player_name}: Cards"].count("Fruit and Vegetable Market")
            count2 = self.game_stat_tracker[f"{player_name}: Cards"].count("Wheat field")
            self.game_stat_tracker[f"{player_name}: Coins"] += count * (count2 * 3)
        if value == 12:
            count = self.game_stat_tracker[f"{player_name}: Cards"].count("Fruit and Vegetable Market")
            count2 = self.game_stat_tracker[f"{player_name}: Cards"].count("Wheat field")
            self.game_stat_tracker[f"{player_name}: Coins"] += count * (count2 * 3)

        self.coin_gain(player_name, card, card_value, blue_card, shopping_mall_buff)
        
        if self.game_stat_tracker[f"{player_name}: Amusement Park Buff"]:
            if roll1 == roll2:
                print(f"{roll1, roll2}, Amusement Doubles!!")
                self.roll(player_name)

    def coin_gain(self, player_name, card, card_value, blue_card, shopping_mall_buff):
            count = self.game_stat_tracker[f"{player_name}: Cards"].count(card)
            if blue_card:
                for x in range(1,self.number_of_players+1):
                    player_name = "Player "+ str(x)
                    count = self.game_stat_tracker[f"{player_name}: Cards"].count(card)
                    if shopping_mall_buff == True:
                        income = (card_value + 1) * count
                        self.game_stat_tracker[f"{player_name}: Coins"] += income
                    else:
                        income = card_value * count
                        self.game_stat_tracker[f"{player_name}: Coins"] += income
                    print(f"{player_name} gains {income} coins from {card}")

    def build(self, player_name):
        '''
        This is the building method for the game. The bot will randomly choose as card to build
        and use the player_spending method to complete and track the spending
        
        '''
        card = ""
        card_cost = 0
        Build_roll = random.randrange(1,18)
        
        if Build_roll == 1:
            card = "Wheat field"
            card_cost = 1
        if Build_roll == 2:
            card = "Ranch"
            card_cost = 1
        if Build_roll == 3:
            card = "Bakery"
            card_cost = 1
        if Build_roll == 4:
            card = "Cafe"
            card_cost = 2
        if Build_roll == 5:
            card = "Convenience Store"
            card_cost = 2
        if Build_roll == 6:
            card = "Forest"
            card_cost = 3
        if Build_roll == 7:
            print (f"{player_name} holds. Current coins : {self.game_stat_tracker[f'{player_name}: Coins']}")
            self.game_stat_tracker[f"{player_name}: Player Holds"] +=1
        if Build_roll == 8:
            if self.game_stat_tracker[f"{player_name}: Cards"].count("Stadium") < 1 and self.game_stat_tracker[f"{player_name}: Cards"].count("TV Station") < 1 and self.game_stat_tracker[f"{player_name}: Cards"].count("Business Center") < 1:
                card = "Stadium"
                card_cost = 6
        if Build_roll == 9:
            if self.game_stat_tracker[f"{player_name}: Cards"].count("Stadium") < 1 and self.game_stat_tracker[f"{player_name}: Cards"].count("TV Station") < 1 and self.game_stat_tracker[f"{player_name}: Cards"].count("Business Center") < 1:
                card = "TV Station"
                card_cost = 7
        if Build_roll == 10:
            if self.game_stat_tracker[f"{player_name}: Cards"].count("Stadium") < 1 and self.game_stat_tracker[f"{player_name}: Cards"].count("TV Station") < 1 and self.game_stat_tracker[f"{player_name}: Cards"].count("Business Center") < 1:
                card = "Business Center"
                card_cost = 8
        if Build_roll == 11:
            card = "Cheese Factory"
            card_cost = 5
        if Build_roll == 12:
            card = "Furniture Factory"
            card_cost = 3
        if Build_roll == 13:
            card = "Furniture Factory"
            card_cost = 5
        if Build_roll == 14:
            card = "Family Restaurant"
            card_cost = 3
        if Build_roll == 15:
            card = "Apple Orchard"
            card_cost = 3
        if Build_roll == 16:
            card = "Fruit and Vegetable Market"
            card_cost = 2
        if Build_roll == 17:
            print (f"{player_name} holds. Current coins : {self.game_stat_tracker[f'{player_name}: Coins']}")
            self.game_stat_tracker[f"{player_name}: Player Holds"] +=1
        
        if card in self.card_pool:
            if self.game_stat_tracker[f'{player_name}: Coins'] >= card_cost :
                    self.player_spending(player_name , card_cost, card, Build_roll)
                    self.card_pool.remove(card)

    def player_spending(self, player_name, cost, card, sequence):
        self.game_stat_tracker[f"{player_name}: Coins"] -= cost
        self.game_stat_tracker[f"{player_name}: Cards"].append(card)
        self.game_stat_tracker[f"{player_name}: Spending"] += cost
        self.game_stat_tracker[f"{player_name}: Buy Sequence"].append(sequence)
        print(f"{player_name} buys {card} for {cost}")

    def Machi_red_cards(self, card, cost):
        '''
        Tried to simplify the red cards in machi koro into a simple function.
        If the player has the shopping mall buff the cost increase by 1
        
        '''
        red_players = []
        for x in range(1,self.number_of_players+1):
            player_name = "Player "+ str(x) 
            if card in self.game_stat_tracker[f"{player_name}: Cards"]:
                card_amount = self.game_stat_tracker[f"{player_name}: Cards"].count(card)
            else:
                card_amount = 0
        
        
        
        if self.game_stat_tracker[f"{player_name}: Coins"] > cost * card_amount:
            if self.game_stat_tracker[f"{player_name}: Shopping Mall Buff"]:
                cards_value = (cost + 1) * card_amount
            else:
                cards_value = cost * card_amount
            return cards_value
        else:
            return 0

    def business_center(self, player_name):
        '''
        This function handles business center trades
        
        needs to be fixed to trade cards between players
        
        '''
        lst = ["wheat field","ranch","bakery","cafe","convenience Store","forest","cheese Factory","furniture Factory","mine","family Restaurant","apple Orchard","fruit and Vegetable Market"]
        banned_lst = ["TV Station","Business Center","Stadium","Train Station","Shopping Mall","Amusement Park","Radio Tower"]
        while True:
            y = random.choice(self.game_stat_tracker[f"{player_name}: Cards"])
            if y not in banned_lst:
                self.game_stat_tracker[f"{player_name}: Cards"].remove(y)
                x  = random.choice(lst)
                self.game_stat_tracker[f"{player_name}: Cards"].append(x)
                self.game_stat_tracker[f"{player_name}: Trades"] += 1
                print(f"{player_name} trades {y} and recives {x}")
                break

    def landmark(self, player_name):
        '''
        This function handles the buying of landmarks, the bot will always buy landmarks first before looking at other cards
        if it can afford the landmark. The landmarks have data points
        '''
        if  not "Train Station" in self.game_stat_tracker[f"{player_name}: Cards"]:
            if self.game_stat_tracker[f"{player_name}: Coins"] >= 4:
                self.game_stat_tracker[f"{player_name}: Coins"] -= 4
                self.game_stat_tracker[f"{player_name}: Cards"].append("Train Station")
                self.game_stat_tracker[f"{player_name}: Landmark Build"] = True
                self.game_stat_tracker[f"{player_name}: Train doubles"] = True
                self.game_stat_tracker[f"{player_name}: Buy Train"] = self.round
                print(f"{player_name} bought Train Station")
        if  not "Shopping Mall" in self.game_stat_tracker[f"{player_name}: Cards"]:
            if self.game_stat_tracker[f"{player_name}: Coins"] >= 10:
                self.game_stat_tracker[f"{player_name}: Coins"] -= 10
                self.game_stat_tracker[f"{player_name}: Cards"].append("Shopping Mall")
                self.game_stat_tracker[f"{player_name}: Buy Shopping"] = self.round
                self.game_stat_tracker[f"{player_name}: Shopping Mall Buff"] = True
                self.game_stat_tracker[f"{player_name}: Landmark Build"] = True
                print(f"{player_name} bought Shopping Mall")
        if  not "Amusement Park" in self.game_stat_tracker[f"{player_name}: Cards"]:
            if self.game_stat_tracker[f"{player_name}: Coins"] >= 16:
                self.game_stat_tracker[f"{player_name}: Coins"] -= 16
                self.game_stat_tracker[f"{player_name}: Cards"].append("Amusement Park")
                self.game_stat_tracker[f"{player_name}: Buy Amusement"] = self.round
                self.game_stat_tracker[f"{player_name}: Landmark Build"] = True
                print(f"{player_name} bought Amusement Park")
        if  not "Radio Tower" in self.game_stat_tracker[f"{player_name}: Cards"]:
            if self.game_stat_tracker[f"{player_name}: Coins"] >= 22:
                self.game_stat_tracker[f"{player_name}: Coins"] -= 22
                self.game_stat_tracker[f"{player_name}: Cards"].append("Radio Tower")
                self.game_stat_tracker[f"{player_name}: Buy Radio"] = self.round
                self.game_stat_tracker[f"{player_name}: Landmark Build"] = True
                print(f"{player_name} bought Radio Tower")

    def end_of_player_round(self):
        for x in range(1,self.number_of_players+1):
            player_name = "Player "+ str(x)
            self.game_stat_tracker[f"{player_name}: Landmark Build"] = False
                
            if "Train Station" in self.game_stat_tracker[f"{player_name}: Cards"]:
                if "Shopping Mall" in self.game_stat_tracker[f"{player_name}: Cards"]:
                    if "Amusement Park" in self.game_stat_tracker[f"{player_name}: Cards"]:
                        if "Radio Tower" in self.game_stat_tracker[f"{player_name}: Cards"]:
                            end_game_message = f"Game Over, bot completed game in {self.round} rounds"
                            print(end_game_message)
                            self.game_active = False
                            self.data_log()
        
    def data_log(self):
        '''
        This function converts the game data of the players dictionaries to a log that is used to export to excel
        
        '''
        for x in range(1,self.number_of_players+1):
            player_name = "Player "+ str(x)
            
            count_cards = {}
            count_rolls = {}
            
            for cards in self.game_stat_tracker[f"{player_name}: Cards"]:
                count_cards[cards] = count_cards.get(cards, 0) + 1
            for roll in self.rolls:
                count_rolls[roll] = count_rolls.get(roll, 0) + 1
            
            game_log = {
                "Game": [self._game_number],
                "Number of Rounds": [self.round],
                "Player": [player_name],
                "Value spent":[self.game_stat_tracker[f"{player_name}: Spending"]],
                "Number of Trades": [self.game_stat_tracker[f"{player_name}: Trades"]],
                "Number of Holds": [self.game_stat_tracker[f"{player_name}: Player Holds"]],
                "Number of Cards": [len(self.game_stat_tracker[f"{player_name}: Cards"])],
                "Percent of Cards": [(len(self.game_stat_tracker[f"{player_name}: Cards"])/72)*100],
                "Train Bought at round": [self.game_stat_tracker[f"{player_name}: Buy Train"]],
                "Shopping Bought at round": [self.game_stat_tracker[f"{player_name}: Buy Shopping"]],
                "Amusement Bought at round": [self.game_stat_tracker[f"{player_name}: Buy Amusement"]],
                "Radio Bought at round": [self.game_stat_tracker[f"{player_name}: Buy Radio"]],
                "Player Cards": [count_cards],
                "Dice Rolls": [count_rolls],
                "Sequence":[self.game_stat_tracker[f"{player_name}: Buy Sequence"]]
            }
            
            self.record_data(game_log, self.dest_filename)
        
    def record_data(self, game_log, path):
        '''
        Records data to path file using openpyxl and pandas
        
        '''
        
        if not self.file_created:
            os.remove(path)
            wb = Workbook()
            ws = wb.active
            ws.title = "Game Data"
            wb.save(self.dest_filename)
            self.file_created = True
            

        df_read_data = pd.read_excel(self.dest_filename, "Game Data")
        df_data = df_read_data.head(self.number_of_games)
        df_game = pd.DataFrame(game_log,index=[self.id_value])
        excel = pd.concat([df_data,df_game])
        excel.to_excel(self.dest_filename,sheet_name="Game Data",index=False)
        self.id_value +=2
        
def main():
    MachiBot(2,2).game()
    
if __name__ == '__main__':
    main()