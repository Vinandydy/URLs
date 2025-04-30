from .base import BaseORMTestCase


class TestAnnotate(BaseORMTestCase):
    def test_simple_annotate(self):
        # Составить дополнительное "поле" из значений других полей групп с помощью .annotate() и Value():
        # ИМЯ + '' + order, например 'Ремонт__5'
        groups = ...  # TODO

        for group in groups:
            self.assertEquals(f'{group.name}__{group.order}', group.str_repr)
            print(group.str_repr)

    def test_alias(self):
        # Сделать то же самое, а потом отфильтровать группы, у которых дополнительное поле равно 'Важное__0'
        # Назвать это поле 'str_repr'
        # Использовать .alias()
        groups = ...  # TODO

        self.assertEquals(1, groups.count())
        self.assertFalse(hasattr(groups.first(), 'str_repr'))

    def test_annotate(self):
        # Получить мин. и макс значение order для групп, используя .aggregate()
        result = ...  # TODO

        # Сделать выборку всех групп и дописать к ней аннотации: min_order и max_order (взять из result)
        groups = ...

        for group in groups:
            self.assertTrue(hasattr(group, 'min_order'))
            self.assertTrue(hasattr(group, 'max_order'))
