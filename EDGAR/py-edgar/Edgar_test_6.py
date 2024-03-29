"""
SEC Filing Scraper
"""

# import modules
import requests
import pandas as pd

# create request header
headers = {'User-Agent': "crossrunway01@gmail.com"}

# get all companies data
companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers=headers
    )

# review response / keys
# print(companyTickers.json().keys())

# format response to dictionary and get first key/value
firstEntry = companyTickers.json()['1']
print('Second Entry:')
print(firstEntry)
print()

# parse CIK // without leading zeros
directCik = companyTickers.json()['1']['cik_str']
print('directCik:',directCik)
print()

# dictionary to dataframe
companyData = pd.DataFrame.from_dict(companyTickers.json(),orient='index')
print('companyData:')
print(companyData)
print()

# add leading zeros to CIK
companyData['cik_str'] = companyData['cik_str'].astype(str).str.zfill(10)
print(companyData)
print()

# review data
print('companyData[1]:')
print(companyData[1:2])
print()

cik = companyData[1:2].cik_str[0]
print('cik:', cik)
print()

# get company specific filing metadata
filingMetadata = requests.get(
    f'https://data.sec.gov/submissions/CIK{cik}.json',
    headers=headers
    )
print('filingMetadata:')
print(filingMetadata)
print()

# review json
print('filingMetadata.json().keys():')
print(filingMetadata.json().keys())
filingMetadata.json()['filings']
filingMetadata.json()['filings'].keys()
filingMetadata.json()['filings']['recent']
filingMetadata.json()['filings']['recent'].keys()
print()

# dictionary to dataframe
allForms = pd.DataFrame.from_dict(
             filingMetadata.json()['filings']['recent']
             )
print('allForms:')
print(allForms)
print()

# review columns
print(allForms.columns)
print()
print(allForms[['accessionNumber', 'reportDate', 'form']].head(50))
print()

# 10-Q metadata
print(allForms.iloc[11]) # allForms의 12번째 행 선택
print()

# get company facts data
companyFacts = requests.get(
    f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',
    headers=headers
    )
print('companyFacts:')
print(companyFacts)
print()

#review data
print(companyFacts.json().keys())
companyFacts.json()['facts']
print(companyFacts.json()['facts'].keys())
print()

# filing metadata
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding'].keys()
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['units']
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares']
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'][0]

# concept data // financial statement line items
companyFacts.json()['facts']['us-gaap']
print(list(companyFacts.json()['facts']['us-gaap'].keys())[:50]) # 50개의 키만 출력
print()

# different amounts of data available per concept
companyFacts.json()['facts']['us-gaap']['AccountsPayableCurrent']
companyFacts.json()['facts']['us-gaap']['Revenues']
companyFacts.json()['facts']['us-gaap']['Assets']

# get company concept data
companyConcept = requests.get(
    (
    f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}'
     f'/us-gaap/Assets.json'
    ),
    headers=headers
    )

# review data
companyConcept.json().keys()
companyConcept.json()['units']
companyConcept.json()['units'].keys()
companyConcept.json()['units']['USD']
companyConcept.json()['units']['USD'][0]

# parse assets from single filing
companyConcept.json()['units']['USD'][0]['val']

# get all filings data 
assetsData = pd.DataFrame.from_dict((companyConcept.json()['units']['USD']))
print(assetsData)
print()

# review data
assetsData.columns
assetsData.form

# get assets from 10Q forms and reset index
assets10Q = assetsData[assetsData.form == '10-Q']
assets10Q = assets10Q.reset_index(drop=True)

# plot 
print(assets10Q.plot(x='end', y='val'))
