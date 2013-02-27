# coding: utf-8

import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from easy_thumbnails.fields import ThumbnailerImageField

USER_TYPE = (
    ('advertiser', u'Рекламодатель'),
    ('agent', u'Агент')
)
WORK_TYPE_CHOICES = (
    ('blog_publication', u'Публикация в блоге'),
)
TONALITY_CHOICES = (
    ('soft', u'Мягкая'),
)
PLATFORM_SUBJECTS_CHOICES = (
    ('sub1', u'Заголовок1'),
)
PLATFORM_STATUS_CHOICES = (
    ('activation', u'активация'),
    ('active', u'активная'),
    ('nonactive', u'не активная'),
    ('reject', u'отклонена'),
)
TASK_STATUS_CHOICES = (
    ('checkout', u'на проверке'),
    ('performed', u'выполняется'),
    ('refine', u'доработать'),
    ('payable',u'оплачивается'),
    ('reject',u'отказаться'),
)
MESSAGE_SECTION_CHOICES = (
    ('technical', u'Технический раздел'),
    ('system', u'События системы'),
    ('admin', u'Администрация'),
)
MESSAGE_STATUS_CHOICES = (
    ('open', u'Открыт'),
    ('processing', u'В процессе'),
    ('close', u'Закрыт'),
)
PAYMENT_TYPE_CHOICES = (
    ('in', u'Введено денег'),
    ('out', u'Вывод денег'),
)
BALANCE_STATUS_CHOICES = (
    ('reject', u'Отклонено'),
    ('process', u'В процессе'),
    ('receive', u'Принято'),
)
PAYMENT_SYSTEM_CHOICES = (
    ('webmoney', u'Webmoney'),
    ('yandex', u'Yandex.Деньги'),
    ('robocassa', u'Robocassa'),
    ('noncash', u'Безналичный расчет'),
)
TAXATION_CHOICES = (
    ('osn', u'ОСН'),
    ('ysn', u'УСН '),
)
USER_TYPE_CHOICES = (
    ('agent', u'Агент'),
    ('advertiser', u'Рекламодатель '),
)
LIST_CHOICES = (
    ('black', 'black'),
    ('white', 'white'),
)
FAVOURITE_CHOICES = (
    ('agent', 'agent'),
    ('platform', 'platform'),
)
REQUEST_FOR_COMPANY_CHOICES = (
    ('stat1', u'Статус'),
)
TRANSFER_STATUS_CHOISES = (
    ('unverified', u'unverified'),
    ('verified', u'verfied'),
    ('rejected', u'rejected'),
)
INVITATION_STATUS_CHOISES = (
    ('new', u'new'),
    ('approve', u'approve'),
    ('reject', u'reject'),
)

class Country(models.Model):
    name = models.CharField(max_length=20)

class Town(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=20)

class UserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have an password')

        user = User(email=UserManager.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password
        )

        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    type = models.CharField(choices=USER_TYPE, max_length=12)
    name = models.CharField(max_length=24, blank=True)
    surname = models.CharField(max_length=24, blank=True)
    town = models.ForeignKey(Town, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    phone = models.CharField(max_length=24, blank=True)
    skype = models.CharField(max_length=24, blank=True)
    icq = models.PositiveIntegerField(blank=True, null=True)
    photo = ThumbnailerImageField(upload_to='photos', resize_source={'size': (180, 190), 'crop': True}, blank=True)
    about = models.TextField(max_length=200, blank=True)
    birthday = models.DateField(blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    rating = models.FloatField(default=0)
    balance = models.FloatField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __unicode__(self):
        return self.email

class Review(models.Model):
    added = models.DateTimeField(auto_now_add=True, verbose_name=u'Добавлен')
    text = models.TextField(verbose_name=u'Текст')
    user = models.ForeignKey(User, related_name='reviews', verbose_name=u'Пользователь')
    reviewer = models.ForeignKey(User, verbose_name=u'Автор')
    type = models.SmallIntegerField()

    class Meta:

        verbose_name = u'Отзыв'
        verbose_name_plural = u'Отзывы'

    def __unicode__(self):
        return u'Отзыв для %s от %s' % (self.user, self.reviewer)

class UserList(models.Model):
    user = models.ForeignKey(User, related_name='user_list')
    date_added = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=LIST_CHOICES, max_length=5)
    object = models.ForeignKey(User)

class Favoutite(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=FAVOURITE_CHOICES, max_length=8)
    object = models.ForeignKey(User, related_name='favourite')

class Tags(models.Model):
    name = models.CharField(max_length=15)

class CampaignPurpose(models.Model):
    name = models.CharField(max_length=35)

class CampaignBlog(models.Model):
    name = models.CharField(max_length=35)

class AdvertisingCampaign(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    max_task_count = models.IntegerField()
    period = models.IntegerField()
    tags = models.ManyToManyField(Tags)
    sum = models.FloatField()
    purpose = models.ManyToManyField(CampaignPurpose)

class CampaignTask(models.Model):
    campaign = models.ForeignKey(AdvertisingCampaign)
    work_type = models.CharField(choices=WORK_TYPE_CHOICES, max_length=20)
    sum = models.FloatField()
    text_size = models.IntegerField()
    tags = models.ManyToManyField(Tags)
    blog = models.ManyToManyField(CampaignBlog)
    tonality = models.CharField(choices=TONALITY_CHOICES, max_length=15)
    exec_count = models.IntegerField()
    link_video = models.URLField(max_length=100)
    link_img = models.URLField(max_length=100)
    link_address = models.URLField(max_length=100)
    link_text = models.CharField(max_length=25)

class PlatformType(models.Model):
    name = models.CharField(max_length=30)

class PlatformApplication(models.Model):
    name = models.CharField(max_length=15)

class AdvertisingPlatform(models.Model):
    user = models.ForeignKey(User)
    address = models.CharField(max_length=40)
    type = models.ManyToManyField(PlatformType)
    user_name = models.CharField(max_length=30)
    application = models.ManyToManyField(PlatformApplication)
    description = models.TextField(max_length=1000)
    subject = models.CharField(choices=PLATFORM_SUBJECTS_CHOICES, max_length=10)
    country = models.ForeignKey(Country)
    tags = models.ManyToManyField(Tags)
    create_date = models.DateTimeField(auto_now=True)
    statistic_password = models.CharField(max_length=128)
    comment_summ = models.FloatField()
    publication_summ = models.FloatField()
    status = models.CharField(choices=PLATFORM_STATUS_CHOICES, max_length=10, default='activation')
    activated_link = models.URLField(blank=True,null=True)

class PaymentSystem(models.Model):
    name = models.CharField(choices=PAYMENT_SYSTEM_CHOICES, max_length=15)

class AgentPurse(models.Model):
    user = models.ForeignKey(User, related_name='user_purse')
    name = models.CharField(max_length=20,unique=True)
    system = models.ForeignKey(PaymentSystem)

class AgentTask(models.Model):
    customer = models.ForeignKey(User, related_name='customer')
    platform = models.ForeignKey(AdvertisingPlatform, related_name='platform')
    user = models.ForeignKey(User, related_name='user')
    status = models.CharField(choices=TASK_STATUS_CHOICES, max_length=10)
    task = models.ForeignKey(CampaignTask)
    last_event = models.DateTimeField(auto_now=True)
    date_start = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField()
    paid = models.BooleanField()

class Invitation(models.Model):
    campaign = models.ForeignKey(AdvertisingCampaign)
    platform = models.ForeignKey(AdvertisingPlatform)
    task = models.ForeignKey(CampaignTask)
    status = models.CharField(INVITATION_STATUS_CHOISES,max_length=10)

class Message(models.Model):
    section = models.CharField(choices=MESSAGE_SECTION_CHOICES, max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)
    last_answer = models.DateTimeField(auto_now=True,default=datetime.datetime.now)
    sender = models.ForeignKey(User, related_name='sender_user')
    receiver = models.ForeignKey(User, related_name='receiver_user', null=True, blank=True)
    watched = models.BooleanField(default=0)
    title = models.CharField(max_length=100)
    msg = models.TextField(max_length=500)
    status = models.CharField(choices=MESSAGE_STATUS_CHOICES, max_length=10)

class MessageReview(models.Model):
    message = models.ForeignKey(Message)
    sender = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True)
    msg = models.TextField(max_length=500)

class Balance(models.Model):
    user = models.ForeignKey(User, related_name='user_balance')
    type = models.CharField(choices=PAYMENT_TYPE_CHOICES, max_length=3)
    status = models.CharField(choices=BALANCE_STATUS_CHOICES, max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    balance_before = models.FloatField()
    sum = models.FloatField()
    balance_after = models.FloatField()
    system = models.ForeignKey(PaymentSystem)
    purse = models.ForeignKey(AgentPurse, blank=True, null=True) #кошелек

class NonCashPayment(models.Model):
    type = models.CharField(choices=PAYMENT_TYPE_CHOICES, max_length=3)
    taxation = models.CharField(choices=TAXATION_CHOICES, max_length=3)
    agency = models.CharField(max_length=50)
    fio = models.CharField(max_length=90)
    basis = models.CharField(max_length=50)
    position = models.CharField(max_length=40)
    post_address = models.CharField(max_length=80)
    requisites = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=11)
    sum = models.FloatField()

class MoneyTransfer(models.Model):
    user = models.ForeignKey(User, related_name='money_transfer')
    date_added = models.DateTimeField(auto_now_add=True)
    date_treatment = models.DateTimeField(blank=True,null=True)
    sum = models.FloatField()
    percent = models.FloatField()
    total_sum = models.FloatField()
    purse = models.ForeignKey(AgentPurse, blank=True,null=True) #кошелек
    type = models.CharField(choices=PAYMENT_TYPE_CHOICES, max_length=3)
    status = models.CharField(choices=TRANSFER_STATUS_CHOISES, max_length=10, default='unverified')
    system = models.ForeignKey(PaymentSystem)
    noncash = models.ForeignKey(NonCashPayment, blank=True, null=True)

class RequestForCompany(models.Model):
    user = models.ForeignKey(User, related_name='agent')
    sender = models.ForeignKey(User, related_name='advertiser')
    date_added = models.DateTimeField(auto_now_add=True)
    platform = models.CharField(max_length=40)
    description = models.TextField(max_length=1000)
    sum = models.FloatField()
    status = models.CharField(choices=REQUEST_FOR_COMPANY_CHOICES, max_length=12)