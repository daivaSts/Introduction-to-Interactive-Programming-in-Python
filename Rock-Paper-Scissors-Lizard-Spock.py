# GUI-based version of RPSLS

# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

###################################################
import simplegui
import random

# helper function converts a number in the range 0 to 4
def number_to_name(number):
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        return None
#helper function converts the string name into a number between 0 and 4    
def name_to_number(name):
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        return None
    
def rpsls(name):  
    #Convert name to player_number using name_to_number function
    player_number = name_to_number(name)
        
    #Compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)
    
    #Check if given name is valid
    if player_number == None:
        print ""
        print "Error: Bad input '" + name +"' to RPSLS"
        return
    
    message1 = "Player chooses " + number_to_name(player_number)+"\n"
    message2 = "Computer chooses " +number_to_name(comp_number)+"\n"
    
    #Determine and print out the winner
    if (comp_number - player_number)%5 == 1:
        print message1, message2, "Computer wins!\n"
        
    elif (comp_number - player_number)%5 == 2:
        print message1, message2, "Computer wins!\n"    
        
    elif (comp_number - player_number)%5 == 3:
        print message1, message2,"Player wins!\n"
        
    elif (comp_number - player_number)%5 == 4:
        print message1, message2,"Player wins!\n"    
        
    else:
        print message1, message2,"Player and computer tie!\n"
    
# Create frame and assign callbacks to event handlers
frame = simplegui.create_frame("GUI-based RPSLS", 200, 200)
frame.add_label("*** RPSL game ***")
frame.add_input("Enter guess here", rpsls, 200)


# Start the frame animation
frame.start()


###################################################
# Test

#rpsls("Spock")
#rpsls("dynamite")
#rpsls("paper")
#rpsls("lazer")

###################################################
# Sample expected output from test
# Note that computer's choices may vary from this sample.

#Player chose Spock
#Computer chose paper
#Computer wins!
#
#Error: Bad input "dynamite" to rpsls
#
#Player chose paper
#Computer chose scissors
#Computer wins!
#
#Error: Bad input "lazer" to rpsls
#
