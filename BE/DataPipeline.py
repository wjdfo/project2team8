from Knuturn import Knuturn
import tiktoken
import os
import json
import chromadb
from openai import OpenAI as op
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

class DataPipeline(Knuturn) :
    def __init__(self) :
        self.gpt_model = 'gpt-3.5-turbo'
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

    def report_summary(self, report_data: dict, option : int) : # param : 사업보고서 크롤링 데이터 원본
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
        
        client = op(api_key = self.GPT_API_KEY)

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

                    #option parameter 이용해서 dart - edgar context 분리
                    if option == 1 : context = self.dart_context
                    else : context = self.edgar_context

                    for query_text in buffer :
                        response = client.chat.completions.create(
                            model = self.gpt_model,
                            messages = context + [{"role": "user", "content": f'Summarize the following text in 5 sentences :\n{query_text}'}],
                            temperature = 0, # 0 ~ 1 실수, response의 다양성
                            top_p = 0.7
                        )

                        output += response.choices[0].message.content + '\n'

                    # test
                    with open("./test_datapipeline_summary.txt", "a", encoding = "utf-8") as test_file :
                        test_file.write(output)
                
                key = f"{corp_name} {report}"

                self.embeddingNsummary(output, key)

        return output

    def embeddingNsummary(self, sum_data: str, key) : # param : 요약된 데이터
        EMBEDDING_MODEL = 'sentence-transformers/all-mpnet-base-v2'
        
        documents = list()

        # vector embedding 저장 위치
        chroma_client = chromadb.PersistentClient(path = self.db_path)

        # i = input('wanna clean collection ( database )? (y/n) : ')
        # if i == 'y' or i == 'Y' or i == '1' or i == 'ㅛ':
        #     collection = chroma_client.get_collection(name = self.collection_name)

        #     y = input('are you sure? (y/n) : ')
        #     if y == 'y' or y == 'Y' or y == '1' or y == 'ㅛ':
        #         chroma_client.delete_collection(name = self.collection_name)
        #         print('collection has been deleted.')

        # cosine 유사도 기반으로 저장
        collection = chroma_client.get_or_create_collection(name = self.collection_name, metadata={'hnsw:space': 'cosine'})
        embed_model = LangchainEmbedding(
            HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        )

        # llamaindex에서 chromadb 다루기
        vector_store = ChromaVectorStore(chroma_collection=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # 파일을 읽어서 임베딩하고 ChromaDB에 저장
        # for file_name in os.listdir(file_path):
        #     # 목차로 요약한 파일인 경우, 생략
        #     if file_name.split('-')[0] != 'test':
        #         continue

        #     if file_name.endswith('.txt'):
        #         with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as file:
        #             content = file.read()
        #             corp_name = file_name.split('-')[1]
        #             report_num = file_name.split('-')[2].split('.')[0]
        #             key = f'{corp_name}/{report_num}'
        #             embedding = embed_model.encode(content)

        #             document = Document(key=key, vector=embedding)
        #         documents.append(document)

        document = Document(key = key, text = sum_data)
        documents.append(document)

        # 임베딩된 문서를 ChromaDB에 적재
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            embed_model=embed_model
        )

