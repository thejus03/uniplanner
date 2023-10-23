from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from json import loads
from .models import User, event, module, usermodule, deadline, toask
from django.views.decorators.cache import never_cache
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

@never_cache
@login_required
def index(request):
    ### for sending data for the events/calendar 
    today = date.today()
    username = request.user.username
    all_info = event.objects.all()
    for i in all_info:
        if i.event_date < today:
            i.delete()
    
    event_info = event.objects.filter(username=username, event_date__gte=today).order_by("event_date", "event_time")
    event_info = [info.serialize() for info in event_info]
    for info in event_info:
        info["event_time"] = info["event_time"].strftime("%I:%M %p")

    ### for sending data for the modules
    
    module_info = module.objects.filter(usermodule__username=username) ### join query possible because of the foreignkey relationship


    return render(request, "uniplanner/index.html", {
        "event_info": event_info,
        "module_info":module_info
    })

@never_cache
def login_view(request):
    if request.method == "GET":
        return render(request, "uniplanner/login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        authentication = authenticate(request, username=username, password=password)
        if authentication is not None:
            login(request, authentication) ## authentication is the user details
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "uniplanner/login.html", {
                "message":"Invalid username and/or password."
            })
        

@never_cache
def register_view(request):
    
    info = loads(request.body)
    if info["new_password"] != info["confirm_password"]:
        return HttpResponse("Passwords do not match")
    else:
        try:
            user = User.objects.create_user(username = info["new_username"], password = info["new_password"])
            user.save()
        except IntegrityError:
            return HttpResponse("Username taken")
        else:
            return HttpResponse("success")
        
@never_cache    
@login_required        
def logoff(request):
    logout(request)
    request.session.flush() 
    return HttpResponseRedirect(reverse('index'))


@never_cache
@login_required
def add_event(request):
    if request.method == "POST":
        info = loads(request.body)

        if info["event_end"]!='':
            
            start_date = datetime.strptime(info["event_date"], "%Y-%m-%d")
            end_date = datetime.strptime(info["event_end"], "%Y-%m-%d")
            repeat = info["event_repeat"]
            if repeat == "Every Day":
                add = 1
            elif repeat == "Every Week":
                add = 7
            elif repeat == "Every 2 Weeks":
                add = 14
            else:
                add = 0
            
            if add==1 or add==7 or add==14:
                while start_date <= end_date:
                    event(username=request.user.username, event_name=info["event_name"], event_date=start_date, event_time=info["event_time"]).save()
                    start_date += timedelta(days=add)
            elif repeat=="Every Month":
                while start_date <= end_date:
                    event(username=request.user.username, event_name=info["event_name"], event_date=start_date, event_time=info["event_time"]).save()
                    start_date += relativedelta(months=+1)
            elif repeat=="Every Year":
                while start_date <= end_date:
                    event(username=request.user.username, event_name=info["event_name"], event_date=start_date, event_time=info["event_time"]).save()
                    start_date += relativedelta(months=+12)

        else:
            event(username=request.user.username, event_name=info["event_name"], event_date=info["event_date"], event_time=info["event_time"]).save()

        return HttpResponse(f"Successfully added {info['event_name']}")
    
    
def update(request):
    today = date.today()
    username = request.user.username
    event_info = event.objects.filter(username=username,event_date__gte=today).order_by("event_date", "event_time")
    event_info = [info.serialize() for info in event_info]
    for info in event_info:
        info["event_time"] = info["event_time"].strftime("%I:%M %p")
    
    return JsonResponse(event_info, safe=False)

def delete(request):
    
    info = loads(request.body)
    event.objects.get(username=info["username"], event_name=info["event_name"],event_time = datetime.strptime(info["event_time"], '%I:%M %p'),event_date = date(int(info["event_year"]), int(datetime.strptime(info["event_month"],'%b').month), int(info["event_day"]))).delete()
    return HttpResponse("deleted")

def addmodule(request):
    if request.method == "POST":
        info = loads(request.body)            
        instance = module(name=info["module_name"])
        instance.save()
        id =instance.id
        usermodule(module_id=instance, username=request.user.username).save()

        return JsonResponse({"id":id}, safe=True)
    
def deletemod(request):
    if request.method == 'POST':
        info = loads(request.body)
        print("this is the ", info["id"])
        module.objects.get(id=info["id"]).delete()
        return HttpResponse("deleted")
    
@never_cache    
@login_required 
def moduled(request,id):
    
    title = module.objects.get(id=id)
    todo = deadline.objects.filter(module_id = id).order_by('date') 
    todo = [i.serialize() for i in todo]
    
    today =date.today()
    questions = toask.objects.filter(module_id = id).order_by("answered_date")
    for question in questions:
        if question.answered_date is not None:
            if ((today-question.answered_date).days >= 1):
                question.delete()

    questions = [question.serialize() for question in questions]
    
    return render(request, "uniplanner/module.html", {
        "title":title,
        "todo": todo,
        "id":id,
        "questions": questions
    })

def done(request):
    if request.method == "POST":
        info = loads(request.body)
        dead_id = info["dead_id"]
        instance = deadline.objects.get(id=dead_id)
        instance.status = "done"
        instance.save()
        return HttpResponse("success done")
    

    
def add_task(request, module_id):
    task_name = request.POST.get('task_name')
    task_date = request.POST.get('task_date')
    task_time = request.POST.get("task_time")
    priority = request.POST.get('priority')
    if priority=='yes':
        module_instance = module.objects.get(id=module_id)
        deadline(module_id=module_instance, task=task_name, date=task_date, time=task_time, priority="yes").save()
    else:
        module_instance = module.objects.get(id=module_id)
        deadline(module_id=module_instance, task=task_name, date=task_date, time=task_time, priority="no").save()
   

    return HttpResponseRedirect(f"/module/{module_id}")  

def asked(request):
    info = loads(request.body)

    question_id = info["question_id"]
    print(question_id)
    instance = toask.objects.get(id=question_id)
    
    instance.answered_date = date.today()
    instance.save()
    today= date.today()
    questions = toask.objects.filter(module_id = info["module_id"]).order_by("answered_date")
    for question in questions:
        if question.answered_date is not None:
            if ((today-question.answered_date).days >= 1):
                question.delete()

    return HttpResponse("success")

def add_question(request, module_id):
    question = request.POST.get("question")
    
    module_instance = module.objects.get(id=module_id)
    toask(module_id = module_instance, toask = question).save()

    return HttpResponseRedirect(f"/module/{module_id}")

def filter(request):
    info = loads(request.body)
    word = info["word"]
    
    event_info = event.objects.filter(username=request.user.username, event_name__icontains = word)

    event_info = [i.serialize() for i in event_info]
    
    return JsonResponse(event_info, safe=False)