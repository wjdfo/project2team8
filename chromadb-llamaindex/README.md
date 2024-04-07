***Chromadb - PersistentClient 생성 후 drop ( or delete) 하는 기능이 안됨 ,, DB_SAVE_PATH 경로에 가서 수동으로 지워줘야 함***

# 설치
pip install -r requirements.txt

( python 3.11.8 환경에서 실행 확인 )
# 실행

db에 적재하고 질의하기 위해서는 `gpt-answer.py` 실행

data 폴더에 있는 파일 읽어와서 요약하기 `summarization.py`


# 주의
꼭 같은 폴더 내에서 실행시켜야함 ( 상대 경로 있어서 )

# 참조
chromadb와 그를 다룰 수 있는 프레임워크 llamaindex 이용했음.

https://docs.llamaindex.ai/en/stable/examples/vector_stores/ChromaIndexDemo/

https://www.trychroma.com/

https://docs.llamaindex.ai/en/stable/examples/llm/openai/

https://docs.llamaindex.ai/en/stable/examples/chat_engine/chat_engine_context/
