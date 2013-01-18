from stu_response.models import Lesson, Response, Question
from django.contrib import admin


def get_num_completed(obj):
    return obj.questions.all().count()
get_num_completed.short_description = "Total Questions"


def get_full_name_display(obj):
    return obj.creator.get_full_name() + " (" + obj.creator.username + ")"
get_full_name_display.short_description = "Creator"


class LessonAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)
    date_hierarchy = 'last_edit_date'
    exclude = ('recorded_responses', )
    list_display = ("name", get_full_name_display, "last_edit_date", get_num_completed)
    readonly_fields = ("key", )
    search_fields = ['name', 'creator__username', 'creator__first_name', 'creator__first_name', 'questions__text']

admin.site.register(Lesson, LessonAdmin)


class ResponseAdmin(admin.ModelAdmin):
    date_hierarchy = 'edit_date'

admin.site.register(Response, ResponseAdmin)


class QuestionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question, QuestionAdmin)
