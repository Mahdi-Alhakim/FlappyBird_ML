# Flappy Bird GAME #
import math
import random
from tkinter import *
from PIL import Image, ImageTk

def rotate(points, angle, anch):
    C = math.cos(angle)
    S = math.sin(angle)
    return [[anch[0] + (x - anch[0]) * C - (y - anch[1]) * S, anch[1] + (x - anch[0]) * S + (y - anch[1]) * C] for x, y
            in points]


### Programming an indivisual cloud ###
class cloud():
    def __init__(self, c, loc):
        self.cnvs = c
        self.loc = loc
        self.rnd = [random.choice(list(range(3, 6))) for x in range(3)]
        self.out = False
        self.puff1 = self.cnvs.create_oval(self.loc[0] - self.rnd[0] * 7 - 6, self.loc[1] - self.rnd[0] * 7 - 6,
                                           self.loc[0] + self.rnd[0] * 7 + 6, self.loc[1] + self.rnd[0] * 7 + 6,
                                           fill="white", outline="")
        self.puff2 = self.cnvs.create_oval(self.loc[0] + self.rnd[0] * 7 - self.rnd[1] * 7,
                                           self.loc[1] + 4 - self.rnd[1] * 7,
                                           self.loc[0] + self.rnd[0] * 7 + self.rnd[1] * 7,
                                           self.loc[1] + 4 + self.rnd[1] * 7, fill="white", outline="")
        self.puff3 = self.cnvs.create_oval(self.loc[0] - self.rnd[0] * 7 - self.rnd[2] * 7,
                                           self.loc[1] + 5 - self.rnd[2] * 7,
                                           self.loc[0] - self.rnd[0] * 7 + self.rnd[2] * 7,
                                           self.loc[1] + 5 + self.rnd[2] * 7, fill="white", outline="")

    def update(self):
        global speed, Cspd
        if self.loc[0] + self.rnd[0] * 7 + self.rnd[1] * 7 <= 0:
            self.out = True
        self.loc[0] -= Cspd + speed / 3
        self.cnvs.move(self.puff1, -Cspd - speed / 3, 0)
        self.cnvs.move(self.puff2, -Cspd - speed / 3, 0)
        self.cnvs.move(self.puff3, -Cspd - speed / 3, 0)
        for x in range(0, 4):
            # make sure clouds are below all other objects
            self.cnvs.tag_lower(self.puff1)
            self.cnvs.tag_lower(self.puff2)
            self.cnvs.tag_lower(self.puff3)


### Programming the shape and attributes of an indivisual column of pipes ###
class pipeLine():
    def __init__(self, c, master, X, score, nature=0):
        self.cnvs = c
        self.master = master
        self.length = random.choice(list(range(4, 16))) * 10
        self.X = X
        self.score = score
        self.scored = False
        self.nature = nature
        self.dlt = False
        self.draw()

    def draw(self):
        # Drawing the shape of an indivisual "pipeLine" (upper + lower pipes)
        self.UPPER_PIPE = self.cnvs.create_rectangle(self.X - 17, 0, self.X + 17, self.length, fill="dark green")
        self.U_open = self.cnvs.create_rectangle(self.X - 21, self.length - 15, self.X + 21, self.length,
                                                 fill="dark green")
        self.LOWER_PIPE = self.cnvs.create_rectangle(self.X - 17, 300, self.X + 17, self.length + 110,
                                                     fill="dark green")
        self.L_open = self.cnvs.create_rectangle(self.X - 21, self.length + 110, self.X + 21, 15 + self.length + 110,
                                                 fill="dark green")
        self.pipeTags = [self.UPPER_PIPE, self.LOWER_PIPE, self.U_open, self.L_open]
        self.text = self.cnvs.create_text(self.X, self.length + 55, fill="black", font="Times 25 bold",
                                          text=str(self.score))

    def update(self, speed):
        # moving the entire column down the X-axis
        if not self.dlt:
            self.X -= speed
            self.cnvs.move(self.UPPER_PIPE, -speed, 0)
            self.cnvs.move(self.LOWER_PIPE, -speed, 0)
            self.cnvs.move(self.U_open, -speed, 0)
            self.cnvs.move(self.L_open, -speed, 0)
            self.cnvs.move(self.text, -speed, 0)
            if self.X + 21 < 0:
                # self.dlt is True once the column has passed by and disappeared
                self.dlt = True

    def flash(self):
        # green flash after scoring a point
        self.cnvs.itemconfig(self.text, fill="blue")
        if self.scored == False:
            self.lightFlash = self.cnvs.create_rectangle(self.X - 21, self.length, self.X + 21, self.length + 110,
                                                         fill="green", outline="")
            self.scored = True
            self.master.after(10, self.flash)
        else:
            self.cnvs.delete(self.lightFlash)


#### programming the bird/ball ###
class bird():
    def __init__(self, master, c, g=9.81):
        self.master = master
        self.cnvs = c
        self.grav = g
        self.rot = 0; self.targetROT = 0
        self.Xloc = 100
        self.Yloc = 140
        self.Yvel = 0
        self.Yacc = self.grav / 60
        self.draw()

    def draw(self):
        self.img = Image.open("resources/bird.gif")
        self.img = self.img.convert('RGBA')
        self.Timg = ImageTk.PhotoImage(self.img)
        self.objct = self.cnvs.create_image(self.Xloc-16.5, self.Yloc-13, anchor=NW, image=self.Timg)

    def update(self):
        # moving bird up and down
        global GO
        self.Yvel += self.Yacc  # constant gravity force downward (acceleration)
        if (self.Yloc + self.Yvel + 15 < 300 and self.Yloc + self.Yvel - 15 > 0) or GO == True:
            self.Yloc += self.Yvel
            self.cnvs.move(self.objct, 0, self.Yvel)
        else:
            # limiting the bird/ball from leaving the top or bottom of the canvas
            if self.Yloc > 150:
                self.cnvs.move(self.objct, 0, 285 - self.Yloc)
                self.Yloc = 285
            else:
                self.cnvs.move(self.objct, 0, 15 - self.Yloc)
                self.Yloc = 15
                self.Yvel *= 1 / 25

        #adjusting the rotation of the image
        if GO == False:
            if self.targetROT == 65:
                if self.targetROT - self.rot >= 3 or self.targetROT - self.rot <= -3:
                    self.rot += (self.targetROT - self.rot)/4.000
                else:
                    self.rot = self. targetROT
                    self.targetROT = -60
            elif self.targetROT == -60:
                self.rot += (self.targetROT - self.rot)/25.000
        else:
            self.rot += 3

        self.Timg = ImageTk.PhotoImage(self.img.rotate(self.rot, expand=1))
        self.cnvs.itemconfig(self.objct, image=self.Timg)

    def collisionCheck(self):
        overLapping = list(canvas.find_overlapping(birdy.Xloc - 16, birdy.Yloc - 12.5, birdy.Xloc + 16, birdy.Yloc + 12.5))
        return overLapping

    def JUMP(self, e):
        global GO
        # making the bird jump (setting velocity to 4.5 pxl/ms upward)
        if GO != True: self.Yvel = -4.5; self.targetROT = 65

def start1(e):
    # no Xspeed or Yspeed before mouseclick
    global strt
    birdy.JUMP(1)
    strt = True
    root.unbind("<Button-1>", binding)
    root.bind("<Up>", birdy.JUMP)
    root.bind("<space>", birdy.JUMP)
    root.bind("<Button-1>", birdy.JUMP)

def collision():
    global GO, speed, Cspd
    birdy.JUMP(1)
    GO = True  # setting this variable true notifies the whole program that its "Game Over"
    birdy.Yacc = 9.90/60
    speed = 0  # no speed anymore
    Cspd = 0.15  # cloud speed slows down
    root.after(2000, dstry)

def dstry():
    # destroys the window and all the classes
    global root, canvas, birdy, pipes, clouds
    canvas.destroy()
    del birdy
    for i in pipes:
        del i
    for i in clouds:
        del i
    root.destroy()

def MAIN():
    global speed, root, canvas, strt
    if strt == True:
        birdy.update()
        overLapping = birdy.collisionCheck()
        for t in overLapping:
            # checking for collision between bird/ball with any pipe
            if t != birdy.objct:
                canvas.tag_raise(birdy.objct)  # < raise bird objects above all other objects
            if t in tags:
                collision()
                break
        for i in range(0, len(pipes)):
            # moving pipeLines and replacing them once their off the screen
            if pipes[i].X - birdy.Xloc > 0 and pipes[i].X - birdy.Xloc <= speed:
                pipes[i].flash()
            if pipes[i].dlt == True:
                pipes.remove(pipes[i])
                L = pipeLine(canvas, root, pipes[len(pipes) - 1].X + 200, pipes[len(pipes) - 1].score + 1)
                tags.extend(L.pipeTags)
                pipes.append(L)
            else:
                pipes[i].update(speed)
    for m in range(0, len(clouds)):
        # moving clouds and replacing them once their off the screen
        if clouds[m].out == True:
            clouds.remove(clouds[m])
            R = cloud(canvas, [clouds[len(clouds) - 1].loc[0] + 350, random.choice(list(range(25, 275)))])
            clouds.append(R)
        else:
            clouds[m].update()
    root.after(15, MAIN)

### Main Code SCRIPT ###
if __name__ == "__main__":
    strt = False

    # FORM WINDOW AND CANVAS
    root = Tk()
    root.title("Flappy Thing")
    root.geometry("500x300")
    canvas = Canvas(root, width=500, height=300, bg="light blue")
    canvas.pack()
    binding = root.bind("<Button-1>", start1)

    #VARs
    GO = False
    tags = []
    speed = 3
    Cspd = 1

    # PIPE LIST CREATION
    pipes = [pipeLine(canvas, root, 900 + i * 200, i + 1) for i in range(0, 6)]
    for g in pipes:
        tags.extend(g.pipeTags)

    # NEW BIRD
    birdy = bird(root, canvas, 9.6)

    # CLOUD LIST CREATION#
    clouds = [cloud(canvas, [random.choice(list(range(300, 500))), random.choice(list(range(25, 275)))])]
    clouds.append(cloud(canvas, [clouds[0].loc[0] + 350, random.choice(list(range(25, 275)))]))

    MAIN()
    root.mainloop()

