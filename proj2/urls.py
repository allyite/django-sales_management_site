"""proj2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views

cxt= {"next":"home","next1":"a1/orders","next2":"a1/tinv"}
login_view= auth_views.LoginView.as_view(template_name='proj/login.html', extra_context=cxt) #, redirect_field_name= "next1")
#logout_view= auth_views.logout_then_login(login_url="")



urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.parent_url_view, name="parent_url"),
    path('login', login_view, name="login"),
    path('logout', auth_views.logout_then_login, name="logout"),
    path('home', views.homeview, name="homeview"),
    path('a1/', include('app1.urls')),
    path('a2/', include('app2.urls')),
]
