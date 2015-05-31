# "Stopwatch: The Game" #2
import simplegui

# define global variables
b = 0
output = ""
count_tries = 0
count_wins = 0
clock_C = 0

# helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(b):
    global clock_C
    clock_A = b//600
    clock_B = (b-(b//600)*600)//100
    clock_C = ((b-(b//600)*600) - ((b-(b//600)*600)//100)*100)/10
    clock_D = b%10
    return str(clock_A)+':'+str(clock_B)+str(clock_C)+'.'+str(clock_D)

# event handlers for buts; "Start", "Stop", "Reset"
def start ():
    global count_tries
    count_tries += 1
    timer.start()
    
def stop():
    global count_wins, clock_C
    timer.stop()
    if b%10 == 0 and (clock_C == 0 or clock_C == 5):
        count_wins += 1
        print clock_C
    
    
def reset():
    global b, count_tries, count_wins
    b = 0
    count_tries = 0
    count_wins = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global b
    b += 1
    

# define draw handler
def draw(canvas):
        
    #output = format (b)
    canvas.draw_text(format (b),[130,120],48,"white", "sans-serif")
    canvas.draw_text(str(count_tries),[295,50],24,"green", "sans-serif")
    canvas.draw_text(str(count_wins),[335,50],24,"green", "sans-serif")
    canvas.draw_text("/",[325,50],24,"green", "sans-serif")
    
# create frame
frame = simplegui.create_frame ("Stopwatch: The Game", 400, 200)
timer = simplegui.create_timer (1000, tick)

# event handlers
frame.add_button ("Start", start, 50)
frame.add_button ("Stop", stop, 50)
frame.add_button ("Reset", reset, 50)
frame.set_draw_handler(draw)

# start frame
frame.start()


# Please remember to review the grading rubric
