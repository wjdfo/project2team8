from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

import chromadb
import os

import json

##########################
# chromadb collection 어디 저장할 것인가
DB_SAVE_PATH = 'C:\\chroma_temp_store\\'

# collection 이름
COLLECTION_NAME = 'whole_240331_0901_json'

# embedding model
EMBEDDING_MODLE = 'sentence-transformers/all-mpnet-base-v2'

# 추출된 파일 어느 폴더에 있는가?
DATA_PATH = 'data'

# 어떤 item들을 저장할 것인가 ? default는 전부 다
EXTRACTED_ITEMS = [ "1", "1A", "1B", "2", "3", "4", "5", "6", "7", "7A",
                 	"8", "9", "9A", "9B", "10", "11", "12", "13", "14", "15"]

# API KEY
API_KEY = ''
###########################

# json 에 해당 키값이 존재하는가
def is_json_key_present(json, key):
    try:
        buf = json[key]
    except KeyError:
        return False

    return True



def main():
    # API_KEY 와 llm 세팅. 터미널에서도 수정 가능
    os.environ['OPENAI_API_KEY'] = API_KEY
    Settings.llm = OpenAI(model='gpt-4', temperature=0)

    # vector embedding 저장 위치
    chroma_client = chromadb.PersistentClient(path=DB_SAVE_PATH)

    # vector embedding 담겨있는 collection 다 지울 것인지 ? - !!지우기 기능 동작을 안 함!! // name 필드에 원하는 이름 적을 수 있음
    print(chroma_client.list_collections())
    i = input('wanna clean collection ( database )? (y/n) : ')
    if i == 'y' or i == 'Y' or i == '1' or i == 'ㅛ':
        collection = chroma_client.get_collection(name=COLLECTION_NAME)

        y = input('are you sure? (y/n) : ')
        if y == 'y' or y == 'Y' or y == '1' or y == 'ㅛ':
            chroma_client.delete_collection(name=COLLECTION_NAME)
            print('collection has been deleted.')

        # chroma_client.delete_collection(name=COLLECTION_NAME)


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
            
            v = int(input('store separate by each items (1), store whole report (2) : '))
            if v == 1 : print('separate by each items - selected')
            elif v == 2 : print('whole report - selected')
            else : continue

            documents = []
            
            # data 가져오기
            if os.path.exists(DATA_PATH):
                file_list = os.listdir(DATA_PATH)
            else :
                print(f'There is no {DATA_PATH} folder')
                exit()

            # 각 파일에 대해,
            for file_name in file_list:
                file_path = os.path.join(DATA_PATH, file_name)

                # json open
                with open(file_path) as fin:
                    file = json.load(fin)

                # field 값 설정 후 document 화 하기
                file_name = file['company']+file['period_of_report']

                # v == 1 : item 별로 나누어서 document 화 하기
                if v == 1 :
                    for items in EXTRACTED_ITEMS:
                        if is_json_key_present(file,f'item_{items}') == False : continue
                        text = file[f'item_{items}']
                        included_items = f'item_{items}'
                        doc_id = 'EDGAR_'+file['filing_type']+'_'+file['cik']+'_'+file['period_of_report']+':'+included_items

                        doc = Document(text = text,doc_id = doc_id, metadata = {'filename' : file_name, 'items' : included_items, 
                                                            'filing_type' : file['filing_type'], 'htm_filing_link' : file['htm_filing_link'], 'report_date' : file['period_of_report']  })
                        documents.append(doc)
                # v == 2 : 전체 내용 다 저장하기
                if v == 2 :
                    text = ''
                    included_items =''
                    for items in EXTRACTED_ITEMS:
                        if is_json_key_present(file,f'item_{items}') == False : continue
                        text += file[f'item_{items}']
                        included_items += f'item_{items}, '
                    included_items = included_items[0:-2]
                    doc_id = 'EDGAR_'+file['filing_type']+'_'+file['cik']+'_'+file['period_of_report']+':'+included_items

                    doc = Document(text = text,doc_id = doc_id, metadata = {'filename' : file_name, 'items' : included_items, 
                                                        'filing_type' : file['filing_type'], 'htm_filing_link' : file['htm_filing_link'], 'report_date' : file['period_of_report']  })
                    documents.append(doc)

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
    
    # query
    chat_engine = index.as_chat_engine(
        chat_mode='context',
        system_prompt = (
            'You are a assistant to anaylsis EDGAR SEC filings. You have to give client more specific information including exact examples, current situation for client to have information to invest',
            'You have to answer in Korean, and if you find there is no exact correspondance of English word to Korean word, you can write both korean & english terms.',
            'and give informations as much as you know'
        )
    )
    response = chat_engine.chat("Categorize [Amazon]'s  [2021] year [10-K] report. at least list 5 of them")

    print(response)

if __name__ == '__main__':
    main()