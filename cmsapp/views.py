from django.shortcuts import render,redirect
from cmsapp.models import *
from django.contrib import messages
from cmsapp.models import *
import uuid
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from cmsapp.forms import *




# Create your views here.
def watchlater(request):
    if request.user.is_authenticated:
        watch = watch_later.objects.filter(user = request.user)
        

        ids = []
        
        for i in watch:
            ids.append(i.course_id)
            
        
        courses =[]
        
        for j in ids:
            value = Course.objects.filter(id = j).first()
            if value:
                courses.append(value)
        if courses != None:
            course_number = len(courses)
        else:
            course_number = None
        print(course_number)
        
        
        return render(request,'cmsapp/watchlater.html',{'courses':courses,'course_number':course_number})
    else:
        return redirect('login')
def index(request):
    
    categories = category.objects.all()
    courses = Course.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(courses,10)
    try:
        courses = paginator.page(page)
    except Exception as  PageNotAnInteger:
        courses = paginator.page(1)
    except Exception as  EmptyPage:
        courses = paginator.page(paginator.num_pages)
    
    
    categoryID = request.GET.get('category')
    if categoryID:
        courses = Course.objects.all()
        courses = Course.get_all_product_by_id(categoryID)
        page = request.GET.get('page',1)
        print(page)
        paginator = Paginator(courses,4)
        try:
            courses = paginator.page(page)
        except courses.PageNotAnInteger:
            courses = paginator.page(1)
        except courses.EmptyPage:
            courses = paginator.page(paginator.num_pages)

    if request.method =="POST":
        
        user = request.user
        course_id = request.POST.get('course_id')
        watch = watch_later.objects.filter(user = user,course_id = course_id)
        # watch = watch_later.objects.filter(user = user)
        x = True if watch.exists() else False
        
        
        # for i in watch:
        #     if course_id == i.course_id:
        #         messages.success(request,'Already added to read later')
                
                
        #         break
        # print(x)
        if x:
            messages.success(request,'Already added to read later')
        else:

            watchlater = watch_later(user = user,course_id = course_id)
            watchlater.save()
            messages.success(request,'Added to read later')
            
           
            
            
        return redirect('home')
    
    
    
    if categoryID is None :
        categoryID = 0
    if page is None:
        page =0
    else:
        page = int(page)
        
    
    
    
    return render(request,'cmsapp/index_tw.html',{'courses':courses,'categories':categories,'categoryID':int(categoryID),'page':page})
@login_required(login_url='login')
def course(request, slug,lesson_slug):
    courses = Course.objects.filter(slug = slug).first()
    total = courses.lessons_set.all().count()
    lesson_ = lessons.objects.filter(slug = lesson_slug).first()
    # print(lesson_.lesson_number)
    # print(total)

    if lesson_slug:
        try:
            lesson = lessons.objects.get(
                slug=lesson_slug, Course=courses)

        except lessons.DoesNotExist:
            lesson = None
    else:
        lesson = lessons.objects.get(
                lesson_number=1, Course=courses)
    tracklesson = Tracklesson.objects.filter(user = request.user,course = courses).first()
    if tracklesson:
        tracklesson.user = request.user
        tracklesson.lesson_slug = lesson_slug
        
        if tracklesson.lesson_number<lesson_.lesson_number:
            # print(lesson_.lesson_number)
            tracklesson.lesson_number = lesson_.lesson_number
        
            
        # tracklesson.lesson_number = 
        tracklesson.save()
    elif not tracklesson:
        tracklesson1 = Tracklesson(user = request.user,course = courses,lesson_slug = lesson_slug,lesson_number = 1)
        tracklesson1.save()

    if lesson.lesson_number==1:
        return render(request, 'cmsapp/course.html', {'courses': courses, 'lesson': lesson})
    elif lesson.lesson_number!=1:

        lesson_ = lessons.objects.filter(Course = courses,lesson_number = lesson.lesson_number-1).first()
        quiz = Quiz.objects.filter(course = courses,lessons = lesson_).first()
        result = Result.objects.filter(quiz = quiz,user = request.user).first()
        if result :
            if result.passed  :          
                return render(request, 'cmsapp/course.html', {'courses': courses, 'lesson': lesson,'result':result.passed})
            
            else:
                
                return redirect(f"/course/{courses.slug}/{lesson_.slug}")
        elif  lesson.is_locked==False:
            
            return render(request, 'cmsapp/course.html', {'courses': courses, 'lesson': lesson,})

            
        else:
            
            return redirect(f"/course/{courses.slug}/{lesson_.slug}")
    


@login_required(login_url='login')
def createcourse(request):
    if request.user.usertype == 'admin' or request.user.usertype == "teacher":
        form = CourseForm()
        if request.method == "POST":
            form = CourseForm(request.POST,request.FILES)
            
            if form.is_valid():
                myform =  form.save(commit=False)
                myform.author = request.user
                myform.save()
                return redirect('createcourse')
        return render(request,'cmsapp/createcourse.html',{'form':form})
    else:
        return redirect('home')
    
 
@login_required(login_url='login')
def course_index(request, slug):
    try:
        courses = Course.objects.get(slug=slug)
        lesson = lessons.objects.get(
            lesson_number=1, Course=courses)
    except (Course.DoesNotExist,lessons.DoesNotExist):
        courses = None
        lesson = None
        return render(request,'cmsapp/error.html',{'courses':courses})
    tracklesson = Tracklesson.objects.filter(user = request.user,course = Course.objects.get(slug = slug)).first()
    if tracklesson: 
        
        return redirect(reverse('course_lesson' ,kwargs={'slug':slug,'lesson_slug':tracklesson.lesson_slug}))
    else:
        
        return redirect(reverse('course_lesson' ,kwargs={'slug':slug,'lesson_slug':lesson.slug}))





def signin(request):
    if  not request.user.is_authenticated:
        if request.method =='POST':
            User = get_user_model()
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username = username).first()
            if  user_obj is None:
                messages.success(request,'User not found!!! please signin with correct username')
                return redirect('/login')
            profile_obj = Person.objects.filter(user = user_obj).first()
            if not profile_obj.is_verified:
                messages.success(request,'Profile is not verified! check your email ')
                return redirect('/login')
            user = authenticate(username = username,password= password)
            if user is not None:
                login(request,user)
            else:
                messages.success(request,'Wrong password')
                return redirect('/login')
            return redirect('/')
            

        return render(request,'cmsapp/login.html')
    else:
        return redirect('home')
def user_logout(request):
    logout(request)

    messages.success(request,'You are now logged out')
    return redirect('home')


def error(request):
    return render(request,'cmsapp/error.html')


def delete_watchlater(request,pk):

    get_watch = watch_later.objects.get(user = request.user,course_id = pk)
    get_watch.delete()
    
    return redirect('readlater')
def delete_watchlater_from_home(request,pk):

    check =  watch_later.objects.filter(user = request.user,course_id = pk)
    
    if check.exists():
        get_watch =watch_later.objects.get(user = request.user,course_id = pk)
        get_watch.delete()
        messages.success(request,' Removed from Read Later')
        return redirect('home')
    else:
        messages.success(request,'Already removed from Read Later')
        return redirect('home')
    


def quiz_view(request,course,lesson):
    course = Course.objects.filter(slug = course).first()
    total = course.lessons_set.all().count()
    print(total)
    lesson_ = lessons.objects.filter(slug = lesson).first()
    if lesson_.lesson_number ==1:
    # print(quiz)
        
        return render(request,'cmsapp/quizview.html',{'obj':lesson_})
    elif lesson_.lesson_number!=1:
        lesson1 = lessons.objects.filter(Course = course,lesson_number = lesson_.lesson_number-1).first()
        print(lesson1.slug)
        quiz = Quiz.objects.filter(course = course,lessons=lesson1).first()
        
        result = Result.objects.filter(quiz= quiz,user = request.user).first()
        if result:
            if result.passed:
                return render(request,'cmsapp/quizview.html',{'obj':lesson_})
            else:
                return redirect(f"/course/{course.slug}/{lesson1.slug}")
        elif lesson_.is_locked == False:
            return render(request,'cmsapp/quizview.html',{'obj':lesson_})

        else:
            return redirect(f"/course/{course.slug}/{lesson1.slug}")
    elif lesson_.lesson_number== total:
        messages.success(request,"Lessons finished")
        return redirect(f"/course/{course.slug}/{lesson_.slug}")

        


def quiz_data_view(request,course,lesson):
    course = Course.objects.get(slug = course)
    lesson_ = lessons.objects.get(slug = lesson)
    quiz = Quiz.objects.filter(course = course,lessons = lesson_).first()
    # print(quiz.get_questions())
    
    questions = []
    for q in quiz.get_questions():
        answer = []
        for a in q.get_answers():
            answer.append(a.text)
        questions.append({str(q):answer})
    print(questions)
    return JsonResponse({
        'data':questions,
        'time':quiz.time
    })


def save_quiz_view(request,course,lesson):
    if request.method == "POST":
        course = Course.objects.get(slug = course)
        lesson = lessons.objects.get(slug = lesson)
        quiz = Quiz.objects.filter(course = course,lessons = lesson).first()
        lesson_count = lessons.objects.filter(Course = course).count()
        
        # question = Question.objects.get(quiz = quiz,text = k)
        # print(quiz)
        # print(request.POST)
        questions = []
        data = request.POST
        data_ = dict(data)
        data_.pop('csrfmiddlewaretoken')
        # print(data_)
        for k in data_.keys():
            question = Question.objects.get(quiz = quiz,text = k)
            questions.append(question)

        user = request.user
        
        score = 0
        multiplier = 100/quiz.number_of_questions
        results = []
        correct_answer = None

        
        for q in questions:
            # count = count +1
            a_selected = request.POST.get(q.text)
            # print(a_selected)
            if a_selected !="":
                question_answer = Answer.objects.filter(question = q)
                # print(question_answer)
                for a in question_answer:
                    
                    if a_selected == a.text:
                        # print(a)
                        if a.correct:
                            correct_answer = a.text
                            # print("correct\n")
                            score +=1
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append({str(q):{'correct answer':correct_answer,"answer":a_selected}})
            else:
                # empty +=1
                results.append({str(q):"not answered"})
                
        result = Result.objects.filter(quiz = quiz,user = request.user).first()
        passed = False
        if result:
            
            
            if score>=quiz.required_score_to_pass:
                
                result.passed = True
                result.save()
                passed = True
            else:
                
                passed  = False
            
            
            
            # result = Result(quiz = quiz,user = request.user,score = score,passed = passed)
            # result.save()
        elif not result:
            if score>=quiz.required_score_to_pass:
                # lesson1.verified = True
                passed = True
            else:
                
                passed  = False
            
            result = Result(quiz = quiz,user = request.user,score = score,passed = passed)
            result.save()
            
        lesson_ = lessons.objects.filter(Course = course,lesson_number = lesson.lesson_number+1).first()
        # print(lesson_.slug)
       
        
        if score>=quiz.required_score_to_pass:
            if lesson.lesson_number == lesson_count:
                
                return JsonResponse({'passed':True,'score':score,'result':results,'course':course.slug,"last_lesson":True})
            else:
                print("this is last lesson")
                return JsonResponse({'passed':True,'score':score,'result':results,'lesson_number':lesson_.slug,'course':course.slug,"last_lesson":False})
        else:
            if lesson.lesson_number == lesson_count:
           
                return JsonResponse({'passed':False,'score':score,'course':course.slug,'lesson_number':lesson.slug,"last_lesson":True})
                        
            else:
                return JsonResponse({'passed':False,'score':score,'lesson_number':lesson.slug,'course':course.slug,"last_lesson":False})
           
    return JsonResponse({'test':'works'})



def requestproject(request):

    if request.method == "POST":
        # name = request.POST.
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        desc = request.POST.get('desc')
        image = request.POST.get('image')
        file = request.POST.get('file')
        website = request.POST.get('website')
        print(image,file,website)
        if amount == "":
            requestproject = RequestProject(name = name,email = email,amount = 0,description = desc)
            requestproject.save()
        else:
            requestproject = RequestProject(name = name,email = email,amount = amount,description = desc)
            requestproject.save()
        return JsonResponse({'success':"success"})
        

    return JsonResponse({})








def register(request):
    if not request.user.is_authenticated:
        try:
                
            if request.method =='POST':
                User = get_user_model()
                username= request.POST.get('username')
                email=request.POST.get('email')
                password=request.POST.get('password')
                confirm_password =request.POST.get('cpassword')
                fname=request.POST.get('fname')
                lname=request.POST.get('lname')
                print(username)
                print(email)
                print(password)
                print(fname)
                print(lname)

                
                if User.objects.filter(username = username).first():
                    messages.success(request,'Username is taken')
                    return redirect('register')
                if User.objects.filter(email = email).first():
                    messages.success(request,'Email is taken')
                    return redirect('register')
                if confirm_password!=password:
                    messages.success(request,"Passwords didn't match!! Please enter same password")
                    return redirect('register')
                user_obj = User.objects.create_user(username = username,email = email,password=password,first_name = fname,last_name = lname)
                user_obj.save()
                auth_token =  str(uuid.uuid4())
                profile_obj = Person.objects.create(user = user_obj,auth_token = auth_token )
                profile_obj.save()
                currentsite = get_current_site(request) 
                subject = 'Your account need to be verified'
                message = render_to_string('core/partial/search-list.html',{'students':students})
                message  = f'<h2>Hello</h2> {fname} ! <p style ="color:red">Welcome to sikshyasala ,<br>please verify you account</p> {currentsite.domain}/verify/{auth_token}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject,message,email_from,recipient_list)
                return redirect('/token_send')
        except Exception as e:
            print(e)

            
        return render(request,'cmsapp/register.html')
    else:
        return redirect('home')

def token_send(request):
    return render(request,'cmsapp/tokensend.html')
def verify(request,auth_token):
    try:
        profile_obj = Person.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request,'Your account is already verified! Please Sign in')
                return redirect('/login')

            profile_obj.is_verified = True
            profile_obj.save()      
            messages.success(request,'Your account is verified')
            return redirect('/login')
            
        else:
            return redirect('/error')
            
    except Exception as e:
        print(e)
def error(request):
    return render(request,'cmsapp/error.html')

def liveSearch(request): 
    if request.method == "POST": 
        inputData = request.POST.get("inputData")
        res = None
        try:
            course = Course.objects.filter(title__icontains = inputData)[0:6]
        except:
            course = Course.objects.all()
        if len(course)>0 and len(inputData)>0:
            data = []
            for pos in course: 
                item = { 
                    'pk':pos.pk,
                    'title':pos.title,
                    'slug':pos.slug
                     
                }
                data.append(item)
            res = data
        else:
            res = "No Course found"
        return JsonResponse({"data":res})
    else:
        return JsonResponse({}) 