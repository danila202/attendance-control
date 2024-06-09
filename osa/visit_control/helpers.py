from .models import Schedule, Group, Visitation, Employee
from django.db.models import Count


def get_schedules():
    hard_code_time = "16:00:00"
    hard_code_day = "Понедельник"
    schedules = Schedule.objects.select_related("group__employee", "group__naming_sport")\
        .filter(day_of_week=hard_code_day, start_time=hard_code_time)
    return schedules


def get_group_subscriptions(group_id, arrival_checked=False):
    group = Group.objects.prefetch_related("subscriptions").get(id=group_id)
    today = "2024-06-10"
    subscriptions = group.subscriptions.all()
    filtered_subscriptions = []

    if arrival_checked:
        subscriptions = []
        visits = group.subscriptions.prefetch_related('visitations')
        for subscription in visits:
            if subscription.visitations.filter(date=today).exists():
                filtered_subscriptions.append(subscription)
    else:
        filtered_subscriptions = subscriptions

    for subscription in filtered_subscriptions:
        visit = subscription.visitations.filter(date=today).first()
        count = subscription.subscription_type.amount_training - subscription.visitations.count()
        subscription.first_visit = visit
        subscription.count = count

    return {
        'group': group,
        'subscriptions': filtered_subscriptions
    }


def get_visitations_today():
    visitations = Visitation.objects.select_related('subscription__group')\
        .filter(date="2024-06-10")\
        .values('subscription__group__naming', 'subscription__group__employee', 'subscription__group__children_count')\
        .annotate(num_people=Count('id'))

    data_groups = []
    for visit in visitations:
        group_data = {
            'group_name': visit['subscription__group__naming'],
            'coach': Employee.objects.get(id=visit['subscription__group__employee']),
            'count_children': visit['subscription__group__children_count'],
            'total_children_visited_today': visit['num_people']
        }
        data_groups.append(group_data)

    return data_groups



