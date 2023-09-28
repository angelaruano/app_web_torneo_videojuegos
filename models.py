from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import db
from flask_login import UserMixin

#Clase Usuarios para registrar los datos de éstos.
class Usuarios ( db.Base, UserMixin ) :
	__tablename__ = 'registro'
	__table_args__ = {'sqlite_autoincrement' : True}
	id = Column ( Integer, primary_key = True )
	usuario = Column ( String, nullable = False )
	password = Column ( String, nullable = False )
	email = Column ( String, nullable = False )
	pais = Column ( String )
	provincia = Column ( String )
	administrador = Column ( Boolean, nullable = False )
	# Relaciones
	puntuacion_space = relationship ( "PuntuacionSpace", back_populates = "id_usuario", cascade = "all, delete-orphan" )
	puntuacion_naves = relationship ( "PuntuacionNaves", back_populates = "id_usuario", cascade = "all, delete-orphan" )
	puntuacion_arkanoid = relationship ( "PuntuacionArkanoid", back_populates = "id_usuario",
	                                     cascade = "all, delete-orphan" )
	
	def __init__(self, usuario, password, email, pais, provincia, administrador) :
		self.usuario = usuario
		self.password = password
		self.email = email
		self.pais = pais
		self.provincia = provincia
		self.administrador = administrador
		
		print ( "Usuario creado con éxito" )
	
	def __repr__(self) :
		return "-id: {} \n" \
		       "-nombre:{} \n" \
		       "-contraseña: {} \n" \
		       "-email: {} \n" \
		       "-pais: {} \n" \
		       "-provincia \n".format ( self.id, self.usuario,self.password,self.email,self.pais,
		self.provincia)
	
#Funciones de Usermixin
	def is_authenticated(self) :
		return True
	
	def is_active(self) :
		return True
	
	def is_anonymous(self) :
		return False
	
	def get_id(self) :
		return str ( self.id )
	
	def is_admin(self) :
		return self.administrador

#Hago las clases para las puntuaciones de los juegos
class PuntuacionSpace ( db.Base ) :
	__tablename__ = 'puntuacion_space'
	__table_args__ = {'sqlite_autoincrement' : True}
	id = Column ( Integer, primary_key = True )
	usuario_id = Column ( Integer, ForeignKey ( "registro.id" ) )
	puntos = Column ( Integer )
	
	# Relaciones
	id_usuario = relationship ( "Usuarios", back_populates = "puntuacion_space", uselist = False, single_parent = True )
	
	def __init__(self, puntos, identidad) :
		self.puntos = puntos
		self.usuario_id = identidad
		
	
	def __repr__(self) :
		return "Space: Puntuación número {}: número de usuario {}, puntos {}".format ( self.id, self.usuario_id,
		                                                                               self.puntos )

class PuntuacionNaves ( db.Base ) :
	__tablename__ = 'puntuacion_naves'
	__table_args__ = {'sqlite_autoincrement' : True}
	id = Column ( Integer, primary_key = True )
	usuario_id = Column ( Integer, ForeignKey ( "registro.id" ) )
	puntos = Column ( Integer )
	# Relaciones
	id_usuario = relationship ( "Usuarios", back_populates = "puntuacion_naves", uselist = False, single_parent = True )
	
	def __init__(self, puntos, identidad) :
		self.puntos = puntos
		self.usuario_id = identidad

	
	def __repr__(self) :
		return "Naves: Puntuación número {}: número de usuario {}, puntos {}".format ( self.id, self.usuario_id,
		                                                                               self.puntos )

class PuntuacionArkanoid ( db.Base ) :
	__tablename__ = 'puntuacion_arkanoid'
	__table_args__ = {'sqlite_autoincrement' : True}
	id = Column ( Integer, primary_key = True )
	usuario_id = Column ( Integer, ForeignKey ( "registro.id" ) )
	puntos = Column ( Integer )
	# Relaciones
	id_usuario = relationship ( "Usuarios", back_populates = "puntuacion_arkanoid", uselist = False,
	                            single_parent = True )
	
	def __init__(self, puntos, identidad) :
		self.puntos = puntos
		self.usuario_id = identidad
	
	def __repr__(self) :
		return "Arkanoid: Puntuación número {}: número de usuario {}, puntos {}".format ( self.id, self.usuario_id,
		                                                                                  self.puntos )

#Creo el administrador
def administrador_principal() :
	administrador = Administrador ( usuario = "angela", password = "proyecto",
	                                is_admin = True )
	
	db.session.add ( administrador )
	db.session.commit ()
	
	print ( "Administrador creado con éxito" )
	
#Función para el borrado de usuarios
def borrar_usuario(identidad):
	borro_usuario = db.session.query(Usuarios).get(identidad)
	db.session.delete(borro_usuario)
	db.session.commit()
	db.session.close()
	return "Usuario borrado con éxito"

#Funación para el cambio de contraseña
def cambio_password(identidad, nueva):
	cambio_usuario = db.session.query(Usuarios).get(identidad)
	cambio_usuario.password = nueva
	db.session.commit()
	db.session.close()
	cambio = db.session.query(Usuarios).get(identidad)
	return "cambio efectuado"
#Función para lograr una lista de todos los usuarios y funciones para listar sus puntajes
def lista_usuarios():
	listar = db.session.query(Usuarios).all()
	return listar
def lista_puntajes_spa(id):
	listarspa = db.session.query(PuntuacionSpace).filter_by(usuario_id = id).order_by(PuntuacionSpace.puntos.desc()).all()
	for puntos in listarspa:
		print(puntos.puntos)
	return listarspa
def lista_puntajes_nav(id):
	listarnav = db.session.query(PuntuacionNaves).filter_by(usuario_id = id).order_by(PuntuacionNaves.puntos.desc()).all()
	for puntos in listarnav:
		print(puntos.puntos)
	return listarnav
def lista_puntajes_ark(id):
	listarark = db.session.query(PuntuacionArkanoid).filter_by(usuario_id = id).order_by(PuntuacionArkanoid.puntos.desc()).all()
	for puntos in listarark:
		print(puntos.puntos)
	return listarark

#Función para listar los emails para que el administrador pueda enviar correos
def coge_email(tipo,identidad):
	tipo = tipo
	if tipo == 1:
		lista_correo = []
		lista_email = db.session.query(Usuarios).all()
		for email in lista_email:
			correo = email.email
			if correo != "":
				lista_correo.append(correo)
		return lista_correo
	if tipo == 2:
		correo = db.session.query(Usuarios).filter_by(id = identidad).first()
		correo_usuario = correo.email
		return correo_usuario
		