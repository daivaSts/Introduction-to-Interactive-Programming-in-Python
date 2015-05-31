# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")  

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images,card_loc,CARD_SIZE,[pos[0]+ CARD_CENTER[0],pos[1]+ CARD_CENTER[1]],CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
        self.hand_value = 0

    def __str__(self):
        return "Hand contains " + " ".join(str(card) for card in self.hand)+" "

    def add_card(self, card):
        return self.hand.append (card)       

    def get_value(self):
        hand_value = 0				
        if len(self.hand) == 0:		# If hand is empty, return 0	
            return hand_value
        else:
            for card in self.hand:  							# Checking, if there is an ace in the hand.
                if card.get_rank() != "A": 						# Computing the value of a hand, 
                    hand_value += VALUES[card.get_rank()]		# taking the values from VALUES dictionery. 
                elif hand_value + 10 <= 21:						# Depending on the total hand value
                    hand_value += (VALUES[card.get_rank()]+10)	# an ace may be valued as either 1 or 11.
        return hand_value
    
    def draw(self, canvas, pos):					# Draw method for the Hand class using the draw 
        for card in self.hand:						# method of the Card class. Looping through cards,
            card.draw(canvas, [pos[0], pos[1]])		# incrementing x position
            pos[0] += 100
                   
# define deck class 
class Deck:
    def __init__(self):															# Modeling a full deck of cards as 
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]		# list of 52 cards.

    def shuffle(self):								# Shuffle the deck of cards
        return random.shuffle(self.deck)			# for each new game.

    def deal_card(self):							# After the card is dealt,
        return self.deck.pop()						# the card is removed from the Deck.
   
    def __str__(self):
        return "Deck contains " + ' '.join(str(card) for card in self.deck)      
       
#define event handlers for buttons
def deal():
    global outcome, in_play,  player_hand, dealer_hand, deck, score
    
    player_hand = Hand()		# Creating new player, dealer hands,deck objects 
    dealer_hand = Hand()		
    deck = Deck()				
                                
    if in_play == True:			# The logic keeps track of whether the
        score -= 1				# "Deal" button is clicked during the middle of a round.
        
    in_play = True				# Initial status for a new game and the dealer's hole card
    deck.shuffle()				# Shuffle the deck for a new game
            
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
       
    if player_hand.get_value() == 21:		# In case the first deal card value is 21
        outcome = "Stand?"
    else: 									
        outcome = "Hit or stand?"

         
def hit():
    global  player_hand, dealer_hand, outcome, in_play, score    
    if in_play == False:							# Logic to prevent the hit button of adding any cards,  
        pass    									# if the game is over (someove already has won or busted)
    else:
        player_hand.add_card(deck.deal_card())

        if player_hand.get_value()  > 21:			# To keep track of the value,score and status of the game
            outcome = "You have busted. New Deal?"	# of the players hand,
            score -= 1								# and print messages accordingly.
            in_play = False        
        elif player_hand.get_value() == 21:
            outcome = "Stand?"
        elif player_hand.get_value() < 21:
            outcome = "Hit or stand?"
                           
def stand():
    global  player_hand, dealer_hand, outcome, in_play, score, image_back  
    
    in_play = False			# The logic keeps track of the dealer's hole card
                            # and if the players round is over 

    while dealer_hand.get_value() < 17:						# To keep track of the value and score
            dealer_hand.add_card(deck.deal_card()) 			# of the game of the deales hand
            
    if dealer_hand.get_value() > 21:
        outcome = "Dealer is busted. New Deal?"				
        score += 1											
        
    elif player_hand.get_value() <= dealer_hand.get_value():# Comparing dealers and players hands, 
        outcome = "Dealer wins. New Deal?"					# and printing messages, changing score
        score -= 1											# accordingly.										
        
    elif player_hand.get_value() > dealer_hand.get_value():	
        outcome = "Player wins!!!! New Deal?"				
        score += 1											

# draw handler    
def draw(canvas):
    global player_hand, dealer_hand, outcome, in_play, score, pos, image_back
   
    canvas.draw_text ("Score: "+str(score), [400,70], 40, "Orange")
    canvas.draw_text ("BLACKJACK", [50,80], 55, "Navy")
    canvas.draw_text ("Dealer", [50,220], 40, "Lime")
    canvas.draw_text ("Player", [50,420], 40, "Lime")
    canvas.draw_text (outcome, [50,160], 40, "Orange")
    
    dealer_hand.draw(canvas,[50,240])  # Drawing card images to canvas, passing position for the 1st card
    player_hand.draw(canvas,[50,440])  # for dealers and players hands.

    if in_play == True:			   # Drawing back side of the card for 1st dealers card.
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (85.5,288), CARD_BACK_SIZE)
           

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()