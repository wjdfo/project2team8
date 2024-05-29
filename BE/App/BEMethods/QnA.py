import os
import tiktoken
from .Knuturn import Knuturn
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter, FilterCondition
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.core.schema import TextNode
from llama_index.llms.openai import OpenAI
from tqdm import tqdm

class QnA(Knuturn) :
    def __init__(self) :
        super().__init__()
        self.question_storage_context = StorageContext.from_defaults(vector_store=self.question_vector_store)
        self.qna_storage_context = StorageContext.from_defaults(vector_store=self.qna_vector_store)

    def insertQnA_GPT(self, question_dict : dict) :
        '''
        question_dict = {
            "삼성전자" : [
                '안녕',
                '하세요',
            ]
        '''
        os.environ['OPENAI_API_KEY'] = self.GPT_API_KEY
        Settings.llm = OpenAI(model=self.gpt_model, temperature=1)
        question_documents = []
        qna_documents = []

        # 회사에 따라 보고서 요약본 먼저 retrieve
        for (idx,corp_name) in enumerate(question_dict.keys(),1) :
            question_documents = []
            qna_documents = []

            # summary collection에서 참고할 보고서 요약 데이터 가져오기
            filters = MetadataFilters(
            filters=[
                    ExactMatchFilter(key="corp_name", value=corp_name),
                    ExactMatchFilter(key="report_num", value='2023'),

                ],
                condition=FilterCondition.AND
            )
            retriever = self.summary_index.as_retriever(filters=filters)

            summary_data = retriever.retrieve('-')
            if(len(summary_data) == 0 ) : continue

            # print(summary_data[0].text)
            encoder = tiktoken.encoding_for_model(self.gpt_model)
            print(f"summary data's # of tokens : {len(encoder.encode(summary_data[0].text))}")

            # 각 질문에 대하여,
            for question in tqdm(question_dict[corp_name], desc = f'{corp_name} ({idx}/{len(question_dict.keys())})'):

                document = TextNode(text = question, metadata = { 'corp_name' : f'{corp_name}'})
                question_documents.append(document)


                # context = (
                #     '주어지는 질문과 사업보고서 데이터를 보고 답변을 \n 구분자로 구분해서 10개 만들어줘',
                #     '답변할 때는 한국어로 높임말을 사용해서 알려줘'
                # )


                response = self.client.chat.completions.create(
                                model = self.gpt_model,
                                messages = [
                                    {"role": "system", "content": "주어지는 질문과 사업보고서 데이터를 보고 답변을 만들어줘"},
                                    {"role": "system", "content": "답변할 때는 한국어로 높임말을 사용해서 알려줘. 정보만 간단히 전달해."},
                                    {"role": "user", "content": f"사업보고서 데이터 :  {summary_data[0].text}, 질문 : {question}"}
                                ],
                                temperature = 1, # 0 ~ 2.0
                                top_p = 0.6
                            )
                # chat_engine = self.summary_index.as_chat_engine(
                #     chat_mode='context',
                #     system_prompt = context,
                #     filters = filters
                # )
                # result = chat_engine.chat(question)

                result = response.choices[0].message.content

            
                print(f"질문 : {question} \n 예상답변 : {result} \n 회사이름 : {corp_name}")

                metadata = {
                    "corp_name" : corp_name,
                    "q" : question
                }
                document = TextNode(text = result, metadata = metadata)
                qna_documents.append(document)

            # 한 회사 질문이 끝나면 DB에 Store
            VectorStoreIndex(nodes=question_documents, storage_context=self.question_storage_context, embed_model=self.embed_model)
            VectorStoreIndex(nodes=qna_documents, storage_context=self.qna_storage_context, embed_model=self.embed_model)

    def insertQnA_User(self, question_dict : dict) :
        '''
        question_dict = {
            "삼성전자" : {
                '예상 질문' : "사용자 정의 답변",
                '예상 질문' : "사용자 정의 답변",
            }
        '''
        qna_documents = []
        question_documents = []

        for corp_name in question_dict.keys() :
            qna_documents.append(TextNode(text = question_dict[corp_name][question], metadata = metadata))
            print(f"-------------------회사명 - {corp_name}-------------------")

            for question in question_dict[corp_name].keys() :
                metadata = {
                    "corp_name" : corp_name,
                    "q" : question
                }
                
                question_documents.append(TextNode(text = question, metadata = {"corp_name" : f"{corp_name}"}))
                print(f"---예상 질문---\n{question}\n---답변---\n{question_dict[corp_name][question]}")
            
            print()
            
        VectorStoreIndex(nodes=question_documents, storage_context=self.question_storage_context, embed_model=self.embed_model)
        VectorStoreIndex(nodes=qna_documents, storage_context=self.qna_storage_context, embed_model=self.embed_model)