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

# 문자열을 원하는 개수로 나누는 함수
def divide_string(string, parts):
   part_length = len(string) // parts

   substrings = [string[i:i + part_length] for i in range(0, len(string), part_length)]

   if len(substrings) > parts and len(encoder.encode(substrings[-1])) < 2000:
      substrings[-2] += substrings[-1]
      substrings.pop()

   return substrings

# Edagr 데이터 요약 함수
def edgar_summ(path: str) :
    if os.path.exists(path) :
        file_list = os.listdir(path)

    else :
        print(f'There is no \"{path}\" folder. you should make one')
        exit()

    # GPT on
    client = op(api_key=API_KEY)

    # output folder
    if not os.path.exists('summarized-data\\edgar'):
        os.makedirs('summarized-data\\edgar')
    # group화 한 목차 저장할 파일
    categorized_file = "summarized-data\\edgar\\edgar-contents-grouping.txt"
    cff = open(categorized_file,"w+", encoding='UTF-8')
    
    # 모든 json 파일에 대하여
    total = len(file_list)
    for idx, file_name in enumerate(file_list) :
        file_path = os.path.join(path, file_name)

        with open(file_path, 'r', encoding = 'utf-8') as f :
            file = json.load(f)

        text_aggre=''
        output_path = f"summarized-data\\edgar\\test-{GPT_MODEL_NAME}-{file['company']}-{file['period_of_report']}.txt"
        # 출력파일
        ff = open(output_path, 'w+' , encoding='UTF-8')

        # 파일 내 모든 item에 대하여
        for items in tqdm(EDGAR_ITEMS, desc=f"{idx}/{total} : {file['company']} {file['period_of_report']}"):
            if is_json_key_present(file,f'item_{items}') == False:
                continue
            text = [file[f'item_{items}']]

            # token 수 세기
            result = encoder.encode(text[0])

            # token이 10000 보다 많으면 오류가 발생할 수 있으므로 분할
            if len(result) > 10000 :
                text = divide_string(text[0],(len(result) // 10000) + 1)

            # 요약해달라는 query
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

        # 요약 파일에 저장
        ff.write(text_aggre)
        ff.close()

        # 목차로 요약할 수 있는 10개의 keywords 반환
        response = client.chat.completions.create(
            model=GPT_MODEL_NAME,
            messages = [
                {"role": "system", "content":'You are an assistant to summarize EDGAR SEC filings. Your task is to help summarizing and categorizing SEC filings to understand whole data of filings.'},
                {"role": "system", "content":'You have to answer in Korean, and if you find there is no exact correspondance of English word to Korean word, you can write both korean & english terms.'},
                {"role": "system", "content":'You have to use specific words in the text. Write company name in English'},
                {"role": "system", "content":'do not give additional illustrations.'},
                {"role": "user", "content": f'Return at least 10 keywords needed to create a table of contents from the following text :\n{text_aggre}'}
            ],
            temperature = 0.5 # 0 ~ 1 실수, response의 다양성
        )

        # 파일에 넣기
        cff.write(f"test-{GPT_MODEL_NAME}-{file['company']}-{file['period_of_report']}\n" + response.choices[0].message.content + "\n\n")
    cff.close()

    return

# Dart 데이터 요약 함수
def dart_summ(path: str) : # param : dart data report file
    if os.path.exists(path):
        file_list = os.listdir(path)
    else:
        print(f'There is no \"{path}\" folder. you should make one')
        exit()

    # output folder
    if not os.path.exists('summarized-data\\dart'): 
        os.makedirs('summarized-data\\dart')
    # group화 한 목차 저장할 파일
    categorized_file = "summarized-data\\dart\\dart-contents-grouping.txt"
    cff = open(categorized_file,"w+", encoding='UTF-8')

    file_name = file_list[0]
    file_path = os.path.join(path, file_name)

    with open(file_path, 'r', encoding = 'utf-8') as f :
        file = json.load(f)

    # GPT on
    client = op(api_key = API_KEY)

    for corp_name in file.keys() :
        # for report_num in file[corp_name].keys() :
        for report_num in tqdm(file[corp_name].keys(), desc = f"{corp_name}") :
            output_path = f"summarized-data\\dart\\test-{GPT_MODEL_NAME}-{corp_name}-{report_num}.txt"

            with open(output_path, 'w+', encoding = 'utf-8') as ff :
                # for item in tqdm(file[corp_name][report_num].keys(), desc = f"{corp_name}, {report_num}") :
                text_aggre = ""
                
                for item in file[corp_name][report_num].keys() :
                    text = ""
                    for element in file[corp_name][report_num][item] :
                        text += element
                    
                    a = [text]
                    # token 수 세기
                    # result = encoder.encode(text)
                    result = encoder.encode(a[0])

                    print(f"기업명 : {corp_name}, rep_no : {report_num}, 목차 : {item}, # of token : {len(result)}")

                    # token이 10000 보다 많으면 오류가 발생할 수 있으므로 분할
                    if len(result) > 10000 :
                        a = divide_string(a[0], (len(result) // 10000) + 1)

                    # 요약해달라는 query
                    for query_text in a:
                        response = client.chat.completions.create(
                            model=GPT_MODEL_NAME,
                            messages = [
                                {"role": "system", "content":'You are an assistant to summarize report data. Your task is to help summarizing and categorizing report items to understand whole data of filings.'},
                                {"role": "system", "content":'You have to answer in Korean, and if you find there is no exact correspondance of English word to Korean word, you can write both korean & english terms.'},
                                {"role": "system", "content":'You have to use specific words in the text. Write company name in English or Korean'},
                                {"role": "system", "content":'do not give additional illustrations.'},
                                {"role": "user", "content": f'Summarize the following text in 5 sentences :\n{query_text}'}
                                # {"role": "user", "content": f'이 글들을 5문장 이내로 요약해줘 :\n{query_text}'}
                            ],
                        temperature = 0, # 0 ~ 1 실수, response의 다양성
                        top_p = 0.8
                    )
                    text_aggre += response.choices[0].message.content + '\n'
                    print(response.usage)

                ff.write(text_aggre)

            # 목차로 요약할 수 있는 10개의 keywords 반환
            response = client.chat.completions.create(
                model=GPT_MODEL_NAME,
                messages = [
                    {"role": "system", "content":'You are an assistant to summarize Korean business report. Your task is to help summarizing and categorizing business report to understand whole data of filings.'},
                    {"role": "system", "content":'You have to answer in Korean, and if you find there is no exact correspondance of English word to Korean word, you can write both korean & english terms.'},
                    {"role": "system", "content":'You have to use specific words in the text. Write company name in English or Korean'},
                    {"role": "system", "content":'do not give additional illustrations.'},
                    {"role": "user", "content": f'Return at least 10 keywords needed to create a table of contents from the following text :\n{text_aggre}'}
                ],
                temperature = 0, # 0 ~ 1 실수, response의 다양성
                top_p = 0.8
            )
        
            # 파일에 넣기
            cff.write(f"test-{GPT_MODEL_NAME}-{corp_name}-{report_num}\n" + response.choices[0].message.content + "\n\n")
    cff.close()

    return

def main():
    i = int(input('edgar(1) or dart(2) : '))

    if i == 1 :
        print('edgar')
        edgar_summ('data-edgar')
    elif i == 2 :
        print('dart')
        dart_summ('data-dart')
    else:
        return
    
if __name__ == "__main__":
    main()
