import os
import sqlite3
from datetime import datetime, timedelta, date
from random import randint
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import load_workbook
import random
import string


#Вычисляем рандомную строку для уникального id записи для Авито (требование)
def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))

    return rand_string

'''
db = sqlite3.connect('server.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT,
    password TEXT,
    cash BIGINT

) """)

db.commit()

user_login = input('Login: ')
user_password = input('Pass: ')

sql.execute("SELECT login FROM users")

if sql.fetchone() is None:
    sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (user_login, user_password, 0))
    db.commit()
else:
    print('Такая запись уже имеется')
'''
#Список геолокаций
ADRESS = [  'Московская область, Воскресенский район',
            'Московская область, Дмитровский район',
            'Московская область, Домодедово',
            'Московская область, Егорьевск',
            'Московская область, Жуковский',
            'Московская область, Ивантеевка',
            'Московская область, Коломна',
            'Московская область, Истра',
            'Московская область, Клин',
            'Московская область, Королев ',
            'Московская область, Красногорск',
            'Московская область, Ленинский район',
            'Московская область, Лобня',
            'Московская область, Луховицы',
            'Московская область, Люберцы', 
            'Московская область, Можайкий район',
            'Московская область, Мытищи', 
            'Московская область, Наро-фоминск',
            'Московская область, Ногинск',
            'Московская область, Одинцовский район',
            'Московская область, Павловский посад',
            'Московская область, Подольск',
            'Московская область, Пушкинский район',
            'Московская область, Раменский район',
            'Московская область, Реутов',
            'Московская область, Сергеево-Пасадский',
            'Московская область, Серпухов',
            'Московская область, Солнечногорский район',
            'Московская область, Ступино',
            'Московская область, Фрязино',
            'Московская область, Химки',
            'Московская область, Чехов',
            'Московская область, Шатура',
            'Московская область, Щелковский район', 
            'Московская область, Электросталь'  ]


#Дата начала публикации
DateBegin = date.today()

#Вычисляем дату окончания публикации
ToDay = datetime.now()
DateEnd = ToDay.date() + timedelta(days=30)

#Путь до главной директории
PATH = '/Volumes/GoogleDrive/Мой диск/avito/base/'

#Возвращает список всех директорий
def get_path(path):

    folders = []

    for folder in os.walk(path):
        folders.append(folder)
        break
    
    return folders[0][1]

#print(get_path(PATH))    


#Собирает данные из категории
def get_data():

    _folder = get_path(PATH)
    _img_folder = get_path(PATH + _folder[0] + '/image_collections')

    #print(_img_folder)

    with open(f'/Volumes/GoogleDrive/Мой диск/avito/base/{_folder[0]}/index.html', mode='rt') as file:

        text = file.read()
    
    soup = BeautifulSoup(text, "html.parser")

    #Не динамические параметры авито для каждой категории
    Category = soup.find('div', {"id": "category"}).text
    Goods_type = soup.find('div', {"id": "GoodsType"}).text
    Price = soup.find('div', {"id": "Price"}).text
    Ad_type = soup.find('div', {"id": "AdType"}).text
    Price_type = soup.find('div', {"id": "pricetype"}).text
    Condition = soup.find('div', {"id": "Condition"}).text
    ContactPhone = soup.find('div', {"id": "ContactPhone"}).text
    GoodsSubType = soup.find('div', {"id": "GoodsSubType"}).text
    CompanyName = soup.find('div', {"id": "CompanyName"}).text

    #Получаем Название записи (Рандомное)
    title_list = []
    for title in soup.find('div', class_='title_wrapper').find_all('div', class_='title'):
        title_list.append(title.text)

    #print(title_list[randint(0, len(title_list) - 1)])

    #Получаем Описание записи (Рандомное)
    description_list = []
    for title in soup.find('div', class_='description_wrapper').find_all('div', class_='description'):
        description_list.append(title)

    #print(description_list[randint(0, len(description_list) - 1)])

    #Получаем коллекцию изображений записи (Рандомно)
    image_list = []
    with os.scandir(f'/Volumes/GoogleDrive/Мой диск/avito/base/Blocks/image_collections/{_img_folder[randint(0, len(_img_folder) - 1)]}/') as files_name:
        for file_name in files_name:
            image_list.append('https://drive.google.com/uc?export=view&id=' + file_name.name[:-5])

    data_row = [
        Category, 
        Goods_type,  
        title_list[randint(0, len(title_list) - 1)], 
        str(description_list[randint(0, len(description_list) - 1)]).replace('\n', '').strip(),
        Condition,
        Price,
        str(DateBegin),
        str(DateEnd),
        'По телефону и в сообщениях',
        'Менеджер',
        str(ContactPhone),
        " | ".join(image_list),
        GoodsSubType,
        CompanyName,
        'Package',
        Ad_type,
        Price_type,
    ]

    return data_row

#Функция для записи CSV файла
def creat_xlsx(data: list):

    autoload_file = '/Volumes/GoogleDrive/Мой диск/avito/autoload.xlsx'
    wb = load_workbook(autoload_file)
    ws = wb['Sheet1']
    ws.append(data)
    wb.save(autoload_file)
    wb.close()

#Главная управляющая функция
def set_data(data: list):

    try:
        db_connection = sqlite3.connect('server.db')
        sql_cursor = db_connection.cursor()

        print('Успешное подключение')

        curent_title = sql_cursor.execute("SELECT * FROM data WHERE Title =?", (data[2], ))

        if curent_title.fetchone() is None:
            print('Такого Title нет')

            sql_query = f"""
                INSERT INTO data
                (Category, GoodsType, Title, Description, Condition, Price, DateBegin, DateEnd, ContactMethod, ManagerName, ContactPhone, ImageUrls, GoodsSubType, CompanyName, ListingFee, AdType, PriceType)
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            print(len(data))

            #list1 = [x for x in data]
            #print(list1)

            count = sql_cursor.execute(sql_query, (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16]))
            db_connection.commit()

            print('Запись успешно добавлена')

            sql_cursor.close()

            for location in ADRESS:

                random_string = generate_random_string(32)

                data.insert(0, random_string)
                data.insert(3, location)
                creat_xlsx(data)
                data.remove(location)
                data.remove(random_string)

        else:
            print('Такой Title есть, была вызвана функция set_data')
            set_data(get_data())   

        

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if db_connection:
            db_connection.close()
            print("Соединение с SQLite закрыто")




# df = pd.DataFrame({'Id': [],
#                    'Category': [],
#                    'GoodsType': [],
#                    'Address': [],
#                    'Title': [],
#                    'Description': [],
#                    'Condition': [],
#                    'Price': [],
#                    'DateBegin': [],
#                    'DateEnd': [],
#                    'ContactMethod': [],
#                    'ManagerName': [],
#                    'ContactPhone': [],
#                    'ImageUrls': [],
#                    'GoodsSubType': [],
#                    'CompanyName': [],
#                    'ListingFee': [],
#                    'AdType': [],
#                    'PriceType': [],
#                    })
# df.to_excel('autoload.xlsx', index=False)

set_data(get_data())

#https://drive.google.com/uc?export=view&id=1MCHQxfFURYoDqbp3BrMkOsYfQ--oYMZY