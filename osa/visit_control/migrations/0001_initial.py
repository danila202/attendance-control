# Generated by Django 4.2 on 2024-06-05 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('name_patronymic', models.CharField(max_length=60, verbose_name='Имя Отчество')),
                ('mobile_phone', models.CharField(max_length=12, null=True, verbose_name='Номер телефона')),
                ('birthdate', models.DateField(verbose_name='Дата рождения')),
            ],
            options={
                'db_table': 'children',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naming', models.CharField(max_length=50, verbose_name='Название')),
                ('whom_issued', models.CharField(max_length=100, verbose_name='Кем выдан')),
                ('validity_period', models.DateField(verbose_name='Срок действия')),
                ('number', models.CharField(max_length=40, verbose_name='Номер')),
                ('series', models.CharField(max_length=40, null=True, verbose_name='Серия')),
                ('child', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='visit_control.child')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('name_patronymic', models.CharField(max_length=60, verbose_name='Имя Отчество')),
                ('mobile_phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('job_title', models.CharField(max_length=30, verbose_name='Должность')),
            ],
            options={
                'db_table': 'employee',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naming', models.CharField(max_length=30)),
                ('max_limitations_people', models.PositiveSmallIntegerField(verbose_name='Максимум детей в группе')),
                ('age_limitations_to', models.PositiveSmallIntegerField(verbose_name='Возраст ограничения до')),
                ('age_limitations_after', models.PositiveSmallIntegerField(verbose_name='Возраст ограничения после')),
                ('children_count', models.PositiveSmallIntegerField(default=0, verbose_name='Количество детей ')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visit_control.employee')),
            ],
            options={
                'db_table': 'group',
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('name_patronymic', models.CharField(max_length=60, verbose_name='Имя Отчество')),
                ('mobile_phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('receive_notifications', models.BooleanField(verbose_name='Получать уведомления')),
            ],
            options={
                'db_table': 'parents',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=100, verbose_name='Причина')),
                ('price', models.SmallIntegerField(verbose_name='Цена')),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naming', models.CharField(max_length=30, verbose_name='Название секции')),
                ('age_limitations_to', models.PositiveSmallIntegerField(verbose_name='Возраст ограничения до')),
                ('age_limitations_after', models.PositiveSmallIntegerField(verbose_name='Возраст ограничения после')),
            ],
            options={
                'db_table': 'type_sport',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conclusion_date', models.DateField(verbose_name='Дата заключения')),
                ('data_end', models.DateField(default=0, verbose_name='Дата окончания')),
                ('price_with_sale', models.DecimalField(decimal_places=2, max_digits=10)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='visit_control.child', verbose_name='Ребенок')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='visit_control.document', verbose_name='Документ')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='visit_control.employee', verbose_name='Сотрудник')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='visit_control.group', verbose_name='Группа')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='visit_control.parent', verbose_name='Родитель')),
                ('sale', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscriptions', to='visit_control.sale', verbose_name='Скидка')),
            ],
            options={
                'db_table': 'subscription',
            },
        ),
        migrations.CreateModel(
            name='SubscriptionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_training', models.PositiveSmallIntegerField(verbose_name='Количество тренировок в месяц')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за месяц')),
            ],
            options={
                'db_table': 'subscription_type',
            },
        ),
        migrations.CreateModel(
            name='Visitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата прихода')),
                ('time_of_arrival', models.TimeField(verbose_name='Время прихода')),
                ('exit_time', models.TimeField(null=True, verbose_name='Время ухода')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitations', to='visit_control.subscription')),
            ],
            options={
                'db_table': 'visitation',
            },
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscription_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='visit_control.subscriptiontype', verbose_name='Тип абонемента'),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(max_length=20, verbose_name='День недели')),
                ('start_time', models.TimeField(verbose_name='Начало тренировки')),
                ('end_time', models.TimeField(verbose_name='Окончание тренировки')),
                ('training_room', models.CharField(max_length=20, verbose_name='Зал')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='visit_control.group', verbose_name='Группа')),
            ],
            options={
                'db_table': 'schedule',
            },
        ),
        migrations.CreateModel(
            name='ParentChild',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='visit_control.child', verbose_name='ребенок')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='visit_control.parent', verbose_name='родитель')),
            ],
            options={
                'db_table': 'parent_child',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='naming_sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='visit_control.sport'),
        ),
        migrations.CreateModel(
            name='EmployeeSport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sports', to='visit_control.employee')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='visit_control.sport')),
            ],
            options={
                'db_table': 'employee_sport',
            },
        ),
        migrations.AddField(
            model_name='document',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='visit_control.parent'),
        ),
        migrations.AddIndex(
            model_name='child',
            index=models.Index(fields=['surname'], name='surname_index'),
        ),
    ]
