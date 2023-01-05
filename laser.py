import pygame

class Laser(pygame.sprite.Sprite):    #Vamos a configurar aquí el laser
    def __init__(self,pos,velocidad,altura_ventana):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill("Yellow")
        self.rect = self.image.get_rect(center = pos)
        self.velocidad = velocidad
        self.alturaventana = altura_ventana

    def destruye(self): #Destruimos los lásers, para que no se acumulen
        if self.rect.y <= -50 or self.rect.y >= self.alturaventana + 50:
            self.kill()


    def update(self): #Le damos su velocidad en "y" al láser
        self.rect.y += self.velocidad
        self.destruye()
