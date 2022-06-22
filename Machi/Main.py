"""
Machi Koro Bot V2 - Main
By Thomas Robertson

"""
import Players
import Cards

class MainBot:
    def __init__(self, games, players):
        self.number_of_games = games
        self.number_of_players = players
        self.game_number = 1
    def start_game(self):
        Players.set_start(self.number_of_players)
        Cards.Card.set_start()

    
def main():
    MainBot(2,2).start_game()
    
if __name__ == '__main__':
    main()