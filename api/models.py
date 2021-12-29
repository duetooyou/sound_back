from django.db import models
from django.contrib.auth import get_user_model


class ActiveCompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active_now=True) 


class StudioManager(models.Manager):
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs).select_related('company__owner')

    def all(self, *args, **kwargs):
        return super().all(*args, **kwargs).select_related('company__owner')


class RecordsManager(models.Manager):
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs).select_related('studio__company__owner')

    def all(self, *args, **kwargs):
        return super().all(*args, **kwargs).select_related('studio__company__owner')


class Company(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Название компании',
                            unique=True)
    owner = models.OneToOneField(get_user_model(),
                                 related_name='companies',
                                 on_delete=models.CASCADE,
                                 verbose_name='Владелец компании')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Время создания')
    active_now = models.BooleanField(default=True,
                                     verbose_name='Активна на сайте')
    company_logo = models.ImageField(upload_to='companies',
                                     verbose_name="Логотип",
                                     blank=True)

    objects = models.Manager()
    active = ActiveCompanyManager()

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Список компаний'

    def __str__(self):
        return f'{self.name}'


class Studio(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Название студии',
                            unique=True
                            )
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                related_name='studios',
                                verbose_name='Лэйбл')
    city = models.CharField(max_length=25,
                            verbose_name='Город')
    address = models.TextField(max_length=200,
                               verbose_name='Адрес')

    objects = StudioManager()

    class Meta:
        ordering = ('company', 'city', 'name')
        verbose_name = 'Студия'
        verbose_name_plural = 'Список студий'
        unique_together = ('name', 'city', 'address')

    def __str__(self):
        return f'{self.company} - {self.name}'


class Record(models.Model):
    studio = models.ForeignKey(Studio,
                               on_delete=models.CASCADE,
                               related_name='records')
    start_recording = models.DateTimeField(verbose_name='Старт записи')
    end_recording = models.DateTimeField(verbose_name='Конец записи')
    duration = models.DurationField(verbose_name='Длительность')
    cost = models.PositiveSmallIntegerField(verbose_name='Стоимость часа записи')
    session_cost = models.PositiveIntegerField(verbose_name='Стоимость сеанса')

    objects = RecordsManager()

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Таблица записи'

    def __str__(self):
        return f'{self.studio} {self.cost} {self.session_cost} {self.start_recording.date()}'
