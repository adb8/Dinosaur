from tkinter import *
import random

window = Tk()
window.geometry("800x550")
window.resizable(False, False)
window.title("Dinosaur game")
window.update()

WINDOW_HEIGHT = window.winfo_height()
WINDOW_WIDTH = window.winfo_width()
SCREEN_HEIGHT = window.winfo_screenheight()
SCREEN_WIDTH = window.winfo_screenwidth()

x = int((SCREEN_WIDTH/2) - (WINDOW_WIDTH)/2)
y = int((SCREEN_HEIGHT/2) - (WINDOW_HEIGHT/2))

window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

BOX_HEIGHT = 50
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
RESTING_POSITION_Y = 250
MAX_POSITION_Y = 100
MILLISECONDS_PER_FRAME = 12
JUMP_INCREMENT = 5

score = 0
ascent = False
descent = False
running = True
cacti = []

label = Label(window, font=("consolas", 40), text="Score: "+str(score))
label.pack()

canvas = Canvas(window, bg="gray", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
canvas.pack()
canvas.create_rectangle(0, 300, CANVAS_WIDTH, CANVAS_HEIGHT, fill="black", outline="")

class Player:

    def __init__(self):
        self.x = 200
        self.y = RESTING_POSITION_Y
        self.square = canvas.create_rectangle(self.x, self.y, self.x+BOX_HEIGHT, self.y+BOX_HEIGHT, fill="red", tag="player", outline="")

class Cactus:

    def __init__(self):
        self.x = CANVAS_WIDTH
        self.y = RESTING_POSITION_Y
        self.square = canvas.create_rectangle(self.x, self.y, self.x+BOX_HEIGHT, self.y+BOX_HEIGHT, tag="cactus", fill="green", outline="")

player = Player()

def space():
    global ascent, descent
    if descent == False:
        ascent = True

window.bind("<space>", lambda event: space())

def handleJump():

    global ascent, descent, cacti
    if ascent:
        player.y -= JUMP_INCREMENT
        if player.y == MAX_POSITION_Y:
            descent = True
            ascent = False

    elif descent:
        player.y += JUMP_INCREMENT
        if player.y == RESTING_POSITION_Y:
            descent = False
            ascent = False

    canvas.delete("player")
    player.square = canvas.create_rectangle(player.x, player.y, player.x+BOX_HEIGHT, player.y+BOX_HEIGHT, tag="player", fill="red", outline="")

def spawnCacti():

    global cacti
    spawnChance = random.randint(0, 200)
    if spawnChance <= 3:

        if len(cacti) == 0:
            cactus = Cactus()
            cacti.append(cactus)
        elif len(cacti) > 0 and cacti[-1].x < 500:
            cactus = Cactus()
            cacti.append(cactus)

def drawCacti():

    global cacti
    for i in cacti:
        i.x -= 5
        canvas.delete(i.square)
        i.square = canvas.create_rectangle(i.x, i.y, i.x+BOX_HEIGHT, i.y+BOX_HEIGHT, tag="cactus", fill="green", outline="")

def deleteCacti():

    global cacti
    tempCacti = cacti
    cacti = []

    for i in tempCacti:
        if i.x > -100:
            cacti.append(i)
        else:
            canvas.delete(i.square)
    tempCacti = []

def updateScore():

    global score, cacti
    for i in cacti:
        if i.x == 150:
            score += 1
            label.configure(text="Score: "+str(score))

def handleCollions():

    global cacti, player
    for i in cacti:
        if player.y > 200:
            if player.x > i.x and player.x < i.x+BOX_HEIGHT:
                gameOver()
            elif player.x+BOX_HEIGHT > i.x and player.x+BOX_HEIGHT < i.x+BOX_HEIGHT:
                gameOver()

def gameOver():
    global running
    running = False

def displayGameOver():

    canvas.delete(ALL)
    canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, text="game over", fill="red", font=("consolas", 70))
    canvas.configure(bg="black")

def nextFrame():

    handleJump()
    spawnCacti()
    drawCacti()
    updateScore()
    handleCollions()

    if running:
        window.after(MILLISECONDS_PER_FRAME, nextFrame)
    else:
        displayGameOver()

nextFrame()
window.after(MILLISECONDS_PER_FRAME, nextFrame)

window.mainloop()