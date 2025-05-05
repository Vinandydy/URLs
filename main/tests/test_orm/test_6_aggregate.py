from django.db.models import Sum, Max, Avg, Min, Count

from .base import BaseORMTestCase
from ...models import Group


class TestAggregate(BaseORMTestCase):
    # Здесь во всех случаях получаем словарики вида {'название_поля__название_функции': ...}

    def test_sum(self):
        # Получить сумму значение поля order всех групп
        result = Group.objects.aggregate(Sum('order'))
        self.assertEquals(11, result['order__sum'])

    def test_count(self):
        # Получить кол-во имён всех групп, используя аггрегирующую функцию
        result = Group.objects.aggregate(Count('name'))
        self.assertEquals(5, result['name__count'])

    def test_min(self):
        # Получить минимальный order среди групп
        result = Group.objects.aggregate(Min('order'))
        self.assertEquals(0, result['order__min'])

    def test_max(self):
        # Получить максимальный order среди групп
        result = Group.objects.aggregate(Max('order'))
        self.assertEquals(5, result['order__max'])

    def test_avg(self):
        # Получить среднее арифметическое для order
        result = Group.objects.aggregate(Avg('order'))
        self.assertEquals(2.2, result['order__avg'])
