from django.http import *
from django.views import View
import json

import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)
from Chatbot import *
from Dart import *

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
            question = json.loads(request.body)["question"]
            dart = Dart()
            dart_list = dart.getCorpList()
            isDart = dart_check(corpName, dart_list)

            chatbot = Chatbot()
            response = chatbot.getResponse(question, isDart)

            return JsonResponse({"response": response}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # 특정 기업 요약
    @classmethod
    def summary(cls, request):
        try:
            corpName = json.loads(request.body)["corpName"]
            reportNum = json.loads(request.body)["reportNum"]
            dart = Dart()
            dart_list = dart.getCorpList()
            isDart = dart_check(corpName, dart_list)

            chatbot = Chatbot()
            response = chatbot.getCorpSummary(corpName, isDart, reportNum)

            return JsonResponse({"summary": response}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    # 기업 리스트
    @classmethod
    def corporations_list(cls, request):
        try:
            corpName = json.loads(request.body)["corpName"]
            dart = Dart()
            dart_list = dart.getCorpList()
            isDart = dart_check(corpName, dart_list)
            
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
            dart = Dart()
            dart_list = dart.getCorpList()
            isDart = dart_check(corpName, dart_list)
            fromDate = json.loads(request.body)["fromDate"]
            toDate = json.loads(request.body)["toDate"]

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
            targetCorpName = json.loads(request.body)["targetCorpName"]
            dart = Dart()
            dart_list = dart.getCorpList()
            corp_isDart = dart_check(corpName, dart_list)
            target_isDart = dart_check(targetCorpName, dart_list)

            # 같은 종류의 공시 데이터만 비교 가능
            if (corp_isDart and target_isDart) or (not corp_isDart and not target_isDart):
                chatbot = Chatbot()
                report = chatbot.Compare2Corps((corpName, targetCorpName), corp_isDart)
            else:
                return JsonResponse({"message": "서로 다른 종류의 공시 데이터는 비교가 불가합니다."})

            return JsonResponse({"report": report}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)