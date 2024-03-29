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
Entry = companyTickers.json()['1']
print(Entry)
print()

# parse CIK // without leading zeros
directCik = companyTickers.json()['1']['cik_str']

# dictionary to dataframe
companyData = pd.DataFrame.from_dict(companyTickers.json(),orient='index')

# add leading zeros to CIK
companyData['cik_str'] = companyData['cik_str'].astype(str).str.zfill(10)
cik = companyData[1:2].cik_str[0]

# get company specific filing metadata
filingMetadata = requests.get(
    f'https://data.sec.gov/submissions/CIK{cik}.json',
    headers=headers
    )

# dictionary to dataframe
allForms = pd.DataFrame.from_dict(
             filingMetadata.json()['filings']['recent']
             )

# review columns
# print(allForms.columns)
print(allForms[['accessionNumber', 'reportDate', 'form']].head(50))
print()

# Apple 10-K metadata
print('Apple 10-K metadata:')
print(allForms.iloc[38])
print()

# get company facts data
companyFacts = requests.get(
    f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',
    headers=headers
    )

# review data
print('review companyFacts data:')
print('companyFacts keys:')
print(companyFacts.json().keys())
# print(companyFacts.json()['facts'])
print('companyFacts / facts keys:')
print(companyFacts.json()['facts'].keys())
print()

# filing metadata
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']
print('companyFacts / facts / dei / EntityCommonStockSharesOutstanding keys:')
print(companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding'].keys())
print('companyFacts / facts / dei / EntityCommonStockSharesOutstanding / units:')
# print(companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['units'])
companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares']
print(companyFacts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'][0])
print()

# concept data // financial statement line items
companyFacts.json()['facts']['us-gaap']
print('companyFacts / facts / us-gaap keys: ')
print(list(companyFacts.json()['facts']['us-gaap'].keys())[:10]) # 50개의 키만 출력
print()

# different amounts of data available per concept
companyFacts.json()['facts']['us-gaap']['AccountsPayableCurrent']
companyFacts.json()['facts']['us-gaap']['Revenues']
companyFacts.json()['facts']['us-gaap']['Assets']

# get company concept data
companyConcept = requests.get(
    (
    f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/Assets.json'
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
print('companyconcept / units / USD / 1st label / val: ')
print(companyConcept.json()['units']['USD'][0]['val'])
print()

# get all filings data
print('assetsData: ')
assetsData = pd.DataFrame.from_dict((companyConcept.json()['units']['USD']))
print(assetsData)
print()

# review data
assetsData.columns
assetsData.form

# get assets from 10K forms and reset index
assets10K = assetsData[assetsData.form == '10-K']
assets10K = assets10K.reset_index(drop=True)

# plot 
print(assets10K.plot(x='end', y='val'))
