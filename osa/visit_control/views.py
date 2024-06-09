from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormView

from notification_bot.bot import send_notification
from .models import Group, Schedule, Visitation, Employee


def index(request):
    return render(request, 'index.html')


class GetSchedulesListView(ListView):
    model = Schedule
    template_name = 'schedule.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        hard_code_time = "16:00:00"
        hard_code_day = "Понедельник"
        schedules = Schedule.objects.select_related("group__employee", "group__naming_sport")\
            .filter(day_of_week=hard_code_day, start_time=hard_code_time)

        return schedules


class GetChildrenListView(ListView):
    model = Group
    template_name = 'group.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return Group.objects.prefetch_related("subscriptions").get(id=group_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        today = "2024-06-10"
        context = super().get_context_data(**kwargs)
        subscriptions = self.get_queryset().subscriptions.all()
        if 'arrival_children' in self.request.POST:
            checked = self.request.POST['arrival_children']
            if checked == 'on':
                subscriptions = []
                s = self.get_queryset().subscriptions.all()
                visits = s.prefetch_related('visitations')
                for visit in visits:
                    if visit.visitations.all().filter(date="2024-06-10"):
                        subscriptions.append(visit)

        for subscription in subscriptions:
            visit = subscription.visitations.filter(date=today).first()
            count = subscription.subscription_type.amount_training - subscription.visitations.count()
            subscription.first_visit = visit
            subscription.count = count

        context["subscriptions"] = subscriptions
        context['group'] = self.get_queryset()

        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


def create_visit(request):
        subscription_id = request.POST.get("subscription_id")
        if subscription_id:
            date = "2024-06-10"
            time_of_arrival = "16:01:00"
            exit_time = "17:35:00"

            if request.POST.get('action') == 'arrival':
                visitation = Visitation.objects.create(
                    date=date,
                    time_of_arrival=time_of_arrival,
                    exit_time=None,
                    subscription_id=subscription_id
                )
                chat_id = visitation.subscription.parent.chat_id
                if chat_id:
                    message = f"Ваш ребенок пришел на тренировку в {visitation.time_of_arrival}"
                    send_notification(message, chat_id)

            elif request.POST.get('action') == 'exit':
                visitation = Visitation.objects.filter(subscription_id=subscription_id).first()
                visitation.exit_time = exit_time
                visitation.save()
                chat_id = visitation.subscription.parent.chat_id
                if chat_id:
                    message = f"Ваш ребенок вышел с тренировки в {visitation.exit_time}"
                    send_notification(message, chat_id)

        return redirect(request.META.get('HTTP_REFERER', '/'))


class GetStatisticGroupToday(ListView):
    model = Visitation
    template_name = 'statistic.html'

    def get_queryset(self):
        return (Visitation.objects.select_related('subscription__group').
                  filter(date="2024-06-10").
                  values('subscription__group__naming',
                         'subscription__group__employee',
                         'subscription__group__children_count').
                  annotate(num_people=Count('id')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        visitations = self.get_queryset()
        data_groups = []
        for visit in visitations:
            group_data = {
                'group_name': visit['subscription__group__naming'],
                'coach': Employee.objects.get(id=visit['subscription__group__employee']),
                'count_children': visit['subscription__group__children_count'],
                'total_children_visited_today': visit['num_people']
            }
            data_groups.append(group_data)

        context['data_groups'] = data_groups
        return context















