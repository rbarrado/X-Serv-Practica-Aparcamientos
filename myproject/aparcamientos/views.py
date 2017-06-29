from django.shortcuts import render
from django.http import HttpResponse
from .models import Aparcamiento, Usuario, Fecha, Comentario
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import Context
from .parser import get_data
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User

#from xml.sax import make_parser
#from xmlparser import myContentHandler
#from urlib.parse import unquote_plus

# Create your views here.
@csrf_exempt
#Lista de aparcamientos con la url
def lista_aparcamientos():
	#obtengo todos los aparcamientos
	aparcamientos = Aparcamiento.objects.all()

	#Creo la lista de aparcamientos
	Lista_Aparcamientos = "<ol>"
	for i in aparcamientos:
		Lista_Aparcamientos += '<li>' + i.Nombre
		Lista_Aparcamientos += '<br><a href="'  + i.Enlace + '">' + i.Nombre + '</a><br>'
		Lista_Aparcamientos += 'Dirección: ' + i.Clase_vial + ' ' + i.Nombre_via + '<br>'
		Lista_Aparcamientos += '<a href=http://localhost:1234/aparcamientos/'+ str(i.ident) + '>' + 'Más información</a><br>'
		Lista_Aparcamientos += "<br>"

	Lista_Aparcamientos += "</ol>"
	return(Lista_Aparcamientos)

#Lista de aparcamientos sin la url
def lista_aparcamientos2():

	#obtengo todos los aparcamientos
	aparcamientos = Aparcamiento.objects.all()
	aparcamientos_ordenados = aparcamientos.order_by("-Num_Megusta")[:5]
	#Creo la lista de aparcamientos
	Lista_Aparcamientos2 = ''
	for i in aparcamientos_ordenados:
		if i.Num_Megusta != 0:
			Lista_Aparcamientos2 += '<li><a href="'  + i.Enlace + '">' + i.Nombre + '</a><br>'
			Lista_Aparcamientos2 += 'Dirección: ' + i.Clase_vial + ' ' + i.Nombre_via + '<br>'
			Lista_Aparcamientos2 += '<a href=http://localhost:1234/aparcamientos/'+ str(i.ident) + '>' + 'Más información</a><br>'
			Lista_Aparcamientos2 += "<br>"

	return(Lista_Aparcamientos2)

#menu para loguearse
def log ():
	salida = '<form action="login" method="POST">'
	salida += 'Nombre de usuario<br><input type="text" name="Usuario"><br>'
	salida += 'Contraseña<br><input type="password" name="Password">'
	salida += '<br><br><input type="submit" value="Entrar"><br><br>'
	salida += '</form>'

	return (salida)

def Lista_Usuarios():

	usuarios = User.objects.all()
	Lista_Usuarios = 'Listado de páginas personales: <br><br>'
	for i in usuarios:
		Lista_Usuarios += i.username + '<br>'
		try:
			Lista_Usuarios += 'Titulo: ' + Usuario.objects.get(Nombre=i.id).Titulo_pagina
		except ObjectDoesNotExist:
			Lista_Usuarios += 'Título: ' + i.username + '<br>'

		Lista_Usuarios += '<li><a href=http://localhost:1234/'+ str(i.username) + '>' + 'Más información</a><br>'
	Respuesta = Lista_Usuarios
	return(Respuesta)

def form_titulo():

	respuesta = '<br><br><form action="" method="POST">'
	respuesta += 'Titulo de página <br><input type="text" name="Titulo"><br>'
	respuesta += '<input type="submit" value="Entrar"><br><br>'
	respuesta += '</form>'
	return (respuesta)

def todos():

	respuesta = '<li><a href="/aparcamientos/"' + '>' + 'Todos</a><br>'

	return(respuesta)

def red_about():

	respuesta = '<li><a href="/about/"' + '>' + 'Ayuda</a><br>'

	return(respuesta)

def footer():

	url = 'http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?'
	url += 'vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-'
	url += 'residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full'

	url2 = 'http://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default'

	pie_pagina = '<html><body><p>Esta aplicación utiliza datos del portal de datos abiertos de la ciudad de Madrid. © Copyright'\
				+ '</p></body></html>'
	pie_pagina += 'Descripcion de los datos en XML: '
	pie_pagina += '<a href="' + url + '">' + url + '</a><br><br>'
	pie_pagina += '<a href="' + url2 + '"> Descripcion de los datos en la pagina</a>'

	#'<a href="'  + i.Enlace + '">' + i.Enlace + '</a>'

	return pie_pagina

@csrf_exempt
def logearse (request):

	usuario = request.POST['Usuario']
	contraseña = request.POST['Password']
	user = authenticate(username=usuario, password=contraseña)
	result = request.user.is_authenticated()
	if user is not None:
		login(request, user)
		return redirect('/')
	else:
		Log = log()
		Texto = 'Usuario inválido'
		Templates = get_template('fallo.html')
		c = Context({'Texto': Texto, 'Log': Log})
		renderizado = Templates.render(c)
		return HttpResponse(renderizado)

def mylogout(request):
    logout(request)
    return redirect('/')

def logeado(request):
	if request.user.is_authenticated:
		Respuesta = '<li><a href=http://localhost:1234/>' + 'Logout</a><br>'
	else:
		Respuesta = log()

	return(Respuesta)
@csrf_exempt
def aparcamientos(request):

	pie_pagina = footer()
	imagen_principal = '<img src="/static/img/banner.jpg"/>'
	Templates = get_template("aparcamientos.html")
	#Hago el formulario para firmar por distritos
	Formulario = ''
	if request.user.is_authenticated():
		Formulario = "<span class='.t-center'> Usuario: " + str(request.user) + ". " + "<a href='/logout'>Logout</a></span><br>"
	Formulario += "Filtrar por distritos:"
	Formulario += '<form action="" method="POST">'
	Formulario += 'Distrito: <input type="text" name="Distrito">'
	Formulario += "<br>"
	Formulario += '<input type="submit" value="Buscar">'
	Formulario += "<br>"
	Formulario += "<br>"

	Lista = lista_aparcamientos ()

	#Si me llegan un POST, porque he enviado un distrito a filtrar
	if request.method == "POST":
		Distrito_filtrado = request.POST['Distrito']
		Distrito_filtrado = Distrito_filtrado.upper()

		if Distrito_filtrado == '':
			Lista = ("No ha introducido ningún distrito, vuelva a intentarlo" + "<br>"  + Lista)
		else:
			aparcamientos = Aparcamiento.objects.all()
			Lista_Filtrada = ""
			for i in aparcamientos:
				if Distrito_filtrado == i.Distrito:
					Distrito = i.Distrito
					Lista_Filtrada += '<li>' + i.Nombre + '</li>'
					Lista_Filtrada += '<a href="'  + i.Enlace + '">' + i.Enlace + '</a>'
					Lista_Filtrada += "<br>"
					Lista_Filtrada += "<br>"

			#Si no hay ningun distrito con ese nombre
			if Lista_Filtrada == '':
				Lista = ("NO HAY APARCAMIENTOS EN ESTE DISTRITO, VUELVA A INTRODUCIR OTRO DISTRITO --->" +"<br>")
			else:
				Lista = "<br>LISTA DE APARCAMIENTOS EN " + Distrito + ":" + "<br><br> "+ Lista_Filtrada

	c = Context({'Formulario': Formulario, 'Lista': Lista})#aqui tengo que meter las variables que qiero en la plantilla
	renderizado = Templates.render(c)
	return HttpResponse(renderizado)
	return HttpResponse(Formulario + Lista)

@csrf_exempt
def aparcamientos_id(request, recurso):

	Templates = get_template("aparcamientos.html")

	try:
		aparcamiento = Aparcamiento.objects.get(ident=recurso)

		Nombre = aparcamiento.Nombre
		Nombre_via = aparcamiento.Nombre_via
		Via = aparcamiento.Clase_vial
		Numero = aparcamiento.Numero
		Localidad = aparcamiento.Numero
		Provincia = aparcamiento.Provincia
		Cod_Postal = aparcamiento.Cod_Postal
		Barrio = aparcamiento.Barrio
		Distrito = aparcamiento.Distrito
		Coord_X = aparcamiento.Coord_X
		Coord_Y = aparcamiento.Coord_Y
		Enlace = aparcamiento.Enlace
		Descripcion = aparcamiento.Descripcion
		Accesibilidad = aparcamiento.Accesibilidad
		Telefono = aparcamiento.Telefono
		Email = aparcamiento.Email

		if Accesibilidad == 1:
			Acces = "Accesible"
		else:
			Acces = "No Accesible"
		Logout=''
		if request.user.is_authenticated():
			Logout = "<span class='.t-center'> Usuario: " + str(request.user) + ". " + "<a href='/logout'>Logout</a></span><br>"
		Respuesta = "<p>Esta es la página con la información del aparcamiento " +'<a href="'  + Enlace + '">' + Nombre + '</a>' + "</br></p>"
		Respuesta += "Descripción: " + Descripcion + "<br>"
		Respuesta += "<br>"
		Respuesta += "Barrio: " + Barrio + "<br>"
		Respuesta += "<br>"
		Respuesta += "Distrito: " + Distrito + "<br>"
		Respuesta += "<br>"
		Respuesta += "Accesibilidad: " + Acces + "<br>"
		Respuesta += "<br>"
		Respuesta += "Telefono: " + Telefono + "<br>"
		Respuesta += "<br>"
		Respuesta += "Email: " + Email + "<br>"
		Formulario = ''
		Boton1 = ''
		Boton1 += "<br> Indica si te gusta el aparcamiento "
		Boton1 += '<br><form action="" method="POST">'
		Boton1 += '<button type="submit" name="Me gusta" value= "Megusta">+1</button><br>'
		Boton1 += "<br>"

		if request.user.is_authenticated():
			Formulario += "<br> Añade un comentario <br>"
			Formulario += '<form action="" method="POST">'
			Formulario += 'Comentario: <input type="text" name="Comentario">'
			Formulario += ""
			Formulario += '<input type="submit" value="Comentar">'
			Formulario += "<br>"
			Formulario += "<br>"

		Respuesta += Boton1
		Respuesta += Formulario

		if request.method == "POST":
			key = request.body.decode('utf-8').split('=')[0]
			if key == "Me+gusta":
				contador = request.POST.get('Megusta')
				aparcamiento = Aparcamiento.objects.get(ident=recurso)
				aparcamiento.Num_Megusta = aparcamiento.Num_Megusta + 1

				aparcamiento.save()
			else:
				comentario = request.POST['Comentario']
				aparcamiento = Aparcamiento.objects.get(ident=recurso)
				aparcamiento.Num_Comentario = aparcamiento.Num_Comentario + 1

				aparcamiento.save()
				p = Comentario(Aparcamiento=aparcamiento, Texto=comentario)
				p.save()
		if aparcamiento.Num_Megusta == 0:
			Respuesta += 'Este aparcamiento no tiene puntuación, sé el primero en indicar que te gusta el aparcamiento <br><br>'
		else:
			Respuesta += '<li>Numero de Me Gusta: ' + str(aparcamiento.Num_Megusta) + '<br><br>'

		if aparcamiento.Num_Comentario == 0:
			Respuesta += 'Este aparcamiento no tiene comentarios, si está registrado, sé el primero en comentar, si no lo está, registrese para comentar <br><br>'
		else:
			Lista_Comentarios = Comentario.objects.all()
			Respuesta += '<li>Lista de comentarios: <br><ol>'
			for i in Lista_Comentarios:
				if aparcamiento == i.Aparcamiento:
					Respuesta += '<li>'
					Respuesta += i.Texto
					Respuesta += '<br><br>'

		c = Context({'Boton1': Logout,'Lista': Respuesta})#aqui tengo que meter las variables que qiero en la plantilla
		renderizado = Templates.render(c)
		return HttpResponse(renderizado)
		return HttpResponse(Respuesta)

	except ObjectDoesNotExist:
		return HttpResponse("Este identificador no corresponde con ningún aparcamiento")


@csrf_exempt
def usuario(request, peticion):

	Templates = get_template("usuario.html")
	Titulo_Pagina = ''
	if request.user.is_authenticated():
		Titulo_Pagina = "<span class='.t-center'> Usuario: " + str(request.user) + ". " + "<a href='/logout'>Logout</a></span>"
		Titulo_Pagina += form_titulo()
	today = datetime.datetime.today()
	user = User.objects.get(username=peticion)
	#Cuando me llega un POST al seleccionar un aparcamiento
	if request.method == "POST":
		usuario = User.objects.get(username=peticion)
		key = request.body.decode('utf-8').split('=')[0]
		if key == 'Titulo':
			Titulo = request.POST[key]
			try:
				usuario = Usuario.objects.get(Nombre=user)
				usuario.Titulo_pagina = Titulo
				usuario.Tamano = '15'
				usuario.save()
			except ObjectDoesNotExist:
				p = Usuario(Nombre=user, Titulo_pagina = Titulo, Tamano=15)
				p.save()
		elif key == 'Seleccion':
			nombre_aparcamiento = request.POST[key]
			lista_usuario = Fecha.objects.all()
			try:
				aparcamiento = Aparcamiento.objects.get(Nombre=nombre_aparcamiento)
				Encontrado = False
				for i in lista_usuario:
					#Si el aparcamiento ya lo tengo en la lista de seleccionados no lo añado
					if str(i.Usuario) == str(peticion):
						if nombre_aparcamiento == i.Aparcamiento.Nombre:
							Encontrado = True

				if Encontrado == False:
					p = Fecha(Aparcamiento=aparcamiento, Usuario=usuario, Fecha=today)
					p.save()
			except ObjectDoesNotExist:
				return('')
		elif key == 'Tamano':
			Tamano = request.POST['Tamano']
			Color = request.POST['Color']
			try:
				username = Usuario.objects.get(Nombre=user) #existe el usuario
			except:
				p = Usuario(Nombre=user) #Creo el usuario porque no existe
				p.save()
				username = Usuario.objects.get(Nombre=user)

			if Tamano == '':
				Tamano = '11';

			username.Tamano = Tamano
			username.Color = Color
			username.save()

	if request.user.is_authenticated():
		if peticion == str(request.user):
			Templates = get_template('usuario.html')
			try:
				Respuesta = Usuario.objects.get(Nombre=user).Titulo_pagina
			except ObjectDoesNotExist:
				Respuesta = 'Página principal de ' + str(user) + ': Página de ' + str(user) + '<br><br>'
		else:
			Respuesta = 'Página de ' + peticion + '<br>'
	else:
		Respuesta = 'Titulo de página: Pagina de ' + peticion + '<br>'
	Formulario = ''

	#Hago la lista de aparcamientos seleccionados por el usuario
	Respuesta += '<br> Lista de aparcamientos seleccionados por el Usuario ' + str(user) + '<br>'
	usuario = User.objects.get(username=peticion)
	lista_usuario = Fecha.objects.filter(Usuario=usuario)
	paginator = Paginator(lista_usuario,5)
	pag = request.GET.get('page')

	try:
		aparcamientos_selec = paginator.page(pag)
	except PageNotAnInteger:
		aparcamientos_selec = paginator.page(1)
	except:
		aparcamientos_selec = paginator.page(paginator.num_pages)
	for i in aparcamientos_selec:
		Formulario += '<br>'
		Formulario += '<li><a href="'  + i.Aparcamiento.Enlace + '">' + i.Aparcamiento.Nombre + '</a><br>'
		Formulario += 'Dirección: ' + i.Aparcamiento.Clase_vial + ' ' + i.Aparcamiento.Nombre_via + '<br>'
		Formulario += 'Fecha: ' + str(i.Fecha) + '<br>'
		Formulario += '<a href=http://localhost:1234/aparcamientos/'+ str(i.Aparcamiento.ident) + '>' + 'Más información</a><br>'
	Respuesta += Formulario + '<br><br>'


	#Hago la lista de todos los aparcamientos para poder seleccionarlos
	Respuesta2=''
	if request.user.is_authenticated():
		if str(request.user) == str(peticion):
			Respuesta2 = '<br><br><form action="" method="POST">'
			Respuesta2 += 'Modifica tamaño de letra <br><input type="text" name="Tamano"><br>'
			Respuesta2 += 'Modifica color <br><input type="color" name="Color"><br>'
			Respuesta2 += '<input type="submit" value="Modificar"><br><br>'
			Respuesta2 += '</form>'
			Respuesta2 += 'Lista de aparcamientos <br><br>'
	aparcamientos = Aparcamiento.objects.all()
	Lista_Aparcamientos = ''
	Boton = ''
	for i in aparcamientos:
		Respuesta2 += i.Nombre
		Respuesta2 += "<br>"
		if request.user.is_authenticated():
			if str(request.user) == str(peticion):
				Respuesta2 += '<form action="" method="POST">'
				Respuesta2 += '<button type="submit" name="Seleccion" value="' + i.Nombre + '">Selecciona el aparcamiento</button><br>'
				Respuesta2 += "<br>"
		else:
			Respuesta2 += '<br>'

	c = Context({'Lista': Respuesta, 'aparcamientos_selec': aparcamientos_selec, 'Lista2': Respuesta2, 'Titulo_Pagina': Titulo_Pagina})#aqui tengo que meter las variables que qiero en la plantilla
	renderizado = Templates.render(c)
	return HttpResponse(renderizado)

def Cambio (request):

	if request.user.is_authenticated():#si el usuario esta autenticado saco el tamaño y el color de sus variables
		user = User.objects.get(username=request.user)
		usuario = Usuario.objects.get(Nombre=user)
		Tamano = str(usuario.Tamano) + 'px'
		Color = usuario.Color
	else:#si el usuario no esta logeado pongo un tamaño y color por defecto
		Tamano = '13px'
		Color = '#FFFFFF'
	css = get_template('usuario.css')
	c = Context({'Tamano': Tamano, 'Color': Color})#aqui tengo que meter las variables que qiero en la plantilla
	renderizado = css.render(c)

	return HttpResponse(renderizado,content_type='text/css')

@csrf_exempt
def pag_ppal (request):

	Listado = Aparcamiento.objects.all()
	if len(Listado) == 0:
		get_data()

	if request.user.is_authenticated():
		Log = 'Página de ' + str(request.user) + '<br>'
		Log += "<span class='.t-center'> Usuario: " + str(request.user) + ". " + "<a href='/logout'>Logout</a></span>"
	else:
		Log = log()
	pie_pagina = footer()
	imagen_principal = '<img src="/static/img/banner.jpg"/>'
	Templates = get_template("index.html")

	#obtengo todos los aparcamientos
	Lista = lista_aparcamientos2()
	Respuesta = Log + Lista
	Todos = todos()
	About = red_about()
	Usuarios = Lista_Usuarios()
	Respuesta = Log + Lista + Usuarios
	#Hagoel botón para que solo se vean los accesibles
	Boton = '<br><form action="" method="POST">'
	Boton += '<button type="submit" name="Accesibles" value= "Accesibles">Aparcamientos Accesibles</button><br>'
	Boton += "<br>"

	Lista_Accesibles = ''
	if request.method == "POST":
		key = request.body.decode('utf-8').split('=')[0]
		value = request.body.decode('utf-8').split('=')[1]

		if key == 'Accesibles':
			Respuesta = Log + Usuarios + '<br>'
	#Ahora paso a hacer el listado de los aparcamientos accesibles
			aparcamientos_accesibles = Aparcamiento.objects.filter(Accesibilidad=1)
			if value == 'No':
				Lista_Accesibles += Lista
				Boton = '<br><form action="" method="POST">'
				Boton += '<button type="submit" name="Accesibles" value= "Accesibles">Aparcamientos Accesibles</button><br>'
				Boton += "<br>"
			else:
				Boton = '<br><form action="" method="POST">'
				Boton += '<button type="submit" name="Accesibles" value= "No">Aparcamientos más puntuados</button><br>'
				Boton += "<br>"
				#Si solo voy a mostrar los aparcamientos disponibles borro la lista y la hago con los accesibles
				Lista = 'Listado de los aparcamientos accesibles: '
				for i in aparcamientos_accesibles:
					Lista += '<li><a href="'  + i.Enlace + '">' + i.Nombre + '</a><br>'
					Lista += 'Dirección: ' + i.Clase_vial + ' ' + i.Nombre_via + '<br>'
					Lista += '<a href=http://localhost:1234/aparcamientos/'+ str(i.ident) + '>' + 'Más información</a><br>'
					Lista += "<br>"
		elif key == 'Todos':
			redirect(aparcamientos)

	Respuesta += Lista_Accesibles + Boton
	Respuesta += Todos
	Respuesta += About

	c = Context({'Log': Log, 'Lista': Lista, 'Usuarios': Usuarios,"Boton":Boton, 'footer': pie_pagina})#aqui tengo que meter las variables que qiero en la plantilla
	renderizado = Templates.render(c)
	return HttpResponse(renderizado)
	return HttpResponse(Respuesta)

def about(request):

	pie_pagina = footer()

	Templates = get_template("ayuda.html")
	cuerpo =  u'<span>Práctica Rubén Barrado Jiménez.</span><br><br>'
	cuerpo += u'<span>Funcionamiento de la practica:</span>'
	cuerpo += '<br><ul style="list-style-type: square"></br>'
	cuerpo += u'<li>Página principal (/): muestra las 5 aparcamientos mas puntuados y las paginas personales.</li>'
	cuerpo += u'<li>Pagina personal (/usuario): muestra las aparcamientos seleccionados por el usuario, un listado de los aparcamientos para poder seleccionarlos, un formulario para cambiar el título de la página y otro para cambiar el tema y tamaño</li>'
	cuerpo += u'<li>Pagina personal (/usuario/XML): muestra la pagina XML de los aparcamientos seleccionados.</li>'
	cuerpo += '<li>Aparcamientos (/aparcamientos): muestra todas los aparcamientos, los filtra por distrito.</li>'
	cuerpo += u'<li>Aparcamiento (/aparcamientos/id): cada aparcamiento tiene su página con información y la posibilidad de puntuarlos.</li>'
	cuerpo += u'<li>Pagina de ayuda (/about): muestra esta misma pagina, con ayuda sobre la pagina.</li>'


	c = Context({'cuerpo': cuerpo, 'footer': pie_pagina})#aqui tengo que meter las variables que qiero en la plantilla
	renderizado = Templates.render(c)
	return HttpResponse(renderizado)

def XML (request,peticion):

	user = User.objects.get(username=peticion)
	try:
		usuario = Usuario.objects.get(Nombre=user)
		lista_usuario = Fecha.objects.filter(Usuario=usuario.Nombre)
		xml = "<?xml version='1.0' encoding='UTF-8' ?>"
		xml += "<data><usuario name='" + str(request.user) +"'>"
		for i in lista_usuario:
			aparcamiento = i.Aparcamiento
			#xml += "<aparcamiento>"
			xml += '<nombre name="' + aparcamiento.Nombre + '">'
			xml += '<address>' + aparcamiento.Clase_vial + ' ' + aparcamiento.Nombre_via + ' ' + str(aparcamiento.Numero) + '</address>'
			xml += '<Localidad>' + aparcamiento.Localidad + '</Localidad>'
			xml += '<Provincia>' + aparcamiento.Provincia + '</Provincia>'
			xml += '<Codigo-Postal>' + str(aparcamiento.Cod_Postal) + '</Codigo-Postal>'
			xml += '<Barrio>' + aparcamiento.Barrio + '</Barrio>'
			xml += '<Distrito>' + aparcamiento.Distrito + '</Distrito>'
			xml += '<CoordX>' + str(aparcamiento.Coord_X) + '</CoordX>'
			xml += '<CoordY>' + str(aparcamiento.Coord_Y) + '</CoordY>'
			#xml += '<Enlace>' + aparcamiento.Enlace + '</Enlace>'
			xml += '<Descripccion>' + aparcamiento.Descripcion + '</Descripccion>'
			xml += '<Accesibilidad>' + str(aparcamiento.Accesibilidad) + '</Accesibilidad>'
			xml += '</nombre>'
		xml += '</usuario></data>'
	except ObjectDoesNotExist:
		print('')
	return HttpResponse(xml, content_type="text/xml")
