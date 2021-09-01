# Generated by Django 3.2.7 on 2021-09-01 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.AlterField(
            model_name='company',
            name='category',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='portal.category'),
        ),
        migrations.AlterField(
            model_name='job',
            name='category',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='portal.category'),
        ),
    ]
