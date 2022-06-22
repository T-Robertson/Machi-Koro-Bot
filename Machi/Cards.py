"""
Machi Koro Bot V2 - Cards
By Thomas Robertson

"""
class Card:
    def __init__(self):
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
    def set_start(self):
        for x in range(6):
            for x in self.game_cards:
                self.card_pool.append(x)