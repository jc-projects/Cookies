import pygame, random, sys

velcookies=0
cantcookies=10
cantbrocolis=5
fps=15
max=0

#Clases y funciones del menu          
class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
    
    def update(self):
        self.left,self.top=pygame.mouse.get_pos()
        
class Boton(pygame.sprite.Sprite):
    def __init__(self,imagen1,imagen2,x=200,y=200):
        self.imagen_normal=imagen1
        self.imagen_seleccion=imagen2
        self.imagen_actual=self.imagen_normal
        self.rect=self.imagen_actual.get_rect()
        self.rect.left,self.rect.top=(x,y)
        
    def update(self,pantalla,cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual=self.imagen_seleccion
        else: 
            self.imagen_actual=self.imagen_normal
            
        pantalla.blit(self.imagen_actual,self.rect)
        
#Clases y funciones del juego
class Recs(object):
    def __init__(self, numeroinicial):
        self.lista=[]
        for x in range(numeroinicial):
            #Creo un rect random
            leftrandom=random.randrange(2, 750)
            toprandom=random.randrange(-460, -10)
            width=random.randrange(10, 30)
            height=random.randrange(15, 30)
            self.lista.append(pygame.Rect(leftrandom, toprandom, width, height))
    def reagregar(self):
        for x in range(len(self.lista)):
            if self.lista[x].top>480:
                leftrandom=random.randrange(2, 750)
                toprandom=random.randrange(-460, -10)
                width=random.randrange(10, 30)
                height=random.randrange(15, 30)
                self.lista[x]=(pygame.Rect(leftrandom, toprandom, width, height))
            
    def mover(self, velcookies):
        for rectangulo in self.lista:
            rectangulo.move_ip(0, velcookies)
    def pintar(self, superficie, imagen):
        for rectangulo in self.lista:
            #pygame.draw.rect(superficie, (255, 0, 0), rectangulo)
            superficie.blit(imagen,rectangulo)

class Player(pygame.sprite.Sprite):
    def __init__(self, imagen):
        self.imagen=imagen
        self.rect=self.imagen.get_rect()
        self.rect.top, self.rect.left=405, 350
    def mover(self, vx):
        #self.rect.move_ip(vx, 0)
        if self.rect.left + vx < 0:
            self.rect.left = 0
        elif self.rect.right + vx > 800:
            self.rect.right = 800
        else:
            self.rect.move_ip(vx, 0)
    def update(self, superficie):
        superficie.blit(self.imagen, self.rect)

def colision(player, recs):
    for rec in recs.lista:
        if player.rect.colliderect(rec):
            return True
    return False

#Clase del juego
def gameLoop(velcookies):
    #Setea ventana
    pantalla1=pygame.display.set_mode((800, 500))
    fuente1=pygame.font.SysFont("data/vgafix.fon", 30, False, False)
    
    #Setea musica
    grito=pygame.mixer.Sound("data/sound/cookies_grito.wav")
    nom=pygame.mixer.Sound("data/sound/niam.wav")
    pygame.mixer.music.load("data/sound/theme.mp3")
    
    #Setea imagenes
    fondo=pygame.image.load("data/image/fondo.jpg")
    monster=pygame.image.load("data/image/monster.png")
    cookie=pygame.image.load("data/image/cookie.png")
    brocoli=pygame.image.load("data/image/brocoli.png")
    top=pygame.image.load("data/image/top.png")
    gameover=pygame.image.load("data/image/gameover.png")
    
    #Variables auxiliares
    salir=False
    recs1=Recs(cantcookies)
    recs2=Recs(cantbrocolis)
    player1=Player(monster)
    vx=0
    velocidad=25
    leftsigueapretada, rightsigueapretada=False, False
    colisiono=False
    death=True
    comidas=0
    global max
    repe=velcookies
    
    pygame.mixer.music.play(3)
    pygame.mixer.music.set_volume(0.4)
    while salir!=True:
        contador=fuente1.render("Cookies comidas:"+str(comidas), 0, (255, 255, 255))
        maxcomidas=fuente1.render("Top cookies comidas:"+str(max), 0, (255, 255, 255))
        pantalla1.fill((0, 0, 0))
        pantalla1.blit(fondo, (0, -150))
        recs1.pintar(pantalla1, cookie)
        recs2.pintar(pantalla1, brocoli)
        pantalla1.blit(top, (0, 0))
        pantalla1.blit(contador, (575, 17))
        pantalla1.blit(maxcomidas, (30, 17))
        player1.update(pantalla1)
        pygame.display.update()
        recs1.reagregar()
        recs2.reagregar()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if colisiono==False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        leftsigueapretada=True
                        vx=-velocidad
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        rightsigueapretada=True
                        vx=velocidad
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        leftsigueapretada=False
                        if rightsigueapretada:
                            vx=velocidad
                        else:
                            vx=0
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        rightsigueapretada=False
                        if leftsigueapretada:
                            vx=-velocidad
                        else:
                            vx=0
        
        for rec in recs1.lista:
            if player1.rect.colliderect(rec):
                comidas+=1
                rec.x=0
                rec.y=0
                nom.play()      
        if colision(player1, recs2):
            colisiono=True
            pygame.mixer.music.stop()
            grito.play()
            while death==True:
                pantalla1.blit(gameover, (0, 0))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if (max<comidas):
                            max=comidas
                        death=False
                        gameLoop(repe)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
        if colisiono==False:
            player1.mover(vx)
            recs2.mover(velcookies)
            recs1.mover(velcookies)
 
#Menu
def main():
    pygame.init()
    pantalla=pygame.display.set_mode((800,500))
    pygame.display.set_caption("COOKIES!")
    salir=False
    reloj1= pygame.time.Clock()
    
    #Setea imagenes
    fondomenu=pygame.image.load("data/image/fondomenu.png")
    juegofacil=pygame.image.load("data/image/juegofacil.png")
    juegodificil=pygame.image.load("data/image/juegodificil.png")
    historia=pygame.image.load("data/image/historia.png")
    salir=pygame.image.load("data/image/salir.png")
    fondohistoria=pygame.image.load("data/image/fondohistoria.png")
    
    #Setea botones
    boton1=Boton(juegofacil,juegofacil,260,210)
    boton2=Boton(juegodificil,juegodificil,240,260)
    boton3=Boton(historia,historia,300,310)
    boton4=Boton(salir,salir,330,360)
    
    #Setea sonidos
    sonido1=pygame.mixer.Sound("data/sound/boton.wav")
    sound_jugar=pygame.mixer.Sound("data/sound/really.wav")   
    
    pantalla.blit(fondomenu,(0,0))
    cursor1=Cursor()
    boton1.update(pantalla, cursor1)
    boton2.update(pantalla, cursor1)
    boton3.update(pantalla, cursor1)
    boton4.update(pantalla, cursor1)
    
    while salir!=True:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(boton1.rect):
                    sound_jugar.play()
                    gameLoop(5)
                if cursor1.colliderect(boton2.rect):
                    sound_jugar.play()
                    gameLoop(10)
                if cursor1.colliderect(boton3.rect):
                    sonido1.play()
                    pantalla.blit(fondohistoria,(0,0))
                if cursor1.colliderect(boton4.rect):
                    salir=True
            if event.type==pygame.QUIT:
                salir=True
                
        reloj1.tick(fps)
        cursor1.update()
        pygame.display.update()
    pygame.quit()
main()
