import mysql.connector
from dotenv import dotenv_values
from pathlib import Path

APP_PATH = Path(__file__).parent.absolute()
DOT_ENV = dotenv_values(APP_PATH.parent.joinpath(".env"))
CREATE_DB = "CREATE DATABASE IF NOT EXISTS  {} "
SELECT = "SELECT rnd_key, url_str  FROM `short_links` WHERE rnd_key= '{}'; "
INSERT = "INSERT  INTO  `short_links` (rnd_key, url_str) VALUES ('{}', '{}');"

DB_VARS = {'host': DOT_ENV['DB_HOST'], 'user': DOT_ENV['DB_USERNAME'],
           'passwd': DOT_ENV['DB_PASSWORD']}

def mysql_db_create_tbl():
    DB_VARS.update({'db': DOT_ENV['DB_DATABASE']})
    cur = mysql.connector.connect(**DB_VARS)
    with open(APP_PATH.joinpath('short_links.sql')) as f:
        cur.cursor().execute(f.read().replace('\n', ''))
    cur.commit()
    cur.close()


def create_db():
    cur = mysql.connector.connect(**DB_VARS)
    cur.cursor().execute(CREATE_DB.format(DOT_ENV['DB_DATABASE']))
    cur.commit()
    cur.close()


def insert_data(key, val):
    cur = mysql.connector.connect(**DB_VARS)
    cur.cursor().execute(INSERT.format(key, val))
    cur.commit()
    cur.close()


def get_key_from_db(key):
    connect = mysql.connector.connect(**DB_VARS)
    cur = connect.cursor()
    cur.execute(SELECT.format(key))
    ret = {rnd_key: url_str for rnd_key, url_str in cur.fetchall()}
    cur.close()
    return ret
