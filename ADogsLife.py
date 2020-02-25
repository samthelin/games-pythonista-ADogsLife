"""
A Dog's Life, a game for the iPhone developed in Pythonista using the Scene module. 

In the game you play as the character of a dog chasing a wolf on a forest meadow. 

You move the dog using the iPhone's built-in gyroscope and accelerometer. 
"""

from scene import *
from random import *
import random
import math 
import numpy
import sound

#The class of the dog, the protagonist of the game. The dog is built up of circular
#shape nodes which are positioned relative to each other. 
class Dog (ShapeNode):
        def __init__(self, **kwargs):
                ShapeNode.__init__(self, ui.Path.oval(0, 0, 20, 20), 'brown', **kwargs) 
                self.head = ShapeNode(ui.Path.oval(0, 0, 18, 18), 'brown')
                self.lear = ShapeNode(ui.Path.oval(0, 0, 7, 7), '#a53e11')
                self.rear = ShapeNode(ui.Path.oval(0, 0, 7, 7), '#a53e11')
                self.nose = ShapeNode(ui.Path.oval(0, 0, 5, 5), 'black')
                self.tail1 = ShapeNode(ui.Path.oval(0, 0, 5, 5), 'brown')
                self.tail2 = ShapeNode(ui.Path.oval(0, 0, 5, 5), 'brown')
                self.tail3 = ShapeNode(ui.Path.oval(0, 0, 5, 5), 'white')
                self.add_child(self.head)
                self.head.position = (0, 10)
                self.add_child(self.tail1)
                self.add_child(self.tail2)
                self.add_child(self.tail3)
                self.tail1.position = (0, -9)
                self.tail2.position = (0, -13)
                self.tail3.position = (0, -17)
                self.head.add_child(self.lear)
                self.head.add_child(self.rear)
                self.head.add_child(self.nose)
                self.lear.position = (8 * math.cos(7 * math.pi / 8), 8 * math.sin(7 * math.pi / 8))
                self.rear.position = (8 * math.cos(1 * math.pi / 8), 8 * math.sin(1 * math.pi / 8))
                self.nose.position = (10 * math.cos(2 * math.pi / 4), 10 * math.sin(2 * math.pi / 4))
                self.turn_head_status = True #This boolean controls if the dog is turning its head. 
                self.max_speed = 10
                self.gait = 15 #Controls with which frequency paw prints are made. 
                self.move_time = 0
                self.radius = 10
        
        #This method returns the paw print of the dog. Each animal in the game (so far there are only dogs and wolves)
        #have their own paw print, which they leave in their wake as they move forward. 
        def paw_print(self):
                paw = ShapeNode(ui.Path.oval(0, 0, 5, 5), 'black') 
                toes = []       
                for i in range(3):
                        toes.append(ShapeNode(ui.Path.oval(0, 0, 2.5, 2.5), 'black'))
                        paw.add_child(toes[i])
                        toes[i].position = (5 * math.cos((2 + i) * math.pi / 6), 5 * math.sin((2 + i) * math.pi / 6))
                return paw
        
        #This method controls the turning of the dog's head. The dog looks around itself when sitting still. In a future version, 
        #where the dog is looking will indicate the location of a wolf. 
        def turn_head(self, velocity):
                actions = [Action.wait(1), Action.rotate_by(-math.pi / 8, 1), Action.wait(2), Action.rotate_by(math.pi / 4, 2), Action.wait(2), Action.rotate_by(-math.pi / 8, 1), Action.call(self.change_turn_head)]

                if velocity < 0.05:
                        if self.turn_head_status:
                                self.turn_head_status = False   
                                self.head.run_action(Action.sequence(actions), 'turn_head')
                else:
                        self.head.remove_action('turn_head')
                        self.head.rotation = 0
                        self.turn_head_status = True    

        def change_turn_head(self):
                if self.turn_head_status:
                        self.turn_head_status = False
                else:
                        self.turn_head_status = True    

        #This method calculates the velocity of the dog based on the input, which is given by the 
        #position of the iPhone, making sure that the dog does not exceed its maximum velocity. 
        def velocity(self, u, v):
                if abs(u) > 0.05:
                        if abs(u) < 1:
                                U = u * self.max_speed
                        else:
                                U = (u / abs(u)) * self.max_speed 
                else: 
                        U = 0

                if abs(v) > 0.05:
                        if abs(v) < 1:
                                V = v * self.max_speed
                        else:
                                V = (v / abs(v)) * self.max_speed
                else:
                        V = 0  

                return [U, V]
        
        #This method calculates the speed given the velocity. 
        def speed(self, velocity):
                u = velocity[0]
                v = velocity[1]
                speed = math.sqrt(u * u + v * v)
                return speed
        
        #This method controls the animation of the dog when its moving. As the dog runs faster,
        #it stretches out, and the various body parts increase and decrease in size in a periodic 
        #fashion, to simulate the effect of the dog moving up and down. It also sees to that
        #the body parts are properly aligned with the direction of movement. 
        def move(self, u, v):
                t = self.move_time
                ang = numpy.angle(numpy.complex(u, v))
                vel = min(math.sqrt(u * u + v * v), 0.7)

                if abs(u) > 0.05 or abs(v) > 0.05:
                        f = 2 - vel
                        t += 1
                        r_1 = 20 + (1 + vel) * math.sin(f * t / 10)
                        r_2 = 20 + (1 + vel) * math.sin(f * (t + 10) / 10)
                        r_3 = 7 * r_2 / 20
                        r_4 = 5 * r_2 / 20
                        r_5 = 7 + (0.25 + 0.5 * vel) * math.sin(f * (t - 10) / 5)
                        r_6 = 7 + (1 + vel) * math.sin(f * (t - 20) / 5)
                        r_7 = 7 + (1 + vel) * math.sin(f * (t - 30) / 5)
                        self.size = (r_1, r_1)
                        self.head.size = (r_2, r_2)
                        self.lear.size = (r_3, r_3)
                        self.rear.size = (r_3, r_3)
                        self.nose.size = (r_4, r_4)
                        self.tail1.size = (r_5, r_5)
                        self.tail2.size = (r_6, r_6)
                        self.tail3.size = (r_7, r_7)
                        self.rotation = ang - math.pi / 2 
                        self.move_time = t 
                        self.head.position = (0, 10 + 13 * vel)
                        self.tail1.position = (self.tail1.position.x, -9 - 5 * vel )
                        self.tail2.position = (self.tail2.position.x, -13 - 10 * vel)
                        self.tail3.position = (self.tail3.position.x, -17 - 15 * vel)
        
        #Being a happy dog, it always wags its tail. In a future version, the dog will cease
        #wagging a tail when it senses the presence of a wolf. 
        def wag_tail(self, t):
                self.tail1.position = (math.sin(0.1 * t), self.tail1.position.y)
                self.tail2.position = (3 * math.sin(0.1 * t - 1), self.tail2.position.y)
                self.tail3.position = (6 * math.sin(0.1 * t - 2), self.tail3.position.y) 

#The class of the wolf, the dog's antagonist. It is very similar to the dog class, with the main exception that 
#the wolf has an additional velocity method, which allows it to move automatically across the screen in a 
#seemingly random fashion. The wolf also has a counter attached to it, which keeps track of how often 
#it has been attacked by the dog (more accurately, how much life it has still got). 
class Wolf (ShapeNode):
        def __init__(self, **kwargs):
                ShapeNode.__init__(self, ui.Path.oval(0, 0, 20, 20), 'gray', **kwargs) 
                self.head = ShapeNode(ui.Path.oval(0, 0, 18, 18), 'gray')
                self.lear = ShapeNode(ui.Path.oval(0, 0, 7, 7), '#b3b3b3')
                self.rear = ShapeNode(ui.Path.oval(0, 0, 7, 7), '#b3b3b3')
                self.nose = ShapeNode(ui.Path.oval(0, 0, 5, 5), 'black')
                self.tail1 = ShapeNode(ui.Path.oval(0, 0, 5, 5), 'gray')
                self.tail2 = ShapeNode(ui.Path.oval(0, 0, 5, 5), 'gray')
                self.tail3 = ShapeNode(ui.Path.oval(0, 0, 5, 5), 'white')
                self.add_child(self.head)
                self.head.position = (0, 10)
                self.add_child(self.tail1)
                self.add_child(self.tail2)
                self.add_child(self.tail3)
                self.tail1.position = (0, -9)
                self.tail2.position = (0, -13)
                self.tail3.position = (0, -17)
                self.head.add_child(self.lear)
                self.head.add_child(self.rear)
                self.head.add_child(self.nose)
                self.lear.position = (8 * math.cos(7 * math.pi / 8), 8 * math.sin(7 * math.pi / 8))
                self.rear.position = (8 * math.cos(1 * math.pi / 8), 8 * math.sin(1 * math.pi / 8))
                self.nose.position = (10 * math.cos(2 * math.pi / 4), 10 * math.sin(2 * math.pi / 4))
                self.turn_head_status = True
                self.max_speed = 7
                self.gait = 15
                self.time = 0
                self.move_time = 0
                self.radius = 10
                self.speed_x = 0
                self.speed_y = 0
                self.relative_speed_x = self.speed_x / self.max_speed
                self.relative_speed_y = self.speed_y / self.max_speed
                self.health = 100

                self.health_font = ('Futura',15)
                self.health_label = LabelNode('100', self.health_font, parent=self, color = 'black')
                #self.add_child(self.health_label)
                self.health_label.position = (20, 20)
        
        #Just like the dog, the wolf leaves paw prints. 
        def paw_print(self):
                paw = ShapeNode(ui.Path.oval(0, 0, 5, 5), 'black') 
                toes = []       
                for i in range(3):
                        toes.append(ShapeNode(ui.Path.oval(0, 0, 2.5, 2.5), 'black'))
                        paw.add_child(toes[i])
                        toes[i].position = (5 * math.cos((2 + i) * math.pi / 6), 5 * math.sin((2 + i) * math.pi / 6))
                return paw
        
        #The wolf also has a method for turning its head. In practice, this does not happen when the automatic 
        #velocity method is used for the wolf however, as it does not come to a stand-still. 
        def turn_head(self, velocity):
                actions = [Action.wait(1), Action.rotate_by(-math.pi / 8, 1), Action.wait(2), Action.rotate_by(math.pi / 4, 2), Action.wait(2), Action.rotate_by(-math.pi / 8, 1), Action.call(self.change_turn_head)]

                if velocity < 0.05:
                        if self.turn_head_status:
                                self.turn_head_status = False   
                                self.head.run_action(Action.sequence(actions), 'turn_head')
                else:
                        self.head.remove_action('turn_head')
                        self.head.rotation = 0
                        self.turn_head_status = True    

        def change_turn_head(self):
                if self.turn_head_status:
                        self.turn_head_status = False
                else:
                        self.turn_head_status = True    
        
        #This method allows the wolf to move automatically. It moves according to the sum of to trigonometric 
        #functions with different periodicity and amplitude, in order to achieve a smooth moving pattern which 
        #appears semi-random. The parameters have been determined through trial and error. 
        def velocity(self, u, v):
                t = self.time
                self.speed_x =  -5 * math.sin(t * 2 * math.pi / 700) + 2 * math.sin(t * 2 * math.pi / 400)

                self.speed_y = -5 * math.cos(t * 2 * math.pi / 2300) + 3 * math.cos(t * 2 * math.pi / 400)

                t += 1
                self.time = t

                self.relative_speed_x = self.speed_x / self.max_speed
                self.relative_speed_y = self.speed_y / self.max_speed

                U = self.speed_x 
                V = self.speed_y 

                return [U, V]

        #The wolf also has a manual velocity method, making it possible to play as the wolf instead
        #(it is mostly used for testing purposes though). 
        def velocity_manual(self, u, v):
                if abs(u) > 0.05:
                        if abs(u) < 1:
                                U = u * self.max_speed
                        else:
                                U = (u / abs(u)) * self.max_speed 
                else: 
                        U = 0

                if abs(v) > 0.05:
                        if abs(v) < 1:
                                V = v * self.max_speed
                        else:
                                V = (v / abs(v)) * self.max_speed
                else:
                        V = 0  

                return [U, V]

        #Calculates the speed give the velocity. 
        def speed(self, velocity):
                u = velocity[0]
                v = velocity[1]
                speed = math.sqrt(u * u + v * v)
                return speed

        #Just as for the dog, this method controls the animation of the wolf as it moves, trying 
        #to make its movements look somewhat dynamic. 
        def move(self, u, v):
                t = self.move_time
                ang = numpy.angle(numpy.complex(u, v))
                vel = min(math.sqrt(u * u + v * v), 0.7)

                if abs(u) > 0.05 or abs(v) > 0.05:
                        f = 2 - vel
                        t += 1
                        r_1 = 20 + (1 + vel) * math.sin(f * t / 10)
                        r_2 = 20 + (1 + vel) * math.sin(f * (t + 10) / 10)
                        r_3 = 7 * r_2 / 20
                        r_4 = 5 * r_2 / 20
                        r_5 = 7 + (0.25 + 0.5 * vel) * math.sin(f * (t - 10) / 5)
                        r_6 = 7 + (1 + vel) * math.sin(f * (t - 20) / 5)
                        r_7 = 7 + (1 + vel) * math.sin(f * (t - 30) / 5)
                        self.size = (r_1, r_1)
                        self.head.size = (r_2, r_2)
                        self.lear.size = (r_3, r_3)
                        self.rear.size = (r_3, r_3)
                        self.nose.size = (r_4, r_4)
                        self.tail1.size = (r_5, r_5)
                        self.tail2.size = (r_6, r_6)
                        self.tail3.size = (r_7, r_7)
                        self.rotation = ang - math.pi / 2 
                        self.move_time = t 
                        self.head.position = (0, 10 + 13 * vel)
                        self.tail1.position = (self.tail1.position.x, -9 - 5 * vel )
                        self.tail2.position = (self.tail2.position.x, -13 - 10 * vel)
                        self.tail3.position = (self.tail3.position.x, -17 - 15 * vel)
                        self.health_label.rotation = math.pi / 2 - ang

        #The wolf can also wag its tail. 
        def wag_tail(self, t):
                self.tail1.position = (math.sin(0.1 * t), self.tail1.position.y)
                self.tail2.position = (3 * math.sin(0.1 * t - 1), self.tail2.position.y)
                self.tail3.position = (6 * math.sin(0.1 * t - 2), self.tail3.position.y) 

#A primitive class for the flowers on the meadow. This has practically been replaced by the 
#updated flower class below. 
class Flower (ShapeNode):
        def __init__(self, **kwargs):
                ShapeNode.__init__(self, ui.Path.oval(0, 0, 10, 10), 'pink', **kwargs) 
                self.cen = ShapeNode(ui.Path.oval(0, 0, 3, 3), 'yellow')
                self.add_child(self.cen)

#The class for the flowers on the meadow. These are built out of shape nodes. Each flower has 
#a yellow centre and five white petals. 
class Flower2 (ShapeNode):
        def __init__(self, **kwargs):
                ShapeNode.__init__(self, ui.Path.oval(0, 0, 5, 5), 'black', **kwargs) 

                self.z_position = 0.5

                petals = []

                for i in range(5):
                        petals.append(ShapeNode(ui.Path.oval(0, 0, 5,5), 'white'))
                        self.add_child(petals[i])
                        petals[i].position = (2.5 * math.cos(2 * math.pi * i / 5), 2.5 * math.sin(2 * math.pi * i / 5))

                cen = ShapeNode(ui.Path.oval(0, 0, 5,5), 'yellow')
                self.add_child(cen)

#The class for the trees making the forest around the meadow, which function as the the bound for 
#the game area. 
class Tree (ShapeNode):
        def __init__(self, **kwargs):
                ShapeNode.__init__(self, ui.Path.oval(0, 0, 150, 150), '#006900', **kwargs) 

#The class taking care of the actual runnning of the game.                 
class Game (Scene):
        def setup(self):
                self.background_color = 'green'
                self.time = 0
                self.gx = 0
                self.gy = 0
                self.factor_x = 1
                self.factor_y = 1
                self.move_time = 0
                self.FIELD_SIZE = 600

                health_font = ('Futura',15)

                self.dog = Dog(parent=self)
                self.dog.position = (self.size.w / 2, self.size.h / 2)
                self.dog.z_position = 1

                self.wolf = Wolf(parent=self)
                self.wolf.position = (self.size.w / 2, self.size.h / 2 - 30)
                self.wolf.z_position = 0.9

                self.flower_list = []
                self.tree_list = []

                #We place 200 flowers randomly on the meadow. 
                for i in range(200):
                        self.flower_list.append(Flower2(parent=self))
                        self.flower_list[i].position = (random.randint(-self.FIELD_SIZE, self.FIELD_SIZE), random.randint(-self.FIELD_SIZE, self.FIELD_SIZE))
                
                #The following four blocks of code make up the boundary of the forest, to make sure it has no
                #holes in it, as the tress below are placed randomly, which could result in patches of grass 
                #at the forest boundary otherwise. 
                forest_right = ShapeNode(ui.Path.rect(0, 0, 300, 2 * (self.FIELD_SIZE + self.size.h / 3)), '#006900')
                self.add_child(forest_right)
                forest_right.position = (self.FIELD_SIZE + 150, 0)
                forest_right.z_position = 2

                forest_left = ShapeNode(ui.Path.rect(0, 0, 300, 2 * (self.FIELD_SIZE + self.size.h / 3)), '#006900')
                self.add_child(forest_left)
                forest_left.position = (- (self.FIELD_SIZE + 150), 0)
                forest_left.z_position = 2

                forest_up = ShapeNode(ui.Path.rect(0, 0, 2 * self.FIELD_SIZE, 300), '#006900')
                self.add_child(forest_up)
                forest_up.position = (0, self.FIELD_SIZE + 150)
                forest_up.z_position = 2

                forest_down = ShapeNode(ui.Path.rect(0, 0, 2 * self.FIELD_SIZE, 300), '#006900')
                self.add_child(forest_down)
                forest_down.position = (0, -(self.FIELD_SIZE + 150))
                forest_down.z_position = 2
        
                #One hundred trees are placed randomly on the sides of the meadow. 
                for i in range(100):
                        self.tree_list.append(Tree(parent=self))
                        x = random.choice([-self.FIELD_SIZE, self.FIELD_SIZE])
                        self.tree_list[i].position = (x + (x / abs(x)) * random.randint(-50, 0), random.randint(-self.FIELD_SIZE, self.FIELD_SIZE)) 
                        self.tree_list[i].z_position = 2
                
                #One hundred trees are placed randomly above and below the meadow. 
                for i in range(100, 200):
                        self.tree_list.append(Tree(parent=self))
                        y = random.choice([-self.FIELD_SIZE, self.FIELD_SIZE])
                        self.tree_list[i].position = (random.randint(-self.FIELD_SIZE, self.FIELD_SIZE), y + (y / abs(y)) * random.randint(-50, 0))
                        self.tree_list[i].z_position = 2 


        #This method is the update loop of the Game class and updates the game at about 60 FPS.
        def update(self):
                self.set_position()
                self.move_animal(self.wolf)
                self.wolf.move(u = self.wolf.relative_speed_x, v = self.wolf.relative_speed_y)
                self.leave_tracks(animal = self.wolf)
                self.move_animal(self.dog)
                self.move_screen(self.dog 
                )
                self.dog.move(u = self.get_velocity()[0], v = self.get_velocity()[1])
                self.dog.wag_tail(t = self.time)
                self.leave_tracks(animal = self.dog)
                self.dog.turn_head(velocity = self.get_speed())
                self.wolf_collision()
                #self.sniff()
                self.time += 1
        
        #This method calculates the velocity based on the position of the iPhone, as the 
        #dog is moved using the iPhone's built-in gyroscope and accelerometer. 
        def get_velocity(self): 
                g = gravity()   
                u = (g.x - self.gx) / self.factor_x
                v = (g.y - self.gy) / self.factor_y
                vel = [u, v]
                return vel
        
        #Same as above, but returns the speed instead. 
        def get_speed(self): 
                g = gravity()           
                u = (g.x - self.gx) / self.factor_x
                v = (g.y - self.gy) / self.factor_y
                speed = math.sqrt(u * u + v * v)
                return speed
        
        #Method to allow the dog to sniff after the wolf. Not currently in use. Will be incorporated 
        #in the Dog class in a future version. 
        def sniff(self):
                t = self.time % 120
                if self.get_speed() < 0.05:
                        if t < 60:
                                self.dog.nose.size = (5 + 2 * math.sin(t), 5 + 2 * math.sin(t))
                        else: 
                                self.dog.nose.size = (5, 5)
        
        #Method that makes the animal (so far dog or wolf) leave tracks as it runs across the screen. 
        #These are aligned with the direction of movement, become spread out as the animal moves faster, 
        #and gradually fade. The current positioning of the paw prints is adapted for the dog and wolf.
        #This will be made more general in future versions. 
       def leave_tracks(self, animal):
                vel = animal.velocity(u = self.get_velocity()[0], v = self.get_velocity()[1])
                speed = animal.speed(velocity = vel)
                mod = int(animal.gait + speed)
                rot = animal.rotation

                t_1 = 0 
                t_2 = int(0.1 * mod)
                t_3 = int(0.6 * mod)
                t_4 = int(0.7 * mod)

                times = [t_1, t_2, t_3, t_4]

                t = self.time % mod
                for i in range(4):
                        if t == times[i]:
                                        paw = animal.paw_print() 
                                        self.add_child(paw)
                                        paw.rotation = rot
                                        paw.position = animal.position + (0.7 * animal.radius * math.cos(rot + (-3 + 4 * i) * math.pi / 4), 0.7 * animal.radius * math.sin(rot + (-3 + 4 * i) * math.pi / 4))
                                        actions = [Action.fade_to(0, 1.5), Action.remove()]
                                        paw.run_action(Action.sequence(actions))                                        
        
        #This method moves the animals across the screen by using the given animals velocity method. 
        #This means that the wolf is moving according to its automatic path, and the dog moves 
        #based on the positioning of the iPhone. 
        def move_animal(self, animal):
                x = animal.position.x
                y = animal.position.y
                S = self.FIELD_SIZE

                x += animal.velocity(u = self.get_velocity()[0], v = self.get_velocity()[1])[0] 
                y += animal.velocity(u = self.get_velocity()[0], v = self.get_velocity()[1])[1] 

                x = max(-S, min(S, x))
                y = max(-S, min(S, y))
                animal.position = (x, y)
        
        #This method centers the screen on the animal fed into it. In the current implementation of the game, 
        #this is the dog, but it can flexibly be changed to any of the animals for a different player experience. 
        def move_screen(self, animal):  
                x = animal.position.x
                y = animal.position.y
                X = self.position.x
                Y = self.position.y

                if x <= - X + self.size.w / 3 or x >= - X + 2 * (self.size.w) / 3:
                        X -= animal.velocity(u = self.get_velocity()[0], v = self.get_velocity()[1])[0] 

                if y <= - Y + self.size.h / 3 or y >= - Y + 2 * (self.size.h) / 3:
                        Y -= animal.velocity(u = self.get_velocity()[0], v = self.get_velocity()[1])[1] 

                self.position = (X, Y)
        
        #This method makes sure that the moving of the dog works well regardless of how the iPhone is positioned 
        #as the game is started. It makes sure that the neutral position (where the dog is not moving), is that 
        #of the phone as the game is started. 
        def set_position(self):
                if self.t == 0:
                        g = gravity()
                        self.gx = g.x
                        self.gy = g.y
                        self.factor_x = min(1 - self.gx, 1 + self.gx)
                        self.factor_y = min(1 - self.gy, 1 + self.gy)
        
        #This method checks for collisions between the dog and the wolf, and takes a point of the 
        #wolf's health counter each time this happens. 
        def wolf_collision(self):
                v1 = Vector2(self.dog.position.x, self.dog.position.y)
                v2= Vector2(self.wolf.position.x, self.wolf.position.y)

                if abs(v1 - v2) < 0.5 * (self.dog.size.x + self.dog.size.y):
                        self.wolf.health -= 1
                        self.wolf.health_label.text = str(self.wolf.health)
                        sound.play_effect('8ve:8ve-tap-toothy')




if __name__ == '__main__':
        run(Game(), PORTRAIT, frame_interval = 1, show_fps=True)
