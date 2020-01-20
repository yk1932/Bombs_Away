import os
import random
import time
path = os.getcwd()
add_library('minim')
N=13
tile_size = 54
player=Minim(this)
class Tile:
    def __init__(self,r,c,s):
        self.r=r
        self.c=c
        self.s=s #'I" or "D" or "S" (indestructible) or destructible or space
        self.rad=27
    
    def display(self):
        if self.s=="I": #(show indestructible)
            tile_img=loadImage(path+"/images/indestructible.png")
        elif self.s=="D": 
            tile_img=loadImage(path+"/images/destructible.png")
        elif self.s=="S": 
            tile_img=loadImage(path+"/images/space.png")
        image(tile_img,self.r*54,self.c*54)
        
class Creature:
    def __init__(self,x,y,r,img,w,h,F):
        self.x=x
        self.y=y
        self.r=r
        self.w=w
        self.h=h
        self.F=F #framecount
        self.vx=0
        self.vy=0
        self.dir=-2 #facing down
        self.img={}
        for dict_key, dict_val in img.items():
            self.img[dict_key] = loadImage(path+"/images/"+dict_val)
        self.tile_size = 54
        
    def display(self):
        self.update()
        sprite_index = (self.F % 12) // 4
        if self.dir==-1:
            image(self.img["left"], self.x,self.y,33,50, 33*sprite_index,0,33*(sprite_index+1),50)
            #show image facing left
        elif self.dir==1:
            image(self.img["right"], self.x,self.y,33,50, 33*sprite_index,0,33*(sprite_index+1),50)
            #show image facing right
        elif self.dir==2:
            image(self.img["up"], self.x,self.y,33,50, 33*sprite_index,0,33*(sprite_index+1),50)
            #show image facing up
        elif self.dir==-2:
            image(self.img["down"], self.x,self.y,33,50, 33*sprite_index,0,33*(sprite_index+1),50)
            #show image facing down
            
    def block(self):
        #if try to move out of boundary, pushed back
        if self.x < 0:
            self.x = self.x+abs(self.vx)
        elif self.x>N*self.tile_size-self.w:
            self.x=self.x-self.vx
        elif self.y<0:
            self.y = self.y+abs(self.vy)
        elif self.y>(N-1)*self.tile_size:
            self.y=self.y-self.vy
        for e in g.tiles:
            if e.s == "D" or e.s =="I":
                if e.r*54-47.5 <= self.y <= (e.r)*54+47.5 and e.c*54-self.w<= self.x <= (e.c+1)*54:
                    if self.vx <0 and self.vy==0:
                        self.x = self.x+abs(self.vx)
                    elif self.vx > 0 and self.vy==0:
                        self.x = self.x-self.vx
                    elif self.vy <0 and self.vx==0:
                        self.y=self.y+abs(self.vy)
                    elif self.vy>0 and self.vx==0:
                        self.y=self.y-self.vy
        
        for b in g.bombs:
            #if player is on bomb, player can move out
            if self.distance(b) <= self.r+b.r-8 and not(self.vx == 0 and self.vy ==0): # very close
                x, y = self.x, self.y
                if self.vx<0 and self.vy==0 and self.x-54>0:
                    x = b.x-self.tile_size
                elif self.vx>0 and self.vy==0 and self.x+54 < N*self.tile_size-27:
                    x = b.x+self.tile_size
                elif self.vy <0 and self.vx==0 and self.y-54>0:
                    y=b.y-self.tile_size
                elif self.vy>0 and self.vx==0 and self.y+54<N*self.tile_size-27:
                    y=b.y+self.tile_size
                x = round(x/self.tile_size) * self.tile_size # x/tile_size is between 0 and N, roudn(x/tlsz) is an integer between 0 and N
                y = round(y/self.tile_size) * self.tile_size 
                #make sure bomb placed on tile
                if (x/self.tile_size)%2==0 or (y/self.tile_size)%2==0:
                    self.x, self.y = x+2, y
                    
            elif self.distance(b) < self.r+b.r: # Not too close but colliding
                if self.vy==0:
                    self.x=self.x-self.vx
                elif self.vx==0:
                    self.y=self.y-self.vy
                    
    
        
    def distance(self, obj):
        return ((self.x+self.w/2-obj.x-obj.w/2)**2+(self.y+self.h/2-obj.y-obj.h/2)**2)**0.5
                
class Player1(Creature):
    def __init__(self, x,y,r,img,w,h,F):
        Creature.__init__(self,x,y,r,img,w,h,F)
        self.B=3
        self.keyHandler={LEFT:False, RIGHT:False, UP:False, DOWN:False, SHIFT:False}
        self.bombRadius=5
        self.alive=True
        self.A = False
        self.gameover=player.loadFile(path+'/sounds/gameover.wav')
    def update(self):
        self.block()
        if self.keyHandler[LEFT]:
            self.vx=-6
            self.dir=-1
            self.vy=0
        elif self.keyHandler[RIGHT]:
            self.vx=6
            self.dir=1
            self.vy=0
        elif self.keyHandler[DOWN]:
            self.vy=6
            self.dir=-2
            self.vx=0
        elif self.keyHandler[UP]:
            self.vy=-6
            self.dir=2
            self.vx=0
        else:
            self.vx =0
            self.vy=0
        
        self.x += self.vx
        self.y += self.vy
        self.F += 1
        if self.keyHandler[SHIFT] and not self.A:
            if self.B >= 1:
                g.placeBomb(self.x,self.y, 1)
                self.B-=1
            self.A = True
class Player2(Creature):
    def __init__(self, x,y,r,img,w,h,F):
        Creature.__init__(self,x,y,r,img,w,h,F)
        self.B=3
        self.keyHandler={LEFT:False, RIGHT:False, UP:False, DOWN:False, SHIFT:False}
        self.bombRadius=5
        self.alive=True
        self.A = False
        self.gameover=player.loadFile(path+'/sounds/gameover.wav')
    def update(self):
        self.block()
        if self.keyHandler[LEFT]:
            self.vx=-6
            self.dir=-1
            self.vy=0
        elif self.keyHandler[RIGHT]:
            self.vx=6
            self.dir=1
            self.vy=0
        elif self.keyHandler[DOWN]:
            self.vy=6
            self.dir=-2
            self.vx=0
        elif self.keyHandler[UP]:
            self.vy=-6
            self.dir=2
            self.vx=0
        else:
            self.vx =0
            self.vy=0
        
        # if not self.blocked(self.x, self.y, self.vx, self.vy): #check whether move is valid or not
        self.x += self.vx
        self.y += self.vy
        self.F += 1
        if self.keyHandler[SHIFT] and not self.A:
            if self.B >= 1:
                g.placeBomb(self.x,self.y, 2)
                self.B-=1
            self.A = True

    # extend update to be able to deal w/ key handlers (refer to Mario)
    # ALSO in update, put in a collision detection check
    # AKA if player is going to try and walk into a block, don't let them move AKA set their vx and vy to zero
class Bomb: 
    def __init__(self,x,y,r,img,w,h,owner):
        self.x=x
        self.y=y
        self.r=r
        self.img = loadImage(path+"/images/"+img)
        self.w=w
        self.h=h
        self.triggerTime=time.time()
        self.owner=owner
        self.bombExplosion=player.loadFile(path+'/sounds/explosion.wav')
    def __eq__(self, obj):
        if isinstance(obj, Bomb):
            return self.triggerTime == obj.triggerTime and self.owner == obj.owner
        else:
            return False
    def display(self):
        image(self.img, self.x,self.y,self.w,self.h)
        fill(255,0,0)
        self.update()
        
    def update(self):
        if time.time()-self.triggerTime > 2: 
            self.explode()
    
    def explode(self):
        if self in g.bombs:
            g.bombs.remove(self)
        self.bombExplosion.rewind()
        self.bombExplosion.play()           
        if self.owner == 1: 
            g.player1.B +=1
        elif self.owner==2:
            g.player2.B +=1
        #center bomb
        bomb1 = loadImage(path+"/images/bomb1.png")
        image(bomb1,self.x,self.y,54,54)
        for b in g.bombs:
            if b.x in range(int(self.x)-54*g.player1.bombRadius, int(self.x)+54*(g.player1.bombRadius+1)) and self.y==b.y:
                b.explode()
            if b.y in range(int(self.y)-54*g.player1.bombRadius, int(self.y)+54*(g.player1.bombRadius+1)) and self.x==b.x:
                b.explode()
                
        if g.player1.x + g.player1.w/2 in range(int(self.x)-54*g.player1.bombRadius, int(self.x)+54*(g.player1.bombRadius+1)) and self.y-g.player1.h/2<=g.player1.y <= self.y+54+g.player1.h/2:
            g.player1.alive=False
        elif g.player1.y + g.player1.h/2 in range(int(self.y)-54*g.player1.bombRadius, int(self.y)+54*(g.player1.bombRadius+1)) and self.x-g.player1.w/2<=g.player1.x <= self.x+54+g.player1.w/2:
            g.player1.alive=False
        if g.player2.x + g.player2.w/2 in range(int(self.x)-54*g.player2.bombRadius, int(self.x)+54*(g.player2.bombRadius+1)) and self.y-g.player2.h/2<=g.player2.y <= self.y+54+g.player2.h/2:
            g.player2.alive=False
        elif g.player2.y + g.player2.h/2 in range(int(self.y)-54*g.player2.bombRadius, int(self.y)+54*(g.player2.bombRadius+1)) and self.x-g.player2.w/2<=g.player2.x <= self.x+54+g.player2.w/2:
            g.player2.alive=False
        
                    
        for i in range(g.player1.bombRadius):
                #enabling up and down direction only if there are no blocks on top and down
                if ((self.x/tile_size)%2==0 and (self.y/tile_size)%2==0) or ((self.x/tile_size)%2==0 and (self.y/tile_size)%2==1):
                    #for up, down continuous bomb (bomb2)
                    for (r,c) in [(-i,0),(i,0)]:
                        xneigh_tile = self.x+(c*tile_size)
                        yneigh_tile = self.y+(r*tile_size)
                        bomb2 = loadImage(path+"/images/bomb2.png")
                        image(bomb2,xneigh_tile,yneigh_tile,54,54)
                    
                    
                    #for up end (bomb4)
                    for (r,c) in [(-(i+1),0)]:
                        xneigh_tile = self.x+(c*tile_size)
                        yneigh_tile = self.y+(r*tile_size)
                        bomb4 = loadImage(path+"/images/bomb4.png")
                        image(bomb4,xneigh_tile,yneigh_tile,54,54)
                            
                    #for down end (bomb5)
                    for (r,c) in [(i+1,0)]:
                        xneigh_tile = self.x+(c*tile_size)
                        yneigh_tile = self.y+(r*tile_size)
                        bomb5 = loadImage(path+"/images/bomb5.png")
                        image(bomb5,xneigh_tile,yneigh_tile,54,54)
                        
                #enabling left and right direction only if there are no blocks left and right
                if ((self.x/tile_size)%2==0 and (self.y/tile_size)%2==0) or ((self.x/tile_size)%2==1 and (self.y/tile_size)%2==0):
                    #for left, right continuous bomb (bomb3)
                    for (r,c) in [(0,-i),(0,i)]:
                        xneigh_tile = self.x+(c*tile_size)
                        yneigh_tile = self.y+(r*tile_size)
                        bomb3 = loadImage(path+"/images/bomb3.png")
                        image(bomb3,xneigh_tile,yneigh_tile,54,54)
                        
                    #for right end (bomb6)
                    for (r,c) in [(0,i+1)]:
                        xneigh_tile = self.x+(c*tile_size)
                        yneigh_tile = self.y+(r*tile_size)
                        bomb6 = loadImage(path+"/images/bomb6.png")
                        image(bomb6,xneigh_tile,yneigh_tile,54,54)
                        
                    #for left end (bomb7)
                    for (r,c) in [(0,-(i+1))]:
                        xneigh_tile = self.x+(c*tile_size)
                        yneigh_tile = self.y+(r*tile_size)
                        bomb7 = loadImage(path+"/images/bomb7.png")
                        image(bomb7,xneigh_tile,yneigh_tile,54,54)    
            
class Game:
    def __init__(self,N,M):
        self.N=N
        self.M=M
        self.tile_size=54
        self.tiles=[]
        self.bombs=[]
        self.play=True
        self.music=player.loadFile(path+'/sounds/background.mp3')
        self.music.play()
        self.bombPlace=player.loadFile(path+'/sounds/bombplace.wav')
        for r in range(self.N):
            for c in range(self.N):
                if r%2!=0 and c%2!=0:
                    self.tiles.append(Tile(r,c,"I"))
        sprite = {}
        sprite["down"] = "bombwoman1.png"
        sprite["up"] = "bombwoman2.png"
        sprite["left"] = "bombwoman3.png"
        sprite["right"] = "bombwoman4.png"
        
        sprite2={}
        sprite2["down"] = "bombman1.png"
        sprite2["up"] = "bombman2.png"
        sprite2["left"] = "bombman3.png"
        sprite2["right"] = "bombman4.png"
        
        self.player1=Player1(0,0,23,sprite,33,50,3)
        self.player2=Player2((N-1)*54,(N-1)*54,23,sprite2,33,50,3)
        
    def checkwin(self):
        if self.player1.alive == False or self.player1.alive == False:
            self.play=False
            

    def displayBoard(self):
        for t in self.tiles:
            t.display()
        for b in self.bombs:
            b.display()
        self.player1.display()
        self.player2.display()
        
        if self.player1.alive == False and self.player2.alive == False:
            g.player1.gameover.play()
            tie=loadImage(path+'/images/tie.png')
            image(tie,101,300) 
        elif self.player1.alive == False and self.player2.alive == True:
            g.player1.gameover.play()
            player2win=loadImage(path+'/images/player2won.png')
            image(player2win,126,300)
        elif self.player2.alive == False and self.player1.alive == True:
            g.player1.gameover.play()
            player1win=loadImage(path+'/images/player1won.png')
            image(player1win,126,300)

            
    def placeBomb(self, x, y, owner):
        # snap x and y to grid
        x = round(x/self.tile_size) * self.tile_size # x/tile_size is between 0 and N, roudn(x/tlsz) is an integer between 0 and N
        y = round(y/self.tile_size) * self.tile_size
        
        #make sure bomb placed on tile
        
        if (x/self.tile_size)%2==0 or (y/self.tile_size)%2==0 and x < N*self.tile_size and x > 0:
            for b in self.bombs:
                if b.x == x and b.y == y:
                    return # if there's already a bomb in the same spot, don't place new one
            self.bombs.append(Bomb(x,y,25,"bomb.png",54,54,owner))
            self.bombPlace.rewind()
            self.bombPlace.play()
            
        
    
g=Game(N,N)
def setup():
    size(N*54,N*54)
    background(0)
def draw():
    background(0,100,0)
    g.displayBoard()


def keyPressed():
    global g
    if g.player1.alive==False or g.player2.alive==False:
        if keyCode == LEFT or keyCode==RIGHT or keyCode ==UP or keyCode ==DOWN or key==' ':
            g=Game(N,N)
            g.player1.alive=True
            g.player2.alive=True
            g.music.pause()
    else:
        if keyCode == LEFT:
            g.player1.keyHandler[LEFT] = True
        if key == "a" or key =='A':
            g.player2.keyHandler[LEFT] = True
        elif keyCode == RIGHT:
            g.player1.keyHandler[RIGHT] = True
        elif key == 'd' or key =='D':
            g.player2.keyHandler[RIGHT]=True
        elif keyCode == UP:
            g.player1.keyHandler[UP] = True
        elif key == 'w' or key =='W':
            g.player2.keyHandler[UP] = True
        elif keyCode== DOWN:
            g.player1.keyHandler[DOWN] = True
        elif key == 's' or key =='S':
            g.player2.keyHandler[DOWN] = True
        elif key == ' ': 
            g.player1.keyHandler[SHIFT] = True
        elif key == TAB:
            g.player2.keyHandler[SHIFT] = True
     
        
        
        
def keyReleased():
    if keyCode == LEFT:
        g.player1.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        g.player1.keyHandler[RIGHT] = False
    elif keyCode == UP:
        g.player1.keyHandler[UP] = False
    elif keyCode== DOWN:
        g.player1.keyHandler[DOWN] = False
    elif key == ' ': 
        g.player1.keyHandler[SHIFT] = False
        g.player1.A = False
    if key == "a" or key =='A':
        g.player2.keyHandler[LEFT] = False
    elif key == 'd' or key == 'D':
        g.player2.keyHandler[RIGHT]=False
    elif key =='w'or key =='W':
        g.player2.keyHandler[UP]=False
    elif key == 's' or key =='S':
        g.player2.keyHandler[DOWN]=False
    elif key == TAB:
        g.player2.keyHandler[SHIFT] = False
        g.player2.A=False
