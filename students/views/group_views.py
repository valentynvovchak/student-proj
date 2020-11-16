from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from students.models import Student, Group
# Create your views here.


#  Views for Groups

def groups_list(request):
    groups = Group.objects.all()
    students = Student.objects.all()

    # order group list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)
    if request.GET.get('reverse', '') == '1':
        groups = groups.reverse()

    return render(request, 'students/groups_list.html', {'groups': groups, 'students': students, })


def groups_add(request):
    # was form posted?:
    if request.method == "POST":

        # was form add button clicked?
        if request.POST.get('add_button') is not None:

            # errors collection
            errors = {}
            # validate group data will go here
            data = {'notes': request.POST.get('notes', ''), }

            # validate user input
            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = "Назва є обов'язковою"
            else:
                data['title'] = title

            leader = request.POST.get('leader', '').strip()
            if leader:
                leader_object = Student.objects.filter(first_name=leader.split()[0]).first()
                if leader_object:
                    data['leader'] = leader_object
                else:
                    errors['leader'] = 'Оберіть коректно студента'
                # group = Group.objects.filter(pk=student_group).first()
                # if group:
                #     data['student_group'] = group
                # else:
                #     errors['student_group'] = "Оберіть коректну групу"

            # save group
            if not errors:
                group = Group(**data)
                group.save()

                # redirect to groups list
                return HttpResponseRedirect(f"{reverse('groups')}?status_message=Групу {title} успішно додано!&amp;alert=success")
            else:
                # initial form render
                return render(request, 'students/groups_add.html', {'students': Student.objects.all().order_by('last_name'),
                                                                    'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            # redirect to groups page on cancel button
            return HttpResponseRedirect(f"{reverse('groups')}?status_message=Додавання групи скасовано!&amp;alert=warning")

    else:
        # initial form render
        return render(request, 'students/groups_add.html', {'students': Student.objects.all().order_by('last_name')})


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)