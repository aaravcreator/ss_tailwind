
from django.urls import path
from . import views

from .new_view import *

urlpatterns = [
    # path('',views.index,name= 'home'), 
    path('',tw_view,name='home'),
    path('event_detail/<int:id>/',event_detail,name='event_detail'),
    path('course/<str:slug>/<str:lesson_slug>',views.course,name ='course_lesson'),
    path('course/<str:slug>/',views.course_index,name ='course'),
    path('login/',views.signin,name='login'),
    path('signup/',views.register,name = 'register'),
    path('coursecreate/',views.createcourse,name = "createcourse"),
    # path('token_send/',views.token_send,name = 'tokensend'),
    # path('verify/<auth_token>',views.verify,name = 'verify'),
    path('error/',views.error,name = 'error'),
    path('logout/',views.user_logout,name='logout'),
    # path('logout/',views.user_logout,name = 'logout'),
    path('watchlater/',views.watchlater,name = 'readlater'),
    path('delete/<pk>/',views.delete_watchlater,name = 'delete'),
    path('deleteCourse/<pk>/',views.delete_watchlater_from_home,name = 'deleteCourse'),
    path('quiz/<course>/<lesson>/',views.quiz_view,name = "quiz_view"),
    path('quiz/<course>/<lesson>/data/',views.quiz_data_view,name= 'quiz-data-view'),
    path('quiz/<course>/<lesson>/save/',views.save_quiz_view,name= 'save_quiz_view'),
    path('request/',views.requestproject,name = "requestproject"),
    path('token_send/',views.token_send,name = 'tokensend'),
    path('verify/<auth_token>',views.verify,name = 'verify'),
    path("seachCourse/",views.liveSearch,name = "liveSearch")
    

]
