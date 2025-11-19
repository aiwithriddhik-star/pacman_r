import pygame
from sys import exit
import random
import copy

pygame.init()
screen = pygame.display.set_mode((400,450))
clock = pygame.time.Clock()
cellsize = 20
score=0
lastchoice="up"
lt=0
mode=""


# Load images
red1= pygame.image.load(r"red.png").convert_alpha()
red1=pygame.transform.scale(red1, (20, 20)) 
pink1= pygame.image.load(r"pink.png").convert_alpha()
pink1=pygame.transform.scale(pink1, (20, 20)) 
blue1= pygame.image.load(r"blue.png").convert_alpha()
blue1=pygame.transform.scale(blue1, (20, 20)) 
orange1= pygame.image.load(r"orange.png").convert_alpha()
orange1=pygame.transform.scale(orange1, (20, 20)) 
font = pygame.font.SysFont("Arial", 24)




pacman_img1 = pygame.image.load(r"1.png").convert_alpha()
pacman_img1= pygame.transform.scale(pacman_img1, (20, 20))    # sizing the image
pacman2 = pygame.image.load(r"2.png").convert_alpha()
pacman2 = pygame.transform.scale(pacman2, (20, 20))
pacman3 = pygame.image.load(r"3.png").convert_alpha()
pacman3 = pygame.transform.scale(pacman3, (20, 20))
pacman4= pygame.image.load(r"4.png").convert_alpha()
pacman4= pygame.transform.scale(pacman4, (20, 20))
frozen=pygame.image.load(r"powerup.png").convert_alpha()
frozen= pygame.transform.scale(frozen, (20, 20))


active=True



# ----------------------------
#       PACMAN CLASS
# ----------------------------
class Pacman:
    def __init__(self):
        self.x = 0 * 20
        self.y = 17 * 20
        self.image = pacman_img1
        self.angle = 0
        self.dir="right"

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        if self.dir == "right":
            pass
        if self.dir == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        if self.dir == "up":
            self.image= pygame.transform.rotate(self.image, 90)
        if self.dir == "down":
             self.image=pygame.transform.rotate(self.image, -90)
            
            

        

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class enemy:
    def __init__(self,a,b,c,start_dir):
        self.x=a
        self.y=b
        self.image=c
        self.gridx=self.y//cellsize
        self.gridy=self.x//cellsize
        self.lastchoice = start_dir

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    
    def move(self):
        choice=random.choice(["up","down","left","right"])
        
        if choice=="up":
                if grid1[(self.y//20)-1][self.x//20]!=1 and (self.y//20)-1>=0:
                        self.y-=cellsize

        if choice=="down":   
                if grid1[(self.y//20)+1][self.x//20]!=1 and (self.y//20)+1 <=20 :
                    self.y+=cellsize
        if choice=="left": 
                if (self.x//20)-1>=0 and grid1[self.y//20][(self.x//20)-1]!=1:
                    self.x-=cellsize
        if choice=="right": 
                if (self.x//20)+1 <20 and grid1[self.y//20][(self.x//20)+1]!=1:
                    self.x+=cellsize 
    
    def move1(self, targetx, targety):
        
        # --- 1. Snap to grid ---
        # Snap properly: round to nearest tile center
        self.x = round(self.x / cellsize) * cellsize if abs(self.x % cellsize) < 2 else self.x
        self.y = round(self.y / cellsize) * cellsize if abs(self.y % cellsize) < 2 else self.y

        ex = self.x // cellsize
        ey = self.y // cellsize
        tx = targetx // cellsize
        ty = targety // cellsize

        # --- 2. Intersections only ---
        if self.x % cellsize == 0 and self.y % cellsize == 0:

            reversedict = {
                "up": "down",
                "down": "up",
                "left": "right",
                "right": "left"
            }

            options = []

            # check all 4 directions
            if ey - 1 >= 0 and grid1[ey-1][ex] != 1:
                dist = abs((ey-1) - ty) + abs(ex - tx)
                options.append(("up", dist))

            if ey + 1 < 20 and grid1[ey+1][ex] != 1:
                dist = abs((ey+1) - ty) + abs(ex - tx)
                options.append(("down", dist))

            if ex - 1 >= 0 and grid1[ey][ex-1] != 1:
                dist = abs(ey - ty) + abs((ex-1) - tx)
                options.append(("left", dist))

            if ex + 1 < 20 and grid1[ey][ex+1] != 1:
                dist = abs(ey - ty) + abs((ex+1) - tx)
                options.append(("right", dist))

            # pick shortest
            min_dist = min(d for _, d in options)
            best = [d for d, dist in options if dist == min_dist]
            a=[]
            for i in options:
                a+=[i[0]]

            # avoid reverse if possible
            choice = None
            for d in best:
                if self.lastchoice in best:
                    choice=self.lastchoice
                    break
                elif self.lastchoice != reversedict[d]:
                    choice = d
                    break

            # if all reverse, then accept reverse
            if choice is None:
                only = best[0]
                if self.lastchoice in a:
                    choice=self.lastchoice
                
                elif reversedict[self.lastchoice] == only and len(options) > 1:
                    for d, dist in options:
                        

                        if d != reversedict[self.lastchoice]:
                            choice = d
                            break
                else:
                    choice = only

            self.lastchoice = choice

           
        # --- 3. Move ghost in chosen direction ---
        if self.lastchoice == "up":
            self.y -= 2
        elif self.lastchoice == "down":
            self.y += 2
        elif self.lastchoice == "left":
            self.x -= 2
        elif self.lastchoice == "right":
            self.x += 2
    def scatter(self,targetx,targety,dead):
                
               if dead:
                pass
               else:
                self.x = round(self.x / cellsize) * cellsize if abs(self.x % cellsize) < 2 else self.x
                self.y = round(self.y / cellsize) * cellsize if abs(self.y % cellsize) < 2 else self.y

                ex = self.x // cellsize
                ey = self.y // cellsize
                tx = targetx // cellsize
                ty = targety // cellsize

                # --- 2. Intersections only ---
                if self.x % cellsize == 0 and self.y % cellsize == 0:

                    reversedict = {
                        "up": "down",
                        "down": "up",
                        "left": "right",
                        "right": "left"
                    }

                    options = []

                    # check all 4 directions
                    if ey - 1 >= 0 and grid1[ey-1][ex] != 1:
                        dist = abs((ey-1) - ty) + abs(ex - tx)
                        options.append(("up", dist))

                    if ey + 1 < 20 and grid1[ey+1][ex] != 1:
                        dist = abs((ey+1) - ty) + abs(ex - tx)
                        options.append(("down", dist))

                    if ex - 1 >= 0 and grid1[ey][ex-1] != 1:
                        dist = abs(ey - ty) + abs((ex-1) - tx)
                        options.append(("left", dist))

                    if ex + 1 < 20 and grid1[ey][ex+1] != 1:
                        dist = abs(ey - ty) + abs((ex+1) - tx)
                        options.append(("right", dist))

                    # pick shortest
                    max_dist = max(d for _, d in options)
                    best = [d for d, dist in options if dist == max_dist]
                    a=[]
                    for i in options:
                        a+=[i[0]]

                    # avoid reverse if possible
                    choice = None
                    for d in best:
                        if self.lastchoice in best:
                            choice=self.lastchoice
                            break
                        elif self.lastchoice != reversedict[d]:
                            choice = d
                            break

                    # if all reverse, then accept reverse
                    if choice is None:
                        only = best[0]
                        if self.lastchoice in a:
                            choice=self.lastchoice
                        
                        elif reversedict[self.lastchoice] == only and len(options) > 1:
                            for d, dist in options:
                                

                                if d != reversedict[self.lastchoice]:
                                    choice = d
                                    break
                        else:
                            choice = only
                    

                    self.lastchoice = choice
                
                
                    # --- 3. Move ghost in chosen direction ---
                if self.lastchoice == "up":
                        self.y -= 2
                elif self.lastchoice == "down":
                        self.y += 2
                elif self.lastchoice == "left":
                        self.x -= 2
                elif self.lastchoice == "right":
                        self.x += 2
             

            
# Create pacman object
player = Pacman()

# give each ghost its own initial lastchoice so they don't all share the same direction
red= enemy(8*20,9*20,red1, start_dir='left')
pink=enemy(6*20,9*20,pink1, start_dir='up')
orange=enemy(10*20,9*20,orange1, start_dir='right')
blue=enemy(12*20,9*20,blue1, start_dir='down')
dead1=False
dead2=False
dead3=False
dead4=False


# Grid
grid1 = grid1 =  [
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
 [1, 2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 2, 2, 2, 1],
 [1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
 [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 3, 1],
 [1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
 [1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1],
 [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2],
 [2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1],
 [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
 [2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1],
 [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1],
 [2, 2, 3, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
 [2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
 [1, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1],
 [2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 1],
 [2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1],
 [2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
 [2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
original_grid = copy.deepcopy(grid1)

# (your same grid)


c = 0

while True:
     for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN: #mademistake here ecause   event.type mai aur uske sa hai

                if event.key == pygame.K_UP:
                    if grid1[(player.y//20)-1][player.x//20]!=1 and (player.y//20)-1>=0:
                        player.move(0, -cellsize)
                        player.dir="up"

                if event.key == pygame.K_DOWN:
                    if grid1[(player.y//20)+1][player.x//20]!=1 and (player.y//20)+1 <=20 :
                        player.move(0, cellsize)
                        player.dir="down"

                if event.key == pygame.K_LEFT:
                    if (player.x//20)-1>=0 and grid1[player.y//20][(player.x//20)-1]!=1  :
                        player.move(-cellsize, 0)
                        player.dir="left"
                if event.key == pygame.K_RIGHT:
                    if (player.x//20)+1 <20 and grid1[player.y//20][(player.x//20)+1]!=1:    
                        player.move(cellsize, 0)
                        player.dir="right"
            if (not active) and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 140 <= mouse_pos[0] <= 260 and 280 <= mouse_pos[1] <= 330:
                        active=True
                        lt=pygame.time.get_ticks()
                        score=0
                        player.x=0
                        player.y=17*20
                        player.dir="right"
                        red.x=8*20
                        red.y=9*20
                        pink.x=6*20
                        pink.y=9*20
                        blue.x=10*20
                        blue.y=9*20
                        orange.x=12*20

                        orange.y=9*20
                        grid1 = copy.deepcopy(original_grid)
     timer=pygame.time.get_ticks() - lt
     if active:
       

        screen.fill((0, 0, 0))

        # Draw grid
        for i in range(len(grid1)):
            for j in range(len(grid1[i])):
                if grid1[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 225), (j*20, i*20, 20, 20))
                if grid1[i][j] == 2:
                    pygame.draw.circle(screen, (0, 255, 0), (j*20+10, i*20+10), 5)
                if grid1[i][j] == 3:
                    pygame.draw.circle(screen, (225, 0, 0), (j*20+10, i*20+10), 10)
        if grid1[player.y//20][player.x//20]==2:
                    score+=1
                    grid1[player.y//20][player.x//20]=0
        if grid1[player.y//20][player.x//20]==3:
                    mode="s"
                    t=timer

                    
                    grid1[player.y//20][player.x//20]=0
                
        red.draw()
        pink.draw()
        blue.draw()
        orange.draw()
        
        

        if mode=="s":
            if timer<t+5000:
                    red.image=frozen
                    pink.image=frozen
                    blue.image=frozen
                    orange.image=frozen

                    if player.x//cellsize == red.x//cellsize and player.y//cellsize== red.y//cellsize:
                        score+=200
                        red.x=8*20
                        red.y=9*20
                        dead1=True

                    else:
                        red.scatter(player.x,player.y,dead1)
                    if player.x//cellsize == pink.x//cellsize and player.y//cellsize== pink.y//cellsize:
                        score+=200
                        pink.x=6*20
                        pink.y=9*20
                        dead2=True
                    else:
                       pink.scatter(player.x+4,player.y+4,dead2)
                    if player.x//cellsize == blue.x//cellsize and player.y//cellsize== blue.y//cellsize:
                        score+=200
                        blue.x=10*20
                        blue.y=9*20
                        dead3=True
                    else:
                       blue.scatter(player.x,player.y,dead3)
                    if player.x//cellsize == orange.x//cellsize and player.y//cellsize== orange.y//cellsize:
                        score+=200
                        orange.x=12*20

                        orange.y=9*20
                        dead4=True
                    else:
                       orange.scatter(player.x,player.y,dead4)

            else:
                 mode=""
                 red.image=red1
                 pink.image=pink1
                 blue.image=blue1
                 orange.image=orange1
                                 
        
       
        else:
            red.move1(player.x,player.y)         
            if timer> 3000:
                pink.move1(player.x+4*20, player.y+4*20)

            # Blue ghost after 5 seconds
            if timer > 6000:
                blue.move1(player.x-2*20, player.y-2*20)

            # Orange ghost after 8 seconds
            if timer > 10000:
                orange.move1(player.x+3*20, player.y+6*20) 
            if player.x//cellsize == red.x//cellsize and player.y//cellsize== red.y//cellsize and mode=="":
                 active=False
                 
                 

            if player.x//cellsize == pink.x//cellsize and player.y//cellsize== pink.y//cellsize and mode=="":
                active=False
                
                
            if player.x//cellsize == blue.x//cellsize and player.y//cellsize== blue.y//cellsize and mode=="":
                active=False
                
                
            if player.x//cellsize == orange.x//cellsize and player.y//cellsize== orange.y//cellsize and mode=="":
                active=False
                

        
                        


        # Alternate mouth open/close
        if c  % 4== 0:
            player.image=pacman_img1
            player.rotate()
           
        elif c  % 4== 1:
             player.image=pacman2
             player.rotate()
             
        elif c  % 4== 2:
             player.image=pacman3
             player.rotate()
            
        else:
             player.image=pacman4
             player.rotate()
        player.draw() 
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (10, 410))   

            

        
        c += 1
     else:
            
            screen.fill("black")

            game_over = font.render("GAME OVER", True, "red")
            screen.blit(game_over, (120, 150))

            final_score = font.render(f"Final Score: {score}", True, "white")
            screen.blit(final_score, (110, 210))

            # Play Again button
            pygame.draw.rect(screen, "yellow", (140, 280, 120, 50), border_radius=10)
            play_text = font.render("Play Again", True, "black")
            screen.blit(play_text, (145, 290))
          
     # --- Draw Score ---
     

     pygame.display.update()
     clock.tick(40)
