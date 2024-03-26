from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

import chromadb
import os

##########################
DB_SAVE_PATH = 'C:\\chromadustmq\\'
COLLECTION_NAME = 'my_coll'
EMBEDDING_MODLE = 'sentence-transformers/all-mpnet-base-v2'

###########################

# API_KEY 와 llm 세팅. 터미널에서도 수정 가능
os.environ['OPENAI_API_KEY'] = 'API KEY'
Settings.llm = OpenAI(model='gpt-4')

# vector embedding 저장 위치
chroma_client = chromadb.PersistentClient(path=DB_SAVE_PATH)


# vector embedding 담겨있는 collection 다 지울 것인지 ? // name 필드에 원하는 이름 적을 수 있음
i = input('wanna clean collection ( database )? (y/n) : ')
if i == 'y' or i == 'Y' or i == '1' or i == 'ㅛ':
    chroma_client.delete_collection(name=COLLECTION_NAME)
    print('collection has been deleted.')


# cosine 유사도 기반으로 저장. embedding model은 찾아봤던 논문에 있던 거 그냥 썼음..
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME,metadata={'hnsw:space' : 'cosine'})
embed_model = LangchainEmbedding(
    HuggingFaceEmbeddings(model_name=EMBEDDING_MODLE)
)


# llamaindex에서 chromadb 다루기
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

while(1):
    i = int(input('store from document data & answer (1), answer from existing vector (2) : '))
    
    # 1 : document 에서 불러와서 저장 후 query 하기
    if i == 1 :
        print('(1) selected')
        documents = SimpleDirectoryReader("data", filename_as_id=True).load_data()
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, embed_model=embed_model
        )
        break

    # 2 : 이미 존재하는 db 불러와서 query 하기
    if i == 2 :
        print('(2) selected')
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model=embed_model,
        )
        break
    else:
        print('do again')


chat_engine = index.as_chat_engine(
    chat_mode='context',
    system_prompt = (
        'You are a assistant to anaylsis EDGAR SEC filings. You have to give client more specific information including exact examples, current situation for client to have information to invest',
        'You have to answer in Korean, and if you find there is no exact correspondance of English word to Korean word, you can write both korean & english terms.',
        'and give informations as much as you know'
    )
)
response = chat_engine.chat('can you explain me about Executive Officers of Zoetis?')

print(response)