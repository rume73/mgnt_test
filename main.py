import sqlite3
import sys

import fitz
import pandas as pd
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def sql_connection():
    """Подключение к БД SQLite"""
    try:
        db = sqlite3.connect('db.sqlite3')
        return db
    except sqlite3.Error as err:
        print('Ошибка при работе с SQLite', err)
    return None


def load_sql_script():
    """Загрузка sql скрипта в БД SQLite"""
    db = sql_connection()
    cursor = db.cursor()
    with open('test.sql', 'r', encoding='utf-8') as sql_file:
        sql_script = sql_file.read()
    try:
        cursor.executescript(sql_script)
        print('sql_script успешно загружен')
        cursor.execute('SELECT name from sqlite_master where type= "table"')
        print(f'Загруженные таблицы:\n{cursor.fetchall()}')
    except sqlite3.Error as err:
        print(f'Произошла ошибка при загрузке sql_script: {err}')
        db.close()
        print("Соединение с SQLite закрыто")
        return False
    db.commit()
    db.close()


def main():
    load_sql_script()
    while True:
        operation = input("""\nВведите название операции:
        import_from_excel
        export_to_excel
        parse_pdf_resume
        create_pdf_resume
        exit:\n""")

        operation_dict = {
            'import_from_excel': import_from_excel,
            'export_to_excel': export_to_excel,
            'parse_pdf_resume': parse_pdf_resume,
            'create_pdf_resume': create_pdf_resume,
            'exit': sys.exit
        }
        if operation in operation_dict:
            operation_dict[operation]()
        else:
            print('Такой команды нет')


def import_from_excel():
    """Импорт данных из .xslx в таблицу users БД SQLite"""
    db = sql_connection()
    cursor = db.cursor()
    try:
        wb = pd.read_excel('data/users.xlsx', sheet_name='Лист1')
    except FileNotFoundError as err:
        print(f'Ошибка при открытии файла users.xlsx, файл не найден: {err}')
        db.close()
        print("Соединение с SQLite закрыто")
        return False
    second_name = wb['second_name'].tolist()
    first_name = wb['first_name'].tolist()
    patronymic = wb['patronymic'].tolist()
    region_id = wb['region_id'].tolist()
    city_id = wb['city_id'].tolist()
    phone = wb['phone'].tolist()
    email = wb['email'].tolist()
    try:
        for i in range(len(second_name)):
            sqlite_insert_user_query = """INSERT OR IGNORE INTO users
                                    (second_name, first_name, patronymic, region_id, city_id, phone, email)
                                    VALUES
                                    (?, ?, ?, ?, ?, ?, ?);"""
            user = (second_name[i], first_name[i], patronymic[i], region_id[i], city_id[i], phone[i], email[i])
            cursor.execute(sqlite_insert_user_query, user)
        db.commit()
        print('Данные импортированы удачно')
    except sqlite3.Error as e:
        print(f'Ошибка при импорте в БД: {e}')
    finally:
        cursor = db.cursor()
        [print(row) for row in cursor.execute('SELECT * FROM users;')]
        db.close()


def export_to_excel():
    """Экспорт данных из таблицы users в excel файл: users_export.xslx"""
    db = sql_connection()
    sqlite_select_query = """
                            SELECT
                                users.id AS id,
                                users.second_name AS second_name,
                                users.first_name AS first_name,
                                users.patronymic AS patronymic,
                                regions.region_name AS region_name,
                                cities.city_name AS city_name,
                                users.phone AS phone,
                                users.email AS email
                            FROM users
                            JOIN cities ON cities.id = city_id
                            JOIN regions ON regions.id = cities.region_id;
                            """
    try:
        df = pd.read_sql(sqlite_select_query, db)
        path = 'data/users_export.xlsx'
        try:
            df.to_excel(path, index=False)
            print(f'Данные экспортированы удачно, путь: {path}')
        except PermissionError as err:
            print(f'Ошибка при открытии файла users.xlsx, нет доступа: {err}')
            db.close()
            print("Соединение с SQLite закрыто")
            return False
    except sqlite3.Error as e:
        print(f'Ошибка при экспорте из БД: {e}')
    finally:
        db.close()


def parse_pdf_resume():
    """Парсинг данных из резюме PDF в таблицу users БД SQLite"""
    db = sql_connection()
    cursor = db.cursor()
    pdf_document = 'data/resume.pdf'
    try:
        doc = fitz.open(pdf_document)
    except fitz.fitz.FileNotFoundError as err:
        print(f'Ошибка при открытии файла resume.pdf, файл не найден: {err}')
        db.close()
        print("Соединение с SQLite закрыто")
        return False
    page1 = doc.loadPage(0)
    page1_text = page1.getText('text')
    list_content = page1_text.split('\n')[:8]
    fullname = list_content[0].split(' ')
    city = list_content[7].split(' ')[1]
    phone = list_content[2].replace('\xa0', '')
    email = list_content[3].split('\xa0—\xa0')[0]
    if city == 'Москва':
        region = 'Московская область'
    else:
        region = 'Неизвестно'
    try:
        sqlite_insert_region_query = """INSERT OR IGNORE INTO regions
                                        (region_name)
                                        VALUES
                                        (?);"""
        cursor.execute(sqlite_insert_region_query, [region])
        db.commit()
        cursor.execute("""SELECT id
                        FROM regions
                        WHERE region_name=\"Московская область\"
                        LIMIT 1""")
        region_id = cursor.fetchone()[0]
        sqlite_insert_city_query = """INSERT OR IGNORE INTO cities
                                    (region_id, city_name)
                                    VALUES
                                    (?, ?);"""
        cursor.execute(sqlite_insert_city_query, (region_id, city))
        db.commit()
        cursor.execute("""SELECT id, region_id
                        FROM cities
                        WHERE city_name=\"Москва\"
                        LIMIT 1""")
        city_id, region_id = cursor.fetchone()
        sqlite_insert_user_query = """INSERT OR IGNORE INTO users
                                    (second_name, first_name, patronymic, region_id, city_id, phone, email)
                                    VALUES
                                    (?, ?, ?, ?, ?, ?, ?);"""
        user = (fullname[0], fullname[1], fullname[2], region_id, city_id, phone, email)
        cursor.execute(sqlite_insert_user_query, user)
        db.commit()
        print('Запись успешно вставлена ​​в таблицу users из PDF')
    except sqlite3.Error as e:
        print(f'Ошибка при загрузке данных в БД: {e}')
    finally:
        print(user)
        db.close()


def create_pdf_resume():
    """Создание/обновление PDF файла на каждой странице с таблицы users"""
    db = sql_connection()
    cursor = db.cursor()
    sqlite_select_query = """
                            SELECT
                                users.id AS id,
                                users.second_name AS second_name,
                                users.first_name AS first_name,
                                users.patronymic AS patronymic,
                                regions.region_name AS region_name,
                                cities.city_name AS city_name,
                                users.phone AS phone,
                                users.email AS email
                            FROM users
                            JOIN cities ON cities.id = city_id
                            JOIN regions ON regions.id = cities.region_id;
                            """
    try:
        cursor.execute(sqlite_select_query)
        users = cursor.fetchall()
        pdfmetrics.registerFont(TTFont('FiraSans', 'fonts/FiraSans.ttf', 'UTF-8'))
        path = 'data/result_resume.pdf'
        page = canvas.Canvas('data/result_resume.pdf')
        for value in users:
            page.setFont('FiraSans', size=16)
            height = 800
            width = 235
            page.drawString(width, height, f'Резюме №{value[0]}')
            height -= 25
            page.drawString(175, height, f'{value[1]} {value[2]} {value[3]}')
            height -= 25
            page.drawString(50, height, f'Проживает: {value[4]}, г. {value[5]}')
            height -= 25
            page.drawString(50, height, f'Номер телефона: {value[6]}')
            height -= 25
            page.drawString(50, height, f'почта: {value[7]}')
            page.showPage()
        page.save()
        print(f'Данные экспортированы удачно, путь: {path}')
    except:
        print('Ошибка при экспорте данных в PDF')
    finally:
        db.close()


if __name__ == '__main__':
    main()
