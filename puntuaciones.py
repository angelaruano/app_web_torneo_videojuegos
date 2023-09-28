

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

from sqlalchemy.orm import joinedload

#Funciónes para las puntuaciones máximas de cada juego
def maxi_space():
	lista = []
	cuenta = 0
	ranking = db.session.query(PuntuacionSpace).order_by(PuntuacionSpace.puntos.desc()).limit(10)
	for x in ranking:
		cuenta += 1
		nombre = db.session.query(Usuarios).get(x.usuario_id)
		lista.append(nombre.usuario)
		lista.append(x.puntos)

	return lista
	
def maxi_naves():
	lista = []
	cuenta = 0
	ranking = db.session.query(PuntuacionNaves).order_by(PuntuacionNaves.puntos.desc()).limit(10)
	for x in ranking:
		cuenta +=1
		nombre = db.session.query(Usuarios).get(x.usuario_id)
		lista.append(nombre.usuario)
		lista.append(x.puntos)

	return lista
	
def maxi_arkanoid():
	lista = []
	cuenta = 0
	ranking = db.session.query(PuntuacionArkanoid).order_by(PuntuacionArkanoid.puntos.desc()).limit(10)
	for x in ranking:
		cuenta += 1
		nombre = db.session.query(Usuarios).get(x.usuario_id)
		lista.append(nombre.usuario)
		lista.append(x.puntos)

	return lista
#Funciones para que el usuario vea sus 5 máximas puntuaciones en cada juego
def ususario_maxi_space(identidad):
	lista = []
	identificacion = identidad
	maxi_usuario = db.session.query(PuntuacionSpace).order_by(PuntuacionSpace.puntos.desc()).filter_by(usuario_id = identificacion).limit(5)
	for x in maxi_usuario:
		lista.append(x.puntos)

	return lista
		
def ususario_maxi_naves(identidad):
	lista = []
	identificacion = identidad
	maxi_usuario = db.session.query(PuntuacionNaves).order_by(PuntuacionNaves.puntos.desc()).filter_by(usuario_id = identificacion).limit(5)
	for x in maxi_usuario:
		lista.append(x.puntos)

	return lista
		
def ususario_maxi_arkanoid(identidad):
	lista = []
	identificacion = identidad
	maxi_usuario = db.session.query(PuntuacionArkanoid).order_by(PuntuacionArkanoid.puntos.desc()).filter_by(usuario_id = identificacion).limit(5)
	for x in maxi_usuario:
		lista.append(x.puntos)

	return lista
	

#Función para sumar las máximas puntuaciones de los tres juegos de cada usuario y saber si alguien se lleva el premio absoluto
def usuario_maxi_puntos():
	lista_space = []
	lista_naves = []
	lista_arkanoid = []
	#Busco las máximas puntuaciones, para meter las identidades de los usuarios en las listas
	cuenta = 0
	ranking_space = db.session.query(PuntuacionSpace).order_by(PuntuacionSpace.puntos.desc()).limit(3)
	for x in ranking_space:
		cuenta += 1
		quien = db.session.query(Usuarios).filter(Usuarios.id == x.usuario_id)
		lista_space.append(x.usuario_id)
		for i in quien:
			print(i.usuario)

	cuenta = 0
	ranking_naves = db.session.query(PuntuacionNaves).order_by(PuntuacionNaves.puntos.desc()).limit(3)
	for x in ranking_naves:
		cuenta += 1
		quien = db.session.query(Usuarios).filter(Usuarios.id == x.usuario_id)
		lista_naves.append(x.usuario_id)
		for i in quien:
			print(i.usuario)
		
	cuenta = 0
	ranking_arkanoid = db.session.query(PuntuacionArkanoid).order_by(PuntuacionArkanoid.puntos.desc()).limit(3)
	for x in ranking_arkanoid:
		cuenta += 1
		quien = db.session.query(Usuarios).filter(Usuarios.id == x.usuario_id)
		lista_arkanoid.append(x.usuario_id)
		for i in quien:
			print(i.usuario)

	#Convierto las listas en conjuntos para buscar coincidencias en las tres
	# el usuario que esté en el ranking de los 3 juegos, gana y,en caso de empate,
	#  se suman los puntos máximos que cada usuario tenga en cada juego, y gana el de mayor puntuación
	set_space = set(lista_space)
	set_naves = set(lista_naves)
	set_arkanoid = set(lista_arkanoid)
	coincidencias = set_space & set_naves & set_arkanoid
	print(coincidencias)
	#Convierto el conjunto en lista
	lista_coincidencias = list(coincidencias)
	
	#Creo la lista de finalistas para saber quién ha sacado más puntos
	lista_finalistas = []
	for datos in lista_coincidencias:
		punt1 = db.session.query(PuntuacionSpace).filter(PuntuacionSpace.usuario_id == datos).order_by(PuntuacionSpace.puntos.desc()).first()
		punt2 = db.session.query(PuntuacionNaves).filter(PuntuacionNaves.usuario_id == datos).order_by(PuntuacionNaves.puntos.desc()).first()
		punt3 = db.session.query(PuntuacionArkanoid).filter(PuntuacionArkanoid.usuario_id == datos).order_by(PuntuacionArkanoid.puntos.desc()).first()
		total = punt1.puntos + punt2.puntos + punt3.puntos
		lista_finalistas.append([total,datos])
		
	ganador = max(lista_finalistas)
	ganador_nombre = db.session.query(Usuarios).get(ganador[1])
	print("EL GANADOR DEL RETO ES, ",ganador_nombre.usuario," con ID: ",ganador[1], ",con la puntuación de ",ganador[0])
	lista_final = []
	for x in lista_finalistas:
		nombre = db.session.query(Usuarios).get(x[1])
		lista_final.append(nombre.usuario)
		lista_final.append(x[0])
	return lista_final
