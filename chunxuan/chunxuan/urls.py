"""chunxuan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from UserInfo.views import login, Home, test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login.login),
    path('logout/', login.logout),
    path('home/', Home.home),
    path('test1/', Home.test1),
    path('test2/', Home.test2),
    path('register/', login.register),
    path('myinfo/<int:nid>/check/', login.checkInfo),
    path('zixun/', Home.zixun),
    path('aitest/', test.aitest),
    
]
