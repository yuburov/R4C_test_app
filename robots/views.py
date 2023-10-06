import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from robots.forms import RobotForm


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = RobotForm(data)

            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Robot information saved successfully'})
            else:
                return JsonResponse({'error': form.errors.as_json()}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
