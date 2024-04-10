from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
import os
import chromadb
import json

def insert_DB(file_path):
    # chromadb collection 저장 위치
    DB_SAVE_PATH = 'C:\\chroma_temp_store\\'
    COLLECTION_NAME = 'test_json'
    EMBEDDING_MODEL = 'sentence-transformers/all-mpnet-base-v2'

    documents = list()

    # vector embedding 저장 위치
    chroma_client = chromadb.PersistentClient(path=DB_SAVE_PATH)

    i = input('wanna clean collection ( database )? (y/n) : ')
    if i == 'y' or i == 'Y' or i == '1' or i == 'ㅛ':
        collection = chroma_client.get_collection(name=COLLECTION_NAME)

        y = input('are you sure? (y/n) : ')
        if y == 'y' or y == 'Y' or y == '1' or y == 'ㅛ':
            chroma_client.delete_collection(name=COLLECTION_NAME)
            print('collection has been deleted.')

    # cosine 유사도 기반으로 저장
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME, metadata={'hnsw:space': 'cosine'})
    embed_model = LangchainEmbedding(
        HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    )

    # llamaindex에서 chromadb 다루기
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 파일을 읽어서 임베딩하고 ChromaDB에 저장
    for file_name in os.listdir(file_path):
        # 목차로 요약한 파일인 경우, 생략
        if file_name.split('-')[0] != 'test':
            continue

        if file_name.endswith('.txt'):
            with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as file:
                content = file.read()
                corp_name = file_name.split('-')[1]
                report_num = file_name.split('-')[2].split('.')[0]
                key = f'{corp_name}/{report_num}'
                embedding = embed_model.encode(content)

                document = Document(key=key, vector=embedding)
                documents.append(document)

    # 임베딩된 문서를 ChromaDB에 적재
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model
    )

def main():
    insert_DB('chromadb-llamaindex/summarized-data/dart')
    insert_DB('chromadb-llamaindex/summarized-data/edgar')

if __name__ == '__main__':
    main()