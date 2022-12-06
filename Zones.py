import os
import cv2
import numpy as np
import math
import datetime

now = datetime.datetime.now()
Date = now.strftime("%d_%m_%Y")

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
        return 'В зоне ДНР/ЛНР'
    elif check_colors(image_colors, red_zone_colors):
        return 'В зоне ДНР/ЛНР'
    else:
        return 'Не в зоне ДНР/ЛНР'


# result_column = {}
# image_names = os.listdir(f'Скриншоты/{Date}')
#
# for image_name in image_names:
#     image_colors = get_image_colors(image_name)
#     zone_name = get_zone_name(image_colors)
#     result_column[image_name.lower()[:-4]] = zone_name
#
# print(result_column)


def get_territory_status(key_words_find: list, result_column: dict):
    territory_status = []
    for i in key_words_find:
        if i == 0:
            territory_status.append(0)
        else:
            row_list = i.split(', ')
            res_list = []
            for j in row_list:
                try:
                    result_column[j]
                except KeyError:
                    pass
                else:
                    res_list.append(result_column[j])

            territory_status.append(res_list)

    return territory_status

