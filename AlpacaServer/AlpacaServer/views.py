from django.http import JsonResponse

def camera_path(request):
    return JsonResponse({'key': 'val'})