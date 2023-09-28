# Los sprites son rectángulos (todas las imágenes en pygame lo son, solo que con transparencias)
import pygame, sys
from pygame.locals import *
import random  # Para enemigos aleatorios
import os #Para que los directorios sean multiplataforma

import main
from juegos.arkanoid.clases import *

class GameArkanoid:
    def __init__(self):
        pygame.init() #Para iniciar juego
        pygame.mixer.init() #Para el sonido

        #Colores
        self.AZUL_C = (144,205,205)
        self.GRIS_C = (120,120,120)
        self.GRIS = (67,67,67)
        self.GRIS2 = (170,170,170)
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.ROJO = (255, 0, 0)
        self.AZUL = (0, 0, 255)
        self.VERDE = (0, 255, 0)
        self.AMARILLO = (255,241,9)
        self.NARANJA = (255,109,13)
        self.MORADO = (194,13,255)

        #Estados iniciales del juego
        self.rejugar = False
        self.gameOver = True #De inicio es True, hasta que empiece a jugar
        self.nivel1_superado = False
        self.puntos = 0
        self.nivel1 = 1
        #Instancio texto de la pantalla de inicio
        self.texto_inicio = Texto(self)

        #Pantalla
        self.RESOLUCION = (1020,660)
        self.FPS = 60 #Frames per second(velocidad del juego)
        #Tamaño de los ladrillos
        self.BLOQUE_ANCHO = 60
        self.BLOQUE_ALTO = 30
        #Límites de la pantalla
        self.LIMITE_IZQ = 60
        self.LIMITE_DER = 960
        self.LIMITE_UP = 30
        self.LIMITE_DOWN = 660

        self.pantalla = pygame.display.set_mode(self.RESOLUCION) #Invoco pantalla
        pygame.display.set_caption("ARKANOID") #Nombre de la pantalla
        self.reloj = pygame.time.Clock() #Velocidad del juego conjugado con FPS y reloj.tick
        self.crear_listas_imagenes() #Invoco a la función para las imágenes

    # La siguiente función es para las listas de sprites
    # Los sprites son rectángulos (todas las imágenes en pygame lo son, solo que con transparencias)
    # Sirven para luego poder crear colisiones
    def crear_listas_imagenes(self):
        self.lista_sprites_dibujar = pygame.sprite.Group()
        self.lista_ladrillo = pygame.sprite.Group()
        self.lista_pala = pygame.sprite.Group()
        self.lista_pelotas = pygame.sprite.Group()
        self.lista_poderes = pygame.sprite.Group()
    
    #La siguiente función es para vaciar la pantalla de imágenes con el método empty en caso de Game Over
    def vaciar_listas(self):
        self.lista_sprites_dibujar.empty()
        self.lista_ladrillo.empty()
        self.lista_pala.empty()
        self.lista_pelotas.empty()
        self.lista_poderes.empty()
    def nuevo_juego(self):
        self.puntos = 0
        self.vidas = 3
        self.nivel1 = 1
        self.nuevo_nivel()

        #Instancio la pelota
        self.pelota = Pelota(self, self.BLOQUE_ANCHO * 9,self.BLOQUE_ALTO * 19,velocidad_x=7, velocidad_y= -7)
        self.lista_sprites_dibujar.add(self.pelota)
        self.lista_pelotas.add(self.pelota)
        self.pelota2 = Pelota(self, self.BLOQUE_ANCHO * 9,self.BLOQUE_ALTO * 19,velocidad_x=7, velocidad_y= -7)
        self.pelota3 = Pelota(self, self.BLOQUE_ANCHO * 9,self.BLOQUE_ALTO * 19,velocidad_x=7, velocidad_y= -7)

        #Instancio la pala
        self.pala = Pala(self, self.RESOLUCION[0]//2, self.RESOLUCION[1] - (self.BLOQUE_ALTO*2), velocidad_x = 6)
        self.lista_sprites_dibujar.add(self.pala)
        self.lista_pala.add(self.pala)

        #Instancio puntos
        self.texto_puntos = Texto(self)
        #Instancio vidas
        self.texto_vidas = Texto(self)

    def nuevo_nivel(self):

        self.dibujarlimites = DibujarLimites(self) #Creo un objeto de la clase DibujarLimites que usaré en la función draw
        #Hago un bucle for con las coordenadas x,y, para que me salgan varias filas y columnas de ladrillos,
        # Dividiendo mis límites entre largo y ancho de ladrillos, éstos saldrían
        # desde la fila 3 a la 7 (multiplicados por el ancho,60) y desde la columna 3 a la 14 por el alto, 30
        for y in range(3, 7, 1):
            for x in range(3, 14, 1):
                #Creo el aleatorio
                self.aleatorio = random.randrange(7) + 1
                #Instancio ladrillo
                self.ladrillo = Ladrillo(self, x * self.BLOQUE_ANCHO, y * self.BLOQUE_ALTO, self.aleatorio)

                self.lista_sprites_dibujar.add(self.ladrillo) #Dibujo ladrillo
                self.lista_ladrillo.add(self.ladrillo) #Para las colisiones

    def update(self):
        if not self.gameOver:
            self.lista_sprites_dibujar.update()

        self.reloj.tick(self.FPS)
        pygame.display.update()

    def draw(self):
        self.pantalla.fill(self.GRIS_C)
        
        #draws

        if not self.gameOver:
            self.dibujarlimites.dibujar_limites()
            self.texto_puntos.muestra_texto(self.pantalla,consolas, str("PUNTOS: {}".format(self.puntos)),self.ROJO,25,70,10)
            self.texto_vidas.muestra_texto(self.pantalla,consolas, str("TE QUEDAN {} VIDAS".format(self.vidas -1)),self.VERDE,25,660,10)
            self.lista_sprites_dibujar.draw(self.pantalla)
            
        if self.gameOver:
            self.texto_inicio.muestra_texto(self.pantalla,consolas,str("Pulse cualquier tecla para comenzar"),self.AMARILLO,40,510,230)
            
    def guarda_puntos(self,puntaje):
        if puntaje >0 or puntaje <0:
            print("mando",puntaje)
            main.puntuacion_arkanoid(puntaje)

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.puntuacion_definitiva = self.puntos
                self.guarda_puntos(self.puntuacion_definitiva)
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and self.gameOver:
                self.puntuacion_definitiva = self.puntos
                self.guarda_puntos(self.puntuacion_definitiva)
                if pygame.K_KP_ENTER:
                    self.gameOver = False
                    self.nuevo_juego()
                    self.run()

    def run(self):
        while not self.gameOver:
            self.check_event()
            self.update()
            self.draw()

        while self.gameOver:
            self.update()
            self.draw()
            self.check_event()

if __name__ == "__main__":
    game = GameArkanoid()
    game.run()



#Crear los poderes
#hacer la bola más rápida y repasar las físicas de movimiento
#Crear game over
#Crear niveles