from django.http import Http404
from rest_framework.generics import get_object_or_404

from .base import BaseORMTestCase
from ...models import Bookmark

#Первая проблема с которой столкнулся, не могу инициализировать лишь один тест
#Пишу команду python manage.py test main.test.test_orm.test_1_select.py

class TestSelect(BaseORMTestCase):
    def test_all(self):
        # Получить выборку всех закладок из таблицы
        all_bookmarks = Bookmark.objects.all()  # TODO

        # Сверим кол-во закладок
        self.assertEquals(7, len(all_bookmarks))

        # Соберём все названия закладок, сравним списки
        bookmark_titles = [bookmark.title for bookmark in all_bookmarks]
        self.assertEquals(self.BOOKMARK_TITLES, bookmark_titles)
    #Базовый подсчет, пока без больших надстроек, поэтому минимум комментов
    def test_count(self):
        # Посчитать кол-во всех заклад средствами ORM
        bookmarks_count = Bookmark.objects.count()  # TODO
        self.assertEquals(7, bookmarks_count)

    def test_first(self):
        # Получить первую запись в выборке
        all_bookmarks = Bookmark.objects.all()  # TODO
        first_bookmark = Bookmark.objects.first() # TODO

        self.assertEquals(first_bookmark, all_bookmarks[0])

    def test_last(self):
        # Получить последнюю запись в выборке
        all_bookmarks = Bookmark.objects.all()  # TODO
        last_bookmark = Bookmark.objects.last()  # TODO

        self.assertEquals(last_bookmark, all_bookmarks[6])

    #Два подхода, работающие одинаково, стоит ли к такой практике прибегать и сильно ли по рукам за такое бьют?
    def test_last_is_equal(self):
        all_bookmarks = Bookmark.objects.all()
        last_bookmark = all_bookmarks.last()
        self.assertEquals(last_bookmark, all_bookmarks[6])

    def test_get(self):
        # Получить запись по ID
        bookmark_by_id = Bookmark.objects.get(id=1) # TODO
        self.assertIsNotNone(bookmark_by_id)

        # Получить запись по другому полю - важна уникальность!
        bookmark = Bookmark.objects.get(url='https://practicum.yandex.ru/profile/backend-developer/')  # TODO
        self.assertIsNotNone(bookmark_by_id)

    #Тут застрял Сейчас подумать
    #Решено, полагаю, что такой подход лучше, чем верхние
    def test_get_object_or_404(self):
        # Получить запись 'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал'
        # или 404 (успешный кейс)
        bookmark = get_object_or_404(Bookmark, title='Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал') # TODO
        # Проверим по полю description
        self.assertEquals((
            'Торт Наполеон в домашних условиях. Вкусный рецепт приготовления с пошаговым описанием на 382 ккал, '
            'c фото и отзывами. Удобный поиск рецептов и кулинарное вдохновение на Gastronom.ru'
        ), bookmark.description)

        # Получить несуществующую запись, выкинет исключение
        with self.assertRaises(Http404):
            get_object_or_404(Bookmark, title='404')  # TODO

    #Как я понял - QuerySet - тип данных который вернулся, используется вместо all, так как быстрее
    def test_values(self):
        # Получить все названия закладок из таблицы средствами ORM
        # Нужно получить QuerySet (~~ список) из словарей
        bookmark_titles = Bookmark.objects.values('title')  # TODO

        for bm_fields_dict in bookmark_titles:
            self.assertIn(bm_fields_dict['title'], self.BOOKMARK_TITLES)

    #Про плоский список не понял, что это
    def test_values_list(self):
        # Получить все названия закладок из таблицы средствами ORM
        # Нужно получить QuerySet (~~ список) из кортежей
        bookmark_titles = Bookmark.objects.values('title')  # TODO

        for bm_fields_tuple in bookmark_titles:
            self.assertIn(bm_fields_tuple[0], self.BOOKMARK_TITLES)

        # Нужно получить плоский список (можно выбрать только 1 поле)
        bookmark_titles = Bookmark.objects.values('title')  # TODO
        self.assertEquals(self.BOOKMARK_TITLES, list(bookmark_titles))

    def test_order_by(self):
        # Выборка всех закладок из таблицы в упорядоченном виде
        all_bookmarks = Bookmark.objects.order_by('title')  # TODO
        first_bookmark = all_bookmarks.first()  # TODO
        last_bookmark = all_bookmarks.last()  # TODO

        # С ORDER BY мы уже можем предположить, что получим в .first() / .last()
        self.assertEquals('Gmail', first_bookmark.title)
        self.assertEquals('Яндекс Практикум', last_bookmark.title)

    def test_offset_limit(self):
        # Получить записи OFFSET 4, LIMIT 2
        bookmarks = Bookmark.objects.all().order_by('id')[4:4+2]

        self.assertEquals(
            'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
            bookmarks[0].title
        )
        self.assertEquals(
            'Три рецепта «Оливье»: классический, советский и современный - РИА Новости, 11.12.2019',
            bookmarks[1].title
        )