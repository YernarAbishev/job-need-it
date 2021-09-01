# Generated by Django 3.2.7 on 2021-09-01 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210901_0811'),
        ('portal', '0003_company_employer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='employer',
            field=models.OneToOneField(default=False, on_delete=django.db.models.deletion.CASCADE, to='users.jobseeker'),
        ),
    ]
