# Generated by Django 2.0.2 on 2018-08-13 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('millionaire', '0003_choice_answer_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='is_answer',
            field=models.BooleanField(),
        ),
    ]
