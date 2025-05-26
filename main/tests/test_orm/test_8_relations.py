from .base import BaseORMTestCase
from ...models import Group, Bookmark
from django.db.models import F, Count, Prefetch

class TestRelations(BaseORMTestCase):
    GROUP_BOOKMARKS_COUNT_MAP = {
        'Учёба': 2,
        'Рецепты': 3,
        'Полезное': 0,
        'Важное': 1,
        'Ремонт': 1,
    }

    #Warning вновь кидает, не знаю, что ему не нравится
    def test_groups_bookmarks(self):
        # Получить названия всех закладок из группы, используя объект group
        group = Group.objects.get(pk=1)

        bookmark_titles = [bookmark.title for bookmark in group.bookmarks.all()]

        self.assertIn('Яндекс Практикум', bookmark_titles)
        self.assertIn('Моё обучение – Stepik', bookmark_titles)

    def test_filter_related(self):
        # Получить названия всех закладок из группы, используя объект group, затем отфильтровать их по
        # "начинается с 'Я'"
        group = Group.objects.get(pk=1)

        bookmark_titles = [bookmark.title for bookmark in group.bookmarks.filter(title__startswith='Я')]

        self.assertIn('Яндекс Практикум', bookmark_titles)

    #Тут помогло, что теперь value и value_list я знаю, что используется почти всегда в конце
    def test_filter_by_related_fields(self):
        # Получить названия закладок по именам групп - 'Полезное', 'Важное', используя только модель Закладка
        bookmark_titles = Bookmark.objects.filter(group__name__in=['Полезное', 'Важное']).values_list('title', flat=True)

        self.assertIn('Gmail', bookmark_titles)

    def test_relations_f(self):
        # Получить список всех закладок, с помощью аннотаций добавить название группы в поле group_title
        bookmarks = Bookmark.objects.annotate(group_title=F('group__name'))

        for bookmark in bookmarks:
            self.assertIn(bookmark.group_title, self.GROUP_BOOKMARKS_COUNT_MAP.keys())

    #Тут кстати оказалось проще, чем я думал, изначально я пытался через Group получить
    #колонки от bookmark, а по итогу достаточно было взять колонку связи
    def test_agregate_related(self):
        # Посчитать кол-во закладок в каждой группе, добавить его в поле bookmarks_cnt
        groups = Group.objects.annotate(bookmarks_cnt=Count('bookmarks'))

        for group in groups:
            bookmarks_count = self.GROUP_BOOKMARKS_COUNT_MAP[group.name]
            self.assertEquals(bookmarks_count, group.bookmarks_cnt)

    #Я долго ходил вокруг, думаю что мне нужно Prefech использовать, но пришел к такому варианту
    def test_prefetch_related(self):
        # Это просто наглядный пример проблемы N + 1, тут ничего делать не нужно
        # Посчитаем кол-во запросов в БД при подтягивании модели по связям
        groups = Group.objects.all()
        queries = [str(groups.query)]

        for group in groups:
            queries.append(str(group.bookmarks.all().query))

        # Итого 6, 1 на выборку всех групп, +5 на выборку закладок из каждой группы
        # Проблема N + 1
        print(queries)
        self.assertEquals(6, len(queries))

        # С prefetch_related кол-во запросов будет тем же, НО
        # вместо обращения к БД каждый раз при вызове закладки
        # будет обращение к закешированному QuerySet закладок
        Group.objects.prefetch_related('bookmarks').all()

    #Все равно не совсем понял особенность select_related
    def test_select_related(self):
        # Получить список всех закладок, подгрузив в тот же запрос связанные группы
        bookmarks = Bookmark.objects.select_related('group')

        self.assertIn('LEFT OUTER JOIN', str(bookmarks.query))

    def test_filtered_prefetch(self):
        # Выбрать все группы и только те их закладки, которые содержат '.ru' в url
        # Необходимо сделать это избегая проблемы N + 1 (подсказка: models.Prefetch)
        groups = Group.objects.prefetch_related(
            Prefetch('bookmarks', queryset=Bookmark.objects.filter(url__contains='.ru'))
        )

        # Соберем полученные bookmark title
        bookmark_titles = []
        for group in groups:
            bookmark_titles.extend(bookmark.title for bookmark in group.bookmarks.all())

        # Проверим, что мы получили только нужные данные
        for title in [
            'Яндекс Практикум',
            'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
            'Три рецепта «Оливье»: классический, советский и современный - РИА Новости, 11.12.2019',
            (
                'Обои флизелиновые Аспект Ру Соло белые 1.06 м 70436-14 в Санкт-Петербурге – '
                'купить по низкой цене в интернет-магазине Леруа Мерлен'
            ),
        ]:
            self.assertIn(title, bookmark_titles)
