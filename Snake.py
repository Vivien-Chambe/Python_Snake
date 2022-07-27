from re import X
import pygame, os,sys
import random as r


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

graphics_dir = resource_path("Graphics")

pygame.init()

#Initialisation de la fenêtre de travail
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
width = 700
height = 700
screen = pygame.display.set_mode((width,height))

snake_head = pygame.image.load(graphics_dir + "/snek_head.png")
help_surface = pygame.image.load(graphics_dir + "/help.png")
snake_body = pygame.Surface((20,20))
snake_body.fill("#22b14c")

background = pygame.Surface((width,height))
background.fill("Black")

pomme = pygame.Surface((20,20))
pomme.fill("Red")

fill_surface = pygame.Surface((200,50))
fill_surface.fill("White")

state = None 


class Snake:
    def __init__(self,x,y,orientation,taille):
        self.headx = x
        self.heady = y
        self.orientation = orientation
        self.taille = taille
        self.body_coords = []
        
    def move(self,x):
        if self.taille > 1:
            for i in range(1,(self.taille)):
                self.body_coords[-(i)] = self.body_coords[-(i+1)]
        if self.orientation == "Est": self.headx += x
        elif self.orientation == "Ouest": self.headx -= x
        elif self.orientation == "Nord": self.heady -= x
        elif self.orientation == "Sud": self.heady += x
        self.body_coords[0] = [self.headx,self.heady]

    def blit(self):
        screen.blit(snake_head,(self.body_coords[0][0],self.body_coords[0][1]))
        for i in range (self.taille-1):
            screen.blit(snake_body,(self.body_coords[i+1][0],self.body_coords[i+1][1]))
    
    def check_itself(self):
        if screen.get_at((self.headx, self.heady)) == (34, 177, 76, 255):
            global state
            state = "Perdu"

    def check_sortie(self):
        if self.headx < 0 or self.headx >= width or self.heady < 0 or self.heady >= height:
            global state
            state = "Perdu"
        

class Pomme:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def new_pom_coord(self):
        self.x = r.randrange(0,width,20)
        self.y = r.randrange(0,height,20)
        if screen.get_at((self.x, self.y)) == (34, 177, 76, 255):
            self.new_pom_coord()
            print("occupé")

Snek = Snake(360,360,"Est",1)
Pom = Pomme(0,0) 
difficulty = 10

def check_eat():
     if Snek.headx == Pom.x and Snek.heady == Pom.y:
        Snek.taille += 1
        x = Pom.x
        y = Pom.y
        Snek.body_coords.append([x,y])
        Pom.new_pom_coord()



def finish():
    screen.blit(background,(0,0))
    resultat = font.render(f"Votre score : {(Snek.taille)-1}",False,"White")
    screen.blit(resultat,(250,350))

def start():
    screen.blit(background,(0,0))
    screen.blit(help_surface,(70,100))
    Snek.headx, Snek.heady, Snek.orientation, Snek.taille = 360,360,"Est",1
    screen.blit(snake_head,(Snek.headx,Snek.heady))
    Pom.new_pom_coord()
    Snek.body_coords = [[Snek.headx,Snek.heady]]
    global state,difficulty
    state = "Pause"
    #difficulty = int(input("Choix difficulté (1-10)"))
    


start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and Snek.orientation != "Est" :
                Snek.orientation = "Ouest"
            elif event.key == pygame.K_RIGHT and Snek.orientation != "Ouest":
                Snek.orientation = "Est"
            elif event.key == pygame.K_UP and Snek.orientation != "Sud":
                Snek.orientation = "Nord"
            elif event.key == pygame.K_DOWN and Snek.orientation != "Nord":
                Snek.orientation = "Sud"
            elif event.key == pygame.K_r:
                start()
            elif event.key == pygame.K_s:
                if state == "Jeu":
                    state = "Pause"
                elif state == "Pause":
                    state = "Jeu"
            elif event.key == pygame.K_t:
                Snek.taille += 1
                Snek.body_coords.append([0,0])



    if state == "Jeu":
        Snek.move(20)
        try:
            Snek.check_itself() # Les coordonnées du point suivant sont déjà calculées dinc pas moyen de changer
        except IndexError:
            print("Hors Map")
        screen.blit(background,(0,0))
        screen.blit(pomme,(Pom.x,Pom.y))
        Snek.blit()
        Snek.check_sortie()
        check_eat()
    if state == "Perdu":
        finish()
        

    # Tracking Cursor ###############################
    #position_surface = font.render(str(pygame.mouse.get_pos()), False, "Black")
    #screen.blit(fill_surface,(0,0))
    #screen.blit(position_surface,(0,0))
    #################################################

    pygame.display.update()
    clock.tick(difficulty*2)