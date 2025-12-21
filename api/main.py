from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from firebase_admin import auth, db
import firebase  # 🔥 solo importa, no inicializa aquí

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== MODELOS =====

class Permisos(BaseModel):
    solicitudes: bool = True
    app: bool = False
    solicitudesAprobadas: bool = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    cobranza: str | None = ""
    permisos: Permisos


# ===== RUTA =====

@app.post("/crear-usuario")
def crear_usuario(user: UserCreate):
    try:
        # 1️⃣ Crear en Authentication
        user_record = auth.create_user(
            email=user.email,
            password=user.password,
            display_name=user.nombre,
        )

        uid = user_record.uid

        # 2️⃣ Guardar en Realtime Database
        db.reference(f"usuarios/{uid}").set({
            "activo":True,
            "nombre": user.nombre,
            "correo": user.email,
            "cobranza": user.cobranza or "",
            "permisos": {
                "solicitudes": user.permisos.solicitudes,
                "app": user.permisos.app,
                "solicitudesAprobadas": user.permisos.solicitudesAprobadas,
            }
        })

        return {
            "uid": uid,
            "mensaje": "Usuario creado en Authentication y Database"
        }

    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="El correo ya existe")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
