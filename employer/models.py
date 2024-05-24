import datetime
import humanize

from PIL import Image
from django.db import models
from django.utils import timezone
from django_jalali.db import models as jmodels

from portal.models import  User, Category


class Company(models.Model):
    employer = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    co_introduction = models.TextField()
    logo = models.ImageField(default='default.png', upload_to='co-logo')
    link  = models.CharField(max_length=80)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs)

        img = Image.open(self.logo.path)

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    title = models.CharField(max_length=80)
    location = models.CharField(max_length=80)
    created_date = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    experience_choices = (
        ('Нет опыта работы','Нет опыта работы'),
        ('1-3 года', '1-3 года'),
        ('3-6 года', '3-6 года'),
        ('6 и выше', '6 и выше'),
    )
    experience = models.CharField(max_length=80, choices=experience_choices)
    salary_choices = (
        ('Не указано', 'Не указано'),
        ('от 100 000 до 190 000 тг.', 'от 100 000 до 190 000 тг.'),
        ('от 200 000 до 290 000 тг.', 'от 200 000 до 290 000 тг.'),
        ('от 300 000 до 390 000 тг.', 'от 300 000 до 390 000 тг.'),
        ('от 400 000 до 490 000 тг.', 'от 400 000 до 490 000 тг.'),
        ('от 500 000 и выше', 'от 500 000 и выше'),
    )
    salary = models.CharField(
        max_length=80, choices=salary_choices
    )
    cooperation_choices = (
        ('Полная занятость', 'Полная занятость'),
        ('Частичная занятость', 'Частичная занятость'),
        ('Удаленная работа', 'Удаленная работа'),
        ('Стажировка', 'Стажировка'),
        ('Производственная практика', 'Производственная практика'),
    )
    cooperation_type = models.CharField(
        max_length=80, choices=cooperation_choices
    )
    job_description = models.TextField()
    skills_required = models.CharField(max_length=80)
    '''
    military_choices = (
        ('Военнообязанный', 'Военнообязанный'),
        ('Есть военный билет', 'Есть военный билет'),
    )
    military_service = models.CharField(
        max_length=80, choices=military_choices
    )
    '''
    degree_choices = (
        ('Не имеет значения', 'Не имеет значения'),
        ('Диплом ТиПО', 'Диплом ТиПО'),
        ('Диплом бакалавра', 'Диплом бакалавра'),
        ('Диплом магистра', 'Диплом магистра'),
        ('Диплом Phd', 'Диплом Phd'),
    )
    degree = models.CharField(max_length=80, choices=degree_choices)

    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
    
    
class JobRequests(models.Model):
    employer = models.ForeignKey(Company, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume_url = models.CharField(max_length=100)
    accepted = models.BooleanField(default=False)
    hired = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Запрос компании {self.jobseeker} на работу {self.job}'
    
    def save(self, *args, **kwargs):
        super(JobRequests, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Запрос на вакансию"
        verbose_name_plural = "Запросы на вакансию"

    