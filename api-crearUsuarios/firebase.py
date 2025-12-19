import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebase-key.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://dbtransactionprueba-default-rtdb.firebaseio.com"
})
