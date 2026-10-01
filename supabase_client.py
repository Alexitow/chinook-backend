import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # En local lee .env; en Render se usan las variables del panel

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_KEY en las variables de entorno")

supabase: Client = create_client(url, key)
