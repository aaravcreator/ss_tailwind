from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
# Register your models here.

from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'banner',
        'scheduled_date',
        'description',
        'location',
        'event_fee',
        'is_free',
        'seats',
        'rules',
        'syllabus',
        'status',
        'timestamp',
    )
    list_filter = ('scheduled_date', 'is_free', 'timestamp')
    search_fields = ('name',)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title', )}
class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class LessonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title', )}

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Quiz)
admin.site.register(Result)
admin.site.register(Course,CourseAdmin)
admin.site.register(lessons,LessonAdmin)
admin.site.register(Person)
admin.site.register(watch_later)
admin.site.register(category)
admin.site.register(Tracklesson)
admin.site.register(RequestProject)



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("username", "is_staff", "is_active","is_superuser","usertype","first_name","last_name","email")
    list_filter =("username", "is_staff", "is_active","is_superuser","usertype")
    fieldsets = (
        (None, {"fields": ("username", "password","usertype","first_name","last_name","email")}),
        ("Permissions", {"fields": ("is_staff", "is_active","is_superuser","groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "password1", "password2",'usertype', "is_staff",
                "is_active", "groups", "user_permissions","first_name","last_name","email"
            )}
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)
admin.site.register(User, CustomUserAdmin)