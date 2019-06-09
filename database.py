import sys
import pymysql.cursors
from project3 import debug

conn = None
database = None
user = None
password = None


def make_connection(database, user, password):
    global conn
    conn = pymysql.connect(host='localhost',
                           user=user,
                           password=password,
                           db=database,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


def insert_into(stmt, line_num=None):
    global conn
    if conn is None:
        get_connection()
    #print(line_num, stmt)
    with conn.cursor() as cursor:
        cursor.execute(stmt)
    conn.commit()


def create_tables(database, user, password, file):
    f = open(file, 'r')
    global conn
    with conn.cursor() as cursor:
        stmt = ""
        for line in f:
            stmt += line[:-1]
            if ';' in stmt:
                cursor.execute(stmt)
                stmt = ''
    conn.commit()
    f.close()


def read_info(file_name):
    with open(file_name, "r") as f:
        d = f.readline().split(" ")[-1].strip()
        u = f.readline().split(" ")[-1].strip()
        p = f.readline().split(" ")[-1].strip()
        return d, u, ''


def get_connection():
    global conn, database, user, password
    if len(sys.argv) == 1:
        fileName = "/Users/JeevanBasnet/PycharmProjects/Project3/credentials.txt"
    else:
        fileName = sys.argv[1]
    database, user, password = read_info(fileName)

    make_connection(database, user, password)
    return database, user, password


@debug(debug=True)
def get_sql_statement_from_query(query):
    sql = "SELECT * FROM questions \
          WHERE questions LIKE '%{}%'"
    sql = sql.format(query)
    sql_stmt = get_sql_statement(sql)
    return sql_stmt


def get_sql_statement(sql):
    global conn
    if conn is None:
        get_connection()
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            return result
        else:
            return None

@debug(debug=True)
def check_if_answer_exists(sql_stmt):
    global conn
    with conn.cursor() as cursor:
        cursor.execute(sql_stmt)
        result = cursor.fetchone()
        if result:
            return result
    return False


def __do_not_use():
    get_connection()
    create_tables(database, user, password, sys.argv[2])
    conn.close()
