from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from django.db import models
from django.http.response import HttpResponseForbidden
from django.core.exceptions import ValidationError

from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper

from ..util import paginate, get_current_group
from students.models import Student, Group
# Create your views here.


#  Views for Groups

def groups_list(request):
    # check if we need to show only one group
    current_group = get_current_group(request)
    if current_group:
        groups = [Group.objects.filter(pk=current_group.pk).first()]
        context = {'groups': groups}
    else:
        # otherwise show only chosen group
        groups = Group.objects.all()

        # order group list
        order_by = request.GET.get('order_by', '')
        if order_by in ('title', 'leader'):
            groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

        context = {}
        context = paginate(groups, 4, request, context, var_name='groups')

    return render(request, 'students/groups_list.html', context)


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

            # leader = request.POST.get('leader', '').strip()
            # if leader:
            #     leader_object = Student.objects.filter(first_name=leader.split()[0]).first()
            #     if leader_object:
            #         data['leader'] = leader_object
            #     else:
            #         errors['leader'] = 'Оберіть коректно студента'


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
                return HttpResponseRedirect(f"{reverse('groups')}?status_message=Групу {title} успішно додано!&amp;alert=success&amp;order_by=title")
            else:
                # initial form render
                return render(request, 'students/groups_add.html', {'students': Student.objects.all().order_by('last_name'),
                                                                    'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            # redirect to groups page on cancel button
            return HttpResponseRedirect(f"{reverse('groups')}?status_message=Додавання групи скасовано!&amp;alert=warning&amp;order_by=title")

    else:
        # initial form render
        return render(request, 'students/groups_add.html', {'students': Student.objects.all().order_by('last_name')})


class GroupUpdateForm(ModelForm):

    class Meta:
        model = Group
        fields = '__all__'

    def clean_leader(self):

        group = Group.objects.filter(pk=self.instance.pk).first()
        students = Student.objects.filter(student_group=group)  # тільки студенти які є в реальній групі

        if (self.cleaned_data['leader'] not in students) and (self.cleaned_data['leader'] is not None):
            raise ValidationError("Даний студент не є студентом обраної групи", code='invalid')

        return self.cleaned_data['leader']

    def clean_title(self):

        group = Group.objects.filter(title=self.cleaned_data['title']).first()

        this_group = Group.objects.filter(pk=self.instance.pk).first()

        if (group is not None) and (group.title != this_group.title):  # group is this_group forever!
            raise ValidationError("Група з такою назвою вже існує", code='invalid')

        return self.cleaned_data['title']

    def __init__(self, *args, **kwargs):
        # call original initializer
        super().__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 col-form-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout.append(FormActions(
            Submit('add_button', 'Зберегти'),
            Submit('cancel_button', 'Скасувати', css_class='btn-danger'),
        ))


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_edit.html'
    form_class = GroupUpdateForm

    def get_success_url(self):
        return f"{reverse('groups')}?status_message=Групу успішно збережено!&amp;alert=success&amp;order_by=title"

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(f"{reverse('groups')}?status_message=Редагування групи відмінено!&amp;alert=warning&amp;order_by=title")
        else:
            return super().post(request, *args, **kwargs)


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        try:
            return super(GroupDeleteView, self).delete(request, *args, **kwargs)

        except models.ProtectedError as e:
            # Return the appropriate response
            return HttpResponseRedirect(f"{reverse('groups')}?status_message=На жаль, ви не можете видалити групу, поки у ній є хочаб один студент&amp;alert=danger&amp;order_by=title")

    def get_success_url(self):
        return f"{reverse('groups')}?status_message=Групу успішно видалено!&amp;alert=success&amp;order_by=title"
