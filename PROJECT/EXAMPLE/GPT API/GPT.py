# https://platform.openai.com/docs/api-reference/introduction
from openai import OpenAI
import os

# api key - https://platform.openai.com/api-keys
api_key = "your-secret-api-key-here"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", api_key))

# client = openai( # organization 있는 경우, header에 이 정보 넣으면 됨 <- 조직에서 비용처리하는 듯
#     organization='YOUR_ORG_ID',
# )

#gpt model types
'''
"gpt-3.5-turbo-0301"
"gpt-3.5-turbo-0613"
"gpt-3.5-turbo"
"gpt-4-0314"
"gpt-4-0613"
"gpt-4"
'''

response = client.chat.completions.create(
    model="gpt-3.5-turbo-0301",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."}, # context
        {"role": "user", "content": "Who won the world series in 2020?"}, #user's question                          <- one shot (example)
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."}, #gpt's answer    <- prompting (example)
        {"role": "user", "content": "Where was it played?"}
    ],
    max_tokens = 4096, # response의 토큰 수 제한, 최대 8192
    temperature = 0, # 0 ~ 1 실수, response의 다양성
    # top_p = 0 # 0 ~ 1, response의 가능성이 몇% 이상인지 <- temperature / top_p 둘 중 하나만 쓰기, 둘 다 쓰는건 권장 X
)
print(response['choices'][0]['message']['content'])