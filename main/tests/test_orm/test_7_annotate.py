from django.db.models.functions import Concat
from django.db.models import Value, CharField, Min, Max, IntegerField
from .base import BaseORMTestCase
from ...models import Group


class TestAnnotate(BaseORMTestCase):
    #Не очень понял, на что warning кидает
    def test_simple_annotate(self):
        # Составить дополнительное "поле" из значений других полей групп с помощью .annotate() и Value():
        # ИМЯ + '' + order, например 'Ремонт__5'
        groups = Group.objects.annotate(
            str_repr = Concat('name', Value("__"), 'order', output_field=CharField())
        )

        for group in groups:
            self.assertEquals(f'{group.name}__{group.order}', group.str_repr)
            print(group.str_repr)

    #Получается annotate такое сделать не позволит, а alias более гибкий
    def test_alias(self):
        # Сделать то же самое, а потом отфильтровать группы, у которых дополнительное поле равно 'Важное__0'
        # Назвать это поле 'str_repr'
        # Использовать .alias()
        groups = Group.objects.alias(
            str_repr = Concat('name', Value("__"), 'order', output_field=CharField())
        ).filter(str_repr__exact='Важное__0')

        self.assertEquals(1, groups.count())
        self.assertFalse(hasattr(groups.first(), 'str_repr'))

    #Наверно тут все же идея в том, чтобы потренироваться получать данные из агрегации например, а потом в аннотации использовать,
    #Все же это можно и только в annotate сделать
    def test_annotate(self):
        # Получить мин. и макс значение order для групп, используя .aggregate()
        result = Group.objects.aggregate(min_order=Min('order'), max_order=Max('order'))

        # Сделать выборку всех групп и дописать к ней аннотации: min_order и max_order (взять из result)
        groups = Group.objects.annotate(
            min_order=Value(result['min_order'], output_field=IntegerField()),
            max_order=Value(result['max_order'], output_field=IntegerField())
        )

        for group in groups:
            self.assertTrue(hasattr(group, 'min_order'))
            self.assertTrue(hasattr(group, 'max_order'))
