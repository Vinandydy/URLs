from django.utils import timezone

from django.http import Http404

from rest_framework.generics import get_object_or_404

from .base import BaseORMTestCase
from ...models import Group, Bookmark


class TestFilters(BaseORMTestCase):
    def test_simple_filters(self):
        # Получить группу 'Рецепты'
        group = Group.objects.get(name="Рецепты")

        # Проверим данные
        self.assertEquals(2, group.order)

        # Получить закладку 'Яндекс Практикум'
        bookmark = Bookmark.objects.get(title='Яндекс Практикум')

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
            Bookmark.objects.filter(title__exact="Яндекс Практикум").first(),
            Bookmark.objects.filter(title__contains='декс').first(),
            Bookmark.objects.filter(title__startswith='Яндекс').first(),
            Bookmark.objects.filter(title__endswith='кум').first(),
            Bookmark.objects.filter(title__regex=r'Я*').first(),
        ]

        for bookmark in bookmarks:
            self.assertEquals('Яндекс Практикум', bookmark.title)
            self.assertEquals('https://practicum.yandex.ru/profile/backend-developer/', bookmark.url)

    def test_date_filters(self):
        # Получить закладки, созданные в этом месяце и в этом году
        bookmark_querysets = [
            Bookmark.objects.filter(time_created__month=5),
            Bookmark.objects.filter(time_created__year=2025)
        ]

        # Т.к. все закладки были созданы сегодня,
        # во всех случаях получим полный их список
        for bookmark_queryset in bookmark_querysets:
            self.assertEquals(7, bookmark_queryset.count(), bookmark_queryset.count())

    #Почему-то выдает ошибку
    def test_exclude(self):
        # Получить названия всех закладок с буквой "м" в названии, исключая 'Яндекс Практикум'
        bookmark_titles = Bookmark.objects.filter(title__contains='м').exclude(title__contains='Яндекс Практикум').values_list('title', flat=True)

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
        bookmark = Bookmark.objects.filter(title__isnull=True).values_list('title', flat=True)

        # Получить названия закладок, которые заполнены
        bookmark_titles = Bookmark.objects.filter(title__isnull=False).values_list('title', flat=True)

        # Закладок без названия нет
        self.assertEquals(0, bookmark.count())
        self.assertEquals(self.BOOKMARK_TITLES, list(bookmark_titles))

        # Получить названия групп, у которых order больше 3
        group_names = Group.objects.filter(order__gt=3).values_list('name', flat=True)
        self.assertEquals(['Ремонт'], list(group_names))

        # Получить названия групп, у которых order больше или равно 3
        group_names = Group.objects.filter(order__gte=3).values_list('name', flat=True)
        for title in ('Полезное', 'Ремонт'):
            self.assertIn(title, group_names)

        # Получить названия групп, у которых order меньше 3
        group_names = Group.objects.filter(order__lt=3).values_list('name', flat=True)
        for title in ('Важное', 'Учёба', 'Рецепты'):
            self.assertIn(title, group_names)

        # Получить группы, которые созданы раньше текущего момента
        bookmarks = Bookmark.objects.filter(time_created__lt=timezone.now())
        self.assertEquals(7, bookmarks.count())

        # Получить названия групп, у которых order 2 или 3 или 4 (вхождение во множество)
        group_names = Group.objects.filter(order__in=[2, 3, 4]).values_list('name', flat=True)
        for title in ('Полезное', 'Рецепты'):
            self.assertIn(title, group_names)

        # Получить названия групп, у которых order от 0 до 1 (вхождение в диапазон)
        group_names = Group.objects.filter(order__range=[0, 1]).values_list('name', flat=True)
        for title in ('Важное', 'Учёба'):
            self.assertIn(title, group_names)

    def test_many_filters(self):
        # Получить группы с названием 'Важное' и order 0
        groups = Group.objects.filter(name__contains='Важное') & Group.objects.filter(order=0)

        self.assertEquals(1, groups.count())


        # Получить группы с названием 'Важное' и order 2
        groups = Group.objects.filter(name__contains='Важное') & Group.objects.filter(order=2)
        self.assertEquals(0, groups.count())

    def test_get_list_or_404(self):
        # Получить список групп или 404, выбирая группы, которые созданы позже текущего момента
        # Т. к. это несуществующая выборка, выкинется исключение
        with self.assertRaises(Http404):
            get_object_or_404(Bookmark, time_created__gt=timezone.now())

    def test_exists(self):
        # Проверить, существуют ли группы с названием 'Важное'
        do_groups_exist = Group.objects.filter(name__exact="Важное")
        self.assertTrue(do_groups_exist)
