# Generated by Django 5.1.1 on 2024-09-22 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('themes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='blue',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='theme',
            name='green',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='theme',
            name='red',
            field=models.IntegerField(default=0),
        ),
    ]