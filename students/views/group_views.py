from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.


#  Views for Groups

def groups_list(request):
    groups = (
        {'id': 1,
         'name': 'ФЕІ-21',
         'leader': 'Марія Круцько'},

        {'id': 2,
         'name': 'ФЕІ-22',
         'leader': 'Юрій Кадіров'},
    )

    return render(request, 'students/groups_list.html', {'groups': groups})


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)