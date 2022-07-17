from django.http import JsonResponse

# Create your views here.

def root(request):
    response = {
        "message": "touchdown-api"
    }
    return JsonResponse(response)
