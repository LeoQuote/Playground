# Generated by Django 2.1.3 on 2018-11-16 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='is_complete',
            field=models.BooleanField(default=False, verbose_name='是否完整?'),
        ),
        migrations.AlterField(
            model_name='rule',
            name='been_triggered_for',
            field=models.IntegerField(default=0, verbose_name='触发次数'),
        ),
        migrations.AlterField(
            model_name='rule',
            name='last_triggered_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='上次触发时间'),
        ),
        migrations.AlterField(
            model_name='rule',
            name='last_triggered_by',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='response_text',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='响应文本'),
        ),
        migrations.AlterField(
            model_name='teleuser',
            name='is_bot',
            field=models.BooleanField(default=False, verbose_name='是机器人吗?'),
        ),
        migrations.AlterField(
            model_name='teleuser',
            name='status',
            field=models.CharField(default='start', max_length=32, verbose_name='现在所处模式'),
        ),
        migrations.AlterField(
            model_name='teleuser',
            name='status_since',
            field=models.DateTimeField(auto_now=True, verbose_name='进入模式时间'),
        ),
    ]
