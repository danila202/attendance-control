from django.urls import path
from django.conf.urls.static import static
from config import settings
from .views import index, GetSchedulesListView, GetChildrenListView, create_visit, GetStatisticGroupToday

app_name = 'visit_control'

urlpatterns = [
    path("", index, name='home'),
    path('show-group/', GetSchedulesListView.as_view(), name='view_schedule'),
    path('show-subscription/<int:group_id>/', GetChildrenListView.as_view(), name='view_subscriptions'),
    path('create-visit', create_visit, name='create_visit'),
    path('statistic-group-today/', GetStatisticGroupToday.as_view(), name='statistic')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)