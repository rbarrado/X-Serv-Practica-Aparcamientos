from django.shortcuts import render
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from .models import Aparcamiento, Usuario
import urllib.request
import sys


def normalize_whitespace(text):
	string = ""
	result = string.join(text)

	return result

class myContentHandler(ContentHandler):
	def __init__ (self):
		self.inItem = False
		self.inContent = False
		self.theContent = ""
		self.entidad = ""
		self.nombre = ""
		self.descripcion = ""
		self.accesibilidad = ""
		self.enlace = ""
		self.url = False
		self.nombrevia = ""
		self.clasevial = ""
		self.tiponum = ""
		self.num = ""
		self.localidad = ""
		self.provincia = ""
		self.codigopostal = ""
		self.barrio = ""
		self.distrito= ""
		self.coordenadax = ""
		self.coordenaday= ""
		self.latitud = ""
		self.longitud = ""
		self.datoscontacto = ""
		self.telefono = ""
		self.email = ""
		self.attr = ""
		self.save = False

	def startElement (self, name, attrs):
		if name == 'contenido':
			self.inItem = True
		if self.inItem:
			if name == 'atributo':
				self.attr = normalize_whitespace(attrs.get('nombre'))
				if self.attr == "ID-ENTIDAD":
					self.inContent = True
				elif self.attr == "NOMBRE":
					self.inContent = True
				elif self.attr == "DESCRIPCION":
					self.incontent = True
				elif self.attr == "ACCESIBILIDAD":
					self.incontent = True
				elif self.attr == "CONTENT-URL":
					self.url = True
					self.incontent = True
				elif self.attr == "CLASE-VIAL":
					self.incontent = True
				elif self.attr == "NUM":
					self.incontent = True
				elif self.attr == "LOCALIDAD":
					self.incontent = True
				elif self.attr == "PROVINCIA":
					self.incontent = True
				elif self.attr == "CODIGO-POSTAL":
					self.incontent = True
				elif self.attr == "BARRIO":
					self.incontent = True
				elif self.attr == "DISTRITO":
					self.incontent = True
				elif self.attr == "COORDENADA-X":
					self.incontent = True
				elif self.attr == "LATITUD":
					self.inContent = True
				elif self.attr == "LONGITUD":
					self.inContent = True
				elif self.attr == "TELEFONO":
					self.inContent = True
				elif self.attr == "EMAIL":
					self.inContent = True
				elif self.attr == "DATOSCONTACTOS":
					self.inContent = True

	def endElement (self, name):
		if self.inContent:
			self.theContent = normalize_whitespace(self.theContent)

		if self.attr == "ID-ENTIDAD":
			self.entidad = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "NOMBRE":
			self.nombre = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "NOMBRE-VIA":
			self.nombrevia = self.theContent
			self.theContent = ""
		elif self.attr == "DESCRIPCION":
			self.descripcion = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "ACCESIBILIDAD":
			self.accesibilidad = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "CONTENT-URL":
			self.url = False
			self.enlace = self.theContent
			self.theContent = ""
		elif self.attr == "CLASE-VIAL":
			self.clasevial = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "NUM":
			self.num = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "LOCALIDAD":
			self.localidad = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "PROVINCIA":
			self.provincia = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "CODIGO-POSTAL":
			self.codigopostal = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "BARRIO":
			self.barrio = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "DISTRITO":
			self.distrito = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "COORDENADA-X":
			self.coordenadax = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "COORDENADA-Y":
			self.coordenaday = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "LATITUD":
			self.latitud = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "LONGITUD":
			self.longitud = self.theContent		#Junto los titulos
			self.theContent = ""
		elif self.attr == "DATOSCONTACTOS":
			p = Aparcamiento(ident = self.entidad, Nombre = self.nombre, Nombre_via = self.nombrevia, Numero = self.num, Localidad = self.localidad, Provincia = self.provincia, Cod_Postal = self.codigopostal, Barrio = self.barrio, Distrito = self.distrito, Coord_X = self.coordenadax, Coord_Y = self.coordenaday, Enlace = self.enlace, Descripcion = self.descripcion, Accesibilidad = self.accesibilidad, Telefono = self.telefono, Email = self.email)
			p.save()

		if self.attr == "TELEFONO":
			self.telefono = self.theContent
			self.theContent = ""
			self.attr = "DATOSCONTACTOS"
		elif self.attr == "EMAIL":
			self.email = self.theContent
			self.theContent = ""
			self.attr = "DATOSCONTACTOS"

		#print(self.entidad)
		#print(self.nombre)
		#print(self.descripcion)
		#print(self.accesibilidad)
		#print(self.clasevial)


	def characters (self, chars):
		if self.inContent:
			if self.url :
				self.theContent = self.theContent + chars
			else:
				self.theContent = chars



def get_data():

	theParser = make_parser()
	theHandler = myContentHandler()
	theParser.setContentHandler(theHandler)

	url = 'http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?'
	url += 'vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-'
	url += 'residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full'

	xmlFile = urllib.request.urlopen(url)
	theParser.parse(xmlFile)

	return("Parser completed")

