from django.db import models


class Subscription(models.Model):
    title = models.CharField('Название', max_length=100)
    classname = models.CharField('classname', max_length=100, default='')
    price = models.IntegerField('Цена (месяц)')
    description = models.TextField('Описание (список преимуществ через ;)')
    stripe_price = models.CharField('Stripe Price', default='', max_length=100,blank=True)

    custom_domain = models.BooleanField('Custom Domain', default=False, blank=False)
    random_domain = models.BooleanField('Random Domain', default=False, blank=False)
    seo_integration = models.BooleanField('SEO Integration', default=False, blank=False)
    free_website_hosting = models.BooleanField('free website hosting', default=False, blank=False)
    web_page_limit = models.IntegerField('web page limit', default=0, blank=True)
    logo_gen_limit = models.IntegerField('logo gen limit', default=0, blank=True)
    image_gen_limit = models.IntegerField('image gen limit', default=0, blank=True)
    seokeyword_gen_limit = models.IntegerField('seokeyword gen limit', default=0, blank=True)
    content_gen_limit = models.IntegerField('content gen limit', default=0, blank=True)


    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['id']

    def __str__(self):
        return self.title

    def get_text(self):
        return self.description.split(';') 


class Payment(models.Model):
    subscription_id = models.CharField('ID подписки', max_length=255)
    date = models.DateTimeField('Дата окончания')
    canceled = models.BooleanField('Отменен', default=False)

    user = models.ForeignKey('user.User', verbose_name='Пользователь', on_delete=models.SET_NULL, null=True)
    subscription_object = models.ForeignKey('Subscription', verbose_name='Подписка', on_delete=models.PROTECT)

    def __str__(self):
        return self.subscription_object.title

    def get_date(self):
        return self.date.strftime('%d.%m.%Y')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

