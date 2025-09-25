import dotenv

dotenv.load_dotenv()
import os


# Usando el hostname del contenedor en lugar de localhost
DB_HOST = os.getenv("DB_HOST", "localhost") 
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "scrapper")
DB_PASS = os.getenv("DB_PASS", "6vT9pQ2sXz1L")  # Contraseña según docker-compose.yml
DB_NAME = os.getenv("DB_NAME", "repuestosDB")  # Nombre de BD según docker-compose.yml

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
