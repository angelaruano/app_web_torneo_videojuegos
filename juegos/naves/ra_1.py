import pygame, sys
from pygame.locals import *
import random  # Para enemigos aleatorios
import os  # Para que los directorios sean multiplataforma
from juegos.naves.run import *

# Directorios
carpeta_juego = os.path.dirname(__file__)
# imágenes
carpeta_imagenes = os.path.join(carpeta_juego, "imagenes")
carpeta_enemigos = os.path.join(carpeta_imagenes, "enemigos")
carpeta_explosiones = os.path.join(carpeta_imagenes, "explosiones")
carpeta_fondo = os.path.join(carpeta_imagenes, "fondo")


class Estrella(pygame.sprite.Sprite):
	def __init__(self, game):
		super().__init__()
		self.game = game
		self.estrellas_lista = ["estrella_imagen3x3.png", "estrella_imagen3x3.png", "estrella_imagen5x5.png",
								"estrella_imagen7x7.png"]
		self.estrellas_imagenes = []
		for imagen in self.estrellas_lista:
			self.estrellas_imagenes.append(pygame.image.load(os.path.join(carpeta_fondo, imagen)))
		self.image = random.choice(self.estrellas_imagenes)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(self.game.RESOLUCION[0] - self.rect.width)
		self.rect.y = random.randrange(self.game.RESOLUCION[1] - self.rect.height * 3)
		self.decimales_y = self.rect.y
		self.vel_y = self.rect.width / 10
	
	def update(self):
		self.decimales_y += self.vel_y
		self.rect.y = self.decimales_y
		
		if self.rect.top > self.game.RESOLUCION[1]:
			self.rect.x = random.randrange(self.game.RESOLUCION[0] - self.rect.width)
			self.rect.y = random.randrange(-50, -10)
			self.decimales_y = self.rect.y


class Enemigos(pygame.sprite.Sprite):
	def __init__(self, game, x, y, vel_x, vel_y, recorrido_top, tipo_enemigo):
		super().__init__()
		
		self.game = game
		self.tipo_enemigo = tipo_enemigo  # 3 tipos de enemigos, y dentro de esos, 3 formas para darles movimiento
		
		self.animacion = []  # Lista para añadir las imágenes
		for i in range(3):  # Rango de 3 porque hay 3 modalidades de enemigos
			file = "enemigo{}{}.png".format(self.tipo_enemigo, i + 1)
			imagen = pygame.image.load(os.path.join(carpeta_enemigos, file)).convert()
			imagen.set_colorkey((255, 255, 255))
			self.animacion.append(imagen)
		
		self.image = self.animacion[0]  # Para iniciar por la primera imagen
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.ir_bajando = 0
		self.recorrido = 0
		self.recorrido_top = recorrido_top  # Ésto se sumará al anterior
		# Para la velocidad de las imágenes
		self.fotograma = 0
		self.ultimo_update = pygame.time.get_ticks()
		self.velocidad_fotograma = 50
	
	def update(self):
		# Al igual que en el update de la clase nave del ra_2, hago el cálculo para que los
		# fotogramas se vayan actualizando
		calculo = pygame.time.get_ticks()  # Atrapa el momento de la última actualización del juego
		if calculo - self.ultimo_update > self.velocidad_fotograma:
			self.ultimo_update = calculo
			self.fotograma += 1  # Cálculo para saber cuándo pasar al siguiente fotograma
			if self.fotograma == len(self.animacion):
				self.fotograma = 0  # Cuando llegue al último fotograma, vuelve a empezar
			centro = self.rect.center  # Atrapo coordenadas del centro del rectángulo en eje x en el momento de pasar el fotograma
			# A continuación hago que el siguiente fotograma aparezca donde estaba el anterior
			self.image = self.animacion[self.fotograma]
			self.rect = self.image.get_rect()
			self.rect.center = centro
		
		# Recorrido de los enemgos de izquierda a derecha con su tope
		self.rect.y += self.vel_y
		self.rect.x += self.vel_x
		self.recorrido += 1
		if self.recorrido >= self.recorrido_top:  # Si el recorrido supera el tope, irá al lado contrario
			self.vel_x = -self.vel_x
			self.recorrido = 0
			self.ir_bajando += 1
			if self.ir_bajando > 15 - self.game.nivel:
				self.rect.y += self.game.RESOLUCION[1] // 20
				self.ir_bajando = 0


class Explosiones(pygame.sprite.Sprite):
	def __init__(self, game, centerx, y):
		super().__init__()
		self.game = game
		
		# Animación de explosiones
		self.animacion = []
		for i in range(6):
			file = "explosion_{}.png".format(i + 1)
			imagen = pygame.image.load(os.path.join(carpeta_explosiones, file))
			imagen.set_colorkey((0, 0, 0))
			self.animacion.append(imagen)
		
		self.image = self.animacion[0]  # Empieza por el fotograma 0
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.y = y
		# Fotogramas
		self.fotograma = 0
		self.ultimo_update = pygame.time.get_ticks()
		self.velocidad_fotograma = 120  # Velocidad de la animación
	
	def update(self):
		calculo = pygame.time.get_ticks()
		if calculo - self.ultimo_update > self.velocidad_fotograma:
			self.ultimo_update = calculo
			self.fotograma += 1
			if self.fotograma == len(self.animacion):
				self.kill()
				self.fotograma = 0
			
			centro = self.rect.centerx
			y = self.rect.y
			self.image = self.animacion[self.fotograma]
			self.rect = self.image.get_rect()
			self.rect.centerx = centro
			self.rect.y = y


class Ovnis(pygame.sprite.Sprite):
	def __init__(self, game, centerx, y, vel_x):
		super().__init__()
		self.game = game
		self.animacion = []
		for x in range(4):
			file = "ovni1{}.png".format(x + 1)
			imagen = pygame.image.load(os.path.join(carpeta_enemigos, file)).convert()
			imagen.set_colorkey((255, 255, 255))
			self.animacion.append(imagen)
		
		self.image = self.animacion[0]
		self.rect = self.image.get_rect()
		self.rect.x = centerx
		self.rect.y = y
		self.vel_x = vel_x
		self.fotograma = 0
		self.ultimo_update = pygame.time.get_ticks()
		self.velocidad_fotograma = 50
	
	def update(self):
		calculo = pygame.time.get_ticks()
		if calculo - self.ultimo_update > self.velocidad_fotograma:
			self.ultimo_update = calculo
			self.fotograma += 1
			if self.fotograma == len(self.animacion):
				self.fotograma = 0
			
			centro = self.rect.center
			self.image = self.animacion[self.fotograma]
			self.rect = self.image.get_rect()
			self.rect.center = centro
		# Creo límites para que el ovni, aunque desaparece de la pantalla, vuelva a aparecer
		if self.rect.x >= self.game.RESOLUCION[0] * 3 or self.rect.x <= -self.game.RESOLUCION[0]:
			self.vel_x = -self.vel_x
		self.rect.x += self.vel_x


class DisparoEnemigos(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		super().__init__()
		self.game = game
		self.image = pygame.image.load(os.path.join(carpeta_enemigos, "disparo_enemigo.png"))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.y = y
		self.vel_y = 10
	
	def update(self):
		self.rect.y += self.vel_y
		if self.rect.top > self.game.RESOLUCION[1]:
			self.kill()



