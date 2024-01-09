from django.shortcuts import render
from .models import *
def tw_view(request):
    events = Event.objects.all()
    courses = Course.objects.all()
    usercoin = UserCoin.objects.filter(user = request.user).first()
    context = {
        'events':events,
        'courses':courses,
        'usercoin':usercoin

        
    }
    return render(request,'cmsapp/index_tw.html',context)

def event_detail(request,id):
    event = Event.objects.get(id=id)
    context = {
        'event':event
    
    }
    return render(request,'cmsapp/event_detail.html',context)