from django.shortcuts import render
from visit_control.models import Parent, Child
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def check_parent_mobile_phone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mobile_phone = data.get('mobile_phone')
        chat_id = data.get('chat_id')
        if not request.body:
            return JsonResponse({'status': 'error', 'message': 'Пустое тело запроса'}, status=400)

    try:
        parent = Parent.objects.get(mobile_phone=mobile_phone)
        if parent.receive_notifications:
            parent.chat_id = chat_id
            parent.save()
            personal_data = {
                "parent": f'{parent.surname} {parent.name_patronymic}',
                "children": []
            }

            children = parent.children.all()
            for child in children:
                personal_data["children"].append(f"{child.child.surname} {child.child.name_patronymic}")
            return JsonResponse({'status': 'success', 'data': personal_data}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Нет прав на получение уведомлений'}
                                                               ,status=400)

    except Parent.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Parent not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


