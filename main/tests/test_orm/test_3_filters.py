from django.http import Http404

from .base import BaseORMTestCase


class TestFilters(BaseORMTestCase):
    def test_simple_filters(self):
        # Получить группу 'Рецепты'
        group = ...  # TODO

        # Проверим данные
        self.assertEquals(2, group.order)

        # Получить закладку 'Яндекс Практикум'
        bookmark = ...  # TODO

        # Проверим данные
        self.assertEquals('https://practicum.yandex.ru/profile/backend-developer/', bookmark.url)

    def test_string_filters(self):
        # Получить закладки и положить в список bookmarks:
        # 1. название в точности 'Яндекс Практикум'
        # 2. название содержит 'декс'
        # 3. название начинается с 'Яндекс'
        # 4. название оканчивается на 'кум'
        # 5. название соответствует маске regexp r'Я*'
        bookmarks = [
            ...  # TODO
        ]

        for bookmark in bookmarks:
            self.assertEquals('Яндекс Практикум', bookmark.title)
            self.assertEquals('https://practicum.yandex.ru/profile/backend-developer/', bookmark.url)

    def test_date_filters(self):
        # Получить закладки, созданные в этом месяце и в этом году
        bookmark_querysets = [
            ...,  # TODO в этом месяце
            ...  # TODO в этом году
        ]

        # Т.к. все закладки были созданы сегодня,
        # во всех случаях получим полный их список
        for bookmark_queryset in bookmark_querysets:
            self.assertEquals(7, bookmark_queryset.count(), bookmark_queryset.count())

    def test_exclude(self):
        # Получить названия всех закладок с буквой "м" в названии, исключая 'Яндекс Практикум'
        bookmark_titles = ...  # TODO

        self.assertEquals(len(bookmark_titles), 3)
        self.assertIn(
            'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
            bookmark_titles
        )
        self.assertIn(
            'Три рецепта «Оливье»: классический, советский и современный - РИА Новости, 11.12.2019',
            bookmark_titles
        )
        self.assertIn(
            'Обои флизелиновые Аспект Ру Соло белые 1.06 м 70436-14 в Санкт-Петербурге – '
            'купить по низкой цене в интернет-магазине Леруа Мерлен',
            bookmark_titles
        )
        self.assertNotIn('Яндекс Практикум', bookmark_titles)

    def test_less_greater_etc_filters(self):
        # Получить закладки, у которых НЕ заполнено название
        bookmark = ...  # TODO

        # Получить названия закладок, которые заполнены
        bookmark_titles = ...  # TODO

        # Закладок без названия нет
        self.assertEquals(0, bookmark.count())
        self.assertEquals(self.BOOKMARK_TITLES, list(bookmark_titles))

        # Получить названия групп, у которых order больше 3
        group_names = ...  # TODO
        self.assertEquals(['Ремонт'], list(group_names))

        # Получить названия групп, у которых order больше или равно 3
        group_names = ...  # TODO
        for title in ('Полезное', 'Ремонт'):
            self.assertIn(title, group_names)

        # Получить названия групп, у которых order меньше 3
        group_names = ...  # TODO
        for title in ('Важное', 'Учёба', 'Рецепты'):
            self.assertIn(title, group_names)

        # Получить группы, которые созданы раньше текущего момента
        bookmarks = ...  # TODO
        self.assertEquals(7, bookmarks.count())

        # Получить названия групп, у которых order 2 или 3 или 4 (вхождение во множество)
        group_names = ...  # TODO
        for title in ('Полезное', 'Рецепты'):
            self.assertIn(title, group_names)

        # Получить названия групп, у которых order от 0 до 1 (вхождение в диапазон)
        group_names = ...  # TODO
        for title in ('Важное', 'Учёба'):
            self.assertIn(title, group_names)

    def test_many_filters(self):
        # Получить группы с названием 'Важное' и order 0
        groups = ...  # TODO

        self.assertEquals(1, groups.count())


        # Получить группы с названием 'Важное' и order 2
        groups = ...  # TODO
        self.assertEquals(0, groups.count())

    def test_get_list_or_404(self):
        # Получить список групп или 404, выбирая группы, которые созданы позже текущего момента
        # Т. к. это несуществующая выборка, выкинется исключение
        with self.assertRaises(Http404):
            ...  # TODO

    def test_exists(self):
        # Проверить, существуют ли группы с названием 'Важное'
        do_groups_exist = ...  # TODO
        self.assertTrue(do_groups_exist)
