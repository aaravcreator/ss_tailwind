from django import template
from cmsapp.models import *

register = template.Library()

@register.filter()
def is_verified(lesson,user):
    # lesson_ = lessons.objects.filter(slug = lessons)
    slug = lesson.slug
    print(slug)
    lesson_ = lessons.objects.filter(slug = slug).first()
    
    if lesson_.lesson_number == 1:
        return True
    else:
        lesson_number = lesson_.lesson_number
        # course = lesson_.Course
        lesson1 = lessons.objects.filter(Course = lesson_.Course,lesson_number = lesson_number-1).first()
        quiz = Quiz.objects.filter(course = lesson_.Course,lessons = lesson1).first()
        result = Result.objects.filter(user = user,quiz = quiz).first()
        if result:
            if result.passed:
                return True
            else:
                return False
        elif lesson_.is_locked == False:
            return True
        else:
            return False
 


    
    
    