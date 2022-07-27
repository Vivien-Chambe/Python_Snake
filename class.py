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