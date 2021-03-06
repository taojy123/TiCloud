# Generated by Django 2.1.4 on 2020-03-05 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_auto_20200304_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerregisterapply',
            name='category',
            field=models.IntegerField(default=1, help_text='1 内部用户； 2 外部用户', verbose_name='用户类型'),
        ),
        migrations.AlterField(
            model_name='user',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='上级主管'),
        ),
    ]
