from os import environ
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()


class Config:
    # Connection String
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    JWT_SECRET_KEY = environ.get("SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
