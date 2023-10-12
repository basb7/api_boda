from typing import Union
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from DB.database_supabase import *

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(description="API para registrar los asistentes a la boda")

origins = ["invitacion-boda-byj.netlify.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Asistente(BaseModel):
    codigo: Union[str, int]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/list_all")
def listAssitant():
    list = get_all()
    return list


@app.post("/check_confirmed")
def test(asistente: Asistente):
    code_user = int(asistente.codigo)
    responseApi = check_confirmed(code_user)
    return responseApi
    """ code_user = int(asistente.codigo)
    check_user_confirmed = check_confirmed(code_user)

    if not check_user_confirmed:
        is_confirmed = get(code_user)

        if not is_confirmed:
            response = {
                "status": "error",
                "user": "No se encontro el usuario",
                "code": code_user,
                "message": "¡Código ingresado no es válido!",
            }
            return JSONResponse(content=response, status_code=404)

        response = {
            "status": "ok",
            "user": "{}".format(is_confirmed.names),
            "code": is_confirmed.code,
            "message": "¡Nos alegra saber que quieres compartir con nosotros este gran día, tu confirmación ha sido registrada!",
        }
        return JSONResponse(content=response, status_code=200)
    else:
        response = {
            "status": "ok",
            "user": "{}".format(
                check_user_confirmed.names
            ),
            "code": check_user_confirmed.code,
            "message": "¡Sabemos que estás ansioso como nosotros, tu confirmación ya fue registrada!",
        }
        return JSONResponse(content=response, status_code=200) """
