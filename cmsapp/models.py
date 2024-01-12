
from django.db import models
# from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
import random
from django.template.defaultfilters import slugify
import uuid 
from django.contrib.auth.models import AbstractUser
from cmsapp.manager import UserManager
import qrcode
from io import BytesIO
from django.core.files import File
from django.template.defaultfilters import slugify
from django.conf import settings

Usertype =(
    ('student', 'student'),
    ('teacher', 'teacher'),
    ('admin', 'admin'),
)
class User(AbstractUser):
    # username = None
    username = models.CharField(unique=True, max_length=16)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    usertype = models.CharField(choices= Usertype,default = "Select User type" ,max_length=60)

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ['username']c
    objects = UserManager()

class category(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name
class Course(models.Model):
    
    author = models.ForeignKey(User,on_delete=models.CASCADE,null = True,blank=True)
    title = models.CharField(max_length =200)
    category = models.ForeignKey(category,on_delete=models.CASCADE,null=True,blank=True,default=1)
    image = models.ImageField(upload_to = 'img')
    slug= models.SlugField(unique = True)
    created = models.DateTimeField(auto_now_add = True)
    ispaid = models.BooleanField(default = False)
    required_points = models.BigIntegerField(default = 0 )

 
    def __str__(self):
        return self.title
    @staticmethod
    def get_all_product_by_id(category_id):
        if category_id:
            return Course.objects.filter(category = category_id)
        else:
            return Course.objects.all()
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{str(uuid.uuid4())}"
        super().save(*args, **kwargs)
            
        

class lessons(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,null = True,blank=True)

    title = models.CharField(max_length= 200)
    Course = models.ForeignKey(Course,on_delete = models.CASCADE)
    body = RichTextUploadingField(blank = True,null = True)
    created = models.DateTimeField(auto_now_add = True)
    lesson_number = models.IntegerField(null = False,default = 1)
    id = models.AutoField(primary_key = True,null = False)
    slug= models.SlugField(unique = True)
    is_locked = models.BooleanField(default = True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{str(uuid.uuid4())}"
        super().save(*args, **kwargs)  



    def __str__(self):
        return self.title

class Person(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default= False)

    def __str__(self):
        return self.user.username
class watch_later(models.Model):
    watch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course_id = models.CharField(max_length = 20000,default="")


    
DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)

class Quiz(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    lessons = models.ForeignKey(lessons,on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizes'

class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):

        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"
    
class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    passed = models.BooleanField(default=False)
    
    

    def __str__(self):
        return f"{self.user}-{self.quiz}-{self.quiz.lessons}"




class Tracklesson(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson_slug = models.CharField(max_length=500)
    lesson_number = models.IntegerField(default=0)
    percent = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.course}-{self.lesson_slug}-{self.user.username}"
    

    def save(self,*args, **kwargs):
        lesson_count = self.course.lessons_set.all().count()
        self.percent = (self.lesson_number/lesson_count)*100
        super().save(*args, **kwargs)   




class RequestProject(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    amount = models.IntegerField(default=0, null = True,blank=True)
    description =RichTextUploadingField(blank = True,null = True)

class Event(models.Model):
    STATUS_CHOICES = [
        ('ONGOING','ONGOING'),
        ('UPCOMING','UPCOMING'),
    ]
    name = models.CharField(max_length=200)
    map_iframe = models.CharField(max_length=400,blank=True,null=True)
    banner = models.ImageField(upload_to='event_banners',default='event.jpg')
    scheduled_date = models.DateTimeField() 
    description = RichTextUploadingField(blank = True,null = True)
    location = models.CharField(max_length=200)
    event_fee = models.IntegerField(default=0)
    is_free = models.BooleanField(default=False)
    seats = models.IntegerField(default=0)
    rules = RichTextUploadingField(blank = True,null = True)
    syllabus = models.FileField(upload_to='syllabus')
    status = models.CharField(choices= STATUS_CHOICES,max_length=20,default="UPCOMING")
    timestamp = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes',blank= True)

    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        self.slug = f"{slugify(self.name)}-{str(uuid.uuid4())}"
        site = f"{settings.SITE_URL}/forms/{self.pk}"

        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=4)
        qr.add_data(site)
        qr.make(fit=True)
        img = qr.make_image(fill_color ="black",back_color = "white")
        fname = f'qr_code-{self.name}+.png'
        buffer = BytesIO()
        img.save(buffer,'PNG')
        self.qr_code.save(fname,File(buffer),save=False)
        super().save(*args, **kwargs)
    


class UserCourseStatus(models.Model): 
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    course = models.ForeignKey(Course,on_delete = models.CASCADE)
    can_access = models.BooleanField(default = False)
    def __str__(self):
        return f"{self.user}-{self.course}"
    


class UserCoin(models.Model): 
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    coin_amount = models.BigIntegerField(default = 0)


class EventRegister(models.Model): 
    CHOICES = [
        ('SEE','SEE'),
        ('+2','+2'),
        ('Bachelors','Bachelors'),
    ]
    PAYMENT_CHOICES = [
        
        ('KHALTI','KHALTI'),
        ('CASH','CASH'),
    ]
    event = models.ForeignKey(Event,on_delete = models.CASCADE,null = True,blank = True)
    name = models.CharField(max_length = 200)
    contact_number = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200 )
    eduction = models.CharField(choices= CHOICES,max_length=20)
    School_or_College_name = models.CharField(max_length=200)
    is_verified = models.BooleanField(default = False)
    payment_method = models.CharField(choices = PAYMENT_CHOICES,max_length = 300,default = "CASH" )

