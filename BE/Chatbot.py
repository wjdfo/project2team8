from Knuturn import Knuturn
from Dart import Dart
from openai import OpenAI as op
from Edgar import Edgar
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.core.vector_stores import MetadataFilters,MetadataFilter, FilterOperator, FilterCondition, ExactMatchFilter
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

class Chatbot(Knuturn) :
    def __init__(self) :
        #self.gpt_model_name = 'gpt-3.5-turbo'
        #self.context = ""
        super().__init__()
        self.dart = Dart()
        self.edgar = Edgar()
        # client = chromadb.PersistentClient(path = self.db_path)
        # qna_collection = client.get_or_create_collection(name = self.qna_table, metadata={'hnsw:space': 'cosine'})
        # summary_collection = client.get_or_create_collection(name = self.summary_table, metadata={'hnsw:space': 'cosine'})
        # self.embed_model = LangchainEmbedding(
        #                         HuggingFaceEmbeddings(model_name = self.EMBEDDING_MODEL)
        #                     )
        # qna_vector_store = ChromaVectorStore(chroma_collection = qna_collection)
        # summary_vector_store = ChromaVectorStore(chroma_collection = summary_collection)
        # self.qna_index = VectorStoreIndex.from_vector_store(vector_store=qna_vector_store, embed_model=self.embed_model)
        # self.summary_index = VectorStoreIndex.from_vector_store(vector_store=summary_vector_store, embed_model=self.embed_model)

    def getCorpList(self, isDart : bool) : # true : dart / false : edgar
        # case : dart
        Dart = [
            "삼성전자", "SK하이닉스", "LG에너지솔루션", "삼성바이오로직스", "현대자동차",
            "POSCO홀딩스", "삼성SDI", "LG화학", "NAVER", "KB금융", "에코프로비엠", "현대모비스",
            "신한지주", "포스코퓨처엠", "삼성생명", "하나금융지주", "에코프로", "메리츠금융지주",
            "LG전자", "LG",
            "HLB", "카카오뱅크", "한미반도체"
        ]

        Edgar = [
            
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
        filter = [MetadataFilter(key = "corp_name", value = corp_name)]
        
        if not report_num : # 사업보고서 있는 경우에만 추가해주기 없으면 회사명으로만 query
            filter.append(
                MetadataFilter(key="report_num", value = report_num)
            )

        filters = MetadataFilters(
                filters= filter,
                condition=FilterCondition.AND, # and 연산자 사용
            )
        
        retriever = self.summary_index.as_retriever(filters=filters)
        query_result = retriever.retrieve('0')
        query_result[0].text

        return query_result[0].text
    
    def getCorpReport(self, corp_name : str, isDart : bool, date : tuple) :
        # Dart
        if isDart :
            report = {}
            report_name = ["정기 보고서", "1분기 보고서", "반기(2분기) 보고서", "3분기 보고서"]
            report_dict = self.dart.getReportCode([corp_name])
            _, report_list = self.dart.getReportURL(report_dict)

            for i in range(len(report_list)) :
                report[report_name[i]] = report_list[i]

        # # Edgar
        else :
            report = self.edgar.getReportUrl(corp_name)
            
        return report
    
    def Compare2Corps(self, corp_list : tuple) :
        # summary table에 두 회사 query 후 (요약본 2개 + LLM 이용 요약본끼리 비교) 출력
        result = {}

        corp1, corp2 = corp_list[0], corp_list[1]

        result[corp1] = self.getCorpSummary(corp1, report_num = None)
        result[corp2] = self.getCorpSummary(corp1, report_num = None)

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