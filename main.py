#API REST: Interfaz de programacion de aplicaciones para compartir recursos

from typing import List, Optional
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

#Inicializamos una variable donde tendrá todas las caracteristicas de una API REST

app = FastAPI()

#Acá definimos el modelo

class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

#Simulamos una db

db = []

#CRUD: Read (Lectura) GET ALL: Leeremos todos los cursos que haya en la db

@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return db

#CRUD: Create (Escribir) POST: Agregaremos un nuevo recurso a nuestra base de datos

@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) # Usamos uuid.uuid4() para que genere un Id
    db.append(curso)
    return curso

# CRUD: Read (Lectura) GET (individual): Leeremos el curso que coincida con el ID que pidamos

@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in db if curso.id == curso_id), None) # Con next tomamos la primer coincidencia del array
    if curso is None:
        raise FastAPI.HTTPException (status_code=404, detail="Curso no encontrado")
    return curso

#CRUD: Update (Actualizar/Modificar) PUT: Modificaremos un recurso que coincida con el ID que mandemos

@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in db if curso.id == curso_id), None) 
    if curso is None:
        raise FastAPI.HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = db.index(curso) # Buscamos el indice exacto donde está el curso en nuestra lista/db
    db[index] = curso_actualizado
    return curso_actualizado

#CRUD: Delete (Eliminar) 

@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in db if curso.id == curso_id), None) # Con next tomamos la primer coincidencia del array
    if curso is None:
        raise FastAPI.HTTPException(status_code=404, detail="Curso no encontrado")
    db.remove(curso)
    return curso
