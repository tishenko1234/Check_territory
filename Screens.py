from selenium.webdriver.common.by import By
from tqdm.auto import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os
import re
import spacy
import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def lemm_finder(list_of_text, stop_words=0):
    """ Функция позволяет перевети все формы слова в леммы"""
    lemma_list = []
    for i in tqdm(list_of_text):
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
    # Настрока и запуск браузера
    options = Options()
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
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
    # Создаем папку для фото
    if not os.path.exists(f"Скриншоты/{Date}"):
        os.mkdir(f"Скриншоты/{Date}")
    for city in tqdm(city_list):
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
            time.sleep(1)
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
    find_list = ', '.join(find_list)
    return find_list


def text_cheсk(df_with_text, text_column_name, all_key_words, cities_list):
    """определеяет в каких текстах есть ключивые слова (пересечение городов и проблеммы)"""
    df_texts = df_with_text.copy()
    # Выделяем леммы
    new_text_list = lemm_finder(list_of_text=list(df_texts[text_column_name]))
    # Проверяем тексты на ключевые слова
    df_texts["New_text"] = new_text_list
    df_texts["Contains_key_words"] = df_texts['New_text'].str.contains('|'.join(all_key_words)).astype(int)
    df_texts["Contains_cities_list"] = df_texts['New_text'].str.contains('|'.join(cities_list)).astype(int)
    df_texts["Contains_sum"] = df_texts["Contains_cities_list"] + df_texts["Contains_key_words"]
    df_with_text['contain_key_words'] = contain_key_words_list = [1 if a == 2 else 0 for a in df_texts["Contains_sum"]]
    df_with_text['key_words_find'] = [
        find_words(all_key_words + cities_list, df_texts.loc[index]['New_text']) if df_texts.loc[index][
                                                                                        'Contains_sum'] == 2 else 0 for
        index in df_texts.index]
    return df_with_text


# Определяем сегодняшнюю дату
now = datetime.datetime.now()
Date = now.strftime("%d_%m_%Y")
# собираем лист название городов
df_cities = pd.read_excel('Входные данные/Список_населенных_пунктов.xlsx')
cities_list = df_cities['Населенные_пункты'].dropna()
get_screens(city_list=cities_list, url='https://lostarmour.info/map/?ysclid=latojsz8nr362636823)', Date=Date)
############################################################################################################
"""БЛОК ТИМОФЕЯ"""

############################################################################################################
# Скачиваем данные
df_texts0 = pd.read_excel('Входные данные/Тексты.xlsx')
# Загружаем модель для обработки русского текста
nlp = spacy.load('ru_core_news_sm-3.4.0')
df_cities = pd.read_excel('Входные данные/Список_населенных_пунктов.xlsx')
# собираем лист название городов
cities_list = lemm_finder(list(df_cities['Населенные_пункты'].dropna()), stop_words=['область', 'обл', 'край', 'обл.'])

# Выявление сообщений с ключевыми словами и городами
text_cheсk(df_with_text=df_texts0, text_column_name='Выдержки из текста',
           all_key_words=lemm_finder(list(df_cities['Тип_проблемы'].dropna())), cities_list=cities_list).to_excel(
    f'Результат_обработки/{Date}.xlsx')
