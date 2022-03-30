#Machi Koro Bot
#By Thomas Robertson

#Assumption 1: Bot buys Landmarks if it has enough money
#Assumption 2: Bot buys randomly
#Assumption 3: There's no other players against the bot
#Assumption 4: Bot roll one dice , until it has the train station
#Assumption 5: Business Center trades a random card and recives a random card

import random
from openpyxl import Workbook
from openpyxl import load_workbook
import pandas as pd
import numpy as np

class MachiBot:
    def __init__(self, games):
        self.number_of_games = games
        self.dest_filename = 'T:\Documents\Python\Machi Koro\Machi_bot_data.xlsx'
        
        self._game_number = 1
        
    def game(self):
        '''
        This is the main method of the program. This will reset the game' data trackers
        and setup.
        
        '''
        for x in range(0,self.number_of_games):
            print(f"Running game # {self._game_number}")
            
            #Data Trackers (reset at the start of ever game)
            self.rolls = []
            self.spending = 0
            self.trades = 0
            self.player_holds = 0
            self.buy_train = 0
            self.buy_shopping = 0
            self.buy_amusement = 0
            self.buy_radio = 0
            self.buy_sequence = []
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
            self.player_coins = 0
            self.player_cards = ['Wheat field','Bakery']
            self.round = 1
            self.train_doubles = False
            self.shopping_mall_buff = False 
            self.amusement_park_buff = False
            self.landmark_build = False
            self.game_active = True

            for x in range(7):
                for x in self.game_cards:
                    self.card_pool.append(x)
            
            #Game Running
            while True:
                self.roll()
                self.landmark()
                if self.landmark_build == False:
                    self.build()
                self.round_end()
                if self.game_active == False:
                    break 
                
            print(f"Recording Game # {self._game_number}")   
            self._game_number += 1
            
    def roll(self):
        '''
        The Rolling function is the first function called ever round and adds to the players coins according 
        to the random roll. Without buying Train station card the bot can only roll one dice.
        
        The red cards are a gain and a lost for the player, however the code assumes that other players can have up tp
        six cards, which is a big loss early game for the player
        
        Need to do
        - Clean up code? every card type having its own function?
        '''
        #Staring roll
        if self.train_doubles == True:
            roll1 = random.randrange(1,7)
            roll2 = random.randrange(1,7)
            value = roll1 + roll2
        else:
            value = random.randrange(1,7)
        self.rolls.append(value)
            
        if value == 1:
            count = self.player_cards.count("Wheat field")
            self.player_coins += 1 * count
        if value == 2:
            count = self.player_cards.count("Ranch")
            self.player_coins += 1 * count
        if value == 2:
            count = self.player_cards.count("Bakery")
            if self.shopping_mall_buff:
                self.player_coins += 2 * count
            else:
                self.player_coins += 1 * count
        if value == 3:
            count = self.player_cards.count("Bakery")
            if self.shopping_mall_buff:
                self.player_coins += 2 * count
            else:
                self.player_coins += 1 * count
        if value == 3:
            count = self.player_cards.count("Cafe")
            x = random.randrange(0, 6 - count) #This isn't the best way to deal with random loss, Idk how to make better
            loss = self.Machi_red_cards(2, x)
            self.player_coins -= loss
            Gain = self.Machi_red_cards(2, count)
            self.player_coins += Gain
        if value == 4:
            count = self.player_cards.count("Convenience Store")
            if self.shopping_mall_buff:
                self.player_coins += 4 * count
            else:
                self.player_coins += 3 * count
        if value == 5:
            count = self.player_cards.count("Forest")
            self.player_coins += 3 * count
        if value == 6:
            if "Stadium" in self.player_cards: # Assume there's 3 other players, that all have enough money
                y = 6
                self.player_coins += y
        if value == 6:
            if "TV Station" in self.player_cards:
                y = random.randrange(0,5) # Assume there's 3 other players, that all have enough money
                self.player_coins += y
        if value == 6:
            if "Business Center" in self.player_cards:
                self.business_center()
        if value == 7:
            count = self.player_cards.count("Cheese Factory")
            count2 = self.player_cards.count("Ranch")
            self.player_coins += count * (count2 * 3)
        if value == 8:
            count = self.player_cards.count("Furniture Factory")
            count2 = self.player_cards.count("Forest")
            count3 = self.player_cards.count("Mine")
            self.player_coins += count * ((count2 * 3) + (count3 * 3))
        if value == 9:
            count = self.player_cards.count("Mine")
            self.player_coins += 5 * count
        if value == 9:
            count = self.player_cards.count("Family Restaurant") # Assume there's 3 other players, that all have enough money
            x = random.randrange(0, 6 - count) #This isn't the best way to deal with random loss, Idk how to make better
            loss = self.Machi_red_cards(2, x)
            self.player_coins -= loss
            Gain = self.Machi_red_cards(2, count)
            self.player_coins += Gain
        if value == 10:
            count = self.player_cards.count("Family Restaurant") # Assume there's 3 other players, that all have enough money
            x = random.randrange(0, 6 - count) #This isn't the best way to deal with random loss, Idk how to make better
            loss = self.Machi_red_cards(2, x)
            self.player_coins -= loss
            Gain = self.Machi_red_cards(2, count)
            self.player_coins += Gain
        if value == 10:
            count = self.player_cards.count("Apple Orchard")
            self.player_coins += 3 * count
        if value == 11:
            count = self.player_cards.count("Fruit and Vegetable Market")
            count2 = self.player_cards.count("Wheat field")
            self.player_coins += count * (count2 * 3)
        if value == 12:
            count = self.player_cards.count("Fruit and Vegetable Market")
            count2 = self.player_cards.count("Wheat field")
            self.player_coins += count * (count2 * 3)

        if self.amusement_park_buff:
            if roll1 == roll2:
                print(f"{roll1, roll2}, Amusement Doubles!!")
                self.roll()

    def build(self):
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
            print (f"Player holds. Current coins : {self.player_coins}")
            self.player_holds +=1
        if Build_roll == 8:
            if self.player_cards.count("Stadium") < 1 and self.player_cards.count("TV Station") < 1 and self.player_cards.count("Business Center") < 1:
                card = "Stadium"
                card_cost = 6
        if Build_roll == 9:
            if self.player_cards.count("Stadium") < 1 and self.player_cards.count("TV Station") < 1 and self.player_cards.count("Business Center") < 1:
                card = "TV Station"
                card_cost = 7
        if Build_roll == 10:
            if self.player_cards.count("Stadium") < 1 and self.player_cards.count("TV Station") < 1 and self.player_cards.count("Business Center") < 1:
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
            print (f"Player holds. Current coins : {self.player_coins}")
            self.player_holds +=1
        
        if card in self.game_cards:
            if self.player_coins >= card_cost :
                    self.player_spending(card_cost, card, Build_roll)
                    self.game_cards.remove(card)

    def player_spending(self, cost, card, sequence):
        self.player_coins -= cost
        self.player_cards.append(card)
        self.spending += cost
        self.buy_sequence.append(sequence)

    def Machi_red_cards(self,cost,card_amount):
        '''
        Tried to simplify the red cards in machi koro into a simple function.
        If the player has the shopping mall buff the cost increase by 1
        
        '''
        if self.player_coins > cost * card_amount:
            if self.shopping_mall_buff:
                cards_value = (cost + 1) * card_amount
            else:
                cards_value = cost * card_amount
            return cards_value
        else:
            return 0

    def business_center(self):
        lst = ["wheat field","ranch","bakery","cafe","convenience Store","forest","cheese Factory","furniture Factory","mine","family Restaurant","apple Orchard","fruit and Vegetable Market"]
        banned_lst = ["tV Station","business Center","stadium","train Station","shopping mall","amusement park","radio tower"]
        while True:
            y = random.choice(self.player_cards)
            if y not in banned_lst:
                self.player_cards.remove(y)
                x  = random.choice(lst)
                self.player_cards.append(x)
                self.trades += 1
                print(f"Player trades {y} and recives {x}")
                break

    def landmark(self):
        if  not self.player_cards.__contains__("train Station"):
            if self.player_coins >= 4:
                self.player_coins -= 4
                self.player_cards.append("train Station")
                print("Bot bought: train Station")
                self.landmark_build = True
                self.train_doubles = True
                self.buy_train = self.round
        if  not self.player_cards.__contains__("shopping mall"):
            if self.player_coins >= 10:
                self.player_coins -= 10
                self.player_cards.append("shopping mall")
                self.buy_shopping = self.round
                print("Bot bought: shopping mall")
                self.landmark_build = True
        if  not self.player_cards.__contains__("amusement park"):
            if self.player_coins >= 16:
                self.player_coins -= 16
                self.player_cards.append("amusement park")
                self.buy_amusement = self.round
                print("Bot bought: amusement park")
                self.landmark_build = True
        if  not self.player_cards.__contains__("radio tower"):
            if self.player_coins >= 22:
                self.player_coins -= 22
                self.player_cards.append("radio tower")
                print("Bot bought: radio tower")
                self.buy_radio = self.round
                self.landmark_build = True

    def round_end(self):
        self.landmark_build = False
        if self.player_cards.__contains__("train Station"):
            if self.player_cards.__contains__("shopping mall"):
                if self.player_cards.__contains__("amusement park"):
                    if self.player_cards.__contains__("radio tower"):
                        end_game_message = f"Game Over, bot completed game in {self.round} rounds"
                        print(end_game_message)
                        self.game_active = False
                        self.data_log()
        self.round += 1
    
    def data_log(self):
        count_cards = {}
        count_rolls = {}
        
        for cards in self.player_cards:
            count_cards[cards] = count_cards.get(cards, 0) + 1
        for roll in self.rolls:
            count_rolls[roll] = count_rolls.get(roll, 0) + 1
        
        game_log = {
            "Game": [self._game_number],
            "Number of Rounds": [self.round],
            "Value spent":[self.spending],
            "Number of Trades": [self.trades],
            "Number of Holds": [self.player_holds],
            "Number of Cards": [len(self.player_cards)],
            "Percent of Cards": [(len(self.player_cards)/72)*100],
            "Train Bought at round": [self.buy_train],
            "Shopping Bought at round": [self.buy_shopping],
            "Amusement Bought at round": [self.buy_amusement],
            "Radio Bought at round": [self.buy_radio],
            "Player Cards": [count_cards],
            "Dice Rolls": [count_rolls],
            "Sequence":[self.buy_sequence]
        }
        
        self.record_data(self._game_number,game_log)
        
    def record_data(self, game_number, game_log,):
        '''
        Records data to path file using openpyxl and pandas
        
        '''
        if game_number == 1:
            wb = Workbook()
            ws = wb.active
            ws.title = "Game Data"
            wb.save(self.dest_filename)

        df_read_data = pd.read_excel(self.dest_filename, "Game Data")
        df_data = df_read_data.head(self.number_of_games)
        df_game = pd.DataFrame(game_log,index=[game_number])
        excel = pd.concat([df_data,df_game])
        excel.to_excel(self.dest_filename,sheet_name="Game Data",index=False)
        
def main():
    MachiBot(2).game()
    
if __name__ == '__main__':
    main()