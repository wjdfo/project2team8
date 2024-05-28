from django.http import *
from django.views import View
import json
from . import recommendation
from django.core.serializers import serialize

import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)
from Chatbot import *

# Dart인지 아닌지 판단
def dart_check(corpName, dart_list):
    if corpName in dart_list:
        return True
    return False

class API(View):
    # ChatBot 답변
    @classmethod
    def chatbot_response(cls, request):
        try:
            corpName = json.loads(request.body)["corpName"]
            isDart = json.loads(request.body)["isDart"]
            question = json.loads(request.body)["question"]
            
            chatbot = Chatbot()
            response = chatbot.getResponse(corpName, question)

            return JsonResponse({"response": response}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # 특정 기업 요약
    @classmethod
    def summary(cls, request):
        try:
            corpName = json.loads(request.body)["corpName"]
            isDart = json.loads(request.body)["isDart"]
            reportNum = json.loads(request.body)["reportNum"]

            chatbot = Chatbot()
            response = chatbot.getCorpSummary(corpName, reportNum)

            return JsonResponse({"summary": response}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # 기업 리스트
    @classmethod
    def corporations_list(cls, request):
        try:
            corpName = json.loads(request.body)["corpName"]
            isDart = json.loads(request.body)["isDart"]
            if isDart == '1' :
                isDart = True
            elif isDart == '0' :
                isDart = False
            
            chatbot = Chatbot()
            list = chatbot.getCorpList(isDart)

            return JsonResponse({"list": list}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # 특정 기업 보고서 원문 url 출력
    @classmethod
    def report(cls, request):
        try:
            corpName = json.loads(request.body)["corpName"]
            isDart = json.loads(request.body)["isDart"]
            fromDate = json.loads(request.body)["fromDate"]
            toDate = json.loads(request.body)["toDate"]
            if isDart == '1' :
                isDart = True
            elif isDart == '0' :
                isDart = False
            chatbot = Chatbot()
            link = chatbot.getCorpReport(corpName, isDart, (fromDate, toDate))

            return JsonResponse({"link": link}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # 보고서 비교
    @classmethod
    def compare(cls, request):
        try:
            corpName = json.loads(request.body)["corpName"]
            corpIsDart = json.loads(request.body)["corpIsDart"]

            targetCorpName = json.loads(request.body)["targetCorpName"]
            targetIsDart = json.loads(request.body)["targetIsDart"]

            if corpIsDart == '1' :
                corpIsDart = True
            elif corpIsDart == '0' :
                corpIsDart = False
            if targetIsDart == '1' :
                targetIsDart = True
            elif targetIsDart == '0' :
                targetIsDart = False

            # 같은 종류의 공시 데이터만 비교 가능
            if (corpIsDart and targetIsDart) or (not corpIsDart and not targetIsDart):
                chatbot = Chatbot()
                report = chatbot.Compare2Corps((corpName, targetCorpName))
            else:
                return JsonResponse({"report": "서로 다른 종류의 공시 데이터는 비교가 불가합니다."})

            return JsonResponse({"report": report}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # 검색 추천
    @classmethod
    def search_recommendation(cls, request):
        try:
            search = json.loads(request.body)["search"]
            matching_stocks = recommendation.recommendation(search)[:10]
            serialized_stocks = serialize('json', matching_stocks)
            
            return JsonResponse({"list": serialized_stocks}, json_dumps_params={'ensure_ascii': False}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
