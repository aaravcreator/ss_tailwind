from django.urls import path
from dashboard import views

app_name = "dashboard"
urlpatterns = [
    path("dashboard/",views.index,name="dashboard_index"),
    path("dashboard/manage_course",views.course_manager,name="manage_course"),
    path("dashboard/manage_course/add_course",views.add_course,name="add_course"),
    path("dashboard/edit_course/<int:id>",views.edit_course,name="edit_course"),
    path("dashboard/manage_course/<int:course_id>",views.manage_lesson,name="manage_lesson"),
    path("dashboard/manage_course/<int:course_id>/add_lesson",views.add_lesson,name="add_lesson"),
    path("dashboard/manage_course/<int:course_id>/edit_lesson/<int:lesson_id>",views.edit_lesson,name="edit_lesson"),
    path("dashboard/manage_quiz/<int:lesson_id>",views.manage_quiz,name="manage_quiz"),
    path("dashboard/manage_quiz/add_question/<int:quiz>",views.createquestion,name="createquestion"),
    path("dashboard/manage_question/<int:question>",views.manage_question,name="managequestion"),
    path("dashboard/manage_quiz/add_answer/<int:question>",views.createanswers,name="createanswers"),
    path("dashboard/manage_course/add_quiz/<int:lesson>",views.createquiz,name="createquiz"),
    path("dashboard/edit/question/<int:question>",views.editquestion,name="editquestion"),
    path("dashboard/edit/answer/<int:answer>",views.editanswer,name="editanswer"),
    path("dashboard/edit/quiz/<int:quiz>",views.editquiz,name="editquiz"),
    path("dashboard/delete/course/<int:course>",views.deletecourse,name="deletecourse"),
    path("dashboard/delete/lesson/<int:lesson>",views.deletelesson,name="deletelesson"),
    path("dashboard/delete/quiz/<int:quiz>",views.deletequiz,name="deletequiz"),
    path("dashboard/delete/question/<int:question>",views.deletequestion,name="deletequestion"),
    path("dashboard/delete/answer/<int:answer>",views.deleteanswer,name="deleteanswer"),
    path("dashboard/user/create",views.createuser,name="createuser"),
    path("dashboard/user/manage",views.manageuser,name="manageuser"),
    path("dashboard/user/edit/<int:user>",views.edituser,name="edituser"),
    path("dashboard/user/delete/<int:user>",views.deleteuser,name="deleteuser"),
    path("dashboard/tracklesson/",views.trackcourse,name = "trackcourse"),


]