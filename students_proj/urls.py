"""students_proj URL Configuration

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
from django.urls import path

from students.views import stud_views
from students.views import group_views
from students.views import journal_views

urlpatterns = [
    # Students urls
    path('', stud_views.students_list, name='home'),

    path('students/add/', stud_views.students_add, name='students_add'),

    path('students/<int:sid>/edit/', stud_views.students_edit, name='students_edit'),

    path('students/<int:sid>/delete/', stud_views.students_delete, name='students_delete'),



    # Groups urls
    path('groups/', group_views.groups_list, name='groups'),

    path('groups/add/', group_views.groups_add, name='groups_add'),

    path('groups/<int:gid>/edit/', group_views.groups_edit, name='groups_edit'),

    path('groups/<int:gid>/delete/', group_views.groups_delete, name='groups_delete'),


    # Journal urls
    path('journal/', journal_views.journal_list, name='journal_list'),


    path('admin/', admin.site.urls),

]
