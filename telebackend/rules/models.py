from django.db import models

# Create your models here.

class TeleUser(models.Model):
    tele_id = models.CharField('Telegram ID', max_length=32)    
    first_name = models.CharField('First Name', max_length=32)
    last_name = models.CharField('Last Name', max_length=32)
    username = models.CharField('用户名', max_length=128)
    is_bot = models.BooleanField('是机器人吗?',default= False)
    json_data = models.CharField('json data', max_length=1024)
    status = models.CharField('现在所处模式', max_length=32, default='start')
    status_since = models.DateTimeField('进入模式时间', auto_now=True)
    added_at = models.DateTimeField('加入时间', auto_now_add=True)
    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    

class Rule(models.Model):
    trigger_text = models.CharField('触发文本', max_length=32)
    response_text = models.CharField('响应文本', max_length=128, blank=True, null=True)
    been_triggered_for = models.IntegerField('触发次数', default=0)
    last_triggered_at = models.DateTimeField('上次触发时间', blank=True, null=True)
    last_triggered_by = models.CharField(max_length=128, blank=True, null=True)
    is_complete = models.BooleanField('是否完整?',default=False)
    added_by = models.CharField('添加用户', max_length=128)
    added_at = models.DateTimeField('添加时间', auto_now_add=True)



    def __str__(self):
        return self.trigger_text

    def __unicode__(self):
        return self.trigger_text
