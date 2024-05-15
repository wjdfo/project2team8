from django.http import *
from django.views import View
import json

class API(View):
    @classmethod
    def chatbot_response(cls, request):
        try:
            question = json.loads(request.body)["question"]
            return JsonResponse({"message": f"Question: {question}, Answer: chatbot response"}, status=200)
        except:
            return HttpResponseBadRequest("Invalid Request")
    
    def corporations_list(self):

        return JsonResponse({"message": "corporations list"}, status=200)

    def summary(self, corporation, cik):
        print(corporation, cik)
        return JsonResponse({"message": f"summary for corporation: {corporation}, cik: {cik}"}, status=200)
    
class DartAPI(View):
    @classmethod
    def chatbot_response(cls, request):
        try:
            question = json.loads(request.body)["question"]
            return JsonResponse({"message": f"Question: {question}, Answer: Dart chatbot response"}, status=200)
        except:
            return HttpResponseBadRequest("Invalid Request")
    
    def corporations_list(self):

        return JsonResponse({"message": "Dart corporations list"}, status=200)

    def summary(self, corporation):

        return JsonResponse({"message": f"Dart summary for corporation: {corporation}"}, status=200)

class EdgarAPI(View):
    @classmethod
    def chatbot_response(cls, request):
        try:
            question = json.loads(request.body)["question"]
            return JsonResponse({"message": f"Question: {question}, Answer: Edgar chatbot response"}, status=200)
        except:
            return HttpResponseBadRequest("Invalid Request")

    def corporations_list(self):

        return JsonResponse({"message": "Edgar corporations list"}, status=200)

    def summary(self, corporation):

        return JsonResponse({"message": f"Edgar summary for corporation: {corporation}"}, status=200)
