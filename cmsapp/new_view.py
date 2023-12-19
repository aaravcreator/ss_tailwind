from django.shortcuts import render
from .models import Event
def tw_view(request):
    events = Event.objects.all()
    context = {
        'events':events

        
    }
    return render(request,'cmsapp/index_tw.html',context)

def event_detail(request,id):
    event = Event.objects.get(id=id)
    context = {
        'event':event
    
    }
    return render(request,'cmsapp/event_detail.html',context)