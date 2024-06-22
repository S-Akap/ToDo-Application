from django.contrib import admin

# Register your models here.

from . import models

class TaskInline(admin.StackedInline):
    model = models.Task
    extra = 1  # 表示される空のフォームの数を指定

@admin.register(models.Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lecture_name', 'instructor', 'contact_info')
    search_fields = ('lecture_name', 'instructor')
    list_filter = ('user',)
    inlines = [TaskInline]

@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_reference', 'title', 'due_date', 'submission_place', 'is_completed')
    search_fields = ('title', 'content')
    list_filter = ('is_completed', 'due_date', 'class_reference')
