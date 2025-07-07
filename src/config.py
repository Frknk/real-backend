#from dotenv import load_dotenv
import os

#load_dotenv()

# SECRET_KEY = "frank123"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN")
DB_URL = os.getenv("DB_URL")
