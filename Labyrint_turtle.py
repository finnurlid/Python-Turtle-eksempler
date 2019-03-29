import math
import turtle
import random

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Et labyrintspill")
wn.setup(700, 700)
wn.tracer(0)

#Registrer sprites
images = ["player.gif", "treasure.gif", "wall.gif"]
for image in images:
	turtle.register_shape(image)

class Pen(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.shape("wall.gif")
		self.color("brown")
		self.penup()
		self.speed(0)

class Player(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.shape("player.gif")
		self.color("green")
		self.penup()
		self.speed(0)
		self.gold = 0

	def go_up(self):
		move_to_x = player.xcor()
		move_to_y = player.ycor() + 24
		if(move_to_x, move_to_y) not in walls:
			self.goto(move_to_x, move_to_y)

	def go_down(self):
		move_to_x = player.xcor()
		move_to_y = player.ycor() - 24
		if(move_to_x, move_to_y) not in walls:
			self.goto(move_to_x, move_to_y)

	def go_left(self):
		move_to_x = player.xcor() - 24
		move_to_y = player.ycor()
		#self.shape("whatever_left.gif")
		if(move_to_x, move_to_y) not in walls:
			self.goto(move_to_x, move_to_y)

	def go_right(self):
		move_to_x = player.xcor() + 24
		move_to_y = player.ycor()
		#self.shape("whatever_right.gif")
		if(move_to_x, move_to_y) not in walls:
			self.goto(move_to_x, move_to_y)

	def is_collision(self, other):
		a = self.xcor() - other.xcor()
		b = self.ycor() - other.ycor()
		distance = math.sqrt((a**2) + (b**2))
		if distance < 5:
			return True
		else:
			return False

class Treasure(turtle.Turtle):
	def __init__(self, x, y):
		turtle.Turtle.__init__(self)
		self.shape("treasure.gif")
		self.color("gold")
		self.penup()
		self.speed(0)
		self.gold = 100
		self.goto(x, y)

	def destroy(self):
		self.goto(2000, 2000)
		self.hideturtle()

class Enemy(turtle.Turtle):
	def __init__(self, x,y):
		super(Enemy, self).__init__()
		self.shape("square")
		self.color("red")
		self.penup()
		self.speed(0)
		self.gold=25
		self.goto(x,y)
		self.direction=random.choice(["up","down","left","right"])
		
	def move(self):
		if self.direction=="up":
			dx=0
			dy=24
		elif self.direction=="down":
			dx=0
			dy=-24
		elif self.direction=="left":
			dx=-24
			dy=0
		elif self.direction=="right":
			dx=24
			dy=0
		else:
			dx=0
			dy=0

		move_to_x = self.xcor() + dx
		move_to_y = self.ycor() + dy

		if (move_to_x, move_to_y) not in walls:
			self.goto(move_to_x, move_to_y)
		else: #hvis fienden møter en vegg, gå en annen vei
			self.direction=random.choice(["up","down","left","right"])
		turtle.ontimer(self.move, t=random.randint(100, 300))

	def destroy(self):
		self.goto(2000,2000)
		self.hideturtle()

#Lag en liste med levels, med et tomt level på plass 0
levels=[""]

#Slik ser level1 ut:
level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"X P  XXXXXXXXXXXXXXXXXXXX",
"XXX              XXXXXXXX",
"XXXX XXXX   XXXX XXXXXXXX",
"XXXX XXE      XX XXXXXXXX",
"XXXX XX       XX XXXXXXXX",
"XXXX XX   T  XXX XXXXXXXX",
"XXXX XXXXXXXXXXX   E    X",
"XX   X           T      X",
"XXXX    XXXXXXXXX XXXXXXX",
"XXXXX XXXXXX      XXXXXXX",
"XXXX  XXXXX  XXXXXXXXXXXX",
"XXXX       E        XXXXX",
"XXXXXXXXXXXXXXXXXXX XXXXX",
"XXXXXXXXXXXXXXXXXXX XXXXX",
"XXXXXXXXXXXXXXXXXXX XXXXX",
"XXXXXXXXXXXXXXXXXXX XXXXX",
"X                    XXXX",
"X       XXXXXXXXXXXXXXXXX",
"X       XXX             X",
"X  T    XXX        T    X",
"X       XXX             X",
"XXXX XXXXXXXXXXXX  XXXXXX",
"XXXX      E        XXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX"
]

#Lag er liste over skatter
treasures = []

#Liste over fiender
enemies = []

#Legg til level_1 i lista
levels.append(level_1)

#Funksjon for å tegne brettet
def setup_maze(level):
	for y in range(len(level)):
		for x in range(len(level[y])):
			letter = level[y][x]	#Bokstav, ikke figur!!
			screen_x = -288 + (x*24)
			screen_y = 288 - (y*24)

			if letter == "X":
				pen.goto(screen_x, screen_y)
				#pen.shape("wall.gif") #Er dette bedre enn i Pen
				pen.stamp()
				walls.append((screen_x, screen_y))

			if letter == "P":
				player.goto(screen_x, screen_y)

			if letter == "T":
				treasures.append(Treasure(screen_x, screen_y))

			if letter == "E":
				enemies.append(Enemy(screen_x, screen_y))



pen = Pen()
player = Player()
#enemy = Enemy()

#Lag en vegg-koordinatliste
walls = []

setup_maze(levels[1])

#Keybindings
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")

#Slå av skjermoppdateringer
wn.tracer(0)

#Flytt rundt på fiendene
for enemy in enemies:
	turtle.ontimer(enemy.move, t=250)

#Main loop
while True:
	for treasure in treasures:
		if player.is_collision(treasure):
			player.gold += treasure.gold
			print("Gullbeholdning: {}".format(player.gold))
			treasure.destroy()
			treasures.remove(treasure)

	for enemy in enemies:
		if player.is_collision(enemy):
			print("Døua!")

	#Oppdater skjerm
	wn.update()