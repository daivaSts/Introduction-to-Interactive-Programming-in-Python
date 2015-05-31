""" 'Guess the number' mini-project """

import simplegui
import random

# initialize global variables used in codeccode
high = 100
secret_num = 0
guess = 0
count = 7

# helper function to start and restart the game
def new_game():
    global secret_num, count
    secret_num = random.randint(0,high)
    #restart the counter
    if high == 100:
        count = 7
    else:
        count = 10
    print "New game started within the range 1-" + str(high) + ".\n"
    return secret_num, count

# define event handlers for control panel
def range100():
    global high, count
    high = 100
    new_game()
    
def range1000():
    global high, count 
    high = 1000
    new_game()

def input_guess(guess):
    global count
    count -= 1
    if count == -1:
        print "You ran out of guesses! The number was " + str(secret_num)+".\n"
        new_game()
  
    if secret_num == int(guess):
        print "Correct!\n"
        new_game()
    elif secret_num > int(guess):
        print "Higher.\nNumber of guesses remaining: " + str(count)+".\n"
    else:
        print "Lower.\nNumber of guesses remaining: " + str(count)+".\n"
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
frame.add_label("Pick the range:")
frame.add_button("Range: 0 -  100", range100)
frame.add_button("Range: 0 - 1000", range1000)
frame.add_input("Type your guess here:",input_guess, 120)

# call new_game and start frame
new_game()
frame.start()

