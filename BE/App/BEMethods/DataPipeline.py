from .Knuturn import Knuturn
import tiktoken
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.schema import TextNode

from tqdm import tqdm

class DataPipeline(Knuturn) :
    def __init__(self) :
        super().__init__()
        self.dart_context = [
            {"role": "system", "content":'You are an assistant to summarize Korean business report. Your task is to help summarizing and categorizing business report to understand whole data of filings.'},
            {"role": "system", "content":'You have to answer in Korean, and if you find there is no exact correspondance of English word to Korean word, you can write both korean & english terms.'},
            {"role": "system", "content":'You have to use specific words in the text. Write company name in English or Korean'},
            {"role": "system", "content":'do not give additional illustrations.'}
        ]
        self.edgar_context = [
            {"role": "system", "content":'You are an assistant to summarize EDGAR SEC filings. Your task is to help summarizing and categorizing SEC filings to understand whole data of filings.'},
            {"role": "system", "content":'You have to answer in Korean, and if you find there is no exact correspondance of English word to Korean word, you can write both korean & english terms.'},
            {"role": "system", "content":'You have to use specific words in the text. Write company name in English'},
            {"role": "system", "content":'do not give additional illustrations.'}
        ]

    def report_summary(self, report_data: dict, isDart : bool) : # param : 사업보고서 크롤링 데이터 원본
        sum_report = {}
        # token 수 세기 위한 model encoder
        encoder = tiktoken.encoding_for_model(self.gpt_model)

        # 문자열을 원하는 개수로 나누는 함수
        def divide_string(string, parts):
            part_length = len(string) // parts

            substrings = [string[i:i + part_length] for i in range(0, len(string), part_length)]

            if len(substrings) > parts and len(encoder.encode(substrings[-1])) < 2000:
                substrings[-2] += substrings[-1]
                substrings.pop()

            return substrings

        for corp_name in report_data.keys() :
            for report in report_data[corp_name].keys() :
                output = ""
                
                for item in report_data[corp_name][report].keys() :
                    text = ""
                    for element in report_data[corp_name][report][item] :
                        text += element

                    buffer = [text]
                    tokenizing = encoder.encode(buffer[0])

                    if len(tokenizing) > 10000 :
                        buffer = divide_string(buffer[0], (len(tokenizing) // 10000) + 1)

                    #dart - edgar context 분리
                    if isDart : context = self.dart_context
                    else : context = self.edgar_context

                    for query_text in buffer :
                        response = self.client.chat.completions.create(
                            model = self.gpt_model,
                            messages = context + [{"role": "user", "content": f'Summarize the following text in 5 sentences :\n{query_text}'}],
                            temperature = 0, # 0 ~ 1 실수, response의 다양성
                            top_p = 0.7
                        )
                        output += response.choices[0].message.content + '\n'
                
                sum_report[report] = output

                self.embeddingNinsert(output, corp_name, report[:4])

                break

        return sum_report

    def embeddingNinsert(self, sum_data: str, corp_name : str, report : str) : # param : 요약된 데이터, 회사명, 보고서명
        print(f"{corp_name}, {report} 요약된 데이터 ----- \n{sum_data}")
        documents = list()

        summary_storage_context = StorageContext.from_defaults(vector_store=self.summary_vector_store)

        document = TextNode(text = sum_data , metadata={'corp_name' : f'{corp_name}', 'report_num' : f'{report}'})
        print(document)
        documents.append(document)

        # 임베딩된 문서를 ChromaDB에 적재
        VectorStoreIndex(nodes=documents, storage_context=summary_storage_context, embed_model=self.embed_model)
        print(f"{corp_name}, {report} 적재 완료")

    