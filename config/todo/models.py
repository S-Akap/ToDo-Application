from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Class(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザーID')
    lecture_name = models.CharField(max_length=100, verbose_name='講義名')
    instructor = models.CharField(max_length=50, verbose_name='担当教諭')
    contact_info = models.EmailField(verbose_name='連絡先')

    def __str__(self):
        return self.lecture_name

class Task(models.Model):
    class_reference = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='講義ID')
    title = models.CharField(max_length=100, verbose_name='タイトル')
    content = models.TextField(verbose_name='内容')
    due_date = models.DateField(verbose_name='期日')
    submission_place = models.CharField(max_length=100, verbose_name='提出先')
    is_completed = models.BooleanField(default=False, verbose_name='完了済み')

    def __str__(self):
        return self.title