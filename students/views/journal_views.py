from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.
#  Views for Journal


def journal_list(request):
    journal = (
        {'id': 1,
         'student': 'Валентин Вовчак'},

        {'id': 2,
         'student': 'Денис Старжевський'},

        {'id': 3,
         'student': 'Ельвіра Громова'},
    )

    return render(request, 'students/visiting.html', {'journal': journal})
