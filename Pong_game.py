# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [1,1]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
s_pressed = True
w_pressed = True
up_pressed = True
down_pressed = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists 
    if direction == RIGHT:
        ball_vel[0] = random.randrange (120,240)/60.0
        ball_vel[1] = - random.randrange (60,180)/60.0
    if direction == LEFT:
        ball_vel[0] = - random.randrange (120,240)/60.0
        ball_vel[1] = - random.randrange (60,180)/60.0
    
    # spawn ball from the center of canvas    
    ball_pos[0] = WIDTH / 2 + ball_vel[0]
    ball_pos[1] = HEIGHT / 2 + ball_vel[1]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are int
    
    # choose random direction LEFT or RIGHT for the ball velocity
    spawn_ball(random.choice([LEFT, RIGHT]))
    
    # reset score for a new game
    score1 = 0
    score2 = 0
    
    # reset initial paddle positions for a new game
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel,s_pressed,w_pressed,up_pressed,down_pressed
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # testing whether the ball touches with the left or right gutters/increase speed on both x and y/update score
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH: 
        if ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT and ball_pos[1] > paddle1_pos - HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
        
    elif ball_pos[0] >= WIDTH- PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT and ball_pos[1] > paddle2_pos - HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)
        
    # bounce ball from the bottom or the top walls   
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
      
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position based on status of the key
    if s_pressed == True:
        paddle1_pos += paddle1_vel
        
    if  w_pressed == True:
        paddle1_pos += paddle1_vel
        
    if up_pressed == True:    
        paddle2_pos += paddle2_vel
        
    if down_pressed == True: 
        paddle2_pos += paddle2_vel
        
    
    # keep paddles on the screen - stop when they reach the top or bottom walls
    if paddle1_pos < HALF_PAD_HEIGHT or paddle1_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_vel = 0
        
    if paddle2_pos < HALF_PAD_HEIGHT or paddle2_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_vel = 0
    
    # draw paddles
    c.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT],[HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, 'White')
    c.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT],[WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH, 'White')
    
    # draw scores
    c.draw_text(str(score1) + " "*15 + str(score2), [200, 40], 40,  "Lime")

# update values of the vertical velocities of the paddles, change status of the key   
def keydown(key):
    global paddle1_vel, paddle2_vel,s_presses,w_presses,up_presses, down_presses
    velocity_constant = 4
   
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += velocity_constant
        s_pressed = True
           
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += velocity_constant 
        down_pressed = True
        
    if key == simplegui.KEY_MAP ["w"]:
        paddle1_vel -= velocity_constant
        w_pressed = True
        
    if key == simplegui.KEY_MAP ["up"]:
        paddle2_vel -= velocity_constant 
        up_pressed = True

# update the vertical velocities when keys are unpressed, change status of the key         
def keyup(key):
    global paddle1_vel, paddle2_vel, s_presses,w_presses,up_presses,down_presses
  
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
        s_pressed = False
        
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
        w_pressed = False
        
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
        up_pressed = False

    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0 
        down_pressed = False
 
    
#restart the game
def button():
    new_game()
    
# create frame and register events
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", button, 100)
frame.add_label("Keybord controls: ")
frame.add_label("Leftside player: 'w'(up),'s'(down) ")
frame.add_label("Rightside player: 'up arrow' (up),'down arrow'(down)")
# start frame
frame.start()
new_game()