import pymysql.cursors
import sys


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


def get_tables():
    global conn
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        res = cursor.fetchone()
        if res:
            f = "/home/jbasnet466/Project3/makeTables.sql"
            with open(f,'r') as f:
                data = f.read()
                data = data.split('\n')
                for line in data:
                    if line.strip():
                        print(line)
                        cursor.execute(line.strip())
    conn.commit()


def insert_into(stmt, line_num=None):
    global conn
    if conn is None:
        get_connection()
        #get_tables()
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
        return d, u, p


def get_connection():
    global conn, database, user, password
    if len(sys.argv) == 1:
       fileName = "/home/jbasnet466/Project3/credentials.txt"
    else:
       fileName = sys.argv[1]
    database, user, password = read_info(fileName)

    make_connection(database, user, password)



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


def check_if_answer_exists(sql_stmt):
    global conn
    if not conn:
       #d,b,p = read_info('/home/jbasnet466/Project3/credentials.txt')
       #make_connection(d,b,p)
       get_connection()
    with conn.cursor() as cursor:
        cursor.execute(sql_stmt)
        result = cursor.fetchall()
        if result:
            return result
    return False
