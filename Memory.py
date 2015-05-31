# implementation of card game - Memory
import simplegui
import random

# helper function to initialize globals
state = 0 	#game state
counter = 0	#turn counter
deck = []	#list of cards 
exposed = [False]*16	#list of boolean values to track flipped/exposed cards
last_two_up = []	#index list to track last two exposed cards

def new_game():
    global deck, exposed, counter, state, last_two_up
    
    # reset variables for a new game
    state = 0
    counter = 0
    deck = []
    exposed = [False]*16
    last_two_up = []

    label.set_text("Turns = %d" % counter)
    
    # creating a list representing a  deck of cards 
    for i in range(0,8):
        deck.append(i)
    deck = deck *2   
    random.shuffle(deck)

# define event handlers
def mouseclick(pos):
    global exposed, counter, state, last_two_up
    
    # determining card index
    x = pos[0] // 50
    
    if exposed[x] == False:		# if card is not exposed
        last_two_up.append(x)	# add card index to a temp list which traks last 2 cards
        
        if state == 0:			 
            state = 1			# change status of the game
            exposed[x] = True	# and the card status

        elif state == 1:    	
            state = 2			# change status of the game
            counter += 1		# add counter
            exposed[x] = True	# change the card status
             
        else:
            if deck[last_two_up[0]] != deck[last_two_up[1]]: # checking if cards have maching numbers
                exposed[last_two_up[0]] = False				 # if not, "flipping" the cards
                exposed[last_two_up[1]] = False        
            last_two_up = last_two_up[2:]				 	 # if yes, "removing" them from the memory			
            state = 1										 
            exposed [x] = True							     # change the card status		
        
    label.set_text("Turns = %d" % counter)				     # updating the "Turns" label		
    
def draw(canvas):
    # drawing cards - face or back side - depending on the status of the card in exposed list
    for num in range(0,16):
        if exposed[num] ==  True:
            canvas.draw_text(str(deck[num]), [num*50 + 10,70], 50, "white")   
        else:     
            canvas.draw_polygon(([num*50, 0],[num*50, 100],[(num+1)*50, 100],[(num+1)*50, 0]),1, "black", "green")
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turn count")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()