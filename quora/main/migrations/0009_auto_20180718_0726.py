# Generated by Django 2.0.7 on 2018-07-18 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20180718_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='votes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='votes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]