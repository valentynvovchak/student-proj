from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.


#  Views for Students

class ContactForm(forms.Form):

    from_email = forms.EmailField(label='Ваша Емейл Адреса')

    subject = forms.CharField(label='Заголовок листа', max_length=128)

    message = forms.CharField(label='Текст повідомлення', max_length=2560, widget=forms.Textarea)


def contact_admin(request):
    #  check if form was posted
    if request.method == 'POST':

        # create a form instance and populate it with data from the request
        form = ContactForm(request.POST)

        # check whether user data is valid:
        if form.is_valid():
            # send email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            try:
                send_mail(subject, message, from_email, [settings.ADMIN_EMAIL])

            except Exception:
                message = 'Під час відправки листа виникла непередбачувана помилка. Спробуйте скористатись даною формою пізніше.'

            else:
                message = 'Повідомлення успішно надіслане!'

            # redirect to same contact page with success message
            return HttpResponseRedirect(f"{reverse('contact_admin')}?status_message={message}")

    else:
        # if there was not POST render blank form
        form = ContactForm()

        return render(request, 'contact_admin/form.html', {'form': form})

