# Generated by Django 2.0.7 on 2018-07-17 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180717_0939'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answered_by',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='asked_by',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]