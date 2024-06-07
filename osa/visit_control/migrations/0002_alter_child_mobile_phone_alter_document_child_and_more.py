# Generated by Django 4.2 on 2024-06-05 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visit_control', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='document',
            name='child',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='visit_control.child'),
        ),
        migrations.AlterField(
            model_name='document',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='visit_control.parent'),
        ),
        migrations.AlterField(
            model_name='document',
            name='series',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Серия'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscriptions', to='visit_control.sale', verbose_name='Скидка'),
        ),
        migrations.AlterField(
            model_name='visitation',
            name='exit_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время ухода'),
        ),
    ]