from Knuturn import Knuturn
from Dart import Dart
from openai import OpenAI as op

class Chatbot(Knuturn) :
    def __init__(self) :
        #self.gpt_model_name = 'gpt-3.5-turbo'
        #self.context = ""
        super().__init__()
        self.dart = Dart()

    def getCorpList(self, isDart : bool) : # true : dart / false : edgar
        # case : dart
        if isDart :
            return self.dart.getCorpList()
        
        # case : edgar
        else :
            return
        
    def getResponse(self, question : str, isDart : bool) :
        # 사용자의 질문을 받아서 qna table에 query

        # # Dart
        # if isDart :

        # # Edgar
        # else :

        return

    def getCorpSummary(self, corp_name : str, isDart : bool, report_num : str = None) :
        # summary table에 query

        # # Dart
        # if isDart :

        # # Edgar
        # else :

        return
    
    def getCorpReport(self, corp_name : str, isDart : bool, date : tuple = None) :
        # Dart
        if isDart :
            report_dict = self.dart.getReportCode([corp_name])
            report = self.dart.getReportURL(report_dict)

        # # Edgar
        # else :

        return report
    
    def Compare2Corps(self, corp_list : tuple, isDart : bool) :
        # summary table에 두 회사 query 후 (요약본 2개 + LLM 이용 요약본끼리 비교) 출력
        result = {}

        corp1, corp2 = corp_list[0], corp_list[1]

        result[corp1] = "VectorDB summary table query 내용"
        result[corp2] = "VectorDB summary table query 내용"

        client = op(api_key = self.GPT_API_KEY)
        response = client.chat.completions.create(
                        model = self.gpt_model,
                        messages = [
                            {"role": "system", "content": "너는 두 기업의 사업보고서 요약본들을 비교해서 중요한 키워드 별로 요약해주는 서비스야."},
                            {"role": "system", "content": "요약할 때, 공통적인 키워드들을 먼저 출력하고 개별적인 키워드들은 끝 부분에서 A기업은 키워드1이 어떻고 ~ B기업은 키워드2가 어떻고~ 이런 식으로 알려줘."},
                            {"role": "system", "content": "사업보고서들은 ### 구분자로 시작해서 들어올거야. 요약할 땐 개조식으로 간단명료하게 알려줘."},
                            {"role": "user", "content": f"###{result[corp1]}, ###{result[corp2]}\n 이 두 기업의 사업보고서를 중요한 키워드들끼리 비교해서 요약한 후 알려줘"}
                        ],
                        temperature = 0.5,
                        top_p = 0.6
                    )
        
        result['chatbot'] = response.choices[0].message.content

        return result