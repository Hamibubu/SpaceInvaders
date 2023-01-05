import pygame

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self,tamaño,color,x,y):
        super().__init__()
        self.image = pygame.Surface((tamaño,tamaño))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))

forma = [  #La figura del obstaculo
"  0000000",
" 000000000",
"00000000000",
"00000000000",
"00000000000",
"000     000",
"00       00",]
