import os
import json
import hashlib
import re

from project.paths import DATA_PATH_ABS


class Repository:
    def __init__(self):
        self.posts_file = os.path.join(DATA_PATH_ABS, 'data.json')
        self.bookmarks_file = os.path.join(DATA_PATH_ABS, 'bookmarks.json')
        self.comments_file = os.path.join(DATA_PATH_ABS, 'comments.json')


    # posts

    def get_all_posts(self):
        with open(self.posts_file) as posts_file:
            all_posts = json.load(posts_file)
        all_posts_parsed = self.parse_post_hashtags(all_posts)
        return all_posts_parsed

    def get_post_by_id(self, searched_post_id):
        all_posts = self.get_all_posts()
        for post in all_posts:
            if post['pk'] == searched_post_id:
                return post

    def get_post_by_search_line(self, search_line):
        all_posts = self.get_all_posts()
        founded_posts = []
        for post in all_posts:
            if search_line.lower() in post['content'].lower():
                founded_posts.append(post)
        return founded_posts

    def get_post_by_user_name(self, user_name):
        all_posts = self.get_all_posts()
        founded_posts = []
        for post in all_posts:
            if post['poster_name'].lower() == user_name.lower():
                founded_posts.append(post)
        return founded_posts

    def parse_post_hashtags(self, all_posts: list[dict]):
        """Получает контент поста и обворачивает хештеги ссылкой, если такой процедуры с постом не производилось ранее"""
        # Эта функция создана исключительно в этой работе, ибо гораздо проще всё это проделывать в функции добавления постов,
        # которой тут нет, и уже в структуре поста иметь ключ hashtags

        # Маркер на наличие изменений
        is_resave_needed = False

        for post in all_posts:
            # Если в структуре поста есть ключ hashtags, значит данный пост уже был проверен и обработан на наличие хештегов
            if post.get('hashtags') != None:
                continue
            # Дальнейший код уже потребует сохранение изменений в базе постов, поэтому...
            is_resave_needed = True

            #если нет хештегов - добавляем ключ с пустым списком
            if post['content'].count('#') == 0:
                post['hashtags'] = []
                continue

            # данный код выполнится в случае, если в тексте имеются хештеги

            # вычисляются все хештеги в список (после каждого хештега присутствует пробел, это важно, не спрашивайте зачем)
            hashtags = re.findall(r'(#\w+ )', post['content'])
            # каждый хештег в тексте заменяется на ссылку
            for hashtag in hashtags:
                post['content'] = post['content'].replace(hashtag, f"<a href='/tag/{hashtag[1:].strip()}'>{hashtag.strip()}</a> ", 1)
            #удаляем пробелы с концов хештегов для феншуя
            hashtags = list(map(lambda x: x.strip(), hashtags))
            # записываем хештеги в ключ,
            post['hashtags'] = hashtags

        # если были какие-нибудь изменения в базе - перезаписываем базу постов
        if is_resave_needed:
            self.rewrite_all_posts_after_parse_hashtags(all_posts)

        return all_posts

    def rewrite_all_posts_after_parse_hashtags(self, all_posts):
        with open(self.posts_file, 'w', encoding='utf-8') as posts_file:
            json.dump(all_posts, posts_file, ensure_ascii=False, indent=4)

    # comments

    def get_all_comments(self):
        with open(self.comments_file) as comments_file:
            all_comments = json.load(comments_file)
        return all_comments

    def get_comments_by_post_id(self, searched_post_id):
        all_comments = self.get_all_comments()

        founded_comments = []
        for comment in all_comments:
            if comment['post_id'] == searched_post_id:
                founded_comments.append(comment)

        return founded_comments




    def add_like(self, post_id):
        ...

    def add_view(self, post_id):
        ...

    def add_comment(self, post_id, name, comment):
        ...

    def get_bookmarsk_count(self):
        with open(self.bookmarks_file) as file:
            all_bookmarks = json.load(file)
        return len(all_bookmarks)


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

