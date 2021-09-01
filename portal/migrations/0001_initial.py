# Generated by Django 3.2.7 on 2021-09-01 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('co_introduction', models.TextField()),
                ('logo', models.ImageField(default='default.jpg', upload_to='company_logo')),
                ('category', models.CharField(max_length=80)),
                ('link', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('category', models.CharField(max_length=80)),
                ('location', models.CharField(max_length=80)),
                ('experience', models.CharField(max_length=80)),
                ('salary', models.IntegerField()),
                ('cooperation_type', models.CharField(max_length=80)),
                ('job_description', models.CharField(max_length=80)),
                ('skills_required', models.CharField(max_length=80)),
                ('military_service', models.CharField(max_length=80)),
                ('degree', models.CharField(max_length=80)),
                ('gender', models.CharField(choices=[('Male', 'مرد'), ('Female', 'زن'), ('not-matter', 'مهم نیست')], max_length=10)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='portal.company')),
            ],
        ),
    ]