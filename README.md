# Дипломный проект для *NETOLOGY* по курсу: "Python для начинающих"
[![License](https://img.shields.io/github/license/m-lundberg/simple-pid.svg)](https://github.com/m-lundberg/simple-pid/blob/master/LICENSE.md)

![Logo](resources/imgs/logo.jpg)

## Общие сведения
VK бот  для для поиска людей, подходящих под условия, на основании информации о пользователе из VK:
- возраст;
- пол;
- город;
- семейное положение.

Тех людей, которые подошли по требованиям пользователю,  бот показывает в чате топ-3 популярных фотографии профиля вместе со ссылкой на найденного человека. Популярность определяется по количеству лайков и комментариев.

## Установка и запуск

1. Удоволетворить зависимости выполнв команду: ```pip install -r requirements.txt```;  
1. Задать настройки в  ```./util/config.py```, указав:
   -  **GROUP_TOKEN** на access_token сообщества и **USER_TOKEN** access_token аккаунта ВК. [(Как получить токен пользователя)](https://dvmn.org/encyclopedia/qna/63/kak-poluchit-token-polzovatelja-dlja-vkontakte/)
   - настройки к подключению СУДБ Postgress **DB_HOST**, **DB_USER**, **DB_PWD**, **DB_NAME**.
1. Запустить бота: ```python3 bot.py```

