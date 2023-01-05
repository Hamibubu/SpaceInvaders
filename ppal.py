import pygame, sys
from io import open
from jugador import Jugador                     #Traemos al jugador de el otro archivo a acá
import obstaculo
from marcianos import Marciano
from random import choice
from laser import Laser
class Juego:
    def __init__(self):   #Declaramos los sprites
        jugador_sprite = Jugador((anchura_ventana/2,altura_ventana),anchura_ventana,4)   #Igualamos la clase del jugador y su posición
        self.jugador = pygame.sprite.GroupSingle(jugador_sprite)
        self.vida = 3
        self.mostrarvida = pygame.image.load("jugador.png").convert_alpha()
        self.vidaposicx = anchura_ventana - (self.mostrarvida.get_size()[0]*2+20)
        self.punto =  0
        self.font = pygame.font.Font("letra/Pixeled.ttf",20)
        self.forma = obstaculo.forma
        self.tamaño_obstaculo = 5
        self.obstaculos = pygame.sprite.Group()
        self.numero_obstaculos = 4
        self.posiciones = [i * anchura_ventana/self.numero_obstaculos for i in range(self.numero_obstaculos)]
        self.crearobstaculos(self.posiciones,ix= anchura_ventana/15,iy=480)
        self.marciano = pygame.sprite.Group()
        self.lasermarciano = pygame.sprite.Group()
        self.marcianoset(filas=6, columnas=7)
        self.aldireccion = 1
        global musica
        musica = pygame.mixer.Sound("audio/music.wav")
        musica.set_volume(0.1)
        musica.play(loops=-1)
        self.explota = pygame.mixer.Sound("audio/laser.wav")
        self.explota.set_volume(0.1)
        self.las = pygame.mixer.Sound("audio/laser.wav")
        self.las.set_volume(0.1)

    def crearobstaculo(self,ix,iy,offset_i):       #Ciclo para convertir esas 0 en partes de nuestro obstaculo
        for index, i in enumerate(self.forma):
            for cindex , columna in enumerate(i):
                if columna == "0":
                    x = ix + cindex * self.tamaño_obstaculo + offset_i
                    y = iy + index * self.tamaño_obstaculo
                    bloque = obstaculo.Obstaculo(self.tamaño_obstaculo,(241,79,80),x,y)
                    self.obstaculos.add(bloque)

    def marcianoset(self,filas,columnas,distanciax=60,distanciay=48,offsetx=70,offsety=100):
        for index, i in enumerate(range(filas)):
            for cindex , columna in enumerate(range(columnas)):
                y = index * distanciay + offsetx
                x = cindex * distanciax + offsety
                if index == 0:
                    alien = Marciano("amarillo",x,y)
                elif 1 <= index <= 2:
                    alien = Marciano("verde",x,y)
                else:
                    alien = Marciano("rojo",x,y)
                self.marciano.add(alien)

    def checar_posicion(self):
        for alien in self.marciano.sprites():
            if  alien.rect.right >= anchura_ventana:
                self.aldireccion = -1
                self.checar_posicionabajo(2)
            elif alien.rect.left <= anchura_ventana-anchura_ventana:
                self.aldireccion = +1
                self.checar_posicionabajo(2)

    def checar_posicionabajo(self,distancia):
        if self.marciano:
            for alien in self.marciano.sprites():
                alien.rect.y += distancia

    def crearobstaculos(self,offset,ix,iy):
        for offset_i in offset:
            self.crearobstaculo(ix,iy,offset_i)

    def disparomarciano(self):
        if self.marciano:
            disparorandom = choice(self.marciano.sprites())
            marlaser = Laser(disparorandom.rect.center,5,altura_ventana)
            self.lasermarciano.add(marlaser)
            self.las.play()

    def puntaje(self):
        punt = self.font.render(f"Puntos : {self.punto}",False,"white")
        puntrect = punt.get_rect(topleft = (0,0))
        ventana.blit(punt, puntrect)

    def colisiones(self):

        #Configuramos el laser del jugador
        if self.jugador.sprite.laserx:
            for laser in self.jugador.sprite.laserx:
                if pygame.sprite.spritecollide(laser,self.obstaculos,True):
                    laser.kill()
                golpe = pygame.sprite.spritecollide(laser,self.marciano,True)
                if golpe:
                    for marcianos in golpe:
                        self.punto += marcianos.valor
                        laser.kill()
                        self.explota.play()

        elif self.lasermarciano:
            for laser in self.lasermarciano:
                if pygame.sprite.spritecollide(laser,self.obstaculos,True):
                    laser.kill()
                elif pygame.sprite.spritecollide(laser,self.jugador,False):
                    laser.kill()
                    self.vida -= 1
                    if self.vida <= 0:
                        self.perdiste(juegoactivo)
        elif self.marciano:
            for destruccion in self.marciano:
                pygame.sprite.spritecollide(destruccion,self.obstaculos,True)
                if pygame.sprite.spritecollide(destruccion,self.jugador,False):
                    self.perdiste(juegoactivo)

    def vidas(self):
        for vida in range(self.vida-1):
            p = self.vidaposicx + (vida * (self.mostrarvida.get_size()[0] + 5))
            ventana.blit(self.mostrarvida,(p,8))

    def victoria(self):
        if not self.marciano.sprites():
            pt = True
            gana = self.font.render("Ganaste",False,"red")
            ganar = gana.get_rect(center=(anchura_ventana/2, altura_ventana/2))
            ventana.blit(gana,ganar)
            if pt:
                puntuacion = open("puntuaciones.txt", "a")
                puntos = self.punto
                puntuacion.write(f"{puntos},")
                puntuacion.close()
                pt = False
                return pt

    def menu(self,juegoactivo):
        while True:
            juegoactivo = False
            ventana.fill((30,30,30))
            self.fontt = pygame.font.Font("letra/Pixeled.ttf",32)
            self.fonty = pygame.font.Font("letra/Pixeled.ttf",20)
            self.fontyy = pygame.font.Font("letra/Pixeled.ttf",10)
            p = self.fontt.render("ARCADE INVADERS", False, "white")
            puntrect = p.get_rect(center = (anchura_ventana/2,100))
            pu = self.fonty.render("Presiona para empezar", False, "white")
            puntrectt = p.get_rect(center = (330,200))
            ventana.blit(pu, puntrectt)
            ventana.blit(p, puntrect)
            mx, my = pygame.mouse.get_pos()
            self.tacha = pygame.image.load("no.png").convert_alpha()
            self.x = self.tacha.get_rect()
            self.x.topright = (600, 10)
            boton = pygame.Rect(200,300,200,50)
            boton2 = pygame.Rect(200,400,200,50)
            botte = self.fontyy.render("Comienza", False, (0,0,0))
            bof = self.fontyy.render("Opciones", False, (0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                click = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button:
                        click = True
                if self.x.collidepoint((mx, my)):
                    if click:
                        pygame.quit()
                        sys.exit()
                if boton.collidepoint((mx, my)):
                    if click:
                        juegoactivo = True
                        return juegoactivo
                if boton2.collidepoint(((mx, my))):
                    if click:
                        juego.opciones()
            pygame.draw.rect(ventana, (241,79,80), boton)
            ventana.blit(botte, (260,310))
            pygame.draw.rect(ventana, (241,79,80), boton2)
            ventana.blit(bof, (260,410))
            ventana.blit(self.tacha, (550, 10))



            pygame.display.update()
            fps.tick(60)


    def opciones(self):
        ru = True
        while ru:
            ventana.fill((30,30,30))
            self.casa = pygame.image.load("casa.png").convert_alpha()
            self.csa = self.casa.get_rect()
            self.fontyy = pygame.font.Font("letra/Pixeled.ttf",10)
            pp = self.fontyy.render("Proyecto de Algoritmos y programacion", False, "white")
            puntrectd = pp.get_rect(center = (anchura_ventana/2,100))
            ventana.blit(pp, puntrectd)
            mx, my = pygame.mouse.get_pos()
            ventana.blit(self.casa, (0, 0))
            bottte = self.fontyy.render("Quitar musica", False, (0,0,0))
            botonf = pygame.Rect(200,300,200,50)
            pygame.draw.rect(ventana, (241,79,80), botonf)
            ventana.blit(bottte, (235,310))
            botttte = self.fontyy.render("Poner musica", False, (0,0,0))
            botonff = pygame.Rect(200,400,200,50)
            pygame.draw.rect(ventana, (241,79,80), botonff)
            ventana.blit(botttte, (235,410))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                click = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                if self.csa.collidepoint((mx, my)):
                    if click:
                        ru = False
                if botonf.collidepoint((mx, my)):
                    if click:
                        musica.set_volume(0.0)
                if botonff.collidepoint((mx, my)):
                    if click:
                        musica.set_volume(0.1)

            pygame.display.update()
            fps.tick(60)
    def perdiste(self, juegoactivo):
        run = True
        while run:
            ventana.fill((30, 30, 30))
            self.fontyxy = pygame.font.Font("letra/Pixeled.ttf",32)
            ppp = self.fontyxy.render("PERDISTE", False, "red")
            ppuntrectd = ppp.get_rect(center = (anchura_ventana/2,100))
            ventana.blit(ppp, ppuntrectd)
            mx, my = pygame.mouse.get_pos()
            botttee = self.fontyy.render("Salir del juego", False, (0,0,0))
            botonef = pygame.Rect(200,300,200,50)
            pygame.draw.rect(ventana, (241,79,80), botonef)
            ventana.blit(botttee, (240,310))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                click = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                if botonef.collidepoint((mx, my)):
                    if click:
                        puntuacion = open("puntuaciones.txt", "a")
                        puntos = self.punto
                        puntuacion.write(f"{puntos},")
                        puntuacion.close()
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            fps.tick(60)

    def run(self):       #Actualiza los sprites
        self.jugador.update()
        self.marciano.update(self.aldireccion)
        self.jugador.sprite.laserx.draw(ventana)
        self.jugador.draw(ventana)
        self.obstaculos.draw(ventana)
        self.marciano.draw(ventana)
        self.checar_posicion()
        self.colisiones()
        self.lasermarciano.update()
        self.lasermarciano.draw(ventana)
        self.vidas()
        self.puntaje()
        self.victoria()

if __name__ == "__main__":
    pygame.init()

    altura_ventana = 600
    anchura_ventana = 600
    ventana = pygame.display.set_mode((anchura_ventana,altura_ventana))
    fps = pygame.time.Clock()

    juego = Juego()

    timerlaser = pygame.USEREVENT + 1
    pygame.time.set_timer(timerlaser,700)

    juegoactivo = True


    juego.menu(juegoactivo)



    while juegoactivo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if juegoactivo:
                if event.type == timerlaser:
                    juego.disparomarciano()
        if juegoactivo:
            ventana.fill((30,30,30))
            juego.run()
            pygame.display.flip()
            fps.tick(60)
