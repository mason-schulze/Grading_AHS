from stu_response.models import Lesson
from django.contrib import admin


class LessonAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)

admin.site.register(Lesson, LessonAdmin)