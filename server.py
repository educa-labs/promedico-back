from flask import Flask
from flask import Response, send_from_directory, render_template, request
from db import DB
import json

app = Flask(__name__)
"""
Ver tema del login

"""

@app.route("/")
def test():
    return render_template("index.html")


@app.route("/signup", methods=['POST'])
def signup():
    db = DB()
    jeison = request.get_json(force = True)
    ret = db.nuevoUsuario(jeison)
    db.conn.close()

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/login", methods=["POST"])
def login():
    db = DB()
    jeison = request.get_json(force = True)
    ret = db.login(jeison)
    db.conn.close()

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/get_actividades", methods=["POST"])
def get_actividades():
    db = DB()
    jeison = request.get_json(force = True)
    ret = db.getActividades(jeison)
    db.conn.close()

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/nueva_actividad", methods=["POST"])
def nueva_actividad():
    db = DB()
    jeison = request.get_json(force = True)
    ret = db.addActividad(jeison)
    db.conn.close()

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/removeActividad", methods=["POST"])
def deleteActividad():
    db = DB()
    jeison = request.get_json(force = True)
    ret = db.removeActividad(jeison)
    db.conn.close()

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp    





"""
Hardcodeo
"""
@app.route("/nueva_clinica", methods = ["POST"])
def nuevaClinica():
    db = DB()
    jeison = request.get_json(force = True)
    titulo = jeison["nombre"]
    db.cur.execute("INSERT INTO Clinica(title) VALUES(%s);",(titulo,))
    db.conn.commit()
    db.conn.close()

    return "Clinica agregada"

@app.route("/nuevo_departamento", methods = ["POST"])
def nuevoDepartamento():
    db = DB()
    jeison = request.get_json(force = True)
    id_clinica = jeison["id_clinica"]
    titulo = jeison["nombre"]
    db.cur.execute("INSERT INTO Departamentos(title,id_clinica,status) VALUES(%s,%s,%s);",(titulo,id_clinica,1))
    db.conn.commit()
    db.conn.close()

    return "Departamento agregado"


@app.route("/getclinicas")
def getClinicas():
    db = DB()
    ret = db.getClinicas()

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/getdeptos/<id_clinica>")
def getDeptos(id_clinica):
    id_clinica = int(id_clinica)
    db = DB()
    ret = db.getDeptos(id_clinica)

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/newtipo", methods = ["POST"])
def newtipo():
    jeison = request.get_json(force = True)
    tupla = (jeison["titulo"], jeison["value"])
    db = DB()
    db.cur.execute("INSERT INTO Tipos (titulo, value) VALUES(%s,%s);", tupla)
    db.conn.commit()
    
    ret = json.dumps({"status":1})

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/newtag", methods = ["POST"])
def newtag():
    jeison = request.get_json(force = True)
    tupla = (jeison["titulo"], jeison["value"], jeison["descripcion"], jeison["meta"], jeison["color"])
    db = DB()
    db.cur.execute("INSERT INTO Tags (title, value, descripcion, meta, color) VALUES(%s,%s,%s,%s,%s);", tupla)
    db.conn.commit()

    ret = json.dumps({"status":1})

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/gettipos", methods = ["GET"])
def gettipos():
    db = DB()
    ret = db.getTipos()

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    
@app.route("/gettags", methods = ["GET"])
def gettags():
    db = DB()
    ret = db.getTags()

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/getTagsInfo", methods = ["POST"])
def gettagsinfo():
    db = DB()
    jeison = request.get_json(force = True)
    ret = db.getTagsInfo(jeison)

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/getAllUsers/<token>", methods=["GET"])
def getAllUsers(token):
    db = DB()
    jeison = {"token": token}
    ret = db.getAllUsers(jeison)

    resp = Response(json.dumps(ret), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp    


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)







