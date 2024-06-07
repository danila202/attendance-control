from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormView

from .models import Group, Schedule, Visitation, Subscription
from .forms import SubscriptionForm



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
        context = super().get_context_data(**kwargs)
        subscriptions = self.get_queryset().subscriptions.all()
        today = "2024-06-10"
        if subscriptions:
            for subscription in subscriptions:
                visit = subscription.visitations.filter(date=today).first()
                count = subscription.subscription_type.amount_training - subscription.visitations.count()
                subscription.first_visit = visit
                subscription.count = count


        context["subscriptions"] = subscriptions
        context['group'] = self.get_queryset()
        return context


def create_visit(request):
        subscription_id = request.POST.get("subscription_id")
        if subscription_id:
            date = "2024-06-10"
            time_of_arrival = "16:01:00"
            exit_time = "17:35:00"

            visitation = Visitation.objects.filter(subscription_id=subscription_id).first()
            if not visitation:
                Visitation.objects.create(
                    date=date,
                    time_of_arrival=time_of_arrival,
                    exit_time=None,
                    subscription_id=subscription_id
                )
            else:
                visitation.exit_time = exit_time
                visitation.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))








