from entities.Ocupancy import Occupancy
from dotenv import load_dotenv
import traceback
import psycopg2
import os

from entities.Permission import Permission


class PermissionDAO:
    def __init__(self):
        load_dotenv()
        self.USER = os.getenv("USER")
        self.PASSWORD = os.getenv("PASSWORD")
        self.HOST = os.getenv("HOST")
        self.PORT = os.getenv("PORT")
        self.DATABASE = os.getenv("DATABASE")

    def openConnection(self):
        return psycopg2.connect(user=self.USER, password=self.PASSWORD,
                                host=self.HOST, port=self.PORT, database=self.DATABASE)


def insertPermission(permission):
    try:
        connection = PermissionDAO().openConnection()
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO permission (beginning_date_time, "
                       f"ending_date_time, professor_user_id, user_id, classroom_id ) "
                       f"VALUES ('{permission.beginning_time}', '{permission.ending_time}', "
                       f"{permission.professor}, {permission.user}, {permission.classroom})")
        connection.commit()
        if cursor.rowcount > 0:
            print("Success insert!")
    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
    finally:
        if connection:
            cursor.close()
        connection.close()


def getOnePermission(id):
    permission = None
    try:
        connection = PermissionDAO().openConnection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM permission WHERE id = '{id}'")
        register = cursor.fetchone()
        if register:
            permission = Permission(register[0], register[1], register[2], register[3], register[4], register[5])
    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
    finally:
        if connection:
            cursor.close()
            connection.close()
        return permission


def getAllPermissions():
    permissions = []
    try:
        connection = PermissionDAO().openConnection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM permission")
        registers = cursor.fetchall()
        for register in registers:
            permission = Permission(register[0], register[1], register[2], register[3], register[4], register[5])
            permissions.append(permission)
    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
    finally:
        if connection:
            cursor.close()
        connection.close()
        return permissions


def updatePermission(id, ending_date_time):
    try:
        connection = PermissionDAO().openConnection()
        cursor = connection.cursor()
        cursor.execute("UPDATE permission SET ending_date_time = %s WHERE id = %s",
                       (ending_date_time, id))

        connection.commit()
        if cursor.rowcount > 0:
            print("Success update!")
    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
    finally:
        if connection:
            cursor.close()
        connection.close()


def deletePermission(id):
    try:
        connection = PermissionDAO().openConnection()
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM permission WHERE id= '{id}'")
        connection.commit()
        if cursor.rowcount > 0:
            print("Success delete!")
    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
    finally:
        if connection:
            cursor.close()
        connection.close()