from django.db import models

# Create your models here.


class Student(models.Model):
    """Student Model"""

    first_name = models.CharField(max_length=256, blank=False, verbose_name="Ім'я")

    last_name = models.CharField(max_length=256, blank=False, verbose_name="Прізвище")

    middle_name = models.CharField(max_length=256, blank=True, verbose_name="По-батькові", default='')

    birthday = models.DateField(blank=False, verbose_name="Дата народження", null=True)

    photo = models.ImageField(blank=True, verbose_name="Фото", null=True)

    number = models.CharField(max_length=256, blank=False, verbose_name="№ залікової")

    notes = models.TextField(blank=True, verbose_name="Додаткові нотатки")

    student_group = models.ForeignKey('Group', verbose_name='Група', blank=False, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенти'

    def __str__(self):
        """Return the first_name plus the last_name, with a space in between"""
        return f'{self.first_name} {self.last_name}'.strip()


class Group(models.Model):
    """Group Model"""

    title = models.CharField(max_length=256, verbose_name='Назва')

    leader = models.OneToOneField('Student', verbose_name='Староста', blank=True, null=True,on_delete=models.SET_NULL)

    notes = models.TextField(blank=True, verbose_name='Додаткові нотатки')

    class Meta:
        verbose_name = 'Група'
        verbose_name_plural = 'Групи'

    def __str__(self):
        if self.leader:
            return f'{self.title} ({self.leader.first_name} {self.leader.last_name})'.strip()
        else:
            return f'{self.title}'.strip()
