from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from students_proj.settings import MAX_UPLOAD_SIZE
from students.models import Student, Group


from django.views.generic import UpdateView, DeleteView
from ..util import paginate, get_current_group
# Create your views here.


#  Views for Students

def students_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)

    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
        students = Student.objects.all()

    # order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'number'):
        students = students.order_by(order_by)
    else:
        students = students.order_by('last_name')

    if request.GET.get('reverse', '') == '1':
        students = students.reverse()

    # apply pagination, 3 students per page
    context = {}
    context = paginate(students, 6, request, context, var_name='students')

    return render(request, 'students/students_list.html', context)


@login_required
def students_add(request):

    # was form posted?:
    if request.method == "POST":

        # was form add button clicked?
        if request.POST.get('add_button') is not None:

            # errors collection
            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name', ''),
                    'notes': request.POST.get('notes', ''), }

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = "Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = "Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = "Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, "%Y-%m-%d")
                except Exception:
                    errors['birthday'] = "Введіть коректний формат дати (2002-12-30)"
                else:
                    data['birthday'] = birthday

            number = request.POST.get('number', '').strip()
            if not number:
                errors['number'] = "Номер залікової є обов'язковим"
            else:
                data['number'] = number

            student_group = request.POST.get('student_group', '').strip()

            if not student_group:
                errors['student_group'] = "Вибір групи обов'язковий"
            else:
                group = Group.objects.filter(pk=student_group).first()
                if group:
                    data['student_group'] = group
                else:
                    errors['student_group'] = "Оберіть коректну групу"

            photo = request.FILES.get('photo', '')
            if photo:
                try:
                    if photo.name.endswith('.jpg') or photo.name.endswith('.png') or photo.name.endswith('.jpeg'):
                        if photo.size > MAX_UPLOAD_SIZE:
                            errors['photo'] = f"Розмір вашого файлу {round(photo.size*9.537e-7, 2)} МБ (максимум {round(MAX_UPLOAD_SIZE*9.537e-7, 2)} МБ)"
                        else:
                            data['photo'] = photo
                    else:
                        errors['photo'] = "Невірний формат файлу (загрузіть зображення)"
                except:
                    errors['photo'] = "Невірний формат файлу (загрузіть зображення)"

            # save student
            if not errors:
                student = Student(**data)
                student.save()

                # redirect to students list
                return HttpResponseRedirect(f"{reverse('home')}?status_message=Студента успішно додано!&amp;alert=success ({first_name} {last_name})")
            else:
                # initial form render
                return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'),
                                                                      'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(f"{reverse('home')}?status_message=Додавання студента скасовано!&amp;alert=warning")

    else:
        # initial form render
        return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})


class StudentUpdateForm(ModelForm):  # Унаслідуємо форму від ModelForm - Django клас, який базується на моделях

    class Meta:  # Мета-дані
        model = Student     # Вказуємо модель для редагування
        fields = '__all__'  # Будемо редагувати усі без винятку поля моделі студента

    def __init__(self, *args, **kwargs):  # Модуль Django Crispy forms реалізовується у конструкторі класу форми
        # викликати оригінальний ініціалайзер
        super().__init__(*args, **kwargs)

        # цей helper об'єкт дозволяє нам катомізувати форму
        self.helper = FormHelper(self)

        # втсанослюємо атрибути для тегу форми
        self.helper.form_class = 'form-horizontal'
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'post'

        # встановлюємо властивості полів форми
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 col-form-label'
        self.helper.field_class = 'col-sm-10'

        # додаємо кнопки Зберегти та Скасувати
        self.helper.layout.append(FormActions(
            Submit('add_button', 'Зберегти'),
            Submit('cancel_button', 'Скасувати', css_class='btn-danger'),
        ))


class StudentUpdateView(UpdateView):  # використовуємо вбудовані в Django класи, які базуються на в'юшках
                                      # (Class Based Views)
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    @method_decorator(login_required)  # Не даємо доступ до форми не залогованим користувачам
    def dispatch(self, *args, **kwargs):  # розкидає запити на різні методи класу в’юшки взалежності від типу запиту
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):  # в разі успішного редгуання студента редіректимось на домашню сторінку
        return f"{reverse('home')}?status_message=Студента успішно збережено!&amp;alert=success"

    # request - об'єкт запиту
    def post(self, request, *args, **kwargs):  # всю важку роботу (валідація даних, збереження студента, підго-
        # товка помилок при некоректних даних) для нас зробить метод “post”  батьківського класу.
        if request.POST.get('cancel_button') is not None:  # Якщо не клікнули на кнопку Скасувати
            return HttpResponseRedirect(f"{reverse('home')}?status_message=Редагування студента відмінено!&amp;alert=warning")

        else:
            return super().post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return f"{reverse('home')}?status_message=Студента успішно видалено!&amp;alert=success"


