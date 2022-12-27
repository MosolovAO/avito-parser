import os
import sqlite3
from datetime import datetime, timedelta, date
from random import randint
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import load_workbook
import random
import string

#source ./.venv/bin/activate


def generate_random_string(length):
    '''Функция для вычисления рандомной строки'''

    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))

    return rand_string

#СПИСОК ВАЖНЫХ ПЕРЕМЕННЫХ

#https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1269Q18wnCxcjGGXiobwLDupHoFUI3q5a
#Список геолокаций
ADRESS = [ 
    'Владимирская область, Петушинский район, Покров',
            'Владимирская область, Петушинский район, деревня Поляны',
            'Московская область, городской округ Пушкинский, рабочий посёлок Правдинский',
            'Московская область, Щёлково, Пролетарский проспект',
            'Рязанская область, рабочий посёлок Пронск'
            'Московская область, Протвино',
            'Московская область, Пушкино',
            'Московская область, Пущино',
            'Московская область, городской округ Коломна, посёлок Радужный',
            'Московская область, Ленинский городской округ, посёлок Развилка',
            'Московская область, Раменское',
            'Московская область, Сергиево-Посадский городской округ, посёлок Реммаш',
            'Московская область, Реутов',
            'Московская область, Раменский городской округ, село Речицы',
            'Московская область, Дмитровский городской округ, село Рогачёво',
            'Московская область, городской округ Шатура, Рошаль',
            'Московская область, Руза',
            'Рязанская область, Рыбное',
            'Рязанская область, Ряжск',
            'Рязанская область, рабочий посёлок Сараи',
            'Рязанская область, рабочий посёлок Сараи, улица Свердлова',
            'Московская область, Наро-Фоминский городской округ, деревня Селятино',
            'Московская область, Сергиев Посад',
            'Московская область, рабочий посёлок Серебряные Пруды',
            'Московская область, Серпухов',
            'Рязанская область, Скопин',
            'Рязанский район, Варсковское сельское поселение, посёлок Варские, коттеджный посёлок Снегири',
            'Владимирская область, Собинка',
            'Московская область, Солнечногорск',
            'Московская область, городской округ Пушкинский, рабочий посёлок Софрино',
            'Рязанская область, Спас-Клепики',

        ]

#Путь до главной директории (Основной)
PATH = '/Volumes/GoogleDrive/Мой диск/avito/base/'

#Путь до главной директории (Временный)
# PATH = '/Volumes/GoogleDrive/Мой диск/avito/testing/'

#Дата начала публикации
DateBegin = date.today()

#Вычисляем дату окончания публикации
ToDay = datetime.now()
DateEnd = ToDay.date() + timedelta(days=30)



def sql_chek(title: str, description: str):
    '''Функция проверяет содержится ли данная запись в базе данных'''

    try:
        db_connection = sqlite3.connect('server.db')
        sql_cursor = db_connection.cursor()

        print('Открыто соединение с sql')
        row = sql_cursor.execute("SELECT title, description, dateend FROM data WHERE Title = ? AND Description = ?", (title, description))
        result = row.fetchall()
        
        if len(result) == 0:
            return True

        for x in result:
            DateEnd = datetime.strptime(x[2], '%Y-%m-%d')
            if ToDay.date() < DateEnd.date():
                print("Срок объявдения еще не вышел!")
                return False  

        # print(len(result))
        # print("Сегодня: ", ToDay.date())
        # print("Дата конца публикации: ", DateEnd.date())
        # print("Сравнение даты: ", DateEnd.date() + timedelta(days=30))
        # print(ToDay.date() > DateEnd.date())

        return True

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if db_connection:
            db_connection.close()
            print("Соединение с SQLite закрыто")
            

def get_path(path):
    '''Функция для поиска подпапок внутри path.'''
    folders = []

    for folder in os.walk(path):
        folders.append(folder)
        break
    
    return folders[0][1]

#print(get_path(PATH))    

def get_data():
    '''Функция для сбора данных'''

    #Получаем список категорий
    folders_list = get_path(PATH)
    data_row = []

    #Цикл сбора данных по всем категориям
    for folder in folders_list:

        with open(f'{PATH}{folder}/index.html', mode='rt') as file:

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
        Day_upload = soup.find('div', {"id": "day_upload"}).text

        if ToDay.day % int(Day_upload) == 0:
            #Получаем Название записи (Рандомное)
            title_list = []
            for title in soup.find('div', class_='title_wrapper').find_all('div', class_='title'):
                title_list.append(title.text)

            #print(title_list[randint(0, len(title_list) - 1)])

            #Получаем Описание записи (Рандомное)
            description_list = []
            for title in soup.find('div', class_='description_wrapper').find_all('div', class_='description'):
                description_list.append(title)

            status = False
            n = 0
            while status == False:
                print(f'Попытка для {folder}: {n}')
                title = title_list[randint(0, len(title_list) - 1)]
                description = str(description_list[randint(0, len(description_list) - 1)]).replace('\n', '').strip()

                if sql_chek(title, description):
                    status == True
                    break
                elif n > 100:
                    break

                n += 1

            #print(description_list[randint(0, len(description_list) - 1)])

            img_folder = get_path(PATH + folder + '/image_collections')

            #Обнуляемый список главных изображений
            head_image_list = []
            #Получаем список загланых изображений
            with os.scandir(f'{PATH}{folder}/head/') as files_name:
                for file_name in files_name:
                    head_image_list.append('https://drive.google.com/uc?export=view&id=' + file_name.name.split('.')[0])

            #Обнуляемый список изображений
            image_list = []
            #Добавляем в массив случайную заглавную фотографию
            image_list.append(head_image_list[randint(0, len(head_image_list) - 1)])
            #Получаем коллекцию изображений записи (Рандомно)
            with os.scandir(f'{PATH}{folder}/image_collections/{img_folder[randint(0, len(img_folder) - 1)]}/') as files_name:
                for file_name in files_name:
                    image_list.append('https://drive.google.com/uc?export=view&id=' + file_name.name.split('.')[0])

            data_row.append([
                Category, 
                Goods_type,  
                title, 
                description,
                Condition,
                Price,
                str(DateBegin),
                str(DateEnd),
                'По телефону и в сообщениях',
                'Менеджер',
                ContactPhone,
                " | ".join(image_list),
                GoodsSubType,
                CompanyName,
                'Package',
                Ad_type,
                Price_type,
            ])
        else:
            print(f"Для категории {folder} время постинга еще не настало") 

    return data_row

def creat_xlsx(data: list):
    '''Функция для записи CSV файла'''

    #Основной путь
    autoload_file = '/Volumes/GoogleDrive/Мой диск/avito/autoload.xlsx'

    #Отладка кода
    # autoload_file = '/Volumes/GoogleDrive/Мой диск/avito/testing/autoload.xlsx'

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

        for item in data:

            sql_query = f"""
                    INSERT INTO data    
                    (Category, GoodsType, Title, Description, Condition, Price, DateBegin, DateEnd, ContactMethod, ManagerName, ContactPhone, ImageUrls, GoodsSubType, CompanyName, ListingFee, AdType, PriceType)
                    VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            sql_cursor.execute(sql_query, (tuple(item)))
                
            db_connection.commit()

            print('Запись успешно добавлена')

            for location in ADRESS:

                random_string = generate_random_string(32)
                item.insert(0, random_string)
                item.insert(3, location)
                creat_xlsx(item)
                item.remove(location)
                item.remove(random_string)    

        sql_cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if db_connection:
            db_connection.close()
            print("Соединение с SQLite закрыто")

set_data(get_data())



#Ссылка на прямое фото в Google Drive
#https://drive.google.com/uc?export=view&id=1MCHQxfFURYoDqbp3BrMkOsYfQ--oYMZY

#Создание Exel файла
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

#                    'CompanyName': [],
#                    'ListingFee': [],
#                    'AdType': [],
#                    'PriceType': [],
#                    })
# df.to_excel('autoload.xlsx', index=False)

'''

'Московская область, городской округ Солнечногорск, рабочий посёлок Андреевка',
        'Московская область, городской округ Коломна, деревня Андреевка',
        'Московская область, городской округ Люберцы, рабочий посёлок Томилино',
        'Московская область, городской округ Люберцы, рабочий посёлок Малаховка',
        'Тульская область',
        'Рязанская область',
        'Москва',
        'Московская область, Балашиха',
        'Московская область, Бронницы ',
        'Тула',
        'Рязань',
        'Тверь',
        'Тула',
        'Тульская область, Заокский район, деревня Прокшино',
        'Москва, посёлок Коммунарка',
        'Тульская область, Венёв',
        'Тульская область, Алексин',
        'Москва, поселение Внуковское, деревня Рассказовка',
        'Московская область, рабочий посёлок Серебряные Пруды',
        'Московская область, городской округ Пушкинский, Ивантеевка',
        'Москва, поселение Щаповское, село Ознобишино',
        'Московская область, городской округ Чехов, село Новый Быт',
        'Московская область, городской округ Коломна, Озёры',
        'Московская область, городской округ Красногорск, деревня Бузланово',
        'Калуга',
        'Калужская область, Дзержинский район, Кондрово',
        'Калужская область, Обнинск',
        'Москва, Щербинка',
        'Московская область, городской округ Истра, Дедовск',
        'Московская область, Одинцовский городской округ, Голицыно',
        'Московская область, городской округ Ступино, рабочий посёлок Михнево',
        'Московская область, Рузский городской округ, рабочий посёлок Тучково',
        'Московская область, Одинцовский городской округ, Кубинка',
        'Московская область, Рузский городской округ, посёлок Дорохово',
        'Московская область, городской округ Подольск, посёлок Железнодорожный',
        'Московская область, Талдомский городской округ, рабочий посёлок Запрудня',
        'Московская область, городской округ Клин, Высоковск',
        'Московская область, Одинцовский городской округ, Звенигород',
        'Московская область, городской округ Шатура, Рошаль', 

'''


'''

'Московская область, городской округ Солнечногорск, рабочий посёлок Андреевка',
        'Московская область, городской округ Коломна, деревня Андреевка',
        'Московская область, городской округ Люберцы, рабочий посёлок Томилино',
        'Московская область, городской округ Люберцы, рабочий посёлок Малаховка',
        'Тульская область',
        'Рязанская область',
        'Москва',
        'Московская область, Балашиха',
        'Московская область, Бронницы ',
        'Тула',
        'Рязань',
        'Тверь',
        'Тула',
        'Тульская область, Заокский район, деревня Прокшино',
        'Москва, посёлок Коммунарка',
        'Тульская область, Венёв',
        'Тульская область, Алексин',
        'Москва, поселение Внуковское, деревня Рассказовка',
        'Московская область, рабочий посёлок Серебряные Пруды',
        'Московская область, городской округ Пушкинский, Ивантеевка',
        'Москва, поселение Щаповское, село Ознобишино',
        'Московская область, городской округ Чехов, село Новый Быт',
        'Московская область, городской округ Коломна, Озёры',
        'Московская область, городской округ Красногорск, деревня Бузланово',
        'Калуга',
        'Калужская область, Дзержинский район, Кондрово',
        'Калужская область, Обнинск',
        'Москва, Щербинка',
        'Московская область, городской округ Истра, Дедовск',
        'Московская область, Одинцовский городской округ, Голицыно',
        'Московская область, городской округ Ступино, рабочий посёлок Михнево',
        'Московская область, Рузский городской округ, рабочий посёлок Тучково',
        'Московская область, Одинцовский городской округ, Кубинка',
        'Московская область, Рузский городской округ, посёлок Дорохово',
        'Московская область, городской округ Подольск, посёлок Железнодорожный',
        'Московская область, Талдомский городской округ, рабочий посёлок Запрудня',
        'Московская область, городской округ Клин, Высоковск',
        'Московская область, Одинцовский городской округ, Звенигород',
        'Московская область, городской округ Шатура, Рошаль',        
'''

'''
'Московская область, Раменское',
        'Московская область, Домодедово',
        'Московская область, Домодедово, микрорайон Барыбино',
        'Московская область, Чехов',
        'Московская область, Коломна, улица Подлипки-6',
        'Московская область, Солнечногорск',
        'Московская область, Клин',
        'Московская область, Пушкино',
        'Московская область, Пущино',
        'Московская область, Наро-Фоминск', 
        'Московская область, Щёлково',
        'Московская область, Мытищи',
        'Калужская область, Малоярославец',
        'Московская область, Серпухов',
        'Московская область, Зарайск',
        'Московская область, Луховицы',
        'Московская область, Егорьевск',
        'Московская область, Ступино',
        'Московская область, Кашира',
        'Московская область, Подольск',
        'Московская область, Одинцово',
        'Московская область, Можайск',
        'Московская область, Волоколамск',
        'Московская область, Руза',
        'Московская область, Реутов',
        'Московская область, Сергиев Посад',
        'Московская область, Дубна',
        'Московская область, Электросталь',
        'Московская область, Красногорск',
        'Московская область, Люберцы',
        'Московская область, Шатура',
        'Московская область, Орехово-Зуево',
        'Московская область, Дмитров',
        'Московская область, Электрогорск',
        'Московская область, Истра',
        'Московская область, Жуковский',





'''

'''
199. Спасск-Рязанский 
200.  Старая Купавна 
201.  Струнино 
202. Ступино 
203. Сухиничи 
204. Талдом 
205.  Таруса 
206.  Томилино 
207.  Торжок 
208. Троицк 
209.  Тума 
210.  Тучково 
211. Уваровка 
212. Углич 
213.  Удельная 
214. Удомля 
215.  Узловая 
216. Фрязино 
217.  Фряново 
218. Химки 
219.  Хорлово 
220.  Хотьково 
221.  Черноголовка 
222.  Черусти 
223. Чехов 
224. Чучково 
225.  Шатура 
226.  Шаховская 
227. Шацк 
228. Шишкин Лес 
229.  Щекино 
230.  Щербинка 
231.  Щёлково 
232.  Электрогорск 
233.  Электросталь 
234. Электроугли 
235. Юрьев-Польский 
236.  Яковлевское 
237. Ясногорск 
238.  Яхрома

'''