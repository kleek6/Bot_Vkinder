"""Дипломный проект Семёнова М.А. для курса "Пайтон для начинающих" Netology 2023"""
import time
import logging
from datetime import datetime
from random import randrange
# import vk_api
from util.vkhelper import VK
from util.config import *
from resources.texts import *
from util.dbhelper import db, init_db
from util.helper import Frend, User

log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger()


# поиск друга, находим популярные фотки и возвращаем их пользователю
def search_frend(user: User, vk: VK):
    # Получаем список пользователей
    request_data = set_search_param(user)

    # Показываем  друзей
    txt = SRCH_CMPLT_MSG
    vk.write_msg(user, txt)
    # time.sleep(2)

    i = 0
    for data in vk.user_search_generator(request_data):

        # Проверяем, показывали этого друга ранее
        if not db.check_is_new_frend(user.id, data['id']):
            continue
        # Получаем фотки
        try:
            photos = vk.get_user_photo(data['id'])
            main_photo_url = photos[0]['sizes'][0]['url']
        except:
            continue
        # ФИО
        i = i + 1
        frend = Frend(data['id'])
        frend.set_first_name(data['first_name'])
        frend.set_last_name(data['last_name'])
        full_name = frend.first_name + " " + frend.last_name
        txt = f"**Анкета** #{i}: {full_name}"
        # text += f"{full_name}"
        frend.set_main_photo(main_photo_url)
        vk.write_msg(user, txt)

        # Ссылка на страницу во вконтакте
        frend.get_profile_url()
        txt = f"Профиль: {frend.profile_url}"
        vk.write_msg(user, txt)

        # Отобразить фотки партнёра
        show_partner_photos(frend, photos, user, vk)

        # Записываем информацию о друге в БД
        db.insert_frend(frend)

        # Записываем информацию, что этот друг был просмотрен
        db.insert_user_frend(user.id, data['id'])

        # Запрос на показ еще одного друга
        vk.write_msg(user, "Показать еще одного?")

        while True:
            answer_of_user = vk.wait_for_answer_from_user()['text']
            if answer_of_user == "Да":
                break
            elif answer_of_user == "Нет":
                txt = LOOK_CMPLT_MSG  # "Просмотр анкет окончен. **Досвидания!**"
                vk.write_msg(user, txt)
                main()
                return
            else:
                txt = DUNDSTD_MSG  # "Не понял вашего ответа.\nПожалуйста, нажмите Да или Нет..."
                vk.write_msg(user, txt)

    vk.write_msg(user, LOOK_CMPLT_REP_MSG)
    while True:
        answer_of_user = vk.wait_for_answer_from_user()['text']
        if answer_of_user == "Да":
            db.delete_all_user_partners(user.id)
            search_frend(user, vk)
            return
        elif answer_of_user == "Нет":
            txt = LOOK_CMPLT_MSG  # "Просмотр анкет окончен. Досвидания!"
            vk.write_msg(user, txt)
            main()
            return
        else:
            txt = DUNDSTD_MSG
            vk.write_msg(user, txt)


# Отобразить фотки партнёра
def show_partner_photos(partner, photos, user, vk: VK):
    z = 0
    for photo in photos:
        if z == 3:
            break
        # Отправить фото
        attachament = partner.get_photo_attachment_link(photo['id'])
        photo_data = {
            'user_id': user.id,
            'message': "",
            'attachment': attachament,
            'random_id': randrange(10 ** 7)
        }
        vk.group_api.method('messages.send', photo_data)
        z = z + 1


# параметры, для поиска друга
def set_search_param(user):
    # Пол друга должен быть противоложным
    sex_partner = 0
    if user.sex == 1 and not GAY:
        sex_partner = 2
    else:
        sex_partner = 1
    # Город
    city_id = user.city_id
    # Возраст
    age = int(user.age)
    age_from = age - AGE_DELTA
    age_to = age + AGE_DELTA
    request_data = {
        "sex": sex_partner,  # пол для поиска
        "count": 50,  # кол-во возвращаемых результатов
        "offset": 0,  #
        "city": city_id,
        "status": 6,  # в активном поиске
        "age_from": age_from,  # возрат "от"
        "age_to": age_to,  # возраст "до"
        "has_photo": 1,  # у пользователя есть фотки
        # параметры, которые должен вернуть АПИ контакта о пользователях
        "fields": {
            "first_name", "last_name", "city", "bdate",
        }
    }
    return request_data


# Выбран пункт "Начать поиск"
def menu_start_search(user: User, vk: VK):
    text = SRCHING_MSG  # "Собираю информацию!"
    vk.write_msg(user, text)

    # Получаем информцию о друге и пишем в базу данных
    set_info_about_user(user, vk)
    db.insert_user(user)

    # Призыв к следующему действию
    vk.write_msg(user, PRS_YES_MSG)

    # Ожидаем ответ
    while True:
        answer = vk.wait_for_answer_from_user()['text']
        if answer == "Да":
            search_frend(user, vk)
            break
        elif answer == "Нет":
            text = SMILES['SIG']
            vk.write_msg(user, text)
            main()
            break
        else:
            text = DUNDSTD_MSG
            vk.write_msg(user, text)


# Заполняем в экземлпяр класса User
def set_info_about_user(user: User, vk: VK):
    # получаем id пользователя
    vk.write_msg(user, f"Ваш id пользователя: **{user.id}**")
    #  город
    city = vk.get_user_city(user)
    user.set_city_title(city['title'])
    user.set_city_id(city['id'])
    vk.write_msg(user, f"Ваш город: **{user.city_title}**")
    #  пол
    sex = vk.get_user_sex(user)
    user.set_sex(sex)
    user_sex_text = "Женский" if user.sex == 1 else "Мужской"
    vk.write_msg(user, f"Ваш пол: **{user_sex_text}**")
    # возраст
    age = vk.get_user_age(user)
    user.set_age(age)
    vk.write_msg(user, f"Ваш возраст: **{user.age}**")


# Главное меню
def show_menu(user, vk: VK):
    # Показать приветственное сообщение и меню доступных действий
    text = HELP_MSG
    vk.write_msg(user, text)
    show_sub_menu(user, vk)
    # Проверка ответа
    while True:
        # ждем выбора пользователя
        answer_of_user = vk.wait_for_answer_from_user()['text']
        # 1 => Поиск друга для отношений
        if answer_of_user == "Да":
            menu_start_search(user, vk)
            break
        # 2 => нет так нет
        elif answer_of_user == "Нет":
            text = SMILES['SIG']
            vk.write_msg(user, text)
            main()
            break
        # ... что то пошло не так
        else:
            text = DUNDSTD_MSG
            vk.write_msg(user, text)
            time.sleep(1)
            show_sub_menu(user, vk)


# Показать подменю
def show_sub_menu(user: User, vk: VK):
    text = GET_SRCH_MSG
    vk.write_msg(user, text)


def main():
    # Инициализация БД
    init_db()

    # Иницииализируем vk_api
    vk = VK(USER_TOKEN, GROUP_TOKEN)

    # получаем dic с сообщением от пользователя и его user_id
    user_data = vk.wait_for_answer_from_user()
    user_id = User(user_data['user_id'])

    # Отобразить главное меню
    show_menu(user_id, vk)


if __name__ == '__main__':
    logger.info("Запуск бота:", datetime.now())
    main()
