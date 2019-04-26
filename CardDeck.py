import random

class Card:
    """ Represents a standard playing card object """
    
    suits = ("CLUBS", "DIAMONDS", "HEARTS", "SPADES")
    ranks = ("TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "JACK", "QUEEN", "KING", "ACE")
    values = {"TWO":2, "THREE":3, "FOUR":4, "FIVE":5, "SIX":6, "SEVEN":7, "EIGHT":8, "NINE":9, "TEN":10, "JACK":10, "QUEEN":10, "KING":10, "ACE":1}
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)
    
    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank

class Deck:
    """ Create a deck of 52 cards and include methods to shuffle, deal and get information """
    def __init__(self):
        self.deck = []
        for suit in Card.suits:
            for rank in Card.ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        full_deck = ""
        for card in self.deck:
            full_deck += "\n"+card.__str__()
        return "The deck has: "+full_deck   

    def get_id(self, id):
        return list(map(lambda x: str(x), self.deck)).index(id)    
    
    def get_deck(self):
        return list(map(lambda x: str(x), self.deck)) 
    
    def deck_size(self):
        return len(self.deck)
    
    def shuffle(self):
        random.shuffle(self.deck)
		
    def deal_card(self):
        single_card = self.deck.pop()
        return single_card
    
class Hand:
    """ Includes methods to add cards and get information out of these cards """
    def __init__(self):
        self.cards = []
    
    def __str__(self):
        result = ""
        for card in self.cards:
            result += card.__str__()+", "
        return "Hand contains: "+result

    def get_hand(self):
        return list(map(lambda x: str(x), self.cards))  
    
    def get_id(self, id):
        return list(map(lambda x: str(x), self.cards)).index(id)      
    
    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        """ Count aces as 1 as long as hand does not go bust. Count aces 10 when 10+11 = 21"""
        value = 0
        contains_ace = False
        
        for card in self.cards:
            rank = card.get_rank()
            value += Card.values[rank]
            
            if rank == "ACE":
                contains_ace = True
        
        if value <= 11 and contains_ace:
            value += 10
        
        return value

class Chips:
    """ Method to initialise bank object and track bet outcomes """
    def __init__(self, total=1000):
        self.total = total # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def __str__(self):
        return self.total
    
    def win_bet(self):
        self.total += self.bet*2 # x2 is necessary because every time bet is made, bank is automatically deducted.
        return self.total
		
    def lose_bet(self):
        self.total -= self.bet
        return self.total