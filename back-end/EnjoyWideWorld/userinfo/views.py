from django.shortcuts import render
from django.shortcuts import HttpResponse
from userinfo import models

# Create your views here.
def index(request):
    if(request.method == "GET"):
        return render(request, "index.html")


def register(request):
    if(request.method == "GET"):
        return render(request, "register.html")
    elif(request.method == "POST"):
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        cpassword = request.POST.get('cpassword', None) # 第二次输入密码
        #判断数据是否为空
        if not all([username, password, cpassword]):
            return render(request, 'register.html', {'errmsg': "数据不能为空"})
        
        # 判断密码是否正确
        if (not password == cpassword):
            return render(request, 'register.html', {'errmsg' : '两次密码不一致'})
        
        #判断用户名
        try:
            user = models.UserInfo.objects.get(username = user_name)
        except Exception as e:
            user = None
        if (user):
            return render(request, 'register.html', {'errmsg': '用户名已经被使用'})
        
        # 创建一个用户对象
        user = models.UserInfo.objects.get_or_create(username = username, password = password)
        return render(request, 'index.html', {"msg" : "注册成功"})

def userinfo(request):
    if(request.method == "GET"):
        user_list = models.UserInfo.objects.all()
        return render(request, "userinfo.html", {"data" : user_list})

    
                          