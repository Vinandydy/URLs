from django.http import Http404

from .base import BaseORMTestCase


class TestSelect(BaseORMTestCase):
    def test_all(self):
        # Получить выборку всех закладок из таблицы
        all_bookmarks = ...  # TODO

        # Сверим кол-во закладок
        self.assertEquals(7, len(all_bookmarks))

        # Соберём все названия закладок, сравним списки
        bookmark_titles = [bookmark.title for bookmark in all_bookmarks]
        self.assertEquals(self.BOOKMARK_TITLES, bookmark_titles)

    def test_count(self):
        # Посчитать кол-во всех заклад средствами ORM
        bookmarks_count = ...  # TODO
        self.assertEquals(7, bookmarks_count)

    def test_first(self):
        # Получить первую запись в выборке
        all_bookmarks = ...  # TODO
        first_bookmark = ...  # TODO

        self.assertEquals(first_bookmark, all_bookmarks[0])

    def test_last(self):
        # Получить последнюю запись в выборке
        all_bookmarks = ...  # TODO
        last_bookmark = ...  # TODO

        self.assertEquals(last_bookmark, all_bookmarks[6])

    def test_get(self):
        # Получить запись по ID
        bookmark_by_id = ...  # TODO
        self.assertIsNotNone(bookmark_by_id)

        # Получить запись по другому полю - важна уникальность!
        bookmark = ...  # TODO
        self.assertIsNotNone(bookmark_by_id)

    def test_get_object_or_404(self):
        # Получить запись 'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал'
        # или 404 (успешный кейс)
        bookmark = ...  # TODO
        # Проверим по полю description
        self.assertEquals((
            'Торт Наполеон в домашних условиях. Вкусный рецепт приготовления с пошаговым описанием на 382 ккал, '
            'c фото и отзывами. Удобный поиск рецептов и кулинарное вдохновение на Gastronom.ru'
        ), bookmark.description)

        # Получить несуществующую запись, выкинет исключение
        with self.assertRaises(Http404):
            ...  # TODO

    def test_values(self):
        # Получить все названия закладок из таблицы средствами ORM
        # Нужно получить QuerySet (~~ список) из словарей
        bookmark_titles = ...  # TODO

        for bm_fields_dict in bookmark_titles:
            self.assertIn(bm_fields_dict['title'], self.BOOKMARK_TITLES)

    def test_values_list(self):
        # Получить все названия закладок из таблицы средствами ORM
        # Нужно получить QuerySet (~~ список) из кортежей
        bookmark_titles = ...  # TODO

        for bm_fields_tuple in bookmark_titles:
            self.assertIn(bm_fields_tuple[0], self.BOOKMARK_TITLES)

        # Нужно получить плоский список (можно выбрать только 1 поле)
        bookmark_titles = ...  # TODO
        self.assertEquals(self.BOOKMARK_TITLES, list(bookmark_titles))

    def test_order_by(self):
        # Выборка всех закладок из таблицы в упорядоченном виде
        all_bookmarks = ...  # TODO
        first_bookmark = ...  # TODO
        last_bookmark = ...  # TODO

        # С ORDER BY мы уже можем предположить, что получим в .first() / .last()
        self.assertEquals('Gmail', first_bookmark.title)
        self.assertEquals('Яндекс Практикум', last_bookmark.title)

    def test_offset_limit(self):
        # Получить записи OFFSET 4, LIMIT 2
        bookmarks = ...

        self.assertEquals(
            'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
            bookmarks[0].title
        )
        self.assertEquals(
            'Три рецепта «Оливье»: классический, советский и современный - РИА Новости, 11.12.2019',
            bookmarks[1].title
        )
