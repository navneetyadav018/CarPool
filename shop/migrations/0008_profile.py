# Generated by Django 5.0.4 on 2024-05-13 13:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_delete_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('corporate', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('my_skills', models.CharField(default='software development', max_length=50)),
                ('needed_skills', models.TextField(default='software development', max_length=50)),
                ('free_time', models.TimeField()),
                ('bio', models.CharField(default=1, max_length=200)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('image', models.ImageField(upload_to='profiles')),
                ('age', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]