from django.db import models


# Create your models here.

class Url(models.Model):
    url = models.URLField(blank=False, null=False, unique=True, verbose_name='Ссылка')
    name = models.CharField(max_length=128, blank=False, null=False, unique=True, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, unique=False, verbose_name='Описание')
    favicon = models.ImageField(blank=True, null=True, unique=False, verbose_name='Иконка')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'url'
        verbose_name = 'Сайт'
        verbose_name_plural = "Сайты"


    def __str__(self):
        return self.url