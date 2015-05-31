# ****** Spaceship ****** 
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
   
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35) #(self, center, size, radius = 0, lifespan = None, animated = False)DS
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(0.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound.set_volume(0.5)

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle  
        self.angle_vel = 0 
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        # drawing the ship image with or without thrust flames based on thrust is on/off:        
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image,[self.image_center[0] + self.image_size[0],self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)    

    def update(self):
        
        self.pos[0] = self.pos[0]%WIDTH 	# ship's position wraps around the screen when it goes off the edge
        self.pos[1] = self.pos[1]%HEIGHT
        
        self.pos[0] += self.vel[0]			# update the position of the ship based on its velocity
        self.pos[1] += self.vel[1]
        
        self.angle += self.angle_vel		 # update the ship angle by its angular velocity
        forward = [math.cos(self.angle), math.sin(self.angle)] # compute the forward vector pointing in the direction 
                                                               # the ship is facing based on the ship's angle.
        
        if self.thrust:						# method to accelerate the ship in the direction of this forward vector
            self.vel[0] += forward[0]		# when the ship is thrusting.
            self.vel[1] += forward[1]
        
        self.vel[0] *= 0.95					# adding friction for the ship to slow down.
        self.vel[1] *= 0.95
    
    def angular_vel_increase(self):			# increment and decrement the ship's angular velocity by a fixed amount.
        self.angle_vel += 0.1
        
    def angular_vel_decrease(self):
        self.angle_vel -= 0.1
    
    def thrust_on_off(self, keys):			#  logic to turn the ship's thrusters on/off, play sounds accordingly.
        if keys == "keydown":
            self.thrust = True
            ship_thrust_sound.play()		
           
        if keys == "keyup":
            self.thrust = False
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
                    
    def shoot(self):						# craeting and spawning a new missile.
        global a_missile
        a_missile.pos[0]= self.pos[0] + self.radius * math.cos(self.angle)		# calculate position and velocity based 
        a_missile.pos[1]= self.pos[1] + self.radius * math.sin(self.angle)		# on the ship's position and velocity.
        a_missile.vel[0]= self.vel[0] + math.cos(self.angle)
        a_missile.vel[1]= self.vel[1] + math.sin(self.angle)
        
        a_missile = Sprite([a_missile.pos[0], a_missile.pos[1]], [a_missile.vel[0],a_missile.vel[1]], 0, 0, missile_image, missile_info, missile_sound)
        missile_sound.play()				# play missile sound
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None): 
        self.pos = [pos[0],pos[1]]		
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self): 
        self.angle += self.angle_vel		# update an angle and position to make the sprite move and rotate.
        self.pos[0] += self.vel[0]	
        self.pos[1] += self.vel[1]
        
        self.pos[0] = self.pos[0]%WIDTH		# sprite's position wraps around the screen when it goes off the edge
        self.pos[1] = self.pos[1]%HEIGHT
                 
def draw(canvas):
    global time, a_rock, a_missile, score, lives
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites 
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
   
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()  
    
    # update score and lives   
    canvas.draw_text("Score: "+ str(score), [WIDTH*3/5, HEIGHT/10],40, "Fuchsia") # text displaying score and lives
    canvas.draw_text("Lives: "+ str(lives), [WIDTH/4, HEIGHT/10],40, "Fuchsia")
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    
    random_list = [-0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 1]			# calculating random rock position, velocity  
    rock_pos = [random.randrange(1, WIDTH), random.randrange(1, HEIGHT)]	# and angular velocity
    rock_vel = [random.choice(random_list),random.choice(random_list)]
    rock_ang_vel = random.choice(random_list[2:4])
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_ang_vel, asteroid_image, asteroid_info) # creating a new rock per second

# key handlers
def keydown(key):
    global a_missile
    
    if key == simplegui.KEY_MAP["up"]:		# controls the thrusters of the spaceship
        my_ship.thrust_on_off("keydown")
        
    if key == simplegui.KEY_MAP["left"]:	# the ship turns in response to the pressed left/right arrow keys when 
        my_ship.angular_vel_decrease()		# increasing or decreasing angular velocity
        
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angular_vel_increase()
        
    if key == simplegui.KEY_MAP["space"]:    # shoots the missile
        my_ship.shoot()
            
def keyup(key):
   
    if key == simplegui.KEY_MAP["up"]:		# stops the ship thrusting  
        my_ship.thrust_on_off("keyup")		# 
        
    if key == simplegui.KEY_MAP["left"]:	# the ship stops turning in response to the un-pressed left/right arrow keys  
        my_ship.angular_vel_increase()		# when increasing or decreasing angular velocity
             
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angular_vel_decrease()
               
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0,0], 0, ship_image, ship_info) 
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0.3, 0.3], 0, 0.1, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
