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
from django.urls import path, re_path, include

from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required

from students.views import stud_views, group_views, exam_views, journal_views, contact_admin_views


urlpatterns = [
    # User related urls
    path('accounts/profile/', login_required(TemplateView.as_view(template_name='account/profile.html')), name='profile'),
    path('accounts/', include('allauth.urls')),

    # Students urls
    path('', stud_views.students_list, name='home'),
    path('students/add/', stud_views.students_add, name='students_add'),
    path('students/<int:pk>/edit/', stud_views.StudentUpdateView.as_view(), name='students_edit'),
    path('students/<int:pk>/delete/', stud_views.StudentDeleteView.as_view(), name='students_delete'),



    # Groups urls
    path('groups/', login_required(group_views.groups_list), name='groups'),
    path('groups/add/', login_required(group_views.groups_add), name='groups_add'),
    path('groups/<int:pk>/edit/', login_required(group_views.GroupUpdateView.as_view()), name='groups_edit'),
    path('groups/<int:pk>/delete/', login_required(group_views.GroupDeleteView.as_view()), name='groups_delete'),

    # Exams urls
    path('exams/', login_required(exam_views.exams_list), name='exams'),
    path('exams/add/', login_required(exam_views.exams_add), name='exams_add'),


    # Journal urls
    re_path(r'journal/(?:(?P<pk>\d+)/)?$', login_required(journal_views.JournalView.as_view()), name='journal'),


    # Contact Admin Form
    path('contact-admin/', contact_admin_views.contact_admin, name='contact_admin'),


    path('admin/', admin.site.urls),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

