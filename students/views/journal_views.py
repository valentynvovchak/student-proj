from datetime import datetime, date

from django.views.generic.base import TemplateView
from django.urls import reverse
from django.http import JsonResponse

from students.models import Student, Group, MonthJournal

from calendar import monthrange, weekday, day_abbr
from dateutil.relativedelta import relativedelta
from ..util import paginate, get_current_group

#  Views for Journal


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super().get_context_data(**kwargs)

        # Перевіряємо чи передали нам місяць в параметрі,
        # якщо ні - вичисляємо поточний;
        # Поки що ми віддаємо лише поточний:

        # check if we need to display some specific month
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()
            # strPtime not strftime! date() stripes  time!

        else:
            # otherwise just displaying current month data
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # calculate current, previous and next month details;
        # we need this for month navigation element in template
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)

        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year

        # змінну cur_month ми використовуватимемо пізніше
        # в пагінації; а month_verbose в
        # помісячній навігації:
        context['month_verbose'] = month.strftime('%B')

        # we'll use this variable in students pagination
        context['cur_month'] = month.strftime('%Y-%m-%d')

        # prepare variable for template to generate
        # journal table header elements

        myear, mmonth = month.year, month.month

        number_of_days = monthrange(myear, mmonth)[1]  # monthrange(<year>, <month>)[1] - к-сть днів року такого-то...м.

        context['month_header'] = [
            {'day': d, 'verbose': day_abbr[weekday(myear, mmonth, d)][:2]} for d in range(1, number_of_days+1)
        ]

        # get all students from database, or just one if we need to
        # display journal for one student
        if kwargs.get('pk'):
            # kwargs.get('<req parameter>') - метод приймає аргументи URL адреси у вигляді словника kwargs
            queryset = [Student.objects.get(pk=kwargs['pk'])]
        else:
            current_group = get_current_group(self.request)

            if current_group:
                queryset = Student.objects.filter(student_group=current_group).order_by('last_name')
            else:
                queryset = Student.objects.all().order_by('last_name')

        # це адреса для посту AJAX запиту, ми
        # робитимемо його на цю ж в'юшку; в'юшка журналу
        # буде і показувати журнал і обслуговувати запити
        # типу пост на оновлення журналу; (url to update student presence, for form post)
        update_url = reverse('journal')

        # пробігаємось по усіх студентах і збираємо
        # необхідні дані:
        students = []
        for student in queryset:
            # try to get journal object by month selected
            # month and current student

            journal = MonthJournal.objects.filter(student=student, date=month).first()

            # набиваємо дні для студента
            days = []
            for day in range(1, number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, f'present_day{day}', False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d')
                })

            # набиваємо усі решту даних студента
            students.append({
                'fullname': f"{student.last_name} {student.first_name}",
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        # застосовуємо пагінацію до списку студентів (10 students per page)
        context = paginate(students, 6, self.request, context, var_name='students')  # пізніше напишемо власну ф-ю

        # finally return updated context
        # with paginated students
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        # prepare student, dates and presence data
        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False  # ("" and True or False) -> False; ("1" and True or False) -> True;
        student = Student.objects.get(pk=data['pk'])

        # get or create journal object for given student and month
        journal, created = MonthJournal.objects.get_or_create(student=student, date=month)

        # set new presence on journal for given student and save result
        setattr(journal, f'present_day{current_date.day}', present)

        journal.save()

        # return success status
        return JsonResponse({'status': 'success'})
