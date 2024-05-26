from Knuturn import Knuturn
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.schema import TextNode

class QnA(Knuturn) :
    def __init__(self) :
        super().__init__()
        self.question_storage_context = StorageContext.from_defaults(vector_store=self.question_vector_store)
        self.qna_storage_context = StorageContext.from_defaults(vector_store=self.qna_vector_store)

    '''
    question_dict = {
        "삼성전자 요즘 어떤 제품으로 사업해?" : {
                "corp_name" : "삼성전자"
            }
        }
    }
    '''

    def insertQnA(self, question_dict : dict) :
        question_documents = []
        qna_documents = []

        for question in question_dict.keys() :
            corp_name = question_dict[question]["corp_name"]
            document = TextNode(text = question, metadata = question_dict[question])
            question_documents.append(document)

            # summary collection에서 참고할 데이터 가져오기
            filters = MetadataFilters(
            filters=[
                    ExactMatchFilter(key="corp_name", value="삼성전자")
                ]
            )

            retriever = self.summary_index.as_retriever(filters=filters)
            summary_data = retriever.retrieve('0')
            print(summary_data[0].text)

            while True :
                response = self.client.chat.completions.create(
                                model = self.gpt_model,
                                messages = [
                                    {"role": "system", "content": "주어지는 질문과 사업보고서 데이터를 보고 답변을 \n 구분자로 구분해서 10개 만들어줘"},
                                    {"role": "system", "content": "답변할 때는 한국어로 높임말을 사용해서 알려줘"},
                                    {"role": "user", "content": f"사업보고서 데이터는 {summary_data[0].text}, 질문은 {question}"}
                                ],
                                temperature = 1, # 0 ~ 2.0
                                top_p = 0.6
                            )

                result = response.choices[0].message.content
                result_list = result.split("\n")
                for i in range(len(result_list)) :
                    print(f"{i+1}. {result_list[i]}")
                print("\n원하는 답변 선택 (1~10), 원하는 답변이 없으면 (1~10) 이외의 아무 숫자나 입력")
                print(" >> ", end = "")
                select = int(input())
                print()

                if select >= 1 and select <= len(result_list) :
                    answer = result_list[select-1]
                    break
            
            print(f"예상질문 : {question}, 예상답변 : {answer}, 회사이름 : {corp_name}")

            metadata = {
                "corp_name" : corp_name,
                "q" : question
            }
            document = TextNode(text = answer, metadata = metadata)
            qna_documents.append(document)

        VectorStoreIndex(nodes=question_documents, storage_context=self.question_storage_context, embed_model=self.embed_model)
        VectorStoreIndex(nodes=qna_documents, storage_context=self.qna_storage_context, embed_model=self.embed_model)