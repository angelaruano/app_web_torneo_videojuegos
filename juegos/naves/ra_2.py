import pygame, sys
from pygame.locals import *
import random  # Para enemigos aleatorios
import os #Para que los directorios sean multiplataforma
from juegos.naves.run import *

#Directorios
carpeta_juego = os.path.dirname(__file__)
#imágenes
carpeta_imagenes = os.path.join(carpeta_juego, "imagenes")
carpeta_naves = os.path.join(carpeta_imagenes, "naves")
carpeta_potenciadores = os.path.join(carpeta_imagenes, "potenciadores")

#Creo la nave del jugador
class NaveJugador(pygame.sprite.Sprite):
	def __init__(self, game):
		super().__init__()
		self.game = game

		#Creo una lista vacía de animaciones a la que luego añado lista de imágenes de mis 3 dibujos de naves
		self.animaciones = []
		for x in range(4):
			file = "nave_{}.png".format(x + 1)
			imagen = pygame.image.load(os.path.join(carpeta_naves, file)).convert()
			imagen.set_colorkey((255,255,255))
			self.animaciones.append(imagen)

		self.image = self.animaciones[0] #Inicio con la primera imagen de la lista
		self.rect = self.image.get_rect() #Rectángulo de la nave
		self.rect.centerx = self.game.RESOLUCION[0]//2 #Centro del rectángulo de la imagen, aparece a mitad del eje x de la pantalla
		self.rect.y = self.game.RESOLUCION[1] - self.rect.height #La nave, en el eje y, aparece abajo restando el alto de la propia nave
		self.vel_x = 0 #Direcciones del eje x
		self.vel_y = 0 #Direcciones del eje y
		self.invisible = 199
		#Para hacerle una cadencia al disparo
		self.ultimo_disparo = pygame.time.get_ticks() #Atrapa el momento del disparo
		self.cadencia_disparo = 400  #Milisegundos (medio segundo)
		#Parámetros para hacer las animaciones del fuego propulsor, cambiando entre las 3 imágener
		self.fotograma = 0 #Empieza por fotograma 0
		self.ultimo_update = pygame.time.get_ticks() #Tiempo de la última actualización para implementar la siguiente función
		self.fotogramas_vel = 40 #Velocidad a la que pasan los fotogramas

	def update(self):
		#Animación de los fotogramas
		calculo = pygame.time.get_ticks() #Atrapa el momento de la última actualización del juego
		if calculo - self.ultimo_update > self.fotogramas_vel:
			self.ultimo_update = calculo
			self.fotograma += 1 #Cálculo para saber cuándo pasar al siguiente fotograma
			if self.invisible > 0:
				fin_animacion = len(self.animaciones)
			else:
				fin_animacion = len(self.animaciones) - 1
				
			if self.fotograma == fin_animacion:
				self.fotograma = 0
			
			centro = self.rect.centerx #Atrapo coordenadas del centro del rectángulo en eje x en el momento de pasar el fotograma
			y = self.rect.y #Y atrapo coordenadas del eje y
			if self.fotograma > 3:
				self.fotograma = 0
			#A continuación hago que el siguiente fotograma aparezca donde estaba el anterior
			self.image = self.animaciones[self.fotograma]
			self.rect = self.image.get_rect()
			self.rect.centerx = centro
			self.rect.y = y
			
		if self.invisible > 0:
			self.invisible -= 1
			
		self.game.invisible = self.invisible
		

		# Teclas para mover nave
		self.vel_x = 0
		self.tecla = pygame.key.get_pressed() #Para que se mueva manteniendo la tecla pulsada
		if self.tecla[pygame.K_LEFT]: #Si pulso flecha izquierda
			self.vel_x = -10 #Descuenta píxeles, por lo que va a la izquierda
		if self.tecla[pygame.K_RIGHT]: #Tecla derecha
			self.vel_x = 10 #Sumo píxeles, por lo qeu va a la derecha
		if self.tecla[pygame.K_SPACE]:
			calculo = pygame.time.get_ticks() #Atrapa el momento de la última actualización del juego
			if calculo - self.ultimo_disparo > self.cadencia_disparo:
				self.ultimo_disparo = calculo
				self.game.disparar()

		# Actualización de los movimientos de la nave
		self.rect.x += self.vel_x #Sumo la velocidad al eje x de la nave
		self.rect.y += self.vel_y

		#Creo los límites para no salir de la pantalla
		if self.rect.right > self.game.RESOLUCION[0]: #Si la parte derecha de la nave supera el ancho de la pantalla
			self.rect.right = self.game.RESOLUCION[0] #Que se quede en el ancho
		if self.rect.left < 0: #Si la coordenada izquierda de la nave en menor que 0 (límite izquierdo de la pantalla)
			self.rect.left = 0 #Que se quede ahí


class Disparo(pygame.sprite.Sprite):
	def __init__(self, game, x, y, disparo_lados):
		super().__init__()
		self.game = game
		self.image = pygame.image.load(os.path.join(carpeta_naves, "bala.png")).convert()
		self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.y = y
		self.vel_x = disparo_lados
		self.vel_y = -15

	def update(self):
		self.rect.y += self.vel_y
		self.rect.x += self.vel_x
		if self.rect.bottom < 0:
			self.kill() #En caso de que la bala llegue arriba, desaparece

class Potenciadores(pygame.sprite.Sprite):
	def __init__(self, game, x, y, aleatorio):
		super().__init__()
		self.game = game
		self.aleatorio = aleatorio
		file = "potenciador_{}.png".format(self.aleatorio + 1)
		self.image = pygame.image.load(os.path.join(carpeta_potenciadores, file)).convert()
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.y = y
		self.vel_y = 5

	def update(self):
		self.rect.y += self.vel_y
		if self.rect.top > self.game.RESOLUCION[1]:
			self.kill()


