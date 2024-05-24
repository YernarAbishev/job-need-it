from django import forms

from .models import Company, Job, Category


class EmployerProfileForm(forms.ModelForm):

    class Meta:
        model = Company
        fields=['category', 'name', 'co_introduction', 'logo', 'link']

    def __init__(self, *args, **kwargs):
        super(EmployerProfileForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Укажите чем занимается ваша компания"
        self.fields['name'].label = "Название компании"
        self.fields['co_introduction'].label = "Представьте свою компанию"
        self.fields['logo'].label = "Загрузите логотип"
        self.fields['link'].label = "Введите ссылку на сайт компании"

class EmployerJobCreationForm(forms.ModelForm):
    
    class Meta:
        model = Job
        fields = [
            'category', 'title', 'location',
            'experience', 'salary', 'cooperation_type',
            'job_description', 'skills_required',
            'degree',
        ]
    
    def __init__(self, *args, **kwargs):
        super(EmployerJobCreationForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Выберите сферу деятельности"
        self.fields['title'].label = "Введите названия вакансии"
        self.fields['location'].label = "Введите местоположение вашей компании"
        self.fields['experience'].label = "Требуемый опыт работы"
        self.fields['salary'].label = "Заработная плата"
        self.fields['cooperation_type'].label = "Занятость"
        self.fields['job_description'].label = "Описание работы"
        self.fields['skills_required'].label = "Требуемые навыки"
        self.fields['degree'].label = "Образование"



