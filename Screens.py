from selenium.webdriver.common.by import By
from tqdm.auto import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import re
import spacy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import itertools
import os
import cv2
import math
import datetime


def lemm_finder(list_of_text, stop_words=0, wrong_geoobjects=0):
    """ Функция позволяет перевети все формы слова в леммы"""
    lemma_list = []
    for i in tqdm(list_of_text, desc='lemm_finder'):
        text = ' '.join(re.findall(r'[А-Яа-я]+', i))
        doc = nlp(text)
        lemma = []
        for token in doc:
            lemma.append(token.lemma_)
        text_new = ' '.join(lemma)
        if stop_words != 0:
            for j in stop_words:
                text_new = re.sub(rf'( {j}\b)', '', text_new)
        lemma_list.append(text_new)
    if wrong_geoobjects != 0:
        lemma_list = [c for c in
                      [0 if len([b for b in a.split() if b not in wrong_geoobjects]) < len(a.split()) else a if len(
                          a.split()) != 1 else 0
                       for a in lemma_list if a not in wrong_geoobjects] if c != 0]
    return lemma_list


def test_page(driver, delay, element):
    '''Функция проверки загрузки страницы
        delay - количесво секунд ожидания
        element - что ищем пример (By.CLASS_NAME, 'popup-obj')
        driver - драйвер пример
        if __name__ == "__main__":
        driver = Chrome(executable_path="./chromedriver.exe")'''
    # проверка загрузилась ли стр
    try:
        myElem = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located(
                element))
    except TimeoutException:
        print("Loading took too much time!")


# запускае браузер
def get_screens(city_list, url='https://lostarmour.info/map/?ysclid=latojsz8nr362636823)', Date='29_11_22'):
    try:
        # Настрока и запуск браузера
        options = Options()
        options.page_load_strategy = 'normal'
        driver = webdriver.Chrome(executable_path="./chromedriver_mac_os.exe", options=options)
        # Переход на сайт
        driver.get(url)
        # Переключаемся на iframe
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
        window_before = driver.window_handles[0]
        # Переходим на страницу яндекс карт
        try:
            driver.find_element(By.XPATH,
                                "/html/body/div/div/div/div[2]/div[1]/div[1]/div[4]/div/a").click()
        except:
            driver.find_element(By.XPATH,
                                "/html/body/div/div/div/div[2]/div[1]/div[1]/div[4]/div/a").click()
        window_after = driver.window_handles[1]
        # Переключаемся обратно
        driver.switch_to.default_content()
        driver.switch_to.window(window_after)
        # Экран в полный формат
        driver.fullscreen_window()

        for city in tqdm(city_list,desc='get_screens'):
            try:
                # Ввод тектса
                driver.find_element(By.TAG_NAME, "input").send_keys(city)
                # Нажать на ввод поиска
                driver.find_element(By.TAG_NAME, "button").click()
                # Цикл для зума
                for i in range(10):
                    time.sleep(0.1)
                    # Нажать на кнопку приближения
                    driver.find_element(By.CLASS_NAME, "zoom-control__zoom-in").click()
                # Проверяем загрузился ли элемент
                test_page(driver=driver, delay=3,
                          element=(By.XPATH,
                                   "//span[@class='inline-image _loaded sidebar-toggle-button__icon']"))
                time.sleep(1)
                # Нажать на кнопку для того, чтобы убрать поиск
                driver.find_element(
                    By.XPATH,
                    "//span[@class='inline-image _loaded sidebar-toggle-button__icon']").click()
                # Создаем папку для фото
                if not os.path.exists(f"Скриншоты/{Date}"):
                    os.mkdir(f"Скриншоты/{Date}")

                # Делаем скриншот
                driver.save_screenshot(f'Скриншоты/{Date}/{city}.png')
                # Отчистить поле поиска нажав кнопку
                driver.find_element(
                    By.XPATH,
                    "//div[@class='small-search-form-view__icon _type_close']").click()
            except:
                print(f'Проблема с городом {city}')
                continue
        driver.quit()
    except:
        # Настрока и запуск браузера
        options = Options()
        options.page_load_strategy = 'normal'
        driver = webdriver.Chrome(executable_path="./chromedriver_windows.exe", options=options)
        # Переход на сайт
        driver.get(url)
        # Переключаемся на iframe
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
        window_before = driver.window_handles[0]
        # Переходим на страницу яндекс карт
        try:
            driver.find_element(By.XPATH,
                                "/html/body/div/div/div/div[2]/div[1]/div[1]/div[4]/div/a").click()
        except:
            driver.find_element(By.XPATH,
                                "/html/body/div/div/div/div[2]/div[1]/div[1]/div[4]/div/a").click()
        window_after = driver.window_handles[1]
        # Переключаемся обратно
        driver.switch_to.default_content()
        driver.switch_to.window(window_after)
        # Экран в полный формат
        driver.fullscreen_window()

        for city in tqdm(city_list,desc='get_screens'):
            try:
                # Ввод тектса
                driver.find_element(By.TAG_NAME, "input").send_keys(city)
                # Нажать на ввод поиска
                driver.find_element(By.TAG_NAME, "button").click()
                # Цикл для зума
                for i in range(10):
                    time.sleep(0.1)
                    # Нажать на кнопку приближения
                    driver.find_element(By.CLASS_NAME, "zoom-control__zoom-in").click()
                # Проверяем загрузился ли элемент
                test_page(driver=driver, delay=3,
                          element=(By.XPATH,
                                   "//span[@class='inline-image _loaded sidebar-toggle-button__icon']"))
                time.sleep(1)
                # Нажать на кнопку для того, чтобы убрать поиск
                driver.find_element(
                    By.XPATH,
                    "//span[@class='inline-image _loaded sidebar-toggle-button__icon']").click()
                # Создаем папку для фото
                if not os.path.exists(f"Скриншоты/{Date}"):
                    os.mkdir(f"Скриншоты/{Date}")

                # Делаем скриншот
                driver.save_screenshot(f'Скриншоты/{Date}/{city}.png')
                # Отчистить поле поиска нажав кнопку
                driver.find_element(
                    By.XPATH,
                    "//div[@class='small-search-form-view__icon _type_close']").click()
            except:
                print(f'Проблема с городом {city}')
                continue
        driver.quit()


def find_words(key_words, text):
    """Проверяет есть ли слова в списке текстов, если есть, то возвращает их, если нет то
    возвращает 0"""
    find_list = []
    for i in key_words:
        if len(re.findall(rf'{i}', text)) != 0:
            find_list = find_list + re.findall(rf'{i}', text)
    # find_list = ', '.join(find_list)
    return find_list


def find_distance(sentence, word1, word2):
    """Находит колличесво слов между двумя словами в тексте"""
    distances = []
    while sentence != "":
        _, _, sentence = sentence.partition(word1)
        text, _, _ = sentence.partition(word2)
        if text != "":
            distances.append(len(text.split()))
    return distances


def text_cheсk(df_with_text, text_column_name, all_key_words, cities_list, russian_cities_list, check_cities_list):
    """определеяет в каких текстах есть ключивые слова (пересечение городов и проблеммы)"""
    df_texts = df_with_text.copy()
    # Выделяем леммы
    new_text_list = lemm_finder(list_of_text=list(df_texts[text_column_name]))
    # Проверяем тексты на ключевые слова
    df_texts["New_text"] = new_text_list
    df_texts["Contains_key_words"] = df_texts['New_text'].str.contains('|'.join(all_key_words)).astype(int)
    df_texts["Contains_cities_list"] = df_texts['New_text'].str.contains('|'.join(cities_list)).astype(int)

    # Разделяем ключевые словосочетания на слова
    all_key_words_split = []
    for i in all_key_words:
        all_key_words_split = all_key_words_split + i.split()
    all_key_words_split = list(set(all_key_words_split))
    # Формируем все возможные комбинации названий городов и ключевых слов
    a = [cities_list, all_key_words_split]
    all_combinations = list(itertools.product(*a))

    df_20_words_length = pd.DataFrame()
    for text_index in tqdm(list(df_texts.index), desc='text_cheсk'):
        for iteration in range(len(all_combinations)):
            try:
                word_distance = find_distance(df_texts.loc[text_index]['New_text'], all_combinations[iteration][0],
                                              all_combinations[iteration][1])[0]
                if word_distance <= 10:
                    df = pd.DataFrame()
                    df['good_index'] = [text_index]
                    df['word_1'] = [all_combinations[iteration]]
                    df_20_words_length = pd.concat([df_20_words_length, df])
            except:
                continue
    good_index = set(list(df_20_words_length["good_index"]))
    df_texts["Contains_20_words_length"] = [1 if a in good_index else 0 for a in df_texts.index]
    df_texts["Contains_sum"] = df_texts["Contains_cities_list"] + df_texts["Contains_key_words"] + df_texts[
        "Contains_20_words_length"]
    df_with_text['contain_key_words'] = [1 if a == 3 else 0 for a in df_texts["Contains_sum"]]
    df_with_text['problem_type'] = [
        ','.join(list(set(find_words(all_key_words, df_texts.loc[index]['New_text'])))) if
        df_texts.loc[index]['Contains_sum'] == 3 else 0 for index in df_texts.index]

    df_with_text['russian_cities'] = [
        ','.join(list(set(find_words(russian_cities_list, df_texts.loc[index]['New_text'])))) if
        df_texts.loc[index]['Contains_sum'] == 3 else 0 for index in df_texts.index]

    df_with_text['checked_cities'] = [
        ','.join(list(set(find_words(check_cities_list, df_texts.loc[index]['New_text'])))) if
        df_texts.loc[index]['Contains_sum'] == 3 else 0 for index in df_texts.index]
    df_with_text
    return df_with_text


def get_image_path(image_name: str):
    now = datetime.datetime.now()
    Date = now.strftime("%d_%m_%Y")

    image_path = f'Скриншоты/{Date}' + '/' + image_name

    return image_path


def get_image_colors(image_name: str):
    image_path = get_image_path(image_name)
    image = cv2.imread(image_path)

    image_colors = []

    for i in (1, 2, 3, 4):
        gbr_colors = image[image.shape[0] // i - 1, image.shape[1] // i - 1]
        image_colors.append(gbr_colors[::-1])

    return image_colors


def calculate_color_differences_percent(first_color: list, second_color: list):
    maximum_difference = math.sqrt(3 * 256 ** 2)

    color_difference = math.sqrt((first_color[0] - second_color[0]) ** 2 + (first_color[1] - second_color[1]) ** 2 + (
            first_color[2] - second_color[2]) ** 2)

    color_difference_percent = color_difference / maximum_difference * 100

    return color_difference_percent


def check_colors(image_colors: list, zone_colors: list):
    count = 0
    for i in image_colors:
        for j in zone_colors:
            if calculate_color_differences_percent(i, j) < 6.00:
                count += 1

    if count >= 2:
        return True
    else:
        return False


def get_zone_name(image_colors: list):
    orange_zone_colors = [[250, 223, 186], [204, 200, 182], [223, 213, 149]]
    red_zone_colors = [[196, 177, 190], [242, 200, 194], [215, 190, 156]]

    if check_colors(image_colors, orange_zone_colors):
        return 'Под контролем РФ'
    elif check_colors(image_colors, red_zone_colors):
        return 'Под контролем РФ'
    else:
        return 'Не под контролем РФ'


def get_territory_status(key_words_find: list, result_column: dict):
    territory_status = []
    for i in key_words_find:
        if i == 0:
            territory_status.append(0)
        else:
            row_list = i.split(',')
            res_list = []
            for j in row_list:
                try:
                    result_column[j]
                except KeyError:
                    pass
                else:
                    res_list.append(f'{j} - {result_column[j]}')

            territory_status.append(res_list)

    return territory_status


########################################################################################################################

# Определяем сегодняшнюю дату
now = datetime.datetime.now()
Date = now.strftime("%d_%m_%Y")

# Загружаем модель для обработки русского текста
nlp = spacy.load('ru_core_news_sm-3.4.0')
# Скачиваем список городов интерфакса
df_cities = pd.read_excel('Входные данные/Аналитическая панель СКАН (1).xlsx', sheet_name='Регионы')
# Убираем лишние города из списка
cities_list = lemm_finder(list(df_cities['Наименование'].dropna()),
                          stop_words=['область', 'обл', 'край', 'обл.', 'город', 'республика', 'район', 'на'],
                          wrong_geoobjects=['сша', 'украина', 'киев', 'европа', 'молдавия'])
# разделяем словосочетания на слова
cities_list_new = []
for i in cities_list:
    cities_list_new = cities_list_new + i.split()
cities_list_new = [a for a in cities_list_new if a not in ['республика']]

# Скачиваем российские территории
geoobject_our = pd.read_excel('our_list_of_geobjects.xlsx')
geoobject_our_list = []
for i in list(geoobject_our['name_area_new'].dropna()) + list(geoobject_our['region_name_new'].dropna().unique()):
    geoobject_our_list = geoobject_our_list + i.split()

# Определяем российские города из списка интерфакса и те, что надо проверить
russian_cities_list = [a for a in cities_list_new if a in geoobject_our_list]
check_cities_list = [a for a in cities_list_new if a not in geoobject_our_list]

get_screens(city_list=check_cities_list, url='https://lostarmour.info/map/?ysclid=latojsz8nr362636823)', Date=Date)
########################################################################################################################

# Скачиваем данные
df_texts0 = pd.read_excel('Входные данные/Тексты.xlsx')
df_key_words = pd.read_excel('Входные данные/Список_населенных_пунктов.xlsx')

# Выявление сообщений с ключевыми словами и городами
text_cheсk_df = text_cheсk(df_with_text=df_texts0, text_column_name='Выдержки из текста',
                           all_key_words=lemm_finder(list(df_key_words['Тип_проблемы'].dropna())),
                           cities_list=cities_list_new,
                           russian_cities_list=russian_cities_list, check_cities_list=check_cities_list)
# Блок Тимофея
image_names = os.listdir(f'Скриншоты/{Date}')
result_column = {}
for image_name in image_names:
    image_colors = get_image_colors(image_name)
    zone_name = get_zone_name(image_colors)
    result_column[image_name.lower()[:-4]] = zone_name

text_cheсk_df['territory_status'] = get_territory_status(list(text_cheсk_df['checked_cities']), result_column)

text_cheсk_df_final = text_cheсk_df[['Дата', 'Источник', 'Заголовок', 'Выдержки из текста', 'Ссылка на источник',
                                     'contain_key_words', 'problem_type', 'russian_cities', 'checked_cities',
                                     'territory_status']]
text_cheсk_df_final.to_excel(f'Результат_обработки/{Date}.xlsx', index=False)
