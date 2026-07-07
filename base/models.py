from django.db import models
from django.utils import timezone

def current_year():
    return timezone.now().year

class Setting(models.Model):
    email = models.TextField('Email обратной связи (через ;)', default='', blank=True)

    main_title = models.CharField('Заголовок', max_length=100, blank=True)
    main_text = models.TextField('Описание', blank=True)
    button_text = models.TextField('Текст кнопки', blank=True)
    video = models.CharField('Ссылка на видео (YouTube)', max_length=255, blank=True)

    youtube = models.CharField('Youtube', blank=True, default='', max_length=255)
    twitter = models.CharField('Twitter', blank=True, default='', max_length=255)
    instagram = models.CharField('Instagram', blank=True, default='', max_length=255)
    facebook = models.CharField('Facebook', blank=True, default='', max_length=255)
    footer_text = models.TextField('Текст в футере', default='', blank=True)
    copyright = models.CharField('Copyright', max_length=100, default='', blank=True)
    
    def save(self, *args, **kwargs):
        self.copyright = f"Copyright © {current_year()} LandlyAI."
        super().save(*args, **kwargs)


    about_title = models.CharField('Заголовок о нас', max_length=100, default='', blank=True)
    about_sub_title = models.CharField('Подзаголовок о нас', max_length=100, default='', blank=True)
    about_text = models.TextField('Описание о нас', default='', blank=True)

    pricing_title = models.CharField('Заголовок подписок', max_length=100, default='', blank=True)
    pricing_sub_title = models.CharField('Подзаголовок подписок', max_length=100, default='', blank=True)

    statistics_text = models.TextField('Статистика', default='', blank=True)

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return 'Настройки'

    def get_statistics(self):
        stat_list = []
        for stat in self.statistics_text.split(';'):
            stat_list.append({
                "title": stat.split(':')[0],
                "value": stat.split(':')[1],
            })
        return stat_list

    def get_email(self):
        return self.email.split(';')

    @staticmethod
    def get_settings():
        settings = Setting.objects.all()
        if settings:
            return settings[0]
        else:
            settings = Setting()
            settings.save()
            return settings


class Faq(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    text = models.TextField('Текст')
    sort = models.IntegerField('Сортировка', default=0)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ('-sort', '-id',)

    def __str__(self):
        return self.title


class Contact(models.Model):
    class Type(models.TextChoices):
        phone = 'phone', 'Телефон'
        email = 'email', 'Почта'
        address = 'address', 'Адрес'

    type = models.CharField('Тип', max_length=12, choices=Type.choices, default=Type.phone)
    text = models.TextField('Текст')
    sort = models.IntegerField('Сортировка', default=0)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакт'
        ordering = ('-sort', '-id',)

    def __str__(self):
        return self.text


class Page(models.Model):
    title = models.CharField('Название', max_length=100)
    slug = models.CharField('Код', max_length=100)
    text = models.TextField('Текст')

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return self.title


class subscriberList(models.Model):
    email = models.CharField('email', max_length=100)

    class Meta:
        verbose_name = 'Subscriber List'
        verbose_name_plural = 'Subscriber List'

    def __str__(self):
        return self.email