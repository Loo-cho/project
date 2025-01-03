import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mariadb+mariadbconnector://root@127.0.0.1:3306/progetto'
