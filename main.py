from typing import Union
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from DB.database import *

from fastapi import FastAPI

app = FastAPI(
    description='API para registrar los asistentes a la boda'
    )

create_tables()

class Asistente(BaseModel):
    codigo: Union[str, int]


lista_asistentes: list[Asistente] = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/listar_asistentes")
def listar_asistentes():
    try:
        response = {
            "status": "ok",
            "asistentes": lista_asistentes,
            "total": len(lista_asistentes)
        }
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        response = {
            "status": "error al listar los asistentes",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=500)


@app.post("/registro_asistente")
def registro_asistentes(asistente: Asistente):
    try:
        lista_asistentes.append(asistente.model_dump())
        response = {
            "status": "created",
            "asistente": asistente.model_dump()
        }
        return JSONResponse(content=response, status_code=201)
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=response, status_code=500)

  
@app.post("/test")
def test(asistente: Asistente):
    code_user = int(asistente.codigo)
    check_user_confirmed = check_confirmed(code_user)

    if not check_user_confirmed:
        is_confirmed = get(code_user)

        if not is_confirmed:
            response = {
            "status": "error",
            "code": code_user,
            "message": "Codigo ingresado no es valido!",
        }
            return JSONResponse(content=response, status_code=404)
        
        response = {
            "status": "ok",
            "user": '{} {}'.format(is_confirmed.name , is_confirmed.lastname),
            "code": is_confirmed.code,
            "message": "Nos alegra saber que quieres compartir con nosotros este gran dia, tu confirmación ha Sido registrada!",
        }
        return JSONResponse(content=response, status_code=200)
    else:
        response = {
            "status": "ok",
            "user": '{} {}'.format(check_user_confirmed.name , check_user_confirmed.lastname),
            "code": check_user_confirmed.code,
            "message": "Se que estas ancioso como nosotros, tu confirmacion ya fue registrada!.",
        }
        return JSONResponse(content=response, status_code=200)
    

@app.get("/create")
def createAssitant():
    user = create()
    print(user)
    return 'ok'