import sqlite3


def sql_connection():
    try:
        db = sqlite3.connect('db.sqlite3')
        return db
    except sqlite3.Error:
        print(sqlite3.Error)


def main():
    db = sql_connection()
    cursor = db.cursor()
    with open('test.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    db.commit()
    db.close()


if __name__ == '__main__':
    main()
