from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.


#  Views for Students

def students_list(request):
    students = (
        {'id': 1,
         'first_name': 'Валентин',
         'last_name': 'Вовчак',
         'number': 3119036,
         'image': 'img/Valya.jpg'},

        {'id': 2,
         'first_name': 'Денис',
         'last_name': 'Старжевський',
         'number': 3119088,
         'image': 'img/Denys.jpg'},

        {'id': 3,
         'first_name': 'Ельвіра',
         'last_name': 'Громова',
         'number': 3119101,
         'image': 'img/Elya.jpg'}
    )

    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)


#  Views for Groups

def groups_list(request):
    return HttpResponse('<h1>Groups Listing</h1>')


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)

