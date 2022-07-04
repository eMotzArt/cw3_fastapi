import os
import json
import hashlib

from project.paths import DATA_PATH_ABS


class Repository:
    def __init__(self):
        self.source_file = os.path.join(DATA_PATH_ABS, 'data.json')

    def get_all_posts(self):
        with open(self.source_file) as file:
            all_posts = json.load(file)
        return all_posts

    def get_post_by_id(self, searched_post_id):
        all_posts = self.get_all_posts()
        for post in all_posts:
            if post['pk'] == searched_post_id:
                return post

    def add_like(self, post_id):
        ...

    def add_view(self, post_id):
        ...

    def add_comment(self, post_id, name, comment):
        ...


class UserIDentifier:
    """Класс для генерации, записи, и получения уникального id пользователя"""
    # Как уникальный идентификатор я придумал привязаться к браузеру клиенту, в догонку добавить сумму регистров ip
    # По идее - эти данные постоянные, в то же время с разных браузеров получится "разные клиенты"
    # В общем выглядит вполне уникальным и постоянным ориентиром

    def generate_user_id(self, request):
        user_browser_agent = request.headers.get('user-agent')
        user_ip_adress_str = request.get('client')[0]
        user_ip_adress_map_int = map(lambda register: int(register), user_ip_adress_str.split('.'))
        user_ip_adress_sum = str(sum(user_ip_adress_map_int))
        user_unique_str = f"{user_browser_agent}__{user_ip_adress_sum}"
        unique_id = (hashlib.md5(user_unique_str.encode('utf-8')).hexdigest())
        return unique_id

    def record_uid_to_user_cookies(self, new_user_id, response):
        response.set_cookie(key="sky-uid", value=new_user_id)

    def initiate_user(self, request, response):
        """Инициализация. Проверяет есть ли в куках пользователя IDшник, если нет генерирует и записывает"""

        if (user_id := request.cookies.get('sky-uid')) is None:
            new_user_id = self.generate_user_id(request)
            self.record_uid_to_user_cookies(new_user_id, response)
            print(f"New User ID generated: {new_user_id}")
        else:
            print(f"User ID: {user_id} is found")

        return user_id




# x = Repository()
# y = Repository().get_all_posts()
# z = Repository().get_post_by_id(7)
pass
