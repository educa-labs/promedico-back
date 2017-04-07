import requests
import sys

"""
Ejemplos de requests Clinicapp
"""



nueva_clinica = requests.post("http://educalabs.cl:5000/nueva_clinica", json={"nombre": "Las Condes"})
nuevo_departamento = requests.post("http://educalabs.cl:5000/nuevo_departamento", json={"nombre": "Pediatria", "id_clinica": 2})
newTag = requests.post("http://educalabs.cl:5000/newtag", json = {"titulo": "Comunicacion y trabajo en equipo", "value": 5, "descripcion": "Esto es una descripcion", "meta": 50})
getTags = requests.get("http://educalabs.cl:5000/gettags")
newTipo = requests.post("http://educalabs.cl:5000/newtipo", json={"titulo": "Docencia", "value": 20})
getTipos = requests.get("http://educalabs.cl:5000/gettipos")
# getActividades = requests.post("http://educalabs.cl:5000/getactividades", json={"token": ""})

print(getTipos.json())