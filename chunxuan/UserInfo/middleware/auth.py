from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

# 编写中间件
class AuthMiddleWare (MiddlewareMixin) :
    
    def process_request (self, request) :
        # 1. 排除那些不需要登陆就能访问的页面
        if request.path_info == "/login/" :
            return 
        
        if request.path_info == "/register/" :
            return 
        
        # 2. 检测当前是否已经登陆，即是否有session和cookie
        info_dict = request.session.get("info")
        
        if info_dict :
            return
        
        # 3.如果没有登陆，则重定向至登陆界面
        return redirect('/login/')