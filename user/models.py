from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    reset_password_code = models.CharField('Код сброса пароля', max_length=100, default='', blank=True)
    chosen_landing = models.ForeignKey('landing.Landing', verbose_name='Выбранный лэндинг', on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='users')
    subscription = models.ForeignKey('payments.Payment', verbose_name='Подписка', on_delete=models.SET_NULL, null=True, related_name='active_users')

    logo_gen_count = models.IntegerField('Logo Gen Count', default=0, blank=True)
    image_gen_count = models.IntegerField('Image Gen Count', default=0, blank=True)
    seokeyword_gen_count = models.IntegerField('Seokeyword Gen Count', default=0, blank=True)
    content_gen_count = models.IntegerField('Content Gen Count', default=0, blank=True)

    projectsCount = models.IntegerField('Projects Count', default=0, blank=True)

    source = models.CharField('How did you come to know about us?',null=True, max_length=255, default='', blank=True)

    generated_Images = models.JSONField(default=list, blank=True)
    generated_Images_Logo = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"Mail id: {self.email} ---  Current Plan: {'FREE' if self.subscription  is None else self.subscription}"

    def get_projects_count(self):
        return len(self.landings.all())

    def is_subscribe(self):
        if self.email == 'admin@admin.com':
            return True
        else:
            return self.subscription and self.subscription.date > timezone.now() and not self.subscription.canceled
