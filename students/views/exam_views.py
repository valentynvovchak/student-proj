from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import models
from django.http.response import HttpResponseForbidden
from django.core.exceptions import ValidationError

from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper

from ..util import paginate, get_current_group
from students.models import Student, Group, Exam


#  Views for Exams

def exams_list(request):
    current_group = get_current_group(request)

    if current_group:
        exams = Exam.objects.filter(exam_group=current_group)
    else:
        # otherwise show all exams
        exams = Exam.objects.all()

    # order exams list
    order_by = request.GET.get('order_by', '')
    if order_by in ('subject', 'datetime', 'teacher'):
        exams = exams.order_by(order_by)
    else:
        exams = exams.order_by('datetime')

    if request.GET.get('reverse', '') == '1':
        exams = exams.reverse()

    # apply pagination, 6 exams per page
    context = {}
    context = paginate(exams, 6, request, context, var_name='exams')

    return render(request, 'students/exams_list.html', context)


@login_required
def exams_add(request):

    # was form posted?:
    if request.method == 'POST':

        # was form add button clicked?
        if request.POST.get('add_button') is not None:  # request.POST !!!!!!!!!!!!!!!!!!

            # errors collection
            errors = {}
            # validate exam data will go here
            data = {}

            # validate user input
            subject = request.POST.get('subject', '').strip()
            if not subject:
                errors['subject'] = 'Назва дисципліни є обов\'язковою'
            else:
                data['subject'] = subject

            date_time = request.POST.get('datetime', '')
            if not date_time:
                errors['datetime'] = 'Дата/час проведення є обов\'язковим полем'
            else:
                try:
                    datetime.strptime(date_time, '%Y-%m-%d %H:%M')
                except Exception:
                    errors['datetime'] = "Введіть коректний формат дати та часу (2021-01-19 16:01)"
                else:
                    data['datetime'] = date_time

            teacher = request.POST.get('teacher', '').strip()
            if not teacher:
                errors['teacher'] = 'Потрібно вказати викладача'
            else:
                data['teacher'] = teacher

            exam_group = request.POST.get('exam_group', '').strip()
            if not exam_group:
                errors['exam_group'] = 'Вибір групи обов\'язковий'
            else:
                group = Group.objects.filter(pk=exam_group).first()
                if group:
                    data['exam_group'] = group
                else:
                    errors['exam_group'] = 'Оберіть коректну групу'

            # save exam
            if not errors:
                exam = Exam(**data)
                exam.save()

                # redirect to exams list
                return HttpResponseRedirect(f"{reverse('exams')}?status_message=Екзамен успішно додано для групи {group} ({subject}: {teacher})!&amp;alert=success ")
            else:
                # Initial form render
                return render(request, 'students/exams_add.html', {'groups': Group.objects.all().order_by('title'),
                                                                   'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(f"{reverse('exams')}?status_message=Додавання екзамена скасовано!&amp;alert=warning")
    else:
        # Initial form render
        return render(request, 'students/exams_add.html', {'groups': Group.objects.all().order_by('title')})
