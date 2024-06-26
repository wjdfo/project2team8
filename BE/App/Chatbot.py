from BEMethods.Knuturn import Knuturn
from BEMethods.Dart import Dart
from openai import OpenAI as op
from BEMethods.Edgar import Edgar
from llama_index.core.vector_stores import MetadataFilters,MetadataFilter, FilterCondition, ExactMatchFilter

class Chatbot(Knuturn) :
    def __init__(self) :
        super().__init__()
        self.dart = Dart()
        self.edgar = Edgar()

    def getCorpList(self, isDart : bool) : # true : dart / false : edgar
        # case : dart
        Dart = [
            "삼성전자", "SK하이닉스", "LG에너지솔루션", "삼성바이오로직스", "현대자동차",
            "POSCO홀딩스", "삼성SDI", "LG화학", "NAVER", "KB금융", "에코프로비엠", "현대모비스",
            "신한지주", "포스코퓨처엠", "삼성생명", "하나금융지주", "에코프로", "메리츠금융지주",
            "LG전자", "LG",
            "HLB", "카카오뱅크", "한미반도체"
        ]


        if isDart :
            # return self.dart.getCorpList()
            return Dart
        
        # case : edgar
        else :
            return self.edgar.getCorpList()
        
    def getResponse(self, corp_name : str, question : str) :
        # 사용자의 질문을 받아서 qna table에 query
        question_filters = MetadataFilters(
                filters=[
                        MetadataFilter(key="corp_name", value=corp_name)
                ]
            )

        question_query = self.question_index.as_retriever(filters = question_filters)
        q = question_query.retrieve(question)
        if q[0].score < 0.5 :
            return '제가 알고 있는 질문이 아닌 것 같아요. 더 정교하게 질문해주시거나 다른 질문을 해주세요.'
        anticipated_question = q[0].text

        qna_filters = MetadataFilters(
                filters=[
                        ExactMatchFilter(key="corp_name", value=corp_name),
                        MetadataFilter(key="q", value = anticipated_question)
                ],
                condition=FilterCondition.AND,
            )
        
        answer_query = self.qna_index.as_retriever(filters = qna_filters)
        a = answer_query.retrieve('0')

        return a[0].text

    def getCorpSummary(self, corp_name : str, report_num : str = None) :
        # summary table에 query

        filters = MetadataFilters(
                filters = [
                    ExactMatchFilter(key = "corp_name", value = corp_name),
                    ExactMatchFilter(key= "report_num", value = report_num)
                ],
                condition=FilterCondition.AND, # and 연산자 사용
            )
        
        retriever = self.summary_index.as_retriever(filters=filters)
        query_result = retriever.retrieve('0')
        if(len(query_result) == 0 ) : return 'DB에 해당 보고서가 없어요. 금방 추가해드릴게요 !'

        return query_result[0].text
    
    def getCorpReport(self, corp_name : str, isDart : bool, date : tuple) :
        # Dart
        if isDart :
            report = {}
            report_dict = self.dart.getReportCode([corp_name],date[0],date[1])
            _, report_list = self.dart.getReportURL(report_dict)
            for item in report_list[corp_name]:
                report[corp_name + ' ' + item[0]] = item[1]
        # # Edgar
        else :
            report = self.edgar.getReportUrl(corp_name,date)
            
        return report
    
    def Compare2Corps(self, corp_list : tuple) :
        # summary table에 두 회사 query 후 (요약본 2개 + LLM 이용 요약본끼리 비교) 출력
        result = {}
        date = '2023'

        corp1, corp2 = corp_list[0], corp_list[1]

        result[corp1] = self.getCorpSummary(corp1, date)
        result[corp2] = self.getCorpSummary(corp1, date)

        client = op(api_key = self.GPT_API_KEY)
        response = client.chat.completions.create(
                        model = self.gpt_model,
                        messages = [
                            {"role": "system", "content": "너는 두 기업의 사업보고서 요약본들을 비교해서 중요한 키워드 별로 요약해주는 서비스야."},
                            {"role": "system", "content": f"요약할 때, 공통적인 키워드들을 먼저 출력하고 개별적인 키워드들은 끝 부분에서 {corp1}은 키워드1이 어떻고 ~ {corp2}은 키워드2가 어떻고~ 이런 식으로 알려줘."},
                            {"role": "system", "content": "사업보고서들은 ### 구분자로 시작해서 들어올거야. 요약할 땐 개조식으로 간단명료하게 알려줘."},
                            {"role": "user", "content": f"###{result[corp1]}, ###{result[corp2]}\n 이 두 기업의 사업보고서를 중요한 키워드들끼리 비교해서 요약한 후 알려줘"}
                        ],
                        temperature = 0.5,
                        top_p = 0.6
                    )
        
        result['chatbot'] = response.choices[0].message.content

        return result['chatbot']
