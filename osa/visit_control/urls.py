from django.urls import path
from django.conf.urls.static import static
from config import settings
from .views import create_visit, all_templates_view
# GetSchedulesListView, GetChildrenListView, GetStatisticGroupToday
app_name = 'visit_control'

urlpatterns = [
    path('create-visit', create_visit, name='create_visit'),
    path('all/', all_templates_view, name='all'),
    path('group/<int:group_id>/', all_templates_view, name='detail-group')

    # path('', GetSchedulesListView.as_view(), name='view_schedule'),
    # path('show-subscription/<int:group_id>/', GetChildrenListView.as_view(), name='view_subscriptions'),

    # path('statistic-group-today/', GetStatisticGroupToday.as_view(), name='statistic')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)