from .base import BaseORMTestCase


class TestAggregate(BaseORMTestCase):
    # Здесь во всех случаях получаем словарики вида {'название_поля__название_функции': ...}

    def test_sum(self):
        # Получить сумму значение поля order всех групп
        result = ...  # TODO
        self.assertEquals(11, result['order__sum'])

    def test_count(self):
        # Получить кол-во имён всех групп, используя аггрегирующую функцию
        result = ...  # TODO
        self.assertEquals(5, result['name__count'])

    def test_min(self):
        # Получить минимальный order среди групп
        result = ...  # TODO
        self.assertEquals(0, result['order__min'])

    def test_max(self):
        # Получить максимальный order среди групп
        result = ...  # TODO
        self.assertEquals(5, result['order__max'])

    def test_avg(self):
        # Получить среднее арифметическое для order
        result = ...  # TODO
        self.assertEquals(2.2, result['order__avg'])
