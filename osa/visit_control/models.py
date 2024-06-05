from django.db import models


class Parent(models.Model):
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    name_patronymic = models.CharField(max_length=60, verbose_name='Имя Отчество')
    mobile_phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    receive_notifications = models.BooleanField(verbose_name="Получать уведомления")

    class Meta:
        db_table = 'parents'


    def __str__(self):
        return f"{self.surname} {self.name_patronymic}"


class Child(models.Model):
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    name_patronymic = models.CharField(max_length=60, verbose_name='Имя Отчество')
    mobile_phone = models.CharField(max_length=12, verbose_name='Номер телефона', null=True)
    birthdate = models.DateField(verbose_name="Дата рождения")

    class Meta:
        db_table = 'children'
        indexes = [
            models.Index(fields=['surname'], name='surname_index')
        ]

    def __str__(self):
        return f"{self.surname} {self.name_patronymic}"


class ParentChild(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children', verbose_name='родитель')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='parents', verbose_name='ребенок')

    class Meta:
        db_table = 'parent_child'

    def __str__(self):
        return (f"{self.parent.surname} {self.parent.name_patronymic} "
                f"{self.child.surname} {self.child.name_patronymic}  ")


class SubscriptionType(models.Model):
    amount_training = models.PositiveSmallIntegerField(verbose_name="Количество тренировок в месяц")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за месяц')

    class Meta:
        db_table = 'subscription_type'

    def __str__(self):
        return f"{self.amount_training} тренировок за {self.price} руб"


class Employee(models.Model):
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    name_patronymic = models.CharField(max_length=60, verbose_name='Имя Отчество')
    mobile_phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    job_title = models.CharField(max_length=30, verbose_name="Должность")

    def __str__(self):
        return f'{self.surname} {self.name_patronymic}'

    class Meta:
        db_table = 'employee'


class Sport(models.Model):
    naming = models.CharField(max_length=30, verbose_name="Название секции")
    age_limitations_to = models.PositiveSmallIntegerField(verbose_name='Возраст ограничения до')
    age_limitations_after = models.PositiveSmallIntegerField(verbose_name='Возраст ограничения после')

    def __str__(self):
        return self.naming

    class Meta:
        db_table = 'type_sport'


class EmployeeSport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='sports')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='employees')

    class Meta:
        db_table = 'employee_sport'

    def __str__(self):
        return f"{self.employee.surname} - {self.sport.naming}"


class Document(models.Model):
    naming = models.CharField(max_length=50, verbose_name="Название")
    whom_issued = models.CharField(max_length=100, verbose_name="Кем выдан")
    validity_period = models.DateField(verbose_name="Срок действия")
    number = models.CharField(max_length=40, verbose_name="Номер")
    series = models.CharField(max_length=40, verbose_name="Серия", null=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True, related_name='documents')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, related_name='documents')


class Group(models.Model):
    naming = models.CharField(max_length=30)
    max_limitations_people = models.PositiveSmallIntegerField(verbose_name="Максимум детей в группе")
    age_limitations_to = models.PositiveSmallIntegerField(verbose_name='Возраст ограничения до')
    age_limitations_after = models.PositiveSmallIntegerField(verbose_name='Возраст ограничения после')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    naming_sport = models.ForeignKey(Sport, on_delete=models.CASCADE,
                                          related_name='groups')
    children_count = models.PositiveSmallIntegerField(default=0, verbose_name='Количество детей ')

    def __str__(self):
        return self.naming

    class Meta:
        db_table = "group"


class Schedule(models.Model):
    day_of_week = models.CharField(max_length=20, verbose_name="День недели")
    start_time = models.TimeField(verbose_name="Начало тренировки")
    end_time = models.TimeField(verbose_name="Окончание тренировки")
    training_room = models.CharField(max_length=20, verbose_name="Зал")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="schedules", verbose_name="Группа")

    def __str__(self):
        return f"{self.day_of_week} {self.start_time}-{self.end_time}"

    class Meta:
        db_table = "schedule"


class Sale(models.Model):
    reason = models.CharField(max_length=100, verbose_name="Причина")
    price = models.SmallIntegerField(verbose_name="Цена")


class Subscription(models.Model):
    conclusion_date = models.DateField(verbose_name="Дата заключения")
    data_end = models.DateField(verbose_name="Дата окончания", default=0)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='subscriptions',
                              verbose_name='Ребенок')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='subscriptions',
                               verbose_name="Родитель")
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE,
                                          related_name='subscriptions', verbose_name="Тип абонемента")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 related_name='subscriptions', verbose_name="Сотрудник")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subscriptions', verbose_name="Группа")

    price_with_sale = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, related_name='subscriptions', verbose_name='Скидка',
                             null = True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='subscriptions',
                                 verbose_name="Документ")

    def __str__(self):
        return f"{self.conclusion_date}.{self.child}.{self.group}"

    class Meta:
        db_table = 'subscription'


class Visitation(models.Model):
    date = models.DateField(verbose_name="Дата прихода")
    time_of_arrival = models.TimeField(verbose_name="Время прихода")
    exit_time = models.TimeField(null=True, verbose_name="Время ухода")
    subscription = models.ForeignKey(Subscription,on_delete=models.CASCADE,
                                     related_name='visitations')

    def __str__(self):
        return f'{self.date} {self.time_of_arrival} - {self.exit_time}'

    class Meta:
        db_table = 'visitation'
