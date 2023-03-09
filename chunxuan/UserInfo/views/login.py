from django.shortcuts import redirect, render
from UserInfo.utils.forms import UserLogin, Register, myInfo
from UserInfo.models import UserInfo, testresult
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import json

## 登陆
def login(request) :
    if request.method == "GET" :
        form = Register()
        form2 = UserLogin()
        return render(request, "login.html", {"form": form, "form2": form2})
    
    form2 = UserLogin(data=request.POST)
    
    if form2.is_valid() :
        data_dict = form2.cleaned_data
        print(data_dict)
        user_object = UserInfo.objects.filter(**data_dict).first()
        if not user_object :
            # 主动显示错误信息
            form2.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form2": form2})
        
    request.session["info"] = {"id": user_object.id, "name": user_object.username}
    
    return redirect("/home/")

## 登出
def logout (request) :
    request.session.clear()
    return redirect('/login/')

## 注册
@csrf_exempt
def register(request) :
    form = Register(data=request.POST)
    print(form)
    if form.is_valid() :
        print(form.instance.birthday)
        form.instance.age = datetime.now().year - int(form.instance.birthday.year)
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)
    
    data_dict = {
        "status": False,
        "error": form.errors,
        }
    
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

## 查看个人资料
def checkInfo(request, nid):
    row_data = UserInfo.objects.filter(id = nid).first()
    row_data2 = testresult.objects.filter(username = row_data.username)[:2]

    if request.method == "GET":
        form = myInfo(instance = row_data)
        cotext = {
            "form": form,
            "row_data": row_data2
        }
        return render(request, "myinfo.html", cotext)
    
    form = myInfo(instance = row_data, data = request.POST)
    if form.is_valid():
        form.instance.age = datetime.now().year - int(form.instance.birthday.year)
        form.save()
        return redirect('/home')
    
    return render(request, "myinfo.html", {"form": form})