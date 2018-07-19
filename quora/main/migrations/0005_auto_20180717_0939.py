# Generated by Django 2.0.7 on 2018-07-17 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180717_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='downvotes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='answer',
            name='upvotes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='downvotes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='upvotes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]