from django.urls import path, include
from .views import check_parent_mobile_phone

app_name = 'notification_bot_api'

urlpatterns = [
    path('check_parent_mobile_phone/', check_parent_mobile_phone, name='check_parent_mobile_phone')
]


