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

    leader = models.OneToOneField('Student', verbose_name='Староста', blank=True, null=True, on_delete=models.SET_NULL)

    notes = models.TextField(blank=True, verbose_name='Додаткові нотатки')

    class Meta:
        verbose_name = 'Група'
        verbose_name_plural = 'Групи'

    def __str__(self):
        if self.leader:
            return f'{self.title} ({self.leader.first_name} {self.leader.last_name})'.strip()
        else:
            return f'{self.title}'.strip()


class MonthJournal(models.Model):
    """Student Monthly Journal"""

    student = models.ForeignKey('Student', verbose_name='Студент', blank=False,
                                unique_for_date='date', on_delete=models.CASCADE)  # unique for date

    # we only need year and month, so always set day to first day of the month
    date = models.DateField(verbose_name='Дата', blank=False)

    # list of days, each says whether student was present or not
    present_day1 = models.BooleanField(default=False)
    present_day2 = models.BooleanField(default=False)
    present_day3 = models.BooleanField(default=False)
    present_day4 = models.BooleanField(default=False)
    present_day5 = models.BooleanField(default=False)
    present_day6 = models.BooleanField(default=False)
    present_day7 = models.BooleanField(default=False)
    present_day8 = models.BooleanField(default=False)
    present_day9 = models.BooleanField(default=False)
    present_day10 = models.BooleanField(default=False)
    present_day11 = models.BooleanField(default=False)
    present_day12 = models.BooleanField(default=False)
    present_day13 = models.BooleanField(default=False)
    present_day14 = models.BooleanField(default=False)
    present_day15 = models.BooleanField(default=False)
    present_day16 = models.BooleanField(default=False)
    present_day17 = models.BooleanField(default=False)
    present_day18 = models.BooleanField(default=False)
    present_day19 = models.BooleanField(default=False)
    present_day20 = models.BooleanField(default=False)
    present_day21 = models.BooleanField(default=False)
    present_day22 = models.BooleanField(default=False)
    present_day23 = models.BooleanField(default=False)
    present_day24 = models.BooleanField(default=False)
    present_day25 = models.BooleanField(default=False)
    present_day26 = models.BooleanField(default=False)
    present_day27 = models.BooleanField(default=False)
    present_day28 = models.BooleanField(default=False)
    present_day29 = models.BooleanField(default=False)
    present_day30 = models.BooleanField(default=False)
    present_day31 = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Місячний Журнал'
        verbose_name_plural = 'Місячні Журнали'

    def __str__(self):
        return f"{self.student.last_name}: {self.date.month}, {self.date.year}"


# class ExamGroup(models.Model):
#     exam = models.ForeignKey('Group', verbose_name='Екзамен', blank=False, on_delete=models.PROTECT)
#     group = models.ForeignKey('Exam', verbose_name='Група', blank=False, on_delete=models.PROTECT)


class Exam(models.Model):
    """Exam Model"""

    subject = models.CharField(max_length=120, verbose_name='Назва дисципліни')

    datetime = models.DateTimeField(verbose_name='Дата/час проведення')

    teacher = models.CharField(max_length=150, verbose_name='Викладач')

    exam_group = models.ForeignKey('Group', verbose_name='Група', blank=False, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Екзамен'
        verbose_name_plural = 'Екзамени'

    def __str__(self):
        return f"{self.subject} ({self.teacher})"
