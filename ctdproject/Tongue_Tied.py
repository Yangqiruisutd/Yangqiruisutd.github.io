# CTD project submittion (From SUTD class of 2026)
# Date 7/12/2022
# Class: SC08 Team 8H: Team members: Elroy (1006569), Le Zhan(1007237),  Yong Zhi(1006894), Ong Qian Ying, Natalie (1007026), Yang Qirui(1003779)

# Title: may a software/game to solve a intresting problem

import turtle  # can only use gif images
import math
import time

# Set up the screen
wn = turtle.Screen()
# make it so the screen can't be resize
wn.cv._rootwindow.resizable(False, False)
wn.title("TONGUE TIED")
wn.setup(600, 800)
wn.tracer(False)
shapes = ["D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\player2.gif", "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\player1.gif",
          "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\lilypad.gif", "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\log.gif",
          "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\longlog.gif", "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\watersprite_huge.gif"]
for shape in shapes:
    wn.register_shape(shape)
wn.bgpic(
    "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\watersprite_huge.gif")
# set the lower left boundary 0,0 upper right to 600, 800
wn.setworldcoordinates(0, 0, 600, 800)

# draw the turtle if not you wont see the turtle in the gui
# We do this as we will have a lot of code that will repetedly use this so
# save coding line
pen = turtle.Turtle()
pen.speed(0)  # animmation speed
pen.hideturtle()  # hid the curcer that created the object
pen.penup()  # hides the line that was created


class Sprite:  # to record the data of one object/charactor
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def render(self, pen):  # draw out the charaters
        pen.goto(self.x, self.y)  # object go to
        pen.shape(self.image)
        pen.stamp()

    def is_collision(self, other):
        """
        code for this  Axis Aligned Bounding Box was taken from 
        https://github.com/wynand1004/Projects/tree/master/Collision%20Detection
        """
        x_collision = (math.fabs(self.x - other.x) *
                       2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) *
                       2) < (self.height + other.height)
        return (x_collision and y_collision)

    def update(self):
        pass


class Player(Sprite):
    def __init__(self, x, y, width, height, image):
        Sprite.__init__(self, x, y, width, height, image)
        self.is_in_goal = False

    def up(self, other):
        if self.far_apart_y(other) <= 60 and self.is_in_goal == False:
            self.y += 30

    def down(self, other):
        if self.far_apart_y(other) >= -60 and self.is_in_goal == False:
            self.y -= 30

    def right(self, other):
        if self.far_apart_x(other) <= 60 and self.is_in_goal == False:
            self.x += 30

    def left(self, other):
        if self.far_apart_x(other) >= -60 and self.is_in_goal == False:
            self.x -= 30

    def far_apart_x(self, other):
        # distance of x axise of 2 players
        x_distance = (math.ceil(abs(self.x) - abs(other.get_x())))
        # print("x_distant = ", x_distance, " self = ", abs(
        #     self.x), " other = ", abs(other.get_x()))
        # if (x_distance > 100):
        #     return False
        return (x_distance)

    def far_apart_y(self, other):
        # distance of y axise of 2 players
        y_distance = (math.ceil(abs(self.y) - abs(other.get_y())))
        # print("y_distant = ", y_distance, " self = ", abs(
        #     self.y), " other = ", abs(other.get_y()))
        return (y_distance)

    def linecreate(self, other):
        # xy cordinets of platers
        object1 = (self.x, self.y)
        object2 = (other.get_x(), other.get_y())
        # clear old line
        turtle.clear()
        turtle.width(3)
        turtle.pencolor("red")
        turtle.penup()
        turtle.goto(object1)
        turtle.pendown()
        turtle.goto(object2)

        turtle.hideturtle()

    def go_home(self):
        self.x = 300
        self.y = 75
        self.is_in_goal = False

    def update(self, other, goal):
        # Border checking if outside "die"
        if self.x < -10 or self.x > 610 or self.y < -10 or self.y > 810:
            self.go_home()
            other.go_home()
            goal.Reset_goal()

    def set_self_in_goal(self):
        self.is_in_goal = True

    def get_in_goal(self):
        return self.is_in_goal

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class Goal(Sprite):
    def __init__(self, x, y, width, height, image):
        Sprite.__init__(self, x, y, width, height, image)
        self.players_on_goal = 0

    def Reset_goal(self):
        self.players_on_goal = 0

    def add_player_on_goal(self):
        self.players_on_goal += 1

    def get_player_on_goal(self):
        return self.players_on_goal


class Car(Sprite):
    def __init__(self, x, y, width, height, image,  x_axis_movment):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = x_axis_movment
        self.speed = 0

    def update(self):
        self.x += self.dx + self.speed  # movement of the enemy/car

        # Border checking move back to the opposit side
        if self.x < -30:
            self.x = 600

        if self.x > 630:
            self.x = 0
    # increase the movement of the car after be in the next level

    def speed_up(self):
        if self.dx > 0:
            self.speed += 0.1

        if self.dx < 0:
            self.speed += -0.1

    def setSpeed(self):
        self.speed = 0


def addEnemys(current_level, current_enemy_list, enemey_list):
    current_enemy_list.extend(enemey_list[current_level])
    # print(current_level, current_enemy_list, enemey_list)
    # remove the 1st in the list that is a goal
    for i in range(1, len(current_enemy_list)):
        current_enemy_list[i].speed_up()
        # print(current_enemy_list)


def resetgame():
    global gamestate, writetime, currentLevel, sprites
    gamestate = "Game"

    writetime = 0
    currentLevel = 1
    for sprite in sprites[1:]:
        sprite.setSpeed()
    sprites.clear()
    sprites = [WinGoal]
    addEnemys(currentLevel, sprites, Level)

# def way to quit game


def quitgame():
    global gamestate
    gamestate = "Quit"


# created players 1 and 2
player1 = Player(
    270, 75, 32, 32, "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\player1.gif")
player2 = Player(
    330, 75, 32, 32, "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\player2.gif")

# create car/enemy for different levels with increasing num and speed of the cars/enermies

Level = {1: [Car(300, 125, 32, 65, "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\longlog.gif", -0.001),
             ],
         2: [Car(0, 250, 32, 32, "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\log.gif", -0.001),
             ],
         3: [Car(200, 500, 32, 32, "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\log.gif", -0.001),
             ],
         4: [Car(0, 400, 32, 65, "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\longlog.gif", -0.001),
             ]}
# create a game state
gamestate = "Start"

# create goal/win conditions
WinGoal = Goal(300, 750, 40, 40,
               "D:\elroy\year_3_sem_2_sutd\progarming_CTD\Python\Project\lilypad.gif")

# def current level
currentLevel = 1
writetime = 0

# create a list of objects
sprites = [WinGoal]
addEnemys(currentLevel, sprites, Level)

# Keyboard binding
wn.listen()
"""
The code for the Key binding was modified from 
https://trinket.io/python/16e316e69f
https://www.codetoday.co.uk/post/how-to-pass-the-key-pressed-to-the-function-when-using-onkeypress-in-python-s-turtle-module 
"""
# player 1 movement
wn.onkeypress(lambda n=player2: player1.up(n), "Up")
wn.onkeypress(lambda n=player2: player1.down(n), "Down")
wn.onkeypress(lambda n=player2: player1.left(n), "Left")
wn.onkeypress(lambda n=player2: player1.right(n), "Right")

# player 2 movement
wn.onkeypress(lambda n=player1: player2.up(n), "w")
wn.onkeypress(lambda n=player1: player2.down(n), "s")
wn.onkeypress(lambda n=player1: player2.left(n), "a")
wn.onkeypress(lambda n=player1: player2.right(n), "d")
# in case of caps lock on
wn.onkeypress(lambda n=player1: player2.up(n), "W")
wn.onkeypress(lambda n=player1: player2.down(n), "A")
wn.onkeypress(lambda n=player1: player2.left(n), "S")
wn.onkeypress(lambda n=player1: player2.right(n), "D")
# to start/restart game
# wn.onkeypress(lambda a=writetime, b=currentLevel, c=sprites, d=Level: resetgame(
#     a, b, c, d), "k")
wn.onkeypress(resetgame, "K")
wn.onkeypress(resetgame, "k")

# to quit game
wn.onkeypress(quitgame, "p")
wn.onkeypress(quitgame, "P")


# ENDdisplay settings
HOMEdisplay = turtle.Turtle()
HOMEdisplay.penup()
HOMEdisplay.goto(300, 400)
HOMEdisplay.pendown()
HOMEdisplay_style = ('Courier', 30, 'bold')
HOMEdisplay.hideturtle()

# Timer display settings
Timedisplay = turtle.Turtle()
Timedisplay.penup()
Timedisplay.goto(300, 450)
Timedisplay.pendown()
Timedisplay_style = ('Courier', 30, 'bold')
Timedisplay.hideturtle()

# HPdisplay settings
HPdisplay = turtle.Turtle()
HPdisplay.penup()
HPdisplay.goto(300, 400)
HPdisplay.pendown()
HPdisplay_style = ('Courier', 30, 'bold')
HPdisplay.hideturtle()


while True:
    # start screen
    """
    The code for the splash screen was modified from https://github.com/wynand1004/Projects/tree/master/Game%20State
    """
    if gamestate == "Start":
        # print you start splash screen
        HOMEdisplay.color("red")
        HOMEdisplay.write("TONGUE TIED\n\n\n\n",
                          font=HOMEdisplay_style, align="center")
        HOMEdisplay.color("black")
        HOMEdisplay.write("press k to begin\npress p to quit\nWASD key for player 1\nArrows key for player 2",
                          font=HOMEdisplay_style, align="center")

    # game over screen
    elif gamestate == "Dead":
        # print you died splash screen
        HOMEdisplay.write("The couple has\npassed away...\n\npress k to restart\npress p to quit",
                          font=HOMEdisplay_style, align="center")

    elif gamestate == "Win":
        # print you Win you shouldn't spend so much time
        HOMEdisplay.write("The couple lives happily\n       ever after! \n\npress k to restart\npress p to quit",
                          font=HOMEdisplay_style, align="center")

    # game loop
    elif gamestate == "Game":
        # clear HOMEdisplay/spash screen
        HOMEdisplay.clear()
        health = 3
        # add function for timer
        start_time = time.time()

        HPdisplay.write("Lives:{}".format(health),
                        font=HPdisplay_style, align="center")

        while health > 0:

            # add function for timer
            """
            The code for the timmer was modified from https://github.com/wynand1004/Projects/blob/master/Timer/timer.py 

            """
            elasped_time = int(time.time() - start_time)
            if writetime == elasped_time:
                # clear the timer
                Timedisplay.clear()
                Timedisplay.write("Time:{}".format(
                    elasped_time), font=HPdisplay_style, align="center")
                writetime += 1

            # Render
            for sprite in sprites:
                sprite.render(pen)
                sprite.update()

            # # # render every new click/movment
            player1.render(pen)
            player2.render(pen)

            # # # to check for the boundery location may have to change that lets see
            player1.update(player2, WinGoal)
            player2.update(player1, WinGoal)
            # # to signify the distance between 2 user is dangerous or not
            player1.linecreate(player2)

        # check for collision:
            for sprite in sprites:
                if player1.is_collision(sprite) or player2.is_collision(sprite):
                    if isinstance(sprite, Car):  # if player collide w Car
                        player1.go_home()
                        player2.go_home()
                        WinGoal.Reset_goal()

                        health -= 1
                        HPdisplay.clear()
                        HPdisplay.write("Lives:{}".format(
                            health), font=HPdisplay_style, align="center")

                        # break
                    if isinstance(sprite, Goal):  # if player collide with Goal
                        # print(WinGoal.get_player_on_goal())
                        if WinGoal.get_player_on_goal() >= 2:  # win condition
                            player1.go_home()
                            player2.go_home()
                            currentLevel += 1
                            writetime = 0
                            start_time = time.time()
                            if currentLevel > len(Level):
                                health = 0
                                break
                            # add enemy systemw
                            """
                            code for the level/enemy system was modified from
                            https://github.com/wynand1004/Projects/tree/master/Snake%20Game
                            """
                            addEnemys(currentLevel, sprites, Level)
                            WinGoal.Reset_goal()
                        else:
                            if player1.is_collision(sprite) and player1.get_in_goal() == False:
                                player1.set_self_in_goal()
                                WinGoal.add_player_on_goal()
                            elif player2.is_collision(sprite) and player2.get_in_goal() == False:
                                WinGoal.add_player_on_goal()
                                player2.set_self_in_goal()

            wn.update()

            # Clear the pen
            pen.clear()

        if health <= 0 and currentLevel <= len(Level):
            gamestate = "Dead"
            HPdisplay.clear()
            Timedisplay.clear()
            player1.linecreate(player2)
            # print(gamestate)
        else:
            gamestate = "Win"
            HPdisplay.clear()
            Timedisplay.clear()
            writetime = 0

    elif gamestate == "Quit":
        turtle.bye()
