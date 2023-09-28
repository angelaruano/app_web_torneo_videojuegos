# Los sprites son rectángulos (todas las imágenes en pygame lo son, solo que con transparencias)
import pygame, sys
from pygame.locals import *
import random  # Para enemigos aleatorios
import os  # Para que los directorios sean multiplataforma
from juegos.espacio.espacio import *




# Ruta dinámica de la carpeta de juego. Ésto permite obtener la ruta, esté donde esté la carpeta
carpeta_juego = os.path.dirname ( __file__ )
# Ruta de la carpeta de imágenes. Join permite enlazar ésta carpeta con la principal
carpeta_imagenes = os.path.join ( carpeta_juego, "imagenes" )
carpeta_imagenes_enemigos = os.path.join ( carpeta_imagenes, "enemigos" )
carpeta_imagenes_jugador = os.path.join ( carpeta_imagenes, "jugador" )
carpeta_imagenes_explosiones = os.path.join ( carpeta_imagenes, "explosiones" )

# Ruta de carpeta de sonidos
carpeta_sonidos = os.path.join ( carpeta_juego, "sonidos" )
carpeta_sonidos_ambiente = os.path.join ( carpeta_sonidos, "ambiente" )
carpeta_sonidos_armas = os.path.join ( carpeta_sonidos, "armas" )
carpeta_sonidos_explosiones = os.path.join ( carpeta_sonidos, "explosiones" )

# Cargo los sonidos del juego

pygame.mixer.init ()  # Función de sonidos
laser = pygame.mixer.Sound ( os.path.join ( carpeta_sonidos_armas, "disparo.wav" ) )
explosion1 = pygame.mixer.Sound ( os.path.join ( carpeta_sonidos_explosiones, "explosion1.wav" ) )
explosion2 = pygame.mixer.Sound ( os.path.join ( carpeta_sonidos_explosiones, "explosion2.wav" ) )
explosion3 = pygame.mixer.Sound ( os.path.join ( carpeta_sonidos_explosiones, "explosion3.wav" ) )
explosion4 = pygame.mixer.Sound ( os.path.join ( carpeta_sonidos_explosiones, "explosion4.wav" ) )
ambiente = pygame.mixer.Sound ( os.path.join ( carpeta_sonidos_ambiente, "intergalactic_odyssey.ogg" ) )

# Creo un pequeño catálogo de fuentes:
consolas = pygame.font.match_font ( 'consolas' )
times = pygame.font.match_font ( 'times' )
arial = pygame.font.match_font ( 'arial' )
courier = pygame.font.match_font ( 'courier' )




# Creamos la clase "jugador" donde se le añadirán todas sus características.
# Ésta clase hereda de la clase Sprite del módulo sprite de pygame, con todos sus métodos y atributos y de GameEspacio
class Jugador ( pygame.sprite.Sprite) :
	# Sprite del jugador (constructor)
	def __init__(self,game) :
		super ().__init__ ()  # Heredo el constructor de la clase Sprite
		self.game = game
		# Rectángulo (jugador)
		self.image = pygame.image.load ( os.path.join ( carpeta_imagenes_jugador, "nave.png" ) )  # Cargo imagen
		
		# Las siguientes dos funciones son para obtener el cuadrado y para ponerlo en el centro
		self.rect = self.image.get_rect ()
		self.rect.center = (self.game.ANCHO // 2, self.game.ALTO // 2)  # Divido entre dos para que se ponga en el centro
		
		# Velocidad del personaje (inicial)
		self.velocidad_x = 0
		self.velocidad_y = 0
		
		# Voy a crear una cadencia entre disparo y disparo del jugador
		self.cadencia = 500  # Milisegundos
		self.ultimo_disparo = pygame.time.get_ticks ()  # se va a encargar de contar los milisegundos desde el último disparo
		
		# Puntos de vida (hp = healt points) del jugador
		self.hp = 100
		
		# Le voy a añadir vidas al jugador
		self.vidas = 3
	
	# Creo una función para que en pantalla aparezca mi barra de vida
	def barra_hp(self, pantalla, x, y, hp) :
		# Tamaño de la barra
		largo = 200
		ancho = 25
		# Hago el porcentaje de vida en la barra. Esto hará que la barra se adapte a los puntos de vida.
		calculo_barra = int ( (hp / 100) * largo )
		# Creo los rectángulos tanto de la barra, como del borde
		borde = pygame.Rect ( x, y, largo, ancho )
		rectangulo = pygame.Rect ( x, y, calculo_barra, ancho )
		pygame.draw.rect ( pantalla, self.game.ROJO, borde, 3 )
		pygame.draw.rect ( pantalla, self.game.VERDE, rectangulo )
		muerte_2 = pantalla.blit ( pygame.transform.scale ( self.image, (25, 25) ), (510, 15) )
		muerte_1 = pantalla.blit ( pygame.transform.scale ( self.image, (25, 25) ), (475, 15) )
	
	# Ahora voy a usar otro método heredado de la clase sprite que va a servir para
	# actualizar lo que voy a poner a continuación en cada vuelta del bucle
	def update(self) :
		
		# Velocidad predeterminada para cada vuelta del bucle si no pulso nada
		self.velocidad_x = 0
		self.velocidad_y = 0
		
		# Para poder mantener las teclas pulsadas para el movimiento sin tener que pulsar una y otra vez
		teclas = pygame.key.get_pressed ()
		
		# Teclas para el movimiento
		# Movimiento a la izquierda:
		if teclas[pygame.K_LEFT] :  # Si presiono tecla izquierda
			self.velocidad_x = -10  # Mi personaje se irá moviendo de 10 en 10 pix. Como estamos hacia la izq, ponemos -10
		# Movimiento a la derecha:
		if teclas[pygame.K_RIGHT] :
			self.velocidad_x = 10  # En éste caso ponemos número positivo
		# Movimiento hacia arriba:
		if teclas[pygame.K_UP] :
			self.velocidad_y = -10
		# Movimiento abajo:
		if teclas[pygame.K_DOWN] :
			self.velocidad_y = 10
		# Disparo
		if teclas[pygame.K_SPACE] :
			ahora = pygame.time.get_ticks ()  # Recoge el momento exacto en el que se ha disparado
			if ahora - self.ultimo_disparo > self.cadencia :  # Si pasa más del tiempo expresado en cadencia
				self.game.disparar ()  # Llamo al método disparo
				self.ultimo_disparo = ahora  # Para volver a recoger el tiempo y que se vuelva a contabilizar
		
		# Para actualizar la velocidad del personaje al moverlo:
		self.rect.x += self.velocidad_x
		self.rect.y += self.velocidad_y
		
		# Voy a poner los límites para que el personaje no se salga de la pantalla:
		# Límite izquierdo (eje X)
		if self.rect.left < 0 :  # Si el límite del personaje toca coordenada X menos a 0
			self.rect.left = 0  # Que el límite se ponga en coordenada X 0
		# Límite derecho (eje X)
		if self.rect.right > self.game.ANCHO :  # Si el límite derecho del personaje llega a una coordenada X mayor de 800(ancho)
			self.rect.right = self.game.ANCHO  # Que el límite se coloque en 800 (ancho)
		# Límite arriba (eje Y)
		if self.rect.top < 0 :  # Si el límite del personaje toca coordenada Y menos a 0
			self.rect.top = 0  # Que el límite se ponga en coordenada Y 0
		# Límite abajo (eje Y)
		if self.rect.bottom > self.game.ALTO :  # Si el límite inferior del personaje llega a una coordenada Y mayor de &00(alto)
			self.rect.bottom = self.game.ALTO  # Que el límite se coloque en 600 (alto)
	
	# Creo un método en el jugador para disparar. Éste mismo método va a instanciar a la clase Disparo:
	def disparo(self) :
		bala = Disparos ( self, self.rect.centerx,self.rect.top)  # Ordeno que el disparo salga desde el centro-superior de la imagen de mi jugador
		balas.add ( bala )  # Añado la imagen de bala a los sprites de los disparos
		laser.play ()  # Sonido de disparo


# Creo varias clases de enemigos donde se le añadirán todas su características
# Cada uno tendrá un color, velocidad y puntuaciones diferentes.
# Ésta clase hereda de la clase Sprite del módulo sprite de pygame, con todos sus métodos y atributos y de GameEspacio
class EnemigosAmarillos ( pygame.sprite.Sprite) :
	def __init__(self,game) :
		super ().__init__ ()
		self.game = game
		self.image = pygame.image.load ( os.path.join ( carpeta_imagenes_enemigos, "enemigo1.png" ) ).convert ()
		self.rect = self.image.get_rect ()
		self.image.set_colorkey ( self.game.NEGRO )
		self.radius = 48
		self.rect.x = random.randrange ( self.game.ANCHO - self.rect.width )
		self.rect.y = random.randrange ( self.game.ALTO - self.rect.height )
		self.velocidad_x = random.randrange ( 1, 3 )
		self.velocidad_y = random.randrange ( 1, 3 )
		# Puntos de vida
		self.hp = 15
	
	def update(self) :
		# Actualiza la velocidad del enemigo
		self.rect.x += self.velocidad_x
		self.rect.y += self.velocidad_y
		
		# Limita el margen izquierdo
		if self.rect.left < 0 :
			self.velocidad_x += 1
		
		# Limita el margen derecho
		if self.rect.right > self.game.ANCHO :
			self.velocidad_x -= 1
		
		# Limita el margen inferior
		if self.rect.bottom > self.game.ALTO :
			self.velocidad_y -= 1
		
		# Limita el margen superior
		if self.rect.top < 0 :
			self.velocidad_y += 1


class EnemigosVerdes ( pygame.sprite.Sprite) :
	def __init__(self,game) :
		super ().__init__ ()
		self.game = game
		self.image = pygame.image.load ( os.path.join ( carpeta_imagenes_enemigos, "enemigo2.png" ) ).convert ()
		self.rect = self.image.get_rect ()
		self.image.set_colorkey ( self.game.NEGRO )
		self.radius = 48
		self.rect.x = random.randrange ( self.game.ANCHO - self.rect.width )
		self.rect.y = random.randrange ( self.game.ALTO - self.rect.height )
		self.velocidad_x = random.randrange ( 3, 5 )
		self.velocidad_y = random.randrange ( 3, 5 )
		# Puntos de vida
		self.hp = 30
	
	def update(self) :
		# Actualiza la velocidad del enemigo
		self.rect.x += self.velocidad_x
		self.rect.y += self.velocidad_y
		
		# Limita el margen izquierdo
		if self.rect.left < 0 :
			self.velocidad_x += 1
		
		# Limita el margen derecho
		if self.rect.right > self.game.ANCHO :
			self.velocidad_x -= 1
		
		# Limita el margen inferior
		if self.rect.bottom > self.game.ALTO :
			self.velocidad_y -= 1
		
		# Limita el margen superior
		if self.rect.top < 0 :
			self.velocidad_y += 1


class EnemigosAzules ( pygame.sprite.Sprite) :
	def __init__(self, game) :
		super ().__init__ ()
		self.game = game
		self.image = pygame.image.load ( os.path.join ( carpeta_imagenes_enemigos, "enemigo3.png" ) ).convert ()
		self.rect = self.image.get_rect ()
		self.image.set_colorkey ( self.game.NEGRO )
		self.radius = 48
		self.rect.x = random.randrange ( self.game.ANCHO - self.rect.width )
		self.rect.y = random.randrange ( self.game.ALTO - self.rect.height )
		self.velocidad_x = random.randrange ( 5, 7 )
		self.velocidad_y = random.randrange ( 5, 7  )
		# Puntos de vida
		self.hp = 45
	
	def update(self) :
		# Actualiza la velocidad del enemigo
		self.rect.x += self.velocidad_x
		self.rect.y += self.velocidad_y
		
		# Limita el margen izquierdo
		if self.rect.left < 0 :
			self.velocidad_x += 1
		
		# Limita el margen derecho
		if self.rect.right > self.game.ANCHO :
			self.velocidad_x -= 1
		
		# Limita el margen inferior
		if self.rect.bottom > self.game.ALTO :
			self.velocidad_y -= 1
		
		# Limita el margen superior
		if self.rect.top < 0 :
			self.velocidad_y += 1


class EnemigosRojos ( pygame.sprite.Sprite) :
	def __init__(self, game) :
		super ().__init__ ()
		self.game = game
		self.image = pygame.image.load ( os.path.join ( carpeta_imagenes_enemigos, "enemigo4.png" ) ).convert ()
		self.rect = self.image.get_rect ()
		self.image.set_colorkey ( self.game.NEGRO )
		self.radius = 48
		self.rect.x = random.randrange ( self.game.ANCHO - self.rect.width )
		self.rect.y = random.randrange ( self.game.ALTO - self.rect.height )
		self.velocidad_x = random.randrange ( 7, 10 )
		self.velocidad_y = random.randrange ( 7, 10)
		# Puntos de vida
		self.hp = 60
	
	def update(self) :
		# Actualiza la velocidad del enemigo
		self.rect.x += self.velocidad_x
		self.rect.y += self.velocidad_y
		
		# Limita el margen izquierdo
		if self.rect.left < 0 :
			self.velocidad_x += 1
		
		# Limita el margen derecho
		if self.rect.right > self.game.ANCHO :
			self.velocidad_x -= 1
		
		# Limita el margen inferior
		if self.rect.bottom > self.game.ALTO :
			self.velocidad_y -= 1
		
		# Limita el margen superior
		if self.rect.top < 0 :
			self.velocidad_y += 1


# Creo la clase para los disparos:
class Disparos ( pygame.sprite.Sprite) :
	# En el constructor, le voy a pasar como parámetros X e Y para luego indicar desde donde exactamente se generan los disparos
	def __init__(self,game, x, y) :
		super ().__init__ ()
		self.game = game
		self.image = pygame.image.load ( os.path.join ( carpeta_imagenes_jugador, "disparo.png" ) )
		self.rect = self.image.get_rect ()
		self.rect.bottom = y  # Especifico que la posición Y se va a ubicar en la parte de abajo de la imagen
		self.rect.centerx = x  # Especifico que la posición X, se va a ubicar en el centro de la imagen
	
	# Método para que se actualice la imagen en la pantalla:
	def update(self) :
		self.rect.y -= 25  # Dirección y velocidad de la bala (irá hacia arriba)
		if self.rect.bottom < 0 :
			self.kill ()  # Ést elimina la bala cuando llegue arriba


# A continuación, voy a crear la clase Meteoritos. El objetivo es que
# aparezcan aleatoriamente y con tamaños diferentes.
class Meteorito ( pygame.sprite.Sprite) :
	def __init__(self,game) :
		super().__init__()
		self.game = game
		self.ANCHO = 800
		self.ALTO = 600
		self.NEGRO = (0, 0, 0)
		# Voy a crear tres tamaños aleatorios. Para ello uso módulo random con rango de 3:
		self.imagen_aleatoria = random.randrange ( 3 )
		# Meto en condicionales las 3 posibilidades y con la función
		# transform.scale hago que la misma imagen se redimensione con los píxeles que le indico.
		if self.imagen_aleatoria == 0 :
			self.image = pygame.transform.scale (
				pygame.image.load ( os.path.join ( carpeta_imagenes_enemigos, "meteorito.png" ) ).convert (),
				(100, 100) )
			self.radius = 50  # Para crear colisiones más precisas sin que el meteorito sea en realidad un rectángulo(50 por que es el radio de 100)
		if self.imagen_aleatoria == 1 :
			self.image = pygame.transform.scale (
				pygame.image.load ( os.path.join ( carpeta_imagenes_enemigos, "meteorito.png" ) ).convert (), (50, 50) )
			self.radius = 25
		if self.imagen_aleatoria == 2 :
			self.image = pygame.transform.scale (
				pygame.image.load ( os.path.join ( carpeta_imagenes_enemigos, "meteorito.png" ) ).convert (), (25, 25) )
			self.radius = 13
		self.image.set_colorkey (self.NEGRO)
		self.rect = self.image.get_rect ()
		# Creo las posiciones iniciales de los meteoritos:
		self.rect.x = random.randrange (
			self.ANCHO - self.rect.width )  # Aparición aleatoria en el rango de: ancho de la pantalla - ancho del rectángulo
		self.rect.y = -self.rect.width  # Evita que el meteorito se genere en mitad de la pantalla
		self.velocidad_y = random.randrange ( 1, 10 )  # Velocidad de arriba a abajo, aleatoria( avanza de 1 a 10 pix)
	
	# Función para actualizar la pantalla
	def update(self) :
		self.rect.y += self.velocidad_y  # Para que el movimiento se renueve según la velocidad aleatoria que lleve
		# El siguiente condicional es para que:
		# Si la parte de arriba del meteorito llega abajo (alto)
		# Vuelva a aparecer por arriba con un rango de velocidad y posición distintas.
		if self.rect.top > self.ALTO :
			self.rect.x = random.randrange ( self.ANCHO - self.rect.width )
			self.rect.y = -self.rect.width
			self.velocidad_y = random.randrange ( 1, 10 )


# Creo la clase para las explosiones
class Explosiones ( pygame.sprite.Sprite) :
	def __init__(self, game, centro, dimensiones) :
		super ().__init__ ()
		self.game = game
		self.dimensiones = dimensiones
		# Explosiones de las naves cuando el disparo les da.
		# Voy a crear un diccionario y voy a hacer que las explosiones salgan con un tamaño ("t") aleatorio
		self.animacion_explosion1 = {"t1" : [], "t2" : [], "t3" : [], "t4" : []}
		# A continiación, creo un bucle for que va a recorrer las 24 imágenes de explosión formateando el nombre de los archivos
		for x in range ( 24 ) :
			archivo_explosiones = f"expl_01_{x:04d}.png"  # 04d = 4 dígitos
			imagenes = pygame.image.load (
				os.path.join ( carpeta_imagenes_explosiones, archivo_explosiones ) ).convert ()
			imagenes.set_colorkey ( self.game.NEGRO )
			# Voy a ir incluyendo los diferentes tamaños dentro del diccionario.
			# El tamaño lo cambio con la función "transform.scale".
			imagenes_t1 = pygame.transform.scale ( imagenes, (32, 32) )  # Tamaño en píxeles
			self.animacion_explosion1["t1"].append ( imagenes_t1 )  # Añado el tamaño al diccionario
			imagenes_t2 = pygame.transform.scale ( imagenes, (64, 64) )
			self.animacion_explosion1["t2"].append ( imagenes_t2 )
			imagenes_t3 = pygame.transform.scale ( imagenes, (128, 128) )
			self.animacion_explosion1["t3"].append ( imagenes_t3 )
			imagenes_t4 = pygame.transform.scale ( imagenes, (256, 256) )
			self.animacion_explosion1["t4"].append ( imagenes_t4 )
		
		self.image = self.animacion_explosion1[self.dimensiones][0]  # self.dimensiones = para que obtenga el tamaño t1,t2,t3 o t4 y 0= para que empiece desde la imagen 0
		self.rect = self.image.get_rect ()
		self.rect.center = centro
		self.fotograma = 0  # Empezar desde fotograma 0
		self.frecuencia_fotograma = 100  # Velocidad a la que se cargan las imágenes en milisegundos
		self.actualizacion = pygame.time.get_ticks ()  # Función para que se produzca la velocidad de carga en milisegundos
		
		
	
	def update(self) :
		ahora = pygame.time.get_ticks ()
		if ahora - self.actualizacion > self.frecuencia_fotograma :  # Si el tiempo obtenido en ahora - tiempo de actualización, es menos que el de la frecuencia fotograma
			self.actualizacion = ahora  # Vuelve a captar el tiempo de ahora
			self.fotograma += 1  # Y avanza un fotograma
			if self.fotograma == len (self.animacion_explosion1[self.dimensiones] ) :  # Si el número de fotogramas llega al final
				self.kill ()  # Que desaparezca de la pantalla
			else :  # Mientras no se cumpla la anterior condición, cada fotograma va a ir saliendo en la posición del anterior
				centro = self.rect.center
				self.image = self.animacion_explosion1[self.dimensiones][self.fotograma]
				self.rect = self.image.get_rect ()
				self.rect.center = centro
