import pygame
from sys import exit

pygame.init()
pygame.mixer.init()

#1 jump = 1500 ms
#mandatory 3 0 at end to prevent closing

#0 = space
#1=triangle
#2=platform
#3=  lower + higher platform 750ms gap 
#4= double triangle in contact
#5 = drop down platform/ close platform
#6 = triple triangle 
#7 = quadruple triangle



screen = pygame.display.set_mode((1400, 700))
pygame.display.set_caption("Geometry Slash")

background = pygame.image.load("full.jpg").convert()
background=pygame.transform.smoothscale(background,(1400,700))

ground=pygame.image.load("groundbox.jpg").convert()
ground=pygame.transform.smoothscale(ground,(1448,175))

clock = pygame.time.Clock()

mapscroll = 0
mapscrollspeed = 12
spin=0

trianglescroll=0
trianglescrollspeed=12
triangle=[]

tilegen = [
    # INTRO BEATS (Continuous Low-Tier Jumps & Platforms)
    1, 2, 1, 2, 1, 3, 2, 1, 1, 2, 1, 3, 1, 2, 5, 2, 1, 2, 1, 3,
    
    # DROP / CHORUS (High Density Spikes & Staggered Platforms)
    4, 4, 1, 4, 2, 3, 5, 2, 4, 1, 6, 2, 3, 5, 4, 4, 1, 6, 2, 3,
    4, 1, 4, 6, 2, 3, 5, 4, 1, 4, 7, 2, 3, 5, 4, 6, 1, 4, 2, 3,

    # VERSE 1 CADENCE (Rapid Single/Double Spikes & Platform Drops)
    1, 1, 4, 1, 1, 2, 5, 2, 1, 4, 1, 6, 2, 3, 1, 1, 4, 1, 5, 2,
    1, 4, 1, 6, 2, 3, 1, 1, 4, 5, 2, 3, 1, 4, 1, 7, 2, 3, 5, 2,

    # HOOK & BREAKDOWN (Quad Spikes & Stacks)
    7, 4, 6, 4, 2, 3, 5, 2, 7, 4, 6, 1, 3, 5, 2, 7, 6, 4, 2, 3,
    7, 4, 6, 4, 2, 3, 5, 2, 7, 4, 6, 1, 3, 5, 2, 7, 6, 4, 2, 3,

    # OUTRO / FINALE
    4, 6, 7, 4, 2, 3, 5, 2, 6, 7, 4, 1, 2, 3, 5, 2, 1, 1, 1, 1,

    # MANDATORY ENDING PADDING (Prevents pop(0) IndexError)
    0, 0, 0]

#tilegen=[7,6,5,4,3,2,1,1,0,0,0,1,0,0,0]


interval=1500
last_spawn_tick= pygame.time.get_ticks()


class geobox(pygame.sprite.Sprite):
    def __init__(self):
        box_img= pygame.image.load("geobox.jpg").convert()
        box_img =pygame.transform.smoothscale(box_img,(70,70))

        self.original_box_img= box_img
        self.box = box_img.get_rect(center=(635,495))
        self.box_img = box_img
        self.gravity = 0
        self.angle = 0
        self.target_angle = 0
        self.spin = 5.5
        self.inair=False
        self.groundlevel=460

    def render(self, screen):
        screen.blit(self.box_img, self.box) 

    def appgravity(self):
        self.gravity+=1
        self.box.y+=self.gravity
        if self.box.y>=self.groundlevel:
            self.box.y=self.groundlevel
            self.gravity=0
            self.inair=False

    def jump(self):
        if self.box.y== self.groundlevel:
            self.gravity=-20
            self.target_angle -= 90
            self.inair=True

    def updaterotation(self):
        if self.angle > self.target_angle and self.inair==True:
            self.angle -= self.spin
            if self.angle < self.target_angle:
                self.angle = self.target_angle

        old_center = self.box.center
        self.box_img = pygame.transform.rotate(self.original_box_img, self.angle)
        self.box = self.box_img.get_rect(center=old_center)
        
            
    def update(self):
        box.appgravity()
        self.updaterotation()


class triangles(pygame.sprite.Sprite):
    def __init__(self,tile_type):
        self.vertices= [[1425, 475], [1400, 525], [1450, 525]]
        self.vertices2=[[1475, 475], [1450, 525], [1500, 525]]
        self.vertices3=[[1525, 475], [1500, 525], [1550, 525]]
        self.vertices4=[[1575, 475], [1550, 525], [1600, 525]]

        self.trirect=pygame.Rect(1400, 475, 50, 50)
        self.trirect2=pygame.Rect(1400, 525, 100, 50)
        self.trirect3=pygame.Rect(1400,525,150,50)
        self.trirect4=pygame.Rect(1400,525,200,50)


        self.rect=pygame.Rect(1400, 425, 110, 10)
        self.rect2=pygame.Rect(1900,325, 110, 10)
        self.rect3=pygame.Rect(1150, 425, 110, 10)

        self.rectlist=[]
        self.rectlist2=[]
        self.rectlist3=[]

        self.rectlist.append(self.rect)
        self.rectlist2.append(self.rect2)
        self.rectlist3.append(self.rect3)


        self.tile_type=tile_type


    def drawtri(self):
        if self.tile_type==1:
            pygame.draw.polygon(screen, (0,0,0),self.vertices)
            for y in self.vertices: y[0]-=trianglescrollspeed
            self.trirect.x-=trianglescrollspeed

        if self.tile_type==2:
            pygame.draw.rect(screen, (0,0,0),self.rect)
            for y in self.rectlist: y.x-=trianglescrollspeed

        if self.tile_type==3:
            pygame.draw.rect(screen, (0,0,0),self.rect)
            for y in self.rectlist: y.x-=trianglescrollspeed

            pygame.draw.rect(screen, (0,0,0),self.rect2)
            for z in self.rectlist2: z.x-=trianglescrollspeed

        if self.tile_type==4:
            pygame.draw.polygon(screen, (0,0,0),self.vertices)
            for y in self.vertices: y[0]-=trianglescrollspeed
            self.trirect.x-=trianglescrollspeed

            pygame.draw.polygon(screen, (0,0,0),self.vertices2)
            for y in self.vertices2: y[0]-=trianglescrollspeed
            self.trirect2.x-=trianglescrollspeed

        if self.tile_type==5:
            pygame.draw.rect(screen, (0,0,0),self.rect3)
            for y in self.rectlist3: y.x-=trianglescrollspeed

        if self.tile_type==6:
            pygame.draw.polygon(screen, (0,0,0),self.vertices)
            for y in self.vertices: y[0]-=trianglescrollspeed
            self.trirect.x-=trianglescrollspeed

            pygame.draw.polygon(screen, (0,0,0),self.vertices2)
            for y in self.vertices2: y[0]-=trianglescrollspeed
            self.trirect2.x-=trianglescrollspeed

            pygame.draw.polygon(screen, (0,0,0),self.vertices3)
            for y in self.vertices3: y[0]-=trianglescrollspeed
            self.trirect3.x-=trianglescrollspeed

        if self.tile_type==7:
            pygame.draw.polygon(screen, (0,0,0),self.vertices)
            for y in self.vertices: y[0]-=trianglescrollspeed
            self.trirect.x-=trianglescrollspeed

            pygame.draw.polygon(screen, (0,0,0),self.vertices2)
            for y in self.vertices2: y[0]-=trianglescrollspeed
            self.trirect2.x-=trianglescrollspeed

            pygame.draw.polygon(screen, (0,0,0),self.vertices3)
            for y in self.vertices3: y[0]-=trianglescrollspeed
            self.trirect3.x-=trianglescrollspeed

            pygame.draw.polygon(screen, (0,0,0),self.vertices4)
            for y in self.vertices4: y[0]-=trianglescrollspeed
            self.trirect4.x-=trianglescrollspeed
        


    def collisoncheck(self, box):
        if self.trirect.colliderect(box.box) and self.tile_type==1:
            pygame.quit()
            exit()

        if self.trirect2.colliderect(box.box) and self.tile_type==4:
            pygame.quit()
            exit()

        if self.trirect3.colliderect(box.box) and self.tile_type==6:
            pygame.quit()
            exit()

        if self.trirect4.colliderect(box.box) and self.tile_type==7:
            pygame.quit()
            exit()

        if self.tile_type == 2:
            horizontal_overlap = (box.box.right > self.rect.left) and (box.box.left < self.rect.right)
            if horizontal_overlap and box.box.bottom <= self.rect.bottom + 10 and box.gravity >= 0:
                box.groundlevel = self.rect.top - box.box.height + 1
                return True
            
        if self.tile_type == 3:
            horizontal_overlap2 = (box.box.right > self.rect2.left) and (box.box.left < self.rect2.right)
            if horizontal_overlap2 and box.box.bottom <= self.rect2.bottom + 10 and box.gravity >= 0:
                box.groundlevel = self.rect2.top - box.box.height + 1
                return True
            
            horizontal_overlap = (box.box.right > self.rect.left) and (box.box.left < self.rect.right)
            if horizontal_overlap and box.box.bottom <= self.rect.bottom + 10 and box.gravity >= 0:
                            box.groundlevel = self.rect.top - box.box.height + 1
                            return True

        if self.tile_type == 5:
            horizontal_overlap = (box.box.right > self.rect3.left) and (box.box.left < self.rect3.right)
            if horizontal_overlap and box.box.bottom <= self.rect3.bottom + 10 and box.gravity >= 0:
                box.groundlevel = self.rect3.top - box.box.height + 1
                return True
        
        return False

pygame.mixer.music.load("Alright.mp3")
pygame.mixer.music.play(-1)
box=geobox()

while True:

    current_tick = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                box.jump()

    screen.blit(background,(0,0))
    screen.blit(ground,(mapscroll,525))
    mapscroll-=mapscrollspeed
    if mapscroll<=-48:
        mapscroll=0
    spin+=1 

    box.update()
    box.render(screen)

    if current_tick - last_spawn_tick >= interval:
        tile_type=tilegen.pop(0)
        new_triangle = triangles(tile_type)
        triangle.append(new_triangle)
        last_spawn_tick = current_tick
        

    on_platform = False
    for tri in triangle:
        tri.drawtri()
        if tri.collisoncheck(box):
            on_platform = True
        if tri.rect.right < 0:
            triangle.remove(tri)


    if not on_platform and box.groundlevel != 460:
        box.groundlevel = 460
        box.inair = True
    pygame.display.update()
    clock.tick(60)  