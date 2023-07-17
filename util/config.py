#!/usr/bin/env python3
"""Конфигурация бота"""
DEBUG = True

# Токены VK
# НЕ ЗАЛИВАТЬ В ГИТХАБ!!!!!!!
# Токен сообщества для авторизации
GROUP_TOKEN = 'vk1.a.iPTjNSIGYwOJ2uaetVVI_ISc0onI5qiSrkiz3rioWiKpRng7SmGFiy7YzCzN34MV9Xl0LfUhQ0jtZ7VAboEvWhPX0XHtzFiVIjPoAlJVnd8H7KI-o6x1csHiGAtDm8rjiVyhlpoxY0aYEkwTiiTyvapiiog3NFbSdwmX8nMziWCd-tl2bXvBQnHv3MDuoJCRsOfmDwu81FTXwLsg8hp8sg'
# Токен пользователя имеющего права на передачу и чтение фоток ВК
USER_TOKEN = 'vk1.a.L4jZvEUzi5PBMLvOJ2omAd0vtPi_TWZHGF5-qxVN2FsLnRGI0ygZfeOie_ATNlfaZkeGpI4cnj4ZLPMbcALvuTzgjL4ynqVbTameDSmCoU6weV1tdcwZpzy-IYo9sf4yWuIQJQwy7WuNm9tOh6u-zLG44LdAtwUOW845hyg_84aWm5LyV3cD13K3CX_U09Vb88WPeh7M50yBc9haklB8Hw'

# Подключение к ДБ
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PWD = "master"
DB_NAME = "postgres"

# Колличество параметров на странице в текстовом блоке.
ELEMENTS_ON_PAGE = 15
MAX_PAGE = 5

# Колличество выводимых записей из таблицы лога
MAX_LOG_ROW_SHOW = 100

# Если да то ищем того же пола
GAY = False

# Раница возроста +- от пользователя
AGE_DELTA = 5