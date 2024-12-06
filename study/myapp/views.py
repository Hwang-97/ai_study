from django.shortcuts import render
from django.http import JsonResponse

def get_data(request):
    data = {
        "message": "Hello, this is your data!",
        "status": "success",
        "data": [1, 2, 3, 4, 5]
    }
    return JsonResponse(data)
