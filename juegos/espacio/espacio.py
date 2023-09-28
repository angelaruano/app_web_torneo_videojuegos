# Los sprites son rectángulos (todas las imágenes en pygame lo son, solo que con transparencias)
import pygame, sys
from pygame.locals import *
import random  # Para enemigos aleatorios
import os  # Para que los directorios sean multiplataforma

import main
from juegos.espacio.clases import *

# Ruta dinámica de la carpeta de juego. Ésto permite obtener la ruta, esté donde esté la carpeta
carpeta_juego = os.path.dirname ( __file__ )
# Ruta de la carpeta de imágenes. Join permite enlazar ésta carpeta con la principal
carpeta_imagenes = os.path.join ( carpeta_juego, "imagenes" )
carpeta_imagenes_enemigos = os.path.join ( carpeta_imagenes, "enemigos" )
carpeta_imagenes_jugador = os.path.join ( carpeta_imagenes, "jugador" )
carpeta_imagenes_explosiones = os.path.join ( carpeta_imagenes, "explosiones" )

# Ruta de carpeta de sonidos
pygame.mixer.init()
carpeta_sonidos = os.path.join ( carpeta_juego, "sonidos" )
carpeta_sonidos_ambiente = os.path.join ( carpeta_sonidos, "ambiente" )
carpeta_sonidos_armas = os.path.join ( carpeta_sonidos, "armas" )
carpeta_sonidos_explosiones = os.path.join ( carpeta_sonidos, "explosiones" )

# Cargo los sonidos del juego

explosion1 = pygame.mixer.Sound ( os.path.join ( carpeta_sonidos_explosiones, "explosion1.wav" ) )
explosion2 = pygame.mixer.Sound ( os.path.join ( carpeta_sonidos_explosiones, "explosion2.wav" ) )
explosion3 = pygame.mixer.Sound ( os.path.join ( carpeta_sonidos_explosiones, "explosion3.wav" ) )
explosion4 = pygame.mixer.Sound ( os.path.join ( carpeta_sonidos_explosiones, "explosion4.wav" ) )
ambiente = pygame.mixer.Sound ( os.path.join ( carpeta_sonidos_ambiente, "intergalactic_odyssey.ogg" ) )
laser = pygame.mixer.Sound (os.path.join(carpeta_sonidos_armas, "disparo.wav"))

# Creo un pequeño catálogo de fuentes:
consolas = pygame.font.match_font ( 'consolas' )
times = pygame.font.match_font ( 'times' )
arial = pygame.font.match_font ( 'arial' )
courier = pygame.font.match_font ( 'courier' )


class GameEspacio :
	def __init__(self) :
		# Paleta de colores
		self.BLANCO = (255, 255, 255)
		self.NEGRO = (0, 0, 0)
		self.ROJO = (255, 0, 0)
		self.AZUL = (0, 0, 255)
		self.VERDE = (0, 255, 0)
		self.BURDEOS = (199, 66, 37)
		self.VERDE_CLARO = (97, 205, 53)
		
		# Estados iniciales del juego
		self.rejugar = False
		self.gameOver = True  # De inicio es True, hasta que empiece a jugar
		self.puntuacion = 0
		self.puntuacion_definitiva = 0
		
		
		
		# Ancho y alto de la ventana
		self.ANCHO = 800
		self.ALTO = 600
		
		# FPS: Frames por segundo (Velocidad del juego)
		self.FPS = 30
		
		# Inicialización del juego, creación de la ventana, título y reloj que controla el FPS
		pygame.init ()
		self.pantalla = pygame.display.set_mode ( (self.ANCHO, self.ALTO) )
		pygame.display.set_caption ( "SPACE" )  # Título de la ventana
		self.reloj = pygame.time.Clock ()  # Velocidad del juego conjugado con FPS y reloj.tick
		self.crear_listas_imagenes ()  # Invoco a la función para las imágenes
	
	# La siguiente función es para las listas de sprites
	# Los sprites son rectángulos (todas las imágenes en pygame lo son, solo que con transparencias)
	# Sirven para luego poder crear colisiones
	def crear_listas_imagenes(self) :
		self.lista_sprites_dibujar = pygame.sprite.Group ()  # Clase Group() de sprite que sirve para agrupar los sprites que quiera para que trabajen en conjunto
		self.lista_jugador = pygame.sprite.Group ()
		self.lista_enemigos_amarillos = pygame.sprite.Group ()
		self.lista_enemigos_verdes = pygame.sprite.Group ()
		self.lista_enemigos_azules = pygame.sprite.Group ()
		self.lista_enemigos_rojos = pygame.sprite.Group ()
		self.lista_balas = pygame.sprite.Group ()
		self.lista_meteoritos = pygame.sprite.Group ()
		self.lista_explosiones = pygame.sprite.Group ()
	
	# La siguiente función es para vaciar la pantalla de imágenes con el método empty en caso de Game Over
	def vaciar_listas(self) :
		self.lista_jugador.empty ()
		self.lista_sprites_dibujar.empty ()
		self.lista_enemigos_amarillos.empty ()
		self.lista_enemigos_verdes.empty ()
		self.lista_enemigos_azules.empty ()
		self.lista_enemigos_rojos.empty ()
		self.lista_balas.empty ()
		self.lista_meteoritos.empty ()
		self.lista_explosiones.empty ()
	
	def nuevo_juego(self) :
		self.puntuacion = 0
		self.vidas = 3
		
		# Istancio a jugador
		self.jugador = Jugador(self)
		self.lista_sprites_dibujar.add ( self.jugador )
		self.lista_jugador.add ( self.jugador )
		
		# Instancio enemigos
		self.enemigos_amarillos = EnemigosAmarillos ( self )
		self.lista_enemigos_amarillos.add ( self.enemigos_amarillos )
		
		self.enemigos_verdes = EnemigosVerdes ( self )
		self.lista_enemigos_verdes.add ( self.enemigos_verdes )
		
		self.enemigos_azules = EnemigosAzules ( self )
		self.lista_enemigos_azules.add ( self.enemigos_azules )
		
		self.enemigos_rojos = EnemigosRojos ( self )
		self.lista_enemigos_rojos.add ( self.enemigos_rojos )
		
		# Instanciación de meteoritos con bucle for, para añadir un rango de 3 meteoritos
		for met in range ( 3 ) :
			self.meteorito = Meteorito ( self )
			self.lista_meteoritos.add ( self.meteorito )
	
	# Instancio puntos
	# self.texto_puntos = Texto ( self )
	# Instancio vidas
	# self.texto_vidas = Texto ( self )
	
	def update(self) :
		if not self.gameOver :
			self.lista_sprites_dibujar.update ()
			self.lista_enemigos_amarillos.update ()
			self.lista_enemigos_verdes.update ()
			self.lista_enemigos_azules.update ()
			self.lista_enemigos_rojos.update ()
			self.lista_balas.update ()
			self.lista_meteoritos.update ()
			self.lista_explosiones.update ()
			self.comprobar_colisiones()
		if self.gameOver:
			self.muestra_texto ( self.pantalla, consolas, str ( self.puntuacion_definitiva ), self.ROJO, 40, 680, 60 )
			self.muestra_texto ( self.pantalla, consolas, str ( "PULSA CUALQUIER TECLA PARA EMPEZAR" ), self.ROJO, 40, 400, 200 )
		
		self.reloj.tick ( self.FPS )
		pygame.display.update ()
	
	
	def draw(self) :
		self.pantalla.fill ( self.NEGRO )
		#Dibujos
		if not self.gameOver:
			# Fondo de pantalla, dibujo de sprites y formas geométricas
			self.lista_sprites_dibujar.draw( self.pantalla )
			self.lista_enemigos_amarillos.draw ( self.pantalla )
			self.lista_enemigos_verdes.draw ( self.pantalla )
			self.lista_enemigos_azules.draw ( self.pantalla )
			self.lista_enemigos_rojos.draw ( self.pantalla )
			self.lista_balas.draw ( self.pantalla )
			self.lista_meteoritos.draw ( self.pantalla )
			self.lista_explosiones.draw ( self.pantalla )
			pygame.draw.line ( self.pantalla, self.VERDE, (400, 0), (400, 800), 1 )
			pygame.draw.line ( self.pantalla, self.AZUL, (0, 300), (800, 300), 1 )
			
			# Llamada al texto de la puntuación
			self.muestra_texto ( self.pantalla, consolas, str ( self.puntuacion ), self.ROJO, 40, 680, 60 )
			# Llamada a la barra de vida
			self.jugador.barra_hp ( self.pantalla, 580, 15, self.jugador.hp )
			
			# Cargo un aspa que va a ir tachando los iconos de vida conforme se gasten
			muerte = pygame.image.load ( os.path.join ( carpeta_imagenes_jugador, "aspa.png" ) )
			
			# Hago condicionales para hacer funcionar el sistema de vidas
			if self.jugador.hp <= 0 and self.jugador.vidas == 3 :  # Si los puntos de vida llegan a 0 y hay 3 vidas
				self.jugador.kill ()  # Hacer que desaparezca el jugador
				self.jugador = Jugador (self)  # Vuelvo a instanciarlo para que reaparezca en su posición inicial
				self.lista_sprites_dibujar.add ( self.jugador )  # Lo vuelvo a añadir a los sprites
				self.jugador.vidas = 2  # Las vidas se quedan a 2
			if self.jugador.vidas == 2 :
				if self.jugador.hp <= 0 :
					self.jugador.kill ()  # Hacer que desaparezca el jugador
					self.jugador = Jugador (self)  # Vuelvo a instanciarlo para que reaparezca en su posición inicial
					self.lista_sprites_dibujar.add( self.jugador )  # Lo vuelvo a añadir a los sprites
					self.jugador.vidas = 1  # Las vidas se quedan a 1
				muerte_1 = self.pantalla.blit ( muerte, (510, 15) )
			if self.jugador.vidas == 1 :
				if self.jugador.hp <= 0 :
					self.jugador.kill ()  # Hacer que desaparezca el jugador
					self.jugador = Jugador (self)  # Vuelvo a instanciarlo para que reaparezca en su posición inicial
					self.lista_sprites_dibujar.add( self.jugador )  # Lo vuelvo a añadir a los sprites
					self.jugador.vidas = 0  # Las vidas se quedan a 0
				muerte_1 = self.pantalla.blit ( muerte, (510, 15) )
				muerte_2 = self.pantalla.blit ( muerte, (475, 15) )
			if self.jugador.vidas == 0 :
				self.vaciar_listas()
	
				self.funcion_game_over(True, self.puntuacion)
				
	# Creo un sistema para que se me muestre el texto con la puntuación
	def muestra_texto(self,pantalla, fuente, texto, color, dimensiones, x, y) :
		tipo_letra = pygame.font.Font ( fuente, dimensiones )
		superficie = tipo_letra.render ( texto, True, color )
		rectangulo = superficie.get_rect ()
		rectangulo.center = (x, y)
		pantalla.blit ( superficie, rectangulo )
		
	def comprobar_colisiones(self):
		colision_disparos_meteoritos = pygame.sprite.groupcollide ( self.lista_meteoritos, self.lista_balas, True, True )
		if colision_disparos_meteoritos :
			self.puntuacion += 25
		if not self.lista_meteoritos :
			for met in range ( 3 ) :
				self.meteorito = Meteorito (self)
				self.lista_meteoritos.add ( self.meteorito )
		
		# Voy a hacer que cuando la nave colisione con los enemigos, se cree la explosión
		colision_nave1 = pygame.sprite.spritecollide ( self.jugador, self.lista_enemigos_amarillos, True,
		                                               pygame.sprite.collide_circle )
		if colision_nave1 :
			explosion1.play ()
			explosion = Explosiones (self, self.enemigos_amarillos.rect.center, "t3" )
			self.lista_explosiones.add ( explosion )
			# Resto vida al jugador
			self.jugador.hp -= 20
			# Hago que, cuando mi nave choque con el enemigo, se resten puntos
			self.puntuacion -= 100
		
		colision_nave2 = pygame.sprite.spritecollide ( self.jugador, self.lista_enemigos_verdes, True,
		                                               pygame.sprite.collide_circle )
		if colision_nave2 :
			explosion2.play ()
			explosion = Explosiones ( self,self.enemigos_verdes.rect.center, "t1" )
			self.lista_explosiones.add ( explosion )
			# Resto vida al jugador
			self.jugador.hp -= 15
			# Resto puntos
			self.puntuacion -= 50
		
		colision_nave3 = pygame.sprite.spritecollide ( self.jugador, self.lista_enemigos_azules, True,
		                                               pygame.sprite.collide_circle )
		if colision_nave3 :
			explosion3.play ()
			explosion = Explosiones ( self, self.enemigos_azules.rect.center, "t2" )
			self.lista_explosiones.add(explosion)
			self.jugador.hp -= 10
			# Resto puntos
			self.puntuacion -= 25
		
		colision_nave4 = pygame.sprite.spritecollide ( self.jugador, self.lista_enemigos_rojos, True,
		                                               pygame.sprite.collide_circle )
		if colision_nave4 :
			explosion4.play ()
			explosion = Explosiones (self, self.enemigos_rojos.rect.center, "t4" )
			self.lista_explosiones.add ( explosion )
			# Resto vida al jugador
			self.jugador.hp -= 5
			# Resto puntos
			self.puntuacion -= 10
		
		colision_jugador_meteoritos = pygame.sprite.spritecollide ( self.jugador, self.lista_meteoritos, True,
		                                                            pygame.sprite.collide_circle )
		if colision_jugador_meteoritos :
			explosion4.play ()
			explosion = Explosiones ( self,self.jugador.rect.center, "t3" )
			self.lista_explosiones.add ( explosion )
			self.jugador.hp -= 10
			self.puntuacion -= 15
		# Creo las colisiones con sus respectivas puntuaciones
		colision_disparos_amarillos = pygame.sprite.groupcollide ( self.lista_enemigos_amarillos, self.lista_balas, True,
		                                                           pygame.sprite.collide_circle )
		if colision_disparos_amarillos :
			self.puntuacion += 10
			explosion1.play ()  # Sonido al impactar
			# Hago que cuando el disparo colisione, la imagen del enemigo, se sustituya por una explosión, con el tamaño indicado
			explosion = Explosiones (self, self.enemigos_amarillos.rect.center, "t3" )
			self.lista_explosiones.add(explosion)
			# Cuando le de el disparo, la vida le decrementa
			self.enemigos_amarillos.hp -= 5
		# Hago que cuando la vida llegue a 0, desaparezca
		if self.enemigos_amarillos.hp <= 0 :
			self.enemigos_amarillos.kill ()

		colision_disparos_verdes = pygame.sprite.groupcollide ( self.lista_enemigos_verdes, self.lista_balas, False, True,
		                                                        pygame.sprite.collide_circle )
		if colision_disparos_verdes :
			self.puntuacion += 25
			explosion2.play ()
			explosion = Explosiones ( self,self.enemigos_verdes.rect.center, "t1" )
			self.lista_explosiones.add ( explosion )
			# Cuando le de el disparo, la vida le decrementa
			self.enemigos_verdes.hp -= 5
		# Hago que cuando la vida llegue a 0, desaparezca
		if self.enemigos_verdes.hp <= 0 :
			self.enemigos_verdes.kill ()
			
		
		
		colision_disparos_azules = pygame.sprite.groupcollide ( self.lista_enemigos_azules, self.lista_balas, False, True,
		                                                        pygame.sprite.collide_circle )
		if colision_disparos_azules :
			self.puntuacion += 50
			explosion3.play ()
			explosion = Explosiones (self, self.enemigos_azules.rect.center, "t2" )
			self.lista_explosiones.add ( explosion )
			# Cuando le de el disparo, la vida le decrementa
			self.enemigos_azules.hp -= 5
		# Hago que cuando la vida llegue a 0, desaparezca
		if self.enemigos_azules.hp <= 0 :
			
			self.enemigos_azules.kill ()
			
		colision_disparos_rojos = pygame.sprite.groupcollide ( self.lista_enemigos_rojos, self.lista_balas, False, True,
		                                                       pygame.sprite.collide_circle )
		if colision_disparos_rojos :
			self.puntuacion += 100
			explosion4.play ()
			explosion = Explosiones (self, self.enemigos_rojos.rect.center, "t4" )
			self.lista_explosiones.add ( explosion )
			# Cuando le de el disparo, la vida le decrementa
			self.enemigos_rojos.hp -= 5
		# Hago que cuando la vida llegue a 0, desaparezca
		if self.enemigos_rojos.hp <= 0 :
			
			self.enemigos_rojos.kill ()
		
		# Cuando no queden enemigos, se reinstancian
		if not self.lista_enemigos_amarillos and not self.lista_enemigos_azules and not self.lista_enemigos_verdes and not self.lista_enemigos_rojos :
			self.enemigos_amarillos = EnemigosAmarillos (self)
			self.lista_enemigos_amarillos.add ( self.enemigos_amarillos )
			
			
			self.enemigos_verdes = EnemigosVerdes (self)
			self.lista_enemigos_verdes.add ( self.enemigos_verdes )
			
			self.enemigos_azules = EnemigosAzules (self)
			self.lista_enemigos_azules.add ( self.enemigos_azules )
			
			self.enemigos_rojos = EnemigosRojos (self)
			self.lista_enemigos_rojos.add ( self.enemigos_rojos )
	
	def disparar(self):
		
		self.balas = Disparos(self, self.jugador.rect.centerx, self.jugador.rect.top )
		self.lista_balas.add(self.balas)
		
		sonido_disparo = pygame.mixer.Sound(os.path.join(carpeta_sonidos_armas, "disparo.wav"))
		sonido_disparo.play()
		
	def funcion_game_over(self, game_over, puntos):
		self.gameOver = game_over
		self.puntuacion_definitiva = puntos
		
	def guarda_puntos(self,puntaje):
		if puntaje >0 or puntaje <0:
			main.puntuacion_space(puntaje)
		
		
	def check_event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.puntuacion_definitiva = self.puntuacion
				self.guarda_puntos(self.puntuacion_definitiva)
				print("salgo, puntos: ", self.puntuacion_definitiva)
				pygame.quit()
				sys.exit()
			
			if event.type == pygame.KEYDOWN and self.gameOver:
				
				self.puntuacion_definitiva = self.puntuacion
				self.guarda_puntos(self.puntuacion_definitiva)
				print(self.puntuacion_definitiva)
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
			
	
if __name__ == "__run__":
	game_naves = GameNaves()
	game_naves.run(debug = True)
	

