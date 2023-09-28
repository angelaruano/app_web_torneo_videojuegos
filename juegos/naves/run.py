# Los sprites son rectángulos (todas las imágenes en pygame lo son, solo que con transparencias)
import pygame, sys
from pygame.locals import *
import random  # Para enemigos aleatorios
import os  # Para que los directorios sean multiplataforma

import main
from juegos.naves.ra_1 import *
from juegos.naves.ra_2 import *


# Ruta dinámica de la carpeta de juego. Ésto permite obtener la ruta, esté donde esté la carpeta
carpeta_juego = os.path.dirname(__file__)

# Directorios de las imágenes
carpeta_imagenes = os.path.join(carpeta_juego, "imagenes")
carpeta_fondo = os.path.join(carpeta_imagenes, "fondo")

# Directorios de sonidos
carpeta_sonidos = os.path.join(carpeta_juego, "sonidos")


class GameNaves:
	def __init__(self):
		pygame.init()
		pygame.mixer.init()
		self.lista_sprites = pygame.sprite.Group()
		self.lista_ataques_dibuja = pygame.sprite.Group()
		self.lista_estrellas = pygame.sprite.Group()
		self.lista_nave = pygame.sprite.Group()
		self.lista_enemigos = pygame.sprite.Group()
		self.lista_disparos = pygame.sprite.Group()
		self.lista_ovnis = pygame.sprite.Group()
		self.lista_potenciadores = pygame.sprite.Group()
		self.lista_ataques = pygame.sprite.Group()
		
		# Colores
		self.AZUL_C = (0, 194, 233)
		
		self.gameOver = True
		self.nivel_superado = True
		self.tomar_tiempo = 0
		self.pausa_nuevo_nivel = pygame.time.get_ticks()
		self.PAUSA_NUEVA_VIDA = 2000  # Milisegundos
		self.RESOLUCION = (1000, 600)
		self.FPS = 60
		self.pantalla = pygame.display.set_mode(self.RESOLUCION)
		pygame.display.set_caption("RETRO ALIENS")
		self.reloj = pygame.time.Clock()
		self.fondo = pygame.transform.scale(
			pygame.image.load(os.path.join(carpeta_fondo, "espacio_negro.jpg")).convert(), (1000, 600))
		self.disparo_extra = 1
		
		self.crear_estrellas()
		self.nuevo_juego()

	def dibuja_texto(self, superficie, texto, talla, x, y):
		fuente = pygame.font.SysFont("serif", talla)
		texto_superficie = fuente.render(texto, True, self.AZUL_C)
		texto_rectangulo = texto_superficie.get_rect()
		texto_rectangulo.midtop = (x, y)
		superficie.blit(texto_superficie, texto_rectangulo)
		
	
	def crear_estrellas(self):
		for i in range(120):
			self.estrella = Estrella(self)
			self.lista_sprites.add(self.estrella)
			self.lista_estrellas.add(self.estrella)
	
	def nuevo_juego(self):
		self.puntos = 0
		self.nivel = 1
		self.vidas = 2
		self.vidas_texto = 3
		self.disparo_lados = [0, 2, -2, 5, -5]
		self.enemigos_abatidos = 0
		
		# Imstancio la nave del jugador
		self.nave_jugador = NaveJugador(self)
		self.lista_sprites.add(self.nave_jugador)
		self.lista_nave.add(self.nave_jugador)
		
		# Instancio ovni:
		self.ovni = Ovnis(self, -self.RESOLUCION[0] // 2, 50, 5)
		self.lista_sprites.add(self.ovni)
		self.lista_ovnis.add(self.ovni)
		
		# Instancio a los enemigos con bucle for. Habrá 10 por cada tipo
		for i in range(10):
			self.enemigo_1 = Enemigos(self, i * 80 + 100, 80, 1, 0, 50, 1)
			self.lista_sprites.add(self.enemigo_1)
			self.lista_enemigos.add(self.enemigo_1)
			
			self.enemigo_2 = Enemigos(self, i * 80 + 50, 150, 1, 0, 50, 2)
			self.lista_sprites.add(self.enemigo_2)
			self.lista_enemigos.add(self.enemigo_2)
			
			self.enemigo_3 = Enemigos(self, i * 80, 220, 3, 0, 50, 3)
			self.lista_sprites.add(self.enemigo_3)
			self.lista_enemigos.add(self.enemigo_3)
	
	# En lo parámetros anteriores (pongo como ejemplo los del enemigo_1):
	# x*80+100 en la coordenada x, tiene la función de que salgan en fila
	# Velocidad x=2, para que se mueva 2 pix a la derecha o a la izquierda, "y" no tiene velocidad
	# #El tope de recorrido será 50 pix a la derecha o a la izquierda.
	# Al ser la velocidad x=2, irían de 2 en 2 pix hasta 50, donde cambiarían al otro lado
	
	def nuevo_nivel(self):
		for i in range(10):
			self.enemigo_1 = Enemigos(self, i * 80 + 100, 80, 1, 0, 50, 1)
			self.lista_sprites.add(self.enemigo_1)
			self.lista_enemigos.add(self.enemigo_1)
			
			self.enemigo_2 = Enemigos(self, i * 80 + 50, 150, 1, 0, 50, 2)
			self.lista_sprites.add(self.enemigo_2)
			self.lista_enemigos.add(self.enemigo_2)
			
			self.enemigo_3 = Enemigos(self, i * 80, 220, 3, 0, 50, 3)
			self.lista_sprites.add(self.enemigo_3)
			self.lista_enemigos.add(self.enemigo_3)
	
	def update(self):
		self.lista_sprites.update()
		self.disparo_enemigo()
		self.lista_ataques_dibuja.update()
		self.lista_enemigos.update()
		self.lista_disparos.update()
		self.comprobar_colisiones()

		pygame.display.flip()
		self.reloj.tick(self.FPS)
	
	def draw(self):
		self.pantalla.blit(self.fondo, (0, 0))
		self.lista_sprites.draw(self.pantalla)
		self.lista_ataques_dibuja.draw(self.pantalla)
		
		if not self.gameOver:
			self.dibuja_texto(self.pantalla, "Puntos: {}".format(str(self.puntos)), 25, self.RESOLUCION[0] // 2, 10)
			self.dibuja_texto(self.pantalla, "Nivel: {}".format(str(self.nivel)), 25, 100, 10)
			self.dibuja_texto(self.pantalla, "Vidas: {}".format(str(self.vidas_texto)), 25, 900, 10)
		else:
			self.lista_enemigos.empty()
			self.lista_sprites.empty()
			self.dibuja_texto(self.pantalla, 'R E T R O   A L I E N S', 70, self.RESOLUCION[0] // 2,self.RESOLUCION[1] // 2 - 100 )
			self.dibuja_texto(self.pantalla, "Pulse INTRO para comenzar...", 30, self.RESOLUCION[0]//2, self.RESOLUCION[1] -80)
			
	def nuevo_ovni(self):
		self.ovni = Ovnis(self, -self.RESOLUCION[0] // 2, 50, 5)
		self.lista_sprites.add(self.ovni)
		self.lista_ovnis.add(self.ovni)
	
	def comprobar_colisiones(self):
		impactos = pygame.sprite.groupcollide(self.lista_disparos, self.lista_enemigos, True, True)
		
		for impacto in impactos:
			self.puntos += 10
			self.enemigos_abatidos += 1
			self.explosion = Explosiones(self, impacto.rect.centerx, impacto.rect.y - 30)
			self.lista_sprites.add(self.explosion)
			sonido_explosion = pygame.mixer.Sound(os.path.join(carpeta_sonidos, "explosion.wav"))
			sonido_explosion.play()
			for i in range(100):
				if self.enemigos_abatidos == 30 * (i + 1):
					self.nivel += 1
					self.nuevo_nivel()
				
		
		impactos = pygame.sprite.groupcollide(self.lista_disparos, self.lista_ovnis, True, True)
		for impacto in impactos:
			self.puntos += 50
			self.explosion = Explosiones(self, impacto.rect.centerx, impacto.rect.y - 30)
			self.lista_sprites.add(self.explosion)
			aleatorio = random.randrange(3)
			self.potenciador = Potenciadores(self, impacto.rect.x, impacto.rect.y - 30, aleatorio)
			self.lista_sprites.add(self.potenciador)
			self.lista_potenciadores.add(self.potenciador)
			self.nuevo_ovni()
			sonido_explosion = pygame.mixer.Sound(os.path.join(carpeta_sonidos, "explosion.wav"))
			sonido_explosion.play()
		
		impactos = pygame.sprite.groupcollide(self.lista_potenciadores, self.lista_nave, True, False)
		for impacto in impactos:
			self.premio()
		
		if self.invisible == 0:
			impactos = pygame.sprite.groupcollide(self.lista_ataques, self.lista_nave, True, True)
			for impacto in impactos:
				
				if self.vidas >= 0:
					self.puntos -= 100
					self.explosion = Explosiones(self, self.nave_jugador.rect.centerx, self.nave_jugador.rect.y - 30)
					self.lista_sprites.add(self.explosion)
					self.tomar_tiempo = pygame.time.get_ticks()
					sonido_explosion = pygame.mixer.Sound(os.path.join(carpeta_sonidos, "explosion.wav"))
					sonido_explosion.play()
					self.disparo_extra = 1
					self.vidas -= 1
					self.vidas_texto -= 1
					self.nave_jugador = NaveJugador(self)
					self.lista_sprites.add(self.nave_jugador)
					self.lista_nave.add(self.nave_jugador)
	
				elif self.vidas < 0:
					print("Muere")
					self.gameOver = True
	
		else:
			impactos = pygame.sprite.groupcollide(self.lista_ataques, self.lista_nave, False, False)
	def premio(self):
		if self.potenciador.aleatorio == 0:
			self.puntos += 100
		if self.potenciador.aleatorio == 1:
			if self.disparo_extra < 5:
				self.disparo_extra += 2
		if self.potenciador.aleatorio == 2 and self.vidas < 3:
			self.vidas += 1
			self.vidas_texto += 1
	
	def disparar(self):
		for i in range(self.disparo_extra):
			disparo_lados = self.disparo_lados[i]
			self.disparo = Disparo(self, self.nave_jugador.rect.centerx, self.nave_jugador.rect.top, disparo_lados)
			self.lista_sprites.add(self.disparo)
			self.lista_disparos.add(self.disparo)
			
			sonido_disparo = pygame.mixer.Sound(os.path.join(carpeta_sonidos, "disparo.wav"))
			sonido_disparo.play()
			
	
	
	# La función siguiente va a encargarse de provocar un disparo enemigo cada vez que éste choque con una de
	# las estrellas que van pasando por el fondo. No afectará al juego, ni se verá la colisión,
	# solo afecta, sin que quien juega se de cuenta, en que se crea un disparo.
	def disparo_enemigo(self):
		disparos = pygame.sprite.groupcollide(self.lista_enemigos, self.lista_estrellas, False, False)
		for disparo in disparos:
			# Necesito crear una cadencia de disparo porque si no, es excesivo. Ésta se hará más veloz según suba el nivel
			cadencia = random.randrange(1, 800)
			if cadencia < self.nivel * 11:
				self.disparo_del_enemigo = DisparoEnemigos(self, disparo.rect.centerx, disparo.rect.centery)
				self.lista_ataques_dibuja.add(self.disparo_del_enemigo)
				self.lista_ataques.add(self.disparo_del_enemigo)

	def guarda_puntos(self,puntaje):
		if puntaje >0 or puntaje <0:
			print("mando",puntaje)
			main.puntuacion_naves(puntaje)
	def check_event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.puntuacion_definitiva = self.puntos
				self.guarda_puntos(self.puntuacion_definitiva)
				print("salgo",self.puntuacion_definitiva)
				pygame.quit()
				sys.exit()
			
			if event.type == pygame.KEYDOWN and self.gameOver:
				self.puntuacion_definitiva = self.puntos
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
	
#NOTA: Falta hacer
#Hacer que la nave sea invulnerable al empezar el nivel
#Ver motivo de que a veces no se instancien los enemigos al pasar nivel (puede que se haya solucionado...comprobar jugando)
#Que en el game over, me pase los puntos logrados
#Que para reiniciar, no valga calquier tecla, sino enter
#Que no inicie directamente, sino que salga el letrero