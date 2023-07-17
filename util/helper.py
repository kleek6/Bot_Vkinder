"""Вспомогательные функции и классы"""


class User:
    """Описание пользователя"""
    def __init__(self, user_id):
        self.id = user_id
        self.city_id = ""
        self.city_title = ""
        self.age = ""
        self.sex = ""

    def set_city_id(self, value):
        self.city_id = value

    def set_age(self, value):
        self.age = value

    def set_sex(self, value):
        self.sex = value

    def set_city_title(self, value):
        self.city_title = value

    def __str__(self):
        return f"Индификатор: {self.id}, Город: {self.city_id}, Возраст: {self.age}"


class Frend:
    """Описание кандидата"""
    def __init__(self, user_id):
        self.id = user_id
        self.first_name = ""
        self.last_name = ""
        self.main_photo = ""
        self.profile_url = ""

    def set_first_name(self, value):
        self.first_name = value

    def set_last_name(self, value):
        self.last_name = value

    def set_main_photo(self, value):
        self.main_photo = value

    def set_profile_url(self, value):
        self.profile_url = value

    def __str__(self):
        return f"Индификатор: {self.id}, Имя: {self.first_name}, Фамилия: {self.last_name}"

    def get_profile_url(self):
        self.profile_url = "vk.com/id" + str(self.id)

    def get_photo_attachment_link(self, photo_id):
        return f"photo{self.id}_{photo_id}"

