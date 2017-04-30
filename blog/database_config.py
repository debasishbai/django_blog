import psycopg2
import urlparse
import os


def server_db():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
    cur = conn.cursor()
    return cur


def local_db():
    conn = psycopg2.connect(host="", user="", password="", dbname="")
    cur = conn.cursor()
    return cur
