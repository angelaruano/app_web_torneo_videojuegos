import pygame
import os
import juegos.arkanoid.arkanoid
from juegos.arkanoid.arkanoid import *

#Creo los directorios de imágenes
carpeta_juego = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_juego,"imagenes")
carpeta_ladrillos = os.path.join(carpeta_imagenes,"ladrillos")
carpeta_pala_y_pelota = os.path.join(carpeta_imagenes, "pala_y_pelota")
carpeta_poderes = os.path.join(carpeta_imagenes,"poderes")

#Creo los directorios de sonidos
carpeta_sonidos = os.path.join(carpeta_juego,"sonidos")
#Cargo los sonidos del juego
pygame.mixer.init() #Función de sonidos
toque_pala_y_limites = pygame.mixer.Sound(os.path.join(carpeta_sonidos,"toque_favo.wav"))
toque_ladrillos = pygame.mixer.Sound(os.path.join(carpeta_sonidos,"toque_debil.wav"))
poder_bueno = pygame.mixer.Sound(os.path.join(carpeta_sonidos,"poder_bueno.wav"))
poder_malo = pygame.mixer.Sound(os.path.join(carpeta_sonidos,"poder_malo.wav"))
diparos = pygame.mixer.Sound(os.path.join(carpeta_sonidos,"toque_disparo.wav"))
pierde_pelota = pygame.mixer.Sound(os.path.join(carpeta_sonidos,"pierde_pelota.wav"))

# Creo un pequeño catálogo de fuentes:
consolas = pygame.font.match_font('consolas')
times = pygame.font.match_font('times')
arial = pygame.font.match_font('arial')
courier = pygame.font.match_font('courier')


# Creo la clase para los ladrillos que va a heredar todos los métodos propios de pygame para sprites
class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, game, x, y, aleatorio):
        super().__init__() # Para heredar todos los métodos de Sprite
        self.game = game
        self.aleatorio = aleatorio
        # #Creo la variable para que la elección de ladrillos sea aleatoria
        ladrillos = os.path.join(carpeta_ladrillos,"ladrillo_{}.png".format(self.aleatorio))
        self.image = pygame.image.load(ladrillos).convert() #convert() optimiza las imágenes
        self.image.set_colorkey((255,255,255)) # set colorkey transparenta el color de fondo, en éste caso, blanco
        # Parámetros para colisiones
        self.rect = self.image.get_rect()
        self.rect.x = x # Coordenadas del ancho, empezando por la parte izquierda del ladrillo
        self.rect.y = y # Coordenadas del alto del ladrillo, empezando por la parte superior

    # Creo la función update() que es especial de las clases "sprites" que sirve para actualizar los movimientos y colisiones
    def update(self):
        pass #En éste caso, el ladrillo está inmóvil

class Pelota(pygame.sprite.Sprite):
    def __init__(self, game, x, y, velocidad_x, velocidad_y):
        super().__init__()
        self.game = game
        pelota = os.path.join(carpeta_pala_y_pelota, "pelota.png")
        self.image = pygame.image.load(pelota).convert()
        self.image.set_colorkey((255,255,255)) #Para transparentar la parte blanca y que nos salga redonda, no cuadrada
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = velocidad_x #Éstas son las direcciones a las que va a ir la pelota
        self.velocidad_y = velocidad_y
        self.num_impactos = 0

    def update(self):
        self.colisiones_ladrillos()

        #Voy a corregir las colisiones con la pala, para que la multiplicación de velocidad no sea infinita
        colisiones_pala = self.colisiones_pala()
        if colisiones_pala:
            if abs(self.velocidad_x) < 6: #abs = valor absoluto
                self.velocidad_x +=2
            elif abs(self.velocidad_x) > 6:
                self.velocidad_x = self.velocidad_x//2

        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        self.check_limites()


    def check_limites(self):

        if self.rect.left + self.velocidad_x < self.game.LIMITE_IZQ:
            self.velocidad_x = -self.velocidad_x
            toque_pala_y_limites.play()
        elif self.rect.right + self.velocidad_x > self.game.LIMITE_DER:
            self.velocidad_x = -self.velocidad_x
            toque_pala_y_limites.play()
        elif self.rect.top + self.velocidad_y < self.game.LIMITE_UP:
            self.velocidad_y = -self.velocidad_y
            toque_pala_y_limites.play()
        elif self.rect.bottom + self.velocidad_y > self.game.LIMITE_DOWN:
            self.mata_pelota()
            pierde_pelota.play()

    def mata_pelota(self):
        self.kill()
        self.game.vidas -= 1
        if self.game.vidas == 2:
            self.game.lista_sprites_dibujar.add(self.game.pelota2)
            self.game.lista_pelotas.add(self.game.pelota2)
        elif self.game.vidas == 1:
            self.game.lista_sprites_dibujar.add(self.game.pelota3)
            self.game.lista_pelotas.add(self.game.pelota3)
        else:
            self.game.gameOver = True
            self.game.vaciar_listas()


    #Creo las colisiones con la pala. Se trata de colisiones entre grupos de sprites con sprite.groupcollide()
    def colisiones_pala(self):
        #Los parámetros de groupcollide serán: el primer y segundo grupo de sprites y dos falses que significan qeu ni uno, ni otro grupo desaparezcan al colisionar
        impactos = pygame.sprite.groupcollide(self.game.lista_pala, self.game.lista_pelotas, False, False)

        #Ahora, con for y condicionales, voy a hacer que si la pelota da en esquita, salga escorada y si da en el centro, salga más recta
        for impacto in impactos:
            toque_pala_y_limites.play()
            if self.rect.centerx < impacto.rect.centerx - self.game.BLOQUE_ANCHO//1.9: #Si las coordenadas del centro de la pelota, son menores que las coordenadas del bloque dividido entre 1.9 (muy a la izquierda
                self.velocidad_x -= 2 #Ésto hace que la pelota salga mucho más doblada a la izquierda
                self.velocidad_y = -self.velocidad_y #Ésto hace que la pelota rebote
            elif self.rect.centerx > impacto.rect.centerx + self.game.BLOQUE_ANCHO//1.9:
                self.velocidad_x += 2
                self.velocidad_y = -self.velocidad_y
            else: #Si lo anterior no ocurre
                self.velocidad_x = self.velocidad_x//1.5 #Que la dirección de la pelota sea más derecha
                self.velocidad_y = -self.velocidad_y

    #Creo las colisiones con los ladrillos
    def colisiones_ladrillos(self):
        #Creo unas variables temporales que ayudan a que si la pelota choca con el ladrillos
        # en el eje vertical rebote verticalemte, y si choca de lado, haga lo propio
        choque_horizontal = abs(self.velocidad_x) + 1
        choque_vertical = abs(self.velocidad_y) + 1
        num_impactos = 0


        impactos = pygame.sprite.groupcollide(self.game.lista_ladrillo, self.game.lista_pelotas, True, False)
        for impacto in impactos:
            toque_ladrillos.play()
            if self.velocidad_x > 0: #Si la pelota va a la derecha
                if self.rect.right > impacto.rect.left and self.rect.right < impacto.rect.left + choque_horizontal: #Si le he dado horizontalmente (en lateral)
                    self.velocidad_x = -self.velocidad_x #Que la pelota vaya hacia el lado contrario

                else: #Si no le he dado lateralmente
                    self.velocidad_y = -self.velocidad_y #Que rebote arriba o abajo

            if self.velocidad_x < 0: #Si la pelota va a la izquierda
                if self.rect.left < impacto.rect.right and self.rect.left > impacto.rect.right - choque_horizontal: #Si le he dado horizontalmente (en lateral)
                    self.velocidad_x = -self.velocidad_x #Que la pelota vaya hacia el lado contrario
                else: #Si no le he dado lateralmente
                    self.velocidad_y = -self.velocidad_y #Que rebote arriba o abajo
            
        
        if impactos:
            
            self.game.puntos += random.randrange(30,100) #Puntuación aleatoria
        
class Pala(pygame.sprite.Sprite):
    def __init__(self, game, x, y, velocidad_x):
        super().__init__()
        self.game = game
        pala = os.path.join(carpeta_pala_y_pelota, "pala.png")
        self.image = pygame.image.load(pala).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x #Cento de la pala
        self.rect.top = y #Parte superior de la pala
        self.velocidad_x = velocidad_x

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.centerx -= self.velocidad_x
        elif teclas[pygame.K_RIGHT]:
            self.rect.centerx += self.velocidad_x
        self.limites_pala()

    def limites_pala(self):
        if self.rect.left + self.velocidad_x < self.game.LIMITE_IZQ:
            self.rect.left = self.game.LIMITE_IZQ
        elif self.rect.right + self.velocidad_x > self.game.LIMITE_DER:
            self.rect.right = self.game.LIMITE_DER


class Poderes(pygame.sprite.Sprite):
    def __init__(self, game, tipo, x, y, velocidad_y):
        super().__init__()
        self.game = game
        self.tipo = tipo
        self.ladrillo = ladrillo

        poder_balas = os.path.join(carpeta_poderes, "poder_balas.png")
        poder_vida = os.path.join(carpeta_poderes, "poder_vida.png")
        poder_lento = os.path.join(carpeta_poderes, "poder_lento.png")
        poder_reductor = os.path.join(carpeta_poderes, "poder_reductor.png")

        if self.tipo == 1:
            self.image = pygame.transform.scale(pygame.image.load(poder_balas).convert(),(15,15))
        if self.tipo == 2:
            self.image = pygame.image.load(poder_vida).convert()
        if self.tipo == 3:
            self.image = pygame.image.load(poder_lento).convert()
        if self.tipo == 4:
            self.image = pygame.image.load(poder_reductor).convert()

        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y #Cento de la pala
        self.velocidad_y = velocidad_y
        self.update()

    def update(self):
        self.rect.centery += self.velocidad_y







# Creo un sistema para que se me muestre el texto con la puntuación
class Texto:
    def __init__(self, game):
        self.game = game

    def muestra_texto(self,pantalla, fuente, texto, color, dimensiones, x, y):
        self.game.pantalla = pantalla
        tipo_letra = pygame.font.Font(fuente, dimensiones)
        superficie = tipo_letra.render(texto, True, color)
        rectangulo = superficie.get_rect()
        rectangulo.center = (x, y)
        self.game.pantalla.blit(superficie, rectangulo)





class DibujarLimites:
    def __init__(self,game):
        self.game = game

    def dibujar_limites(self):
        pygame.draw.rect(self.game.pantalla, self.game.GRIS2,(51,21,919,9))
        pygame.draw.rect(self.game.pantalla, (5,5,5),(60,29,900,1))
        pygame.draw.rect(self.game.pantalla, (250,250,250), (51,21,919,2))

        pygame.draw.rect(self.game.pantalla, self.game.GRIS2,(51,29,9,630))
        pygame.draw.rect(self.game.pantalla, (5,5,5),(59,29,1,630))
        pygame.draw.rect(self.game.pantalla, (250,250,250),(51,21,2,639))

        pygame.draw.rect(self.game.pantalla, self.game.GRIS2,(960,29,9,630))
        pygame.draw.rect(self.game.pantalla, (5,5,5),(960,29,1,630))
        pygame.draw.rect(self.game.pantalla, (250,250,250),(968,21,2,639))
