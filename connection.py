import mysql.connector

import logging
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime

logging.basicConfig(filename='example.log',
                    level=logging.DEBUG, format='%(asctime)s %(message)s')

TABLES = {}
TABLES['users'] = (
    "CREATE TABLE `users` ("
    "  `user_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `first_name` varchar(100) NULL,"
    "  `email` varchar(100) NOT NULL,"
    "  `points` FLOAT NOT NULL,"
    "  `probability` VARCHAR(6000) NOT NULL,"
    "  `created_at` DATETIME NOT NULL,"
    "  `updated_at` DATETIME NOT NULL,"
    "  PRIMARY KEY (`user_id`)"
    ") ENGINE=InnoDB")


TABLES['luckydraws'] = (
    "CREATE TABLE `luckydraws` ("
    "  `luckydraw_id` bigint NOT NULL AUTO_INCREMENT,"
    "  `winner_id` int(11) NOT NULL,"
    "  `created_at` DATETIME NOT NULL,"
    "  `updated_at` DATETIME NOT NULL,"
    "  PRIMARY KEY (`luckydraw_id`),"
    "  CONSTRAINT `luckydraws_ibfk_1` FOREIGN KEY (`winner_id`) "
    "     REFERENCES `users` (`user_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")


class MySQLDatabase:
    def __init__(self):
        self.con = None
        self.cur = None

    def connect(self):
        config = {
            'user': 'root',
            'password': 'Test1234',
            'host': '192.168.64.3',
            'database': 'luckydraw501',
            'raise_on_warnings': True,
        }

        try:
            self.con = mysql.connector.connect(**config)
            self.cur = self.con.cursor()

            if self.con.is_connected():
                db_Info = self.con.get_server_info()
                # print("Connected to MySQL Server version ", db_Info)

        except Error as e:
            print("Error while connecting to MySQL", e)

    def close(self):
        self.cur.close()
        self.con.close()

    def add_user(self, first_name, email, points, probability):
        try:
            logging.info('Add user ' + first_name + "," +
                         email + "," + str(points) + "," + str(probability))
            self.connect()
            now = datetime.now()
            add_user_statement = ('INSERT INTO users ( first_name, email, points, probability, created_at, updated_at) '
                                  'VALUES (%s, %s, %s, %s, %s, %s)')
            self.cur.execute(add_user_statement,
                             (first_name, email, points, probability, now.strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%d %H:%M:%S')))
            self.con.commit()
            self.close()
        except mysql.connector.Error as err:
            logging.exception('Error in Add luckydrawrecord ' + first_name)
            print("Add user Something went wrong: {}".format(err))

    def update_user(self, user_id, first_name, email, points, probability):
        try:
            self.connect()
            print(user_id, first_name, email, points, probability)
            update_user_statement = ('UPDATE users (user_id, first_name, email, points, probability,updated_at) '
                                     'SET first_name = %s, email = %s, points = %d, probability = %d'
                                     'WHERE user_id = %s')
            self.cur.execute(update_user_statement,
                             (first_name, email, points, probability, user_id))
            self.close()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

    def retrieve_user(self, first_name):
        try:
            self.connect()
            get_user_statement = (
                "SELECT * FROM users WHERE first_name LIKE %s ORDER BY created_at DESC")
            self.cur.execute(get_user_statement, (first_name,))
            user = self.cur.fetchone()
            return user
        except mysql.connector.Error as err:
            print("Retrieve user Something went wrong: {}".format(err))

    def add_luckydrawrecord(self, first_name):
        try:

            logging.info('Add luckydrawrecord ' + first_name)
            self.connect()
            get_user_statement = (
                "SELECT * FROM users WHERE first_name LIKE %s ORDER BY created_at DESC LIMIT 0, 1")
            self.cur.execute(get_user_statement, (first_name,))
            winner_id = self.cur.fetchone()[0]
            print(winner_id)
            now = datetime.now()
            add_ld_record_statement = ('INSERT INTO luckydraws (winner_id,created_at,updated_at) '
                                       'VALUES (%s, %s, %s)')
            self.cur.execute(add_ld_record_statement,
                             (winner_id, now.strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%d %H:%M:%S')))
            self.con.commit()
            self.close()
        except mysql.connector.Error as err:
            logging.exception('Error in Add luckydrawrecord ' + first_name)
            print("Add luckydraw Something went wrong: {}".format(err))

    def create_database(self):
        # CREATE DATABASE
        try:
            self.cur.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format('luckydraw501'))

        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

        # CREATE TABLES
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cur.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")


def main():
    db = MySQLDatabase()
    db.connect()
    db.create_database()
    db.close()


if __name__ == '__main__':
    main()
