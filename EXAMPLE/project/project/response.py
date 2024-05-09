from django.http import JsonResponse
from django.views import View
import json

class Response(View) :
    def post(self, request):
        print("post 요청 받음.")
        data = json.loads(request.body)
        print(data["id"])
        return JsonResponse({"post_success" : True}, status = 200)
    
    def get(self, request) :
        print("get 요청 받음.")
        return JsonResponse({"get_success" : True}, status = 200)