import pygame

class Marciano(pygame.sprite.Sprite): #Configuramos al marciano
    def __init__(self,tipo,x,y):
        super().__init__()
        imageneleccion = "marcianos/"+tipo+".png"
        self.image = pygame.image.load(imageneleccion).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        if tipo == "rojo":
            self.valor = 100
        elif tipo == "verde":
            self.valor = 200
        elif tipo == "amarillo":
            self.valor = 300

    def update(self,direccion):
        self.rect.x += direccion
