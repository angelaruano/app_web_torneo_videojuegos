

from flask import Flask, session, render_template, redirect, request, url_for, flash
#from flask_login import LoginManager
import db
import webbrowser

import puntuaciones
import juegos.espacio.espacio
import models
from models import Usuarios, PuntuacionSpace, PuntuacionNaves, PuntuacionArkanoid
import pygame, sys
from pygame.locals import *

import os
from juegos.naves import run, ra_1, ra_2
from juegos.naves.run import GameNaves
from juegos.espacio.espacio import *
from juegos.arkanoid import arkanoid,clases
from juegos.arkanoid.arkanoid import GameArkanoid


app = Flask ( __name__ )
#login_manager = LoginManager(app)
app.secret_key = "Clave_secreta"  # Necesario para que funcione la función flash de flask

#Manejo de sesiones y vistas restringidas
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "logueo"

@login_manager.user_loader
def load_user(user_id):
	return db.session.query(Usuarios).get(user_id)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("login"))

#Ruta y función para que cada usuario pueda ver sus datos
@app.route('/perfil', methods=["GET", "POST"])
@login_required
def perfil():
	user = current_user
	perfil = db.session.query(Usuarios).filter_by(usuario = user.usuario).first()
	recordspa = puntuaciones.ususario_maxi_space(user.id)
	while len(recordspa) < 3:
		recordspa.append(0) #Relleno las listas con 0 puntos
	recordnav = puntuaciones.ususario_maxi_naves(user.id)
	while len(recordnav) < 3:
		recordnav.append(0)
	recordark = puntuaciones.ususario_maxi_arkanoid(user.id)
	while len(recordark) < 3:
		recordark.append(0)
	
	return render_template("perfil.html",perfil = perfil,
	                       punspa1 = recordspa[0],punspa2 = recordspa[1],punspa3 = recordspa[2],
	                       punnav1 = recordnav[0],punnav2 = recordnav[1],punnav3 = recordnav[2],
	                       punark1 = recordark[0],punark2 = recordark[1],punark3 = recordark[2])

#Ruta y función para darse de baja
@app.route("/baja", methods = ["GET", "POST"])
def baja():
	user = current_user
	models.borrar_usuario(user.id)
	print("usuario borrado")
	return redirect(url_for("login"))

#Ruta y función para cambiar contraseña
@app.route("/cambio", methods = ["GET","POST"])
def cambio():
	user = current_user
	antigua = db.session.query(Usuarios).get(user.id)
	contr_antigua = antigua.password
	print(antigua.password)
	if request.method == "POST" :
		nueva = request.form["password"]
		contr_nueva = nueva
		print(nueva)
		models.cambio_password(user.id,nueva)
		flash ("CONTRASEÑA CAMBIADA A: {}".format(contr_nueva) )
	
	return render_template("/cambio.html",password = contr_antigua)

#Rutas y funciones del administrador

@app.route("/admin/listarusuarios", methods = ["GET", "POST"])
def busca_usuario():
	#Listado de todos los usuarios
	listar = models.lista_usuarios()
	return render_template("/admin/listarusuarios.html",listar = listar)

@app.route("/admin/verusuario/<int:id>")
def ver_usuario(id):
	perfil = db.session.query(Usuarios).filter_by(id = id).first()
	lista_spa=models.lista_puntajes_spa(id)
	veces_spa = len(lista_spa)
	lista_nav=models.lista_puntajes_nav(id)
	veces_nav = len(lista_nav)
	lista_ark=models.lista_puntajes_ark(id)
	veces_ark = len(lista_ark)
	return render_template("/admin/verusuario.html", perfil = perfil,
	                       lista_spa = lista_spa,veces_spa=veces_spa,
	                       lista_nav = lista_nav,veces_nav = veces_nav,
	                       lista_ark = lista_ark,veces_ark = veces_ark)

@app.route("/borrar/<int:id>")
def borrar_usuario(id):
	models.borrar_usuario(id)
	print ("Usuario borrado")
	return redirect(url_for("index"))
	
@app.route("/emailmasivo" ,methods = ["GET", "POST"])
def email_masivo():
	correo1 = models.coge_email(tipo = 1,identidad = None)
	return render_template("/admin/email.html",correo1 = correo1)

@app.route("/emailindividual/<int:id>" ,methods = ["GET", "POST"])
def email_individual(id):
	correo2 = models.coge_email(tipo = 2,identidad = id)
	return render_template("/admin/email.html",correo2 = correo2)

#Rutas y funciones para inicio,registro y logueo
@app.route ( "/" )
def inicio() :
	
	return redirect ( url_for ( "login" ) )


@app.route ( "/pagina-registro" )
def pagina_registro() :
	return render_template ( "auth/registro.html" )

@app.route ( "/crear-registro", methods = ["POST"] )
def crear_registro() :
	usuario = request.form["usuario"]
	password = request.form["password"]
	usuarios = Usuarios ( usuario, password,
	                      email = request.form["email"], pais = request.form["pais"],
	                      provincia = request.form["provincia"] ,administrador = comprueba_admin(usuario,password) )
	#En el parámetro de "administrador" invoco a la función "comprueba_admin" para saber si se registra o mo el administrador
	db.session.add ( usuarios )
	db.session.commit ()
	print ( "Guardado" )
	

	return render_template ( "auth/login.html" )


@app.route ( "/login", methods = ["GET", "POST"] )
def login() :
	if request.method == "POST" :
		print ( request.form["usuario"] )
		usuario_web = request.form["usuario"]
		print ( request.form["password"] )
		password_web = request.form["password"]
		
		resultado2 = db.session.query ( Usuarios ).filter ( Usuarios.usuario.ilike ( usuario_web ) ).all ()
		
		if resultado2 == [] :
			flash (
				"Usuario no válido..." )  # Éste mensaje va enlazado al html de login, para que se muestre en la página
			return redirect ( url_for ( "login" ) )
		for x in resultado2 :
			login_user(x)
			if x.usuario == usuario_web :
				resultado3 = str ( x.password )
				if resultado3 == password_web :
					session['usuario'] = usuario_web
					session['password'] = password_web
					return redirect ( url_for ( "index" ) )
				elif resultado3 == [] :
					flash (
						"Contraseña no válida..." )  # Éste mensaje va enlazado al html de login, para que se muestre en la página
					return redirect ( url_for ( "login" ) )
				
				else :
					flash (
						"Contraseña no válida..." )  # Éste mensaje va enlazado al html de login, para que se muestre en la página
					return redirect ( url_for ( "login" ) )
		
		return render_template ( "index.html" )
	else :
		return render_template ( "auth/login.html" )


@app.route ( "/index" )
@login_required #Este decorador autoriza a ver la ruta sólo si se está regustrado
def index() :
	return render_template ( "index.html" )

#Rutas para pestañas
@app.route("/contacto")
def contacto():
	return render_template("/contacto.html")

@app.route("/instrucciones")
def instrucciones():
	return render_template("/instrucciones.html")

#Ruta para resultados del torneo y sus bases
@app.route("/torneo")
def torneo():
	lista_final = puntuaciones.usuario_maxi_puntos()
	lista = puntuaciones.maxi_space()
	lista_nav = puntuaciones.maxi_naves()
	lista_ark = puntuaciones.maxi_arkanoid()
	while len(lista_final) < 6:
		lista_final.append(0) #Relleno las listas con 0 puntos
	while len(lista_nav) < 20:
		lista_nav.append(0) #Relleno las listas con 0 puntos
	while len(lista_ark) < 20:
		lista_ark.append(0) #Relleno las listas con 0 puntos
	return render_template("/torneo.html", lista = lista, lista_nav = lista_nav, lista_ark = lista_ark, lista_final = lista_final)

#Ruta para mostrar los premios
@app.route("/premios")
def premios():
	return render_template("/premios.html")

#RUTAS Y FUNCIONES PARA INICIAR LOS JUEGOS
@app.route ( "/juegaspace")
@login_required
def juegaspace():
	nueva_ventana("space")
	return render_template("index.html")
@app.route ( "/jueganaves")
@login_required
def jueganaves():
	nueva_ventana("naves")
	return render_template("index.html")
@app.route ( "/juegaarkanoid")
@login_required
def juegaarkanoid():
	nueva_ventana("arkanoid")
	return render_template("index.html")

#Utilizo éste método para que al jugar, se cargue en una nueva ventana.
#Ésto es porque para cerrar la ventana del juego y que no se reinstancie, hay que cerrar la pestaña primero.
#De ésta forma, logro no tener que cerrar la web entera

def nueva_ventana(tipo_juego = ""):
	if tipo_juego == "space":
		return [webbrowser.open_new_tab("http://127.0.0.1:5000/comenzarspace")]
	elif tipo_juego == "naves":
		return [webbrowser.open_new_tab("http://127.0.0.1:5000/comenzarnaves")]
	elif tipo_juego == "arkanoid":
		return [webbrowser.open_new_tab("http://127.0.0.1:5000/comenzararkanoid")]
	
#Arranco los juegos
@app.route("/comenzarspace")
@login_required
def vamosspace():
	game = GameEspacio()
	game.run()
@app.route("/comenzarnaves")
@login_required
def vamosnaves():
	game = GameNaves()
	game.run()
@app.route("/comenzararkanoid")
@login_required
def vamosarkanoid():
	game = GameArkanoid()
	game.run()
	
#Creación de los objetos para puntuaciones
def puntuacion_space(puntos) :
	user = session["usuario"]
	identidad = db.session.query(Usuarios).filter_by(usuario = user).first()
	puntuacion = PuntuacionSpace ( puntos,identidad.id )
	db.session.add ( puntuacion )
	db.session.commit ()
	
def puntuacion_naves(puntos) :
	user = session["usuario"]
	identidad = db.session.query(Usuarios).filter_by(usuario = user).first()
	puntuacion = PuntuacionNaves ( puntos, identidad.id )
	db.session.add ( puntuacion )
	db.session.commit ()

def puntuacion_arkanoid(puntos) :
	user = session["usuario"]
	identidad = db.session.query(Usuarios).filter_by(usuario = user).first()
	puntuacion = PuntuacionArkanoid ( puntos, identidad.id )
	db.session.add ( puntuacion )
	db.session.commit ()

	
#En ésta función, si el usuario y contraseña coinciden con los requeridos, se tendrá rol de administrador
def comprueba_admin(usuario, password):
	if usuario == "angela" and password == "proyecto":
		return True
	else:
		return False

if __name__ == "__main__" :
	db.Base.metadata.create_all ( db.engine )
	app.run ( debug = True )

	
	
	

