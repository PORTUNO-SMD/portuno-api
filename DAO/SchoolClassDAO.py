from entities.SchoolClass import SchoolClass
from dotenv import load_dotenv
import traceback
import psycopg2
import os


class SchoolClassDao:
    def __init__(self):
        load_dotenv()  # Load the variables from .env file
        self.USER = os.getenv("USER")
        self.PASSWORD = os.getenv("PASSWORD")
        self.HOST = os.getenv("HOST")
        self.PORT = os.getenv("PORT")
        self.DATABASE = os.getenv("DATABASE")

    def openConnection(self):
        return psycopg2.connect(user=self.USER, password=self.PASSWORD,
                                host=self.HOST, port=self.PORT, database=self.DATABASE)


def insertSchoolClass(schoolClass):
    try:
        connection = SchoolClassDao().openConnection()
        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO class (day_week, subject, start_hour, finish_hour) "
                       f"VALUES ('{schoolClass.day_week}', '{schoolClass.subject}', "
                       f"'{schoolClass.start_hour}', '{schoolClass.finish_hour}')")
        connection.commit()
        if cursor.rowcount > 0:
            print("Success insert!")
    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
    finally:
        if connection:
            cursor.close()
        connection.close()


def getOneSchoolClass(id):
    schoolClass = None
    try:
        connection = SchoolClassDao().openConnection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM class WHERE id = '{id}'")
        register = cursor.fetchone()
        if register:
            schoolClass = SchoolClass(register[0], register[1], register[2], register[3].strftime("%H:%M:%S"),
                                      register[4].strftime("%H:%M:%S"))
    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
    finally:
        if connection:
            cursor.close()
            connection.close()
        return schoolClass


def getAllSchoolClasses():
    schoolClasses = []
    try:
        connection = SchoolClassDao().openConnection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM class")
        registers = cursor.fetchall()
        for register in registers:
            schoolClasses.append(SchoolClass(register[0], register[1], register[2], register[3].strftime("%H:%M:%S"),
                                             register[4].strftime("%H:%M:%S")))
    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
    finally:
        if connection:
            cursor.close()
        connection.close()
        return schoolClasses


def updateSchoolClass(id, newSchoolClass):
    try:
        connection = SchoolClassDao().openConnection()
        cursor = connection.cursor()

        cursor.execute(f"UPDATE class SET "
                       f"day_week = '{newSchoolClass.day_week}', "
                       f"subject = '{newSchoolClass.subject}', "
                       f"start_hour = '{newSchoolClass.start_hour}', "
                       f"finish_hour = '{newSchoolClass.finish_hour}' "
                       f"WHERE id = '{id}'")

        connection.commit()
        if cursor.rowcount > 0:
            print("Success update!")
    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
    finally:
        if connection:
            cursor.close()
        connection.close()


def deleteSchoolClass(id):
    try:
        connection = SchoolClassDao().openConnection()
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM class WHERE id= '{id}'")
        connection.commit()
        if cursor.rowcount > 0:
            print("Success delete!")
    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
    finally:
        if connection:
            cursor.close()
        connection.close()
