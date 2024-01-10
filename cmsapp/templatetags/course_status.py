from django import template
from cmsapp.models import *

register = template.Library()
@register.filter()
def course_status(course,user):
    # lesson_ = lessons.objects.filter(slug = lessons)
    slug = course.slug
    # print(slug)
    course_ = Course.objects.filter(slug = slug).first()
    
    user_course_status =UserCourseStatus.objects.filter(course = course_,user = user).first()
    if course_.ispaid:
        if user_course_status and user_course_status.can_access ==True:
            return True
        else:
            return False
    else:
        return True
 