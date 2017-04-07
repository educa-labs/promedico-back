**Signup**
----
  Returns status of signup.

* **URL**

  /signup `POST`

* **Data Params**

  **JSON** : ```{nombre : [string],
  ocupacion: [string],
  password: [string],
  mail: [string], 
  clinica: [string], 
  departamento: [string]
  }``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** ` { status : 1 } `
   
----
    
**Login**
----
  Returns all user activities

* **URL**

  /login `POST`

* **Data Params**

  **JSON** : ```{mail: [string], pass: [string]}``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** ```{ status : 1, token: "h82h38f8h38dhaoszxcw", nombre: "Juanito Perez", ocupacion: "Medico", mail: "juan@per.ez" } ```

----
    
**Get Actividades**
----
  Returns all activities and its tags.

* **URL**

  /get_actividades `POST`

* **Data Params**

  **JSON** : ```{token: [string]}``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ titulo : "Conferencia de prensa
    ", "fecha": [datetime], fecha_registro: [datetime], tipo: "Docencia", tags: list,  } `
    
    
----
    
**Nueva Actividad**
----
  Returns status if all parameters are ok.

* **URL**

  /nueva_actividad `POST`

* **Data Params**

  **JSON** : ```{token: [string], fecha: datetime, titulo: [string], tipo: [string], reflexion: [string] }``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ status : 1 } `
    
----
    
**Nueva Clinica**
----
  Adds a Clinica to the base de datos.

* **URL**

  /nueva_actividad `POST`

* **Data Params**

  **JSON** : ```{ nombre : [string] }``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ status : 1 } `
    
----
    
**Nuevo Departamento**
----
  Adds a Departamento to the base de datos.

* **URL**

  /nuevo_departamento `POST`

* **Data Params**

  **JSON** : ```{ nombre : [string] }``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ status : 1 } `
    
 ----
    
**Get Clinicas**
----
  Gets all the Clincas that are in the DB.

* **URL**

  /getclinicas `GET`

* **Data Params**

  **JSON** : ```None``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ clinicas : [ {title: "Alemana", id: 1}, {title: "Las Condes", id: 2} ] } `   

----
    
**Get Departamentos**
----
  Gets all the Departamentos that belong to a Clinica.

* **URL**

  /getdepartamentos/:id_clinica `GET`

* **Data Params**

  **id_clinica** : ```Id de la Clinica que se consulta``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ departamentos : [ {title: "Oncologia", id: 5}, {title: "Traumatologia", id: 7} ] } `
    
----
    
**Agregar Tipo**
----
  Adds a Tipo to the table Tipos.

* **URL**

  /newtipo `POST`

* **Data Params**

  **JSON** : ```{ titulo: [string], value: [int] }``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ status : 1 } `
    
----
    
**Agregar Tag**
----
  Adds a Tipo to the table Tipos.

* **URL**

  /newtag `POST`

* **Data Params**

  **JSON** : ```{ titulo: [string], value: [int] }``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ status : 1 } `
    
----
    
**Get all Tipos**
----
  Gets all the available tipos.

* **URL**

  /gettipos `GET`

* **Data Params**

  **JSON** : ```None``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ tipos : [{id: 3, titulo: "", "value": 10}] } `
    
----
    
**Get all Tags**
----
  Gets all the available tags.

* **URL**

  /gettags `GET`

* **Data Params**

  **JSON** : ```None``` 

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ tags : [{id: 3, titulo: "", "value": 10}] } `
