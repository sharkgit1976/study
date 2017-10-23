# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import  View
from django.contrib.auth import  authenticate,login
# Create your views here.

class Login(View):
    def get(self,request):
        return render(request, 'my_login.html')
    def post(self,request):
        user_name = request.POST.get("username","")
        pass_word = request.POST.get("password", "")
        print user_name,pass_word
        user = authenticate(username=user_name,password=pass_word)
        print user
        if user is not None:
            if user.is_active:
                login(request,user)
                return render(request, 'index.html')
            else:
                return render(request,'my_login.html',{'errors':u"账户验证失败"})
        else:
            return render(request, 'my_login.html',{'errors':u"无效的账户"})
