import django_filters
from django_filters import CharFilter,BooleanFilter,NumberFilter
from .models import Course
from django.conf import settings

class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = ['title','category',]

# class UserFilter(django_filters.FilterSet):
#     first_name = CharFilter(field_name='first_name', label='First Name',lookup_expr='icontains')
#     last_name = CharFilter(field_name='last_name',label='Last Name', lookup_expr='icontains')
#     contact = CharFilter(field_name='contact', label='Contact',lookup_expr='icontains')
#     email = CharFilter(field_name='email',label='Email', lookup_expr='icontains')
#     class Meta:
#         model = CustomUser
#         fields = ['first_name','last_name','contact','email']