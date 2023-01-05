import pygame
from laser import Laser #Traemos al laser del archivo


class Jugador(pygame.sprite.Sprite): #Creamos el jugador o "nave"
    def __init__(self,pos,limite,velocidad): #En esta parte introducimos los datos, imágenes de nuestro jugador
        super().__init__()
        self.image = pygame.image.load("jugador.png").convert_alpha() #Imágen del jugador
        self.rect = self.image.get_rect(midbottom = pos) #Declaramos donde va la imagen, que está dada fuera de esta funcion
        self.velocidad = velocidad
        self.limite_max_x = limite
        self.listo = True #Configurar cada cuanto se dispara nuestro láser
        self.laser_tiempo = 0
        self.laser_cooldown = 600

        self.laserx = pygame.sprite.Group()
        self.las = pygame.mixer.Sound("audio/laser.wav")
        self.las.set_volume(0.3)
    def get_input(self):         #Estas son las instrucciones que el jugador recibirá
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_RIGHT]: #Decimos que si se presiona esta tecla se realizarán las intrucciones
            self.rect.x += self.velocidad
        elif teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_SPACE] and self.listo:
            self.disparo()
            self.listo = False
            self.laser_tiempo = pygame.time.get_ticks()
            self.las.play()

    def recarga(self):
        if not self.listo:
            tiempo = pygame.time.get_ticks()
            if tiempo - self.laser_tiempo >= self.laser_cooldown:
                self.listo = True

    def disparo(self): #Configuramos el disparo del láser
        self.laserx.add(Laser(self.rect.center, -8,self.rect.bottom))

    def limite(self):  #Configuramos lo que pasa si el jugador llega al límite de la ventana
        if self.rect.left <= 0:
           self.rect.left = 0
        if self.rect.right >= self.limite_max_x:
            self.rect.right = self.limite_max_x

    def update(self):
        self.get_input()
        self.limite()
        self.recarga()
        self.laserx.update()


