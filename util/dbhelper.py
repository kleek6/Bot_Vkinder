"""Работа с базой данных"""
import psycopg2
import logging

from util.config import DB_HOST, DB_USER, DB_PWD, DB_NAME
from util.helper import Frend, User

logger = logging.getLogger()


class Database:

    def __init__(self, host, user, password, database):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=database,
            port=5432
        )
        self.connection.autocommit = True

    # Создаем БД  пользователей, которые общаются с ботом
    def create_users(self, ):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                    id serial,
                    vk_id varchar(30) PRIMARY KEY
                    );"""
            )
        logger.info("[+] Table users created")

    # Добавляем пользователя
    def insert_user(self, user: User):
        with self.connection.cursor() as cursor:
            # check user exist
            cursor.execute(
                f"""SELECT id FROM users WHERE vk_id = '{user.id}';"""
            )
            id = cursor.fetchone()
            if id:
                logger.info(f"[-] User with vk_id={user.id} already exist")
                return
            # insert
            cursor.execute(
                f"""INSERT INTO users (vk_id) 
                VALUES ('{user.id}');"""
            )
            logger.info(f"[+] User with vk_id={user.id} inserted")

    # Cоздаем таблицу с просмотренными друзьями
    def create_frend(self, ):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS partners(
                    id serial,
                    vk_id varchar(30) PRIMARY KEY);
                    """
            )
        logger.info("Table partners created")

    # Добавляем просмотренного друга
    def insert_frend(self, partner: Frend):
        with self.connection.cursor() as cursor:
            # check partner exist
            cursor.execute(
                f"""SELECT id FROM partners WHERE vk_id = '{partner.id}';"""
            )
            id = cursor.fetchone()
            if id:
                logger.info(f"[-] Partner with vk_id={partner.id} already exist")
                return
            # insert
            cursor.execute(
                f"""INSERT INTO partners (vk_id) 
                VALUES ('{partner.id}');"""
            )
            logger.info(f"Partner with vk_id={partner.id} inserted")

    def create_users_frend(self, ):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users_partners(
                    user_vk_id varchar(30) NOT NULL REFERENCES users(vk_id),
                    partner_vk_id varchar(30) NOT NULL REFERENCES partners(vk_id));"""
            )
        logger.info("[+] Table partners created")

    # Добавляем просмотренных друзей пользователем
    def insert_user_frend(self, user_vk_id, partner_vk_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO users_partners (user_vk_id, partner_vk_id) 
                VALUES ('{user_vk_id}', '{partner_vk_id}');"""
            )
            logger.info(f"User with vk_id={user_vk_id} and partner with vk_id={partner_vk_id} inserted")

    def delete_all_user_partners(self, user_vk_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""DELETE FROM users_partners WHERE user_vk_id = '{user_vk_id}';"""
            )

    # Проверка, показывали ли мы партнера пользователю ранее
    def check_is_new_frend(self, user_id, partner_id) -> bool:
        with self.connection.cursor() as cursor:
            # check partner exist
            cursor.execute(
                f"""SELECT * FROM users_partners WHERE user_vk_id = '{user_id}' AND partner_vk_id = '{partner_id}';"""
            )
            # Партнер старый
            if cursor.fetchone():
                logger.info(f"[INFO] user with id = {partner_id} was already showed previously")
                return False
            # Партнер новый
            return True


db = Database(
    user=DB_USER,
    password=DB_PWD,
    host=DB_HOST,
    database=DB_NAME
)


def init_db():
    # Cоздать таблицу users
    db.create_users()
    # Создать табилцу partners
    db.create_frend()
    # Cоздать таблицу users_partners
    db.create_users_frend()


def main():
    init_db()


if __name__ == '__main__':
    main()
