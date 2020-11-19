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
from django.urls import path, re_path

from django.conf import settings
from django.conf.urls.static import static

from students.views import stud_views, group_views, journal_views, contact_admin_views


urlpatterns = [
    # Students urls
    path('', stud_views.students_list, name='home'),

    path('students/add/', stud_views.students_add, name='students_add'),

    path('students/<int:pk>/edit/', stud_views.StudentUpdateView.as_view(), name='students_edit'),

    path('students/<int:pk>/delete/', stud_views.StudentDeleteView.as_view(), name='students_delete'),



    # Groups urls
    path('groups/', group_views.groups_list, name='groups'),

    path('groups/add/', group_views.groups_add, name='groups_add'),

    path('groups/<int:pk>/edit/', group_views.GroupUpdateView.as_view(), name='groups_edit'),

    path('groups/<int:pk>/delete/', group_views.GroupDeleteView.as_view(), name='groups_delete'),


    # Journal urls
    re_path(r'journal/(?:(?P<pk>\d+)/)?$', journal_views.JournalView.as_view(), name='journal'),


    # Contact Admin Form
    path('contact-admin/', contact_admin_views.contact_admin, name='contact_admin'),


    path('admin/', admin.site.urls),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

