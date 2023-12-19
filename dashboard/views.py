from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q

from cmsapp.forms import CourseForm, LessonForm, QuizForm, QuestionForm, AnswerForm
from cmsapp.filters import CourseFilter
from cmsapp.models import Course, lessons, Quiz, Question, Answer, Tracklesson, User, Person

@login_required(login_url='login')
def index(request):
    return render(request, 'dashboard/dashboard.html', {})

@login_required(login_url='login')
def course_manager(request):
    if request.user.usertype in ["admin", "teacher"]:
        courses = Course.objects.filter(author=request.user) if request.user.usertype == "teacher" else Course.objects.all()
        courses = courses.select_related('category').order_by('-id')
        course_filter = CourseFilter(request.GET, queryset=courses)
        paginated_filter = Paginator(course_filter.qs, per_page=10)
        page_number = request.GET.get('page')
        courses = paginated_filter.get_page(page_number)
        context = {
            'courses': courses,
            'course_filter': course_filter
        }
        return render(request, 'dashboard/course/manage_course.html', context)
    else:
        return redirect('home')

@login_required(login_url='login')
def add_course(request):
    if request.user.usertype in ["admin", "teacher"]:
        if request.method == "POST":
            course_form = CourseForm(request.POST, request.FILES)
            if course_form.is_valid():
                form = course_form.save(author=request.user)
                messages.success(request, "Course Created")
                return redirect("dashboard:manage_course")
        else:
            course_form = CourseForm()
        return render(request, 'dashboard/course/add_course.html', {'form': course_form})
    else:
        return redirect('home')

@login_required(login_url='login')
def edit_course(request, id):
    if request.user.usertype in ["admin", "teacher"]:
        course = get_object_or_404(Course, id=id)
        if request.method == "POST":
            course_form = CourseForm(request.POST, request.FILES, instance=course)
            if course_form.is_valid():
                course_form.save()
                messages.success(request, "Course Updated")
                return redirect("dashboard:manage_course")
        else:
            course_form = CourseForm(instance=course)
        return render(request, 'dashboard/course/add_course.html', {'form': course_form})
    else:
        return redirect('home')

@login_required(login_url='login')
def createquiz(request, lesson):
    if request.user.usertype == 'admin' or request.user.usertype == "teacher":
        form = QuizForm()
        if request.method == "POST":
            form = QuizForm(request.POST)
            lesson = lessons.objects.filter(id=lesson).first()
            course = lesson.Course
            if form.is_valid():
                myform = form.save(commit=False)
                myform.lessons = lesson
                myform.course = course
                myform.save()
                return redirect(reverse('dashboard:manage_lesson', kwargs={'course_id': course.id}))
        return render(request, 'dashboard/quiz/createquestion.html', {'form': form})
    else:
        return redirect('home')

# Continue with the rest of your views

# def manage_lesson(request,course_id):
#     course = Course.objects.get(id=course_id)
#     if request.method == "POST":
#         lesson_form = LessonForm(request.POST,request.FILES)
#         if lesson_form.is_valid:
#             lesson_form.save()
#             messages.success(request,"Lesson Created for {}".format(course.title))
#             return redirect('dashboard:manage_course')
#     else:
#         lesson_form = LessonForm()

#     return render(request,'dashboard/lesson/add_lesson.html',{'form':lesson_form})

@login_required(login_url='login')
def manage_lesson(request,course_id):
    if request.user.usertype == "admin" or request.user.usertype == "teacher":
        course =Course.objects.get(id=course_id)
        lessons = course.lessons_set.all()
        return render(request,'dashboard/lesson/manage_lesson.html',{'lessons':lessons,'course':course})
    else:
        return redirect('home')
    

@login_required(login_url='login')
def manage_quiz(request,lesson_id):
    if request.user.usertype == "admin" or request.user.usertype == "teacher":
        lesson =lessons.objects.filter(id=lesson_id).first()
        quiz = Quiz.objects.filter(lessons = lesson).first()
        questions = Question.objects.filter(quiz = quiz)
        
        return render(request,'dashboard/quiz/manage.html',{'quiz':quiz,'questions':questions})
    else:
        return redirect('home')

@login_required(login_url='login')
def createquestion(request,quiz):
    if request.user.usertype == 'admin' or request.user.usertype == "teacher":
        form = QuestionForm()
        quiz = Quiz.objects.filter(id = quiz).first()
        lesson = quiz.lessons
        if request.method == "POST":
            button = request.POST['button']
            if button == "create":
                form = QuestionForm(request.POST)
                
                if form.is_valid():
                    myform =  form.save(commit=False)
                    myform.quiz = quiz
                    myform.save()
                    return redirect(reverse('dashboard:manage_quiz' ,kwargs={'lesson_id':lesson.id}))
            elif button == "cancel":
                return redirect(reverse('dashboard:manage_quiz' ,kwargs={'lesson_id':lesson.id}))
        return render(request,'dashboard/quiz/createquestion.html',{'form':form})
    else:
        return redirect('home')

@login_required(login_url='login')
def manage_question(request,question):
    if request.user.usertype == "admin" or request.user.usertype == "teacher":
        
        question = Question.objects.filter(id =question).first()
        answers = Answer.objects.filter(question = question)
        

        
        return render(request,'dashboard/quiz/managequestion.html',{'answers':answers,'questions':question})
    else:
        return redirect('home')
@login_required(login_url='login')
def createanswers(request,question):
    if request.user.usertype == 'admin' or request.user.usertype == "teacher":
        form = AnswerForm()
        if request.method == "POST":
            form = AnswerForm(request.POST)
            button = request.POST['button']
            if button == "create":
            
                if form.is_valid():
                    myform =  form.save(commit=False)
                    myform.question = Question.objects.filter(id = question).first()
                    myform.save()
                    return redirect(f"/dashboard/manage_quiz/add_answer/{question}")
            elif button == "cancel":
                return redirect(reverse('dashboard:managequestion' ,kwargs={'question':question}))
        return render(request,'dashboard/quiz/createanswer.html',{'form':form})
    else:
        return redirect('home')

@login_required(login_url='login')
def add_lesson(request,course_id):

    course = Course.objects.get(id=course_id)
    last_lesson = course.lessons_set.last()
    lesson_count = course.lessons_set.all().count()
    
    if request.method == "POST":
        lesson_form = LessonForm(request.POST,request.FILES)
        if lesson_form.is_valid:
            my_lesson = lesson_form.save(commit=False)
            my_lesson.Course = course
            my_lesson.save()
            
            messages.success(request,"Lesson Created for {}".format(course.title))
            return redirect(reverse('dashboard:add_lesson' ,kwargs={'course_id':course_id}))
    else:
        lesson_form = LessonForm(initial={'lesson_number':lesson_count+1})

    return render(request,'dashboard/lesson/add_lesson.html',{'form':lesson_form,"course":course,'last_lesson':last_lesson,'lesson_count':lesson_count})


def edit_lesson(request,course_id,lesson_id):
    if request.user.usertype == 'admin' or request.user.usertype == "teacher":
        course = Course.objects.get(id=course_id)
        lesson = course.lessons_set.get(id=lesson_id)
        lesson_count = course.lessons_set.all().count()
        lesson_count = 1
        
        if request.method == "POST":
            lesson_form = LessonForm(request.POST,request.FILES,instance=lesson)
            if lesson_form.is_valid:
                my_lesson = lesson_form.save(commit=False)
                my_lesson.Course = course
                my_lesson.save()
                
                messages.success(request,"Lesson Created for {}".format(course.title))
                return redirect(reverse('dashboard:add_lesson' ,kwargs={'course_id':course_id}))
        else:
            lesson_form = LessonForm(instance=lesson)

        return render(request,'dashboard/lesson/add_lesson.html',{'form':lesson_form,"course":course,'lesson_count':lesson_count})
    
    else:
        return redirect('home')


def editquestion(request,question):
    question = Question.objects.filter(id = question).first()
    print(question)
    questionForm = QuestionForm(instance=question)
    quiz_ = question.quiz
    lesson = quiz_.lessons
    print(lesson)
    if request.method == "POST":
        question_form = QuestionForm(request.POST,instance=question)
        question_form.save()
        return redirect(reverse('dashboard:manage_quiz' ,kwargs={'lesson_id':lesson.id}))
    return render(request,'dashboard/quiz/updatequestion.html',{'form':questionForm})

def editanswer(request,answer):
    answer = Answer.objects.filter(id = answer).first()
    print(answer)
    answerForm = AnswerForm(instance=answer)
    
    question = answer.question
    if request.method == "POST":
        answerForm = AnswerForm(request.POST,instance=answer)
        answerForm.save()
        return redirect(reverse('dashboard:managequestion' ,kwargs={'question':question.id}))
    return render(request,'dashboard/quiz/createanswer.html',{'form':answerForm})


def editquiz(request,quiz):
    quiz_ = Quiz.objects.filter(id = quiz).first()
    lesson  = quiz_.lessons
    course = lesson.Course
    
    quizForm = QuizForm(instance=quiz_)
    
    
    if request.method == "POST":
        quizForm = QuizForm(request.POST,instance=quiz_)
        quizForm.save()
        return redirect(reverse('dashboard:manage_lesson' ,kwargs={'course_id':course.id,}))
    return render(request,'dashboard/quiz/createquestion.html',{'form':quizForm})



def deletecourse(request,course):
    course = Course.objects.get(id = course)
    course.delete()
    return redirect('dashboard:manage_course')

def deletelesson(request,lesson):
    lesson = lessons.objects.get(id = lesson)
    course = lesson.Course
    print(course.id)
    lesson.delete()
    return redirect(reverse('dashboard:manage_lesson' ,kwargs={'course_id':course.id,}))

def deletequiz(request,quiz):
    quiz = Quiz.objects.get(id = quiz)
    lesson = quiz.lessons
    course = lesson.Course
    
    # print(course.id)
    quiz.delete()
    return redirect(reverse('dashboard:manage_lesson' ,kwargs={'course_id':course.id,}))

def deletequestion(request,question):
    question = Question.objects.get(id = question)
    quiz = question.quiz
    lesson  = quiz.lessons
    
    # print(course.id)
    question.delete()
    return redirect(reverse('dashboard:manage_quiz' ,kwargs={'lesson_id':lesson.id}))

def deleteanswer(request,answer):
    answer = Answer.objects.get(id = answer)
    question = answer.question
    
    
    # print(course.id)
    answer.delete()
    return redirect(reverse('dashboard:managequestion' ,kwargs={'question':question.id}))



def createuser(request):
    if request.user.usertype == "admin":
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            usertype = request.POST.get('usertype')
            createuser = User.objects.create_user(username=username,password=password,usertype = usertype)
            profile_obj = Person.objects.create(user = createuser,is_verified = True,auth_token = str(uuid.uuid4) )
            profile_obj.save()
            
            # createuser.save()
            return redirect('dashboard:createuser')

        return render(request,'dashboard/user/createuser.html',)
    else:
        return redirect('home')


def manageuser(request):
    if request.user.usertype == "admin":
        users = User.objects.all()
        return render(request,'dashboard/user/manageuser.html',{'users':users})

    else:
        return redirect('home')
    

def edituser(request,user):
    user = User.objects.filter(id = user).first()
    context = {"username":user.username,'usertype':user.usertype}
    print(user.usertype)
    if request.method == "POST":
        username = request.POST.get("username")
        usertype = request.POST.get("usertype")
        user.username = username
        user.usertype = usertype
        user.save()
        return redirect('dashboard:manageuser')

    return render(request,'dashboard/user/edituser.html',context)


def deleteuser(request,user):
    user = User.objects.filter(id = user).first()
    user.delete()

    return redirect('dashboard:manageuser')



def trackcourse(request):
    course = Tracklesson.objects.filter(user = request.user)

    return render(request,'dashboard/track/coursetrack.html',{'coruses':course})




# def liveSearch(request): 
#     if request.method == "POST": 
#         inputData = request.POST.get("inputData")
#         print(inputData)  
#         return JsonResponse(("data":inputData))