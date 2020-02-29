# Generated by Django 3.0.3 on 2020-02-29 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_auto_20200226_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, help_text='唯一标识，编码规则中指定关联的申请记录id', max_length=128, unique=True, verbose_name='工单号')),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='任务主题')),
                ('creator', models.CharField(blank=True, max_length=32, verbose_name='申请人姓名')),
                ('creator_department', models.CharField(blank=True, max_length=64, verbose_name='申请人部门')),
                ('creator_job', models.CharField(blank=True, max_length=32, verbose_name='申请人职位')),
                ('status', models.CharField(blank=True, max_length=32, verbose_name='工单状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.AlterField(
            model_name='vendorapiapply',
            name='cache_ms',
            field=models.IntegerField(default=0, help_text='必填', verbose_name='缓存时间/毫秒'),
        ),
        migrations.AlterField(
            model_name='vendorapiapply',
            name='timeout_ms',
            field=models.IntegerField(default=0, help_text='必填', verbose_name='超时时间/毫秒'),
        ),
        migrations.CreateModel(
            name='TicketFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField(default=0, verbose_name='流程次序')),
                ('handler_name', models.CharField(blank=True, max_length=32, verbose_name='审批人')),
                ('result', models.CharField(blank=True, max_length=32, verbose_name='审批结果')),
                ('content', models.TextField(blank=True, verbose_name='审批意见')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.Ticket', verbose_name='工单')),
            ],
        ),
    ]
