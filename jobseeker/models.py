from django.db import models

from employer.models import Job
from portal.models import User
from django.urls import reverse

class JobSeekerProfile(models.Model):
    jobseeker = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    resume = models.FileField(null=True, upload_to='user_resume')
    
    def __str__(self):
        return f'Профиль - {self.jobseeker}'


    class Meta:
        verbose_name = "Профиль соискателя"
        verbose_name_plural = "Профиль соискателей"
    

class JobSeekerRequests(models.Model):
    requests = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=80, default="Ожидание встречи с работодателем")    

    def __str__(self):
        return f'{self.requests} Запрос на работу {self.job}'
    
    def save(self, *args, **kwargs):
        super(JobSeekerRequests, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Запрос соискателя"
        verbose_name_plural = "Запросы соискателя"


class JobSeekerSaveJob(models.Model):
    saved_job = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.saved_job}'
    
    def save(self, *args, **kwargs):
        super(JobSeekerSaveJob, self).save(*args, **kwargs)

    
    class Meta:
        verbose_name = "Сохраненная вакансия"
        verbose_name_plural = "Сохраненные вакансии"