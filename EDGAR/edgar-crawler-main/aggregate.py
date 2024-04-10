import edgar_crawler
import extract_items
import json
import os
from __init__ import TXTDATA_DIR, DATASET_DIR
import datetime

def main():


    edgar_crawler.main()

    print('edgar_crawler done')

    extract_items.main()

    print('extarct_items done')


    # with open("config.json") as fin:
    #     config = json.load(fin)["extract_items"]
    # extracted_filings_file = os.path.join(DATASET_DIR, config["extracted_filings_folder"] )

    # if os.path.exists(extracted_filings_file):
    #     file_list = os.listdir(extracted_filings_file)
    # else :
    #     print('There is no EXTRACTED_FILLINGS folder, check config.json')
    #     return
    
    # for file_name in file_list:
    #     file_path = os.path.join(extracted_filings_file, file_name)
    #     json_file = open(file_path,encoding='UTF-8')
    #     data = json.load(json_file)
    #     company_name = data['company']
    #     filing_date = data['period_of_report']
    #     filing_type = data['filing_type']
    #     if os.path.exists(TXTDATA_DIR):
    #         output_path = os.path.join(TXTDATA_DIR, f'{company_name}_{filing_date}_{filing_type}.txt')
    #         output_file = open(output_path,encoding='UTF-8',mode='w+')
    #     else :
    #         print('There is no TXTDATA_DIR folder')
    #         return
        
    #     data_keys = list(data.keys())
    #     want_to_extract = data_keys[13:]
    #     print(want_to_extract)
    #     output_file.write(f'{company_name}_{filing_date}_{filing_type}\n')
    #     date = datetime.datetime.strptime(filing_date, '%Y-%m-%d')
    #     output_file.write(f'year : {date.year} / month : {date.month} / day : {date.day}\n')
    #     for item in want_to_extract:
    #         output_file.write(data[item])
    #         output_file.write('\n')

    #     output_file.close()
    #     json_file.close()
    
        



if __name__ == "__main__":
    main()
