import os

import dotenv


BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__))
)

dotenv.load_dotenv(os.path.join(BASE_DIR, ".env"))

SQLITE_FILE_PATH = os.getenv("SQLITE_FILE_PATH")
SECRET_KEY = os.getenv("SECRET_KEY")
