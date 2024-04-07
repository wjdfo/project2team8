import tiktoken
import os
import json
from tqdm import tqdm
from openai import OpenAI as op
##################################

# 추출할 item들의 항목(default는 모두 선택)
EDGAR_ITEMS = [ "1", "1A", "1B", "2", "3", "4", "5", "6", "7", "7A",
                 	"8", "9", "9A", "9B", "10", "11", "12", "13", "14", "15"]

GPT_MODEL_NAME = 'gpt-3.5-turbo'

# GPT API KEY
try:
    with open('./GPT_API_KEY.txt', 'r') as f:
        API_KEY = f.readline()
except FileNotFoundError:
    # 파일이 없을 경우 직접 입력
    API_KEY = input("GPT API KEY를 입력하세요: ")
    
##################################

# token 수 세기 위한 model encoder
encoder = tiktoken.encoding_for_model(GPT_MODEL_NAME)

# json에 해당 키값이 존재하는가
def is_json_key_present(json, key):
    try:
        buf = json[key]
    except KeyError:
        return False

    return True

# string을 parts 수로 나누고 싶다.
def divide_string(string, parts):
   part_length = len(string) // parts

   substrings = [string[i:i + part_length] for i in range(0, len(string), part_length)]

   if len(substrings) > parts:
      substrings[-2] += substrings[-1]
      substrings.pop()

   return substrings


def edgar_summ(path: str) :
    if os.path.exists(path) :
        file_list = os.listdir(path)

    else :
        print(f'There is no \"{path}\" folder. you should make one')
        exit()

    client = op(api_key=API_KEY)

    # 모든 json 파일에 대하여
    for file_name in file_list :
        file_path = os.path.join(path, file_name)

        with open(file_path, 'r', encoding = 'utf-8') as f :
            file = json.load(f)

        text_aggre=''

        if not os.path.exists('summarized-data\\edgar'): os.makedirs('summarized-data\\edgar')
        output_path = 'summarized-data\\edgar'
        output_path = os.path.join(output_path,f"test-{GPT_MODEL_NAME}-{file['company']}.txt")
        # 출력파일
        ff = open(output_path, 'w+' , encoding='UTF-8')

        for items in tqdm(EDGAR_ITEMS, desc=f"{file['company']} {file['period_of_report']}"):
            if is_json_key_present(file,f'item_{items}') == False : continue
            text = [file[f'item_{items}']]


            # token 수 세기
            result = encoder.encode(text[0])

            # token이 10000 보다 많으면 text 쪼개기
            if len(result) > 10000 :
                text = divide_string(text[0],len(result) // 10000)

            for query_text in text:
                response = client.chat.completions.create(
                    model=GPT_MODEL_NAME,
                    messages = [
                        {"role": "system", "content":'You are an assistant to summarize EDGAR SEC filings. Your task is to help summarizing and categorizing SEC filings to understand whole data of filings.'},
                        {"role": "system", "content":'You have to answer in Korean, and if you find there is no exact correspondance of English word to Korean word, you can write both korean & english terms.'},
                        {"role": "system", "content":'You have to use specific words in the text. Write company name in English'},
                        {"role": "system", "content":'do not give additional illustrations.'},
                        {"role": "user", "content": f'Summarize the following text in 5 sentences :\n{query_text}'}
                    ],
                    temperature = 0.5 # 0 ~ 1 실수, response의 다양성
                )
                text_aggre += response.choices[0].message.content + '\n'


        ff.write(text_aggre)
        ff.close()

    return

def main():
    i = int(input('edgar(1) or dart(2) : '))

    if i == 1 :
        print('edgar')
        edgar_summ('data-edgar')
    elif i == 2 :
        print('dart')
    else:
        return


if __name__ == "__main__":
    main()