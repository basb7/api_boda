
import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def create_asistents(_names: str, _telephone: str, _cant_tikets: int, _code: int):
    try:
        data, count = supabase.table('Asistentes').insert({
                "names": _names,
                "telephone": _telephone,
                "cant_tikets": _cant_tikets,
                "code": _code,
                "confirmed": False,
                "confirmation_date": None
            }).execute()
        
        print(data)
        print(count)
        return data
    except Exception as e:
        print(e)
        return False


def check_code(_code: int):
    try:
        # confirmar que el codigo existe
        data, count = supabase.table('Asistentes').select('*').eq('code', _code).execute()

        if len(data[1]) == 0:
            return False
        
        return True

    except Exception as e:
        print(e)
        return False
    
def check_confirmed(_code: int):
    try:
        is_valid_code = check_code(_code)

        if is_valid_code is False:
            response = {
                "status": "error",
                "user": "No se encontro el usuario",
                "code": _code,
                "message": "¡Código ingresado no es válido!",
            }
            return response
        
        # confirmar si ya esta registrado
        data, count = supabase.table('Asistentes').select('*').match({"code": _code}).execute()

        if len(data[1]) > 0:
            user = data[1][0]

            if user['confirmed']:              
                response = {
                    "status": "ok",
                    "user": "{}".format(
                        user['names']
                    ),
                    "code": user['code'],
                    "message": "¡Sabemos que estás ansioso como nosotros, tu confirmación ya fue registrada!",
                }
                return response
            
            # Actualizar confirmacion a true
            data, count = supabase.table('Asistentes').update({"confirmed": True, "confirmation_date": '{}'.format(datetime.now())}).match({"code": _code}).execute()
            if len(data[1]) > 0:
                response = {
                    "status": "ok",
                    "user": "{}".format(user['names']),
                    "code": user['code'],
                    "message": "¡Nos alegra saber que quieres compartir con nosotros este gran día, tu confirmación ha sido registrada!",
                }
                return response
        else:
            response = {
                "status": "error",
                "message": "Error en la consulta db"
            }

    except Exception as e:
        print(e)
        return False
    

def get_all():
    try:
        data, count = supabase.table('Asistentes').select('*').execute()
        print(data)
        return data[1]
    except Exception as e:
        print(e)
        return False
    
print(check_confirmed(123))