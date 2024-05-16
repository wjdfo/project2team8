from django.http import *
from django.views import View
import json

class API(View):
    @classmethod
    def chatbot_response(cls, request):
        try:
            isDart = True
            corp_name = json.loads(request.body)["corpName"]
            question = json.loads(request.body)["question"]
            response = chatbot.getResponse(isDart, question)
            return JsonResponse({"message": f"Question: {question}, Answer: chatbot response"}, status=200)
        except:
            return HttpResponseBadRequest("Invalid Request")
    
    def corporations_list(self, request):
        try:
            isDart = True
            corp_name = json.loads(request.body)["corpName"]
            list = chatbot.getCorpList(isDart)
            return JsonResponse({"message": f"List: {list}"}, status=200)
        except:
            return HttpResponseBadRequest("Invalid Request")

    def summary(self, request):
        try:
            corp_name = json.loads(request.body)["corpName"]
            reportNum = json.loads(request.body)["reportNum"]
            summary = chatbot.getCorpSummary(corp_namee, reportNum)
            return JsonResponse({"message": f"Summary: {summary}"}, status=200)
        except:
            return HttpResponseBadRequest("Invalid Request")
    
    def report(self, request):
        # 특정 기업 보고서 원문 url 출력
        try:
            isDart = True
            corp_name = json.loads(request.body)["corpName"]
            fromDate = json.loads(request.body)["fromDate"]
            toDate = json.loads(request.body)["toDate"]
            list = chatbot.getCorpList(isDart, corp_name, date)
            return JsonResponse({"message": f"List: {list}"}, status=200)
        except:
            return HttpResponseBadRequest("Invalid Request")
        
    def compare(self, request):
        # 보고서끼리 비교
        try:
            isDart = True
            corpName = json.loads(request.body)["corpName"]
            targetCorpName = json.loads(request.body)["targetCorpName"]
            report = chatbot.getCorpList(isDart, corpList)
            return JsonResponse({"message": f"Report: {report}"}, status=200)
        except:
            return HttpResponseBadRequest("Invalid Request")
    
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
