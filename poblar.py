import requests
import sys
import json
# Url API global
api = 'http://api.promedico.cl'
while True:
	# Imprimir menu
	print("1. Crear una clínica")
	print("2. Crear un departamento")
	print("3. Crear un tipo de actividad")
	print("4. crear un tag")
	print("5. Ver Clinicas")
	print("6. Ver departamentos")
	print("7. Volver admin")
	print("\n")
	# Preguntar eleccion al usuario
	eleccion = input("¿Qué deseas hacer?: ")
	if eleccion == "1":
		""" Para crear una clinica """
		nombre_clinica = input("Ingrese nombre: ")
		requests.post(api + "/nueva_clinica", json={"nombre": nombre_clinica})
	elif eleccion == "2":
		""" Crear un departamento """
		nombre_departamento = input("Ingrese nombre: ")
		getClinicas = requests.get(api + "/getclinicas")
		# Imprimir el json recibido de las clinicas
		for elemento in getClinicas:
			print(elemento)
		id_clinica = input("Ingrese el id de la clínica: ")
		requests.post(api + "/nuevo_departamento",
					  json={"nombre": nombre_departamento, "id_clinica": id_clinica})
	elif eleccion == "3":
		""" Crear un tipo de actividad """
		nombre_tipo = input("Ingrese nombre del tipo: ")
		valor = input("Ingrese valor del tipo: ")
		requests.post(api + "/newtipo",
					  json={"titulo": nombre_tipo, "value": valor})
	elif eleccion == "4":
		""" Crear un tag """
		titulo_tag = input("Ingrese titulo del tag: ")
		color_tag = input("Ingrese el color del tag: ")
		valor_tag = input("Ingrese el valor del tag: ")
		descripcion_tag = input("Ingrese una descripcion del tag: ")
		meta_tag = input("Ingrese el puntaje meta del tag: ")
		requests.post(api + "/newtag", json={"titulo": titulo_tag, "color": color_tag,
											 "value": valor_tag, "descripcion": descripcion_tag, "meta": meta_tag})
	elif eleccion == "5":
		""" Ver clinicas """
		variable = requests.get(api + "/getclinicas")
		for i in variable:
			print(i)
	elif eleccion == "6":
		""" Ver departamentos de cada clinica """
		id_clinica = input("Ingrese id de la clinica: ")
		variable = requests.get(api + "/getdeptos/" + id_clinica)
		for i in variable:
			print(i)
	elif eleccion == "7":
		""" Convertir usuario en administrador de un departamento """
		id_depto = input("Ingrese el id del depto: ")
		mail_usuario = input("Ingrese el mail del usuario: ")
		print(requests.post(api + "/make_admin",
							json={"mail": mail_usuario, "id_depto": id_depto}).text)


""" 
EJEMPLOS DE REQUEST PARA POBLAR BASE DE DATOS
"""
# nueva_clinica = requests.post("http://api.promedico.cl/nueva_clinica", json={"nombre": "Clínica las lilas"})
# nuevo_departamento = requests.post("http://api.promedico.cl/nuevo_departamento", json={"nombre": "Departamento clinica alemana", "id_clinica": 2})
# getTags = requests.get("http://educalabs.cl:5000/gettags")
# newTipo = requests.post("http://educalabs.cl:5000/newtipo", json={"titulo": "Docencia", "value": 20})
# getTipos = requests.get("http://educalabs.cl:5000/gettipos")
# getActividades = requests.post("http://educalabs.cl:5000/getactividades", json={"token": ""})

# newTag = requests.post("http://educalabs.cl:5000/newtag", json = {"titulo": "Tag numero 1", "color": "seguridad","value": 5, "descripcion": "Esto es una descripcion", "meta": 50})
# newTag = requests.post("http://educalabs.cl:5000/newtag", json = {"titulo": "Tag numero 2", "color": "confianza","value": 5, "descripcion": "Esto es una descripcion", "meta": 50})
# newTag = requests.post("http://api.promedico.cl/newtag", json = {"titulo": "Tag", "color": "comunicacion","value": 5, "descripcion": "Esto es una descripcion", "meta": 80})

# getClinicas = requests.get("http://api.promedico.cl/getclinicas")

# print(getClinicas.json())
