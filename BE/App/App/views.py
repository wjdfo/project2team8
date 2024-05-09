from django.http import *
from rest_framework.views import APIView

class DartAPI(APIView):
    def chatbot_response(self):

        return JsonResponse({"message": "Dart chatbot response"})

    def corporations_list(self):

        return JsonResponse({"message": "Dart corporations list"})

    def summary(self, corporation):

        return JsonResponse({"message": f"Dart summary for corporation: {corporation}"})

class EdgarAPI(APIView):
    def chatbot_response(self):

        return JsonResponse({"message": "Dart chatbot response"})

    def corporations_list(self):

        return JsonResponse({"message": "Dart corporations list"})

    def summary(self, corporation):

        return JsonResponse({"message": f"Dart summary for corporation: {corporation}"})
