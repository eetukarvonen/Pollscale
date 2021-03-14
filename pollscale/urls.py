"""pollscale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from scale import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:scale_id>', views.detail, name='detail'),
    path('add', views.add, name='add'),
    path('add/yay/<int:scale_id>', views.add_yay, name='add_yay'),
    path('add/nay/<int:scale_id>', views.add_nay, name='add_nay'),
    path('register/', views.register, name='register'),
    path('vote/<int:scale_id>', views.vote, name='vote'),
    path('info', views.info, name='info'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
