import sqlite3
import pandas as pd


def sql_connection():
    try:
        db = sqlite3.connect('db.sqlite3')
        return db
    except sqlite3.Error:
        print(sqlite3.Error)


def main():
    db = sql_connection()
    cursor = db.cursor()
    with open('test.sql', 'r', encoding='utf-8') as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    db.commit()
    cursor.execute('SELECT * FROM regions;')
    regions = cursor.fetchall()
    print(f'регионы: {regions}')
    cursor.execute('SELECT * FROM cities;')
    cities = cursor.fetchall()
    print(f'города в регионах: {cities}')
    db.close()


def import_from_excel():
    db = sql_connection()
    wb = pd.read_excel('data/users.xlsx', sheet_name='Лист1')
    wb.to_sql(name='users', con=db, if_exists='replace', index=False)
    db.commit()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    print(f'пользователи: {users}')
    db.close()


def export_to_excel():
    db = sql_connection()
    df = pd.read_sql(
        (
            'SELECT '
            'users.id AS id, '
            'users.second_name AS second_name, '
            'users.first_name AS first_name, '
            'users.patronymic AS patronymic, '
            'regions.region_name AS region_name, '
            'cities.city_name AS city_name, '
            'users.phone AS phone, '
            'users.email AS email '
            'FROM users '
            'JOIN cities ON cities.id = city_id '
            'JOIN regions ON regions.id = cities.region_id;'
        ),
        db
        )
    df.to_excel('data/users_export.xlsx', index=False)
    db.close()


if __name__ == '__main__':
    main()
    import_from_excel()
    export_to_excel()
