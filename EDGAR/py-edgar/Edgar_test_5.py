API_KEY = 'ca311b955133ca50ff0d6bcdd4c692d0de2400302d6cd90d6d678414f28a2b52'

from sec_api import ExtractorApi
extractorApi = ExtractorApi(API_KEY)


# helper function to pretty print long, single-line text to multi-line text
def pprint(text, line_length=100):
  words = text.split(' ')
  lines = []
  current_line = ''
  for word in words:
    if len(current_line + ' ' + word) <= line_length:
      current_line += ' ' + word
    else:
      lines.append(current_line.strip())
      current_line = word
  if current_line:
    lines.append(current_line.strip())
  print('\n'.join(lines))

# URL of Tesla's 10-K filing
filing_10_k_url = 'https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231.htm'

# extract text section "Item 1 - Business" from 10-K
item_1_text = extractorApi.get_section(filing_10_k_url, '1', 'text')

print('Extracted Item 1 (Text)')
print('-----------------------')
pprint(item_1_text[0:1500])
print('... cut for brevity')
print('---------------------------------------------------------------------')



from IPython.display import display, HTML

# extract the HTML version of section "Item 6 - Selected Financial Data"
item_6_html = extractorApi.get_section(filing_10_k_url, '6', 'html')


print('Extracted Item 6 (HTML)')
print('-----------------------')
display(HTML(item_6_html[0:150000]))
print('... cut for brevity')
print('---------------------------------------------------------------------')




import pandas as pd

# read HTML table from a string and convert to dataframe
tables = pd.read_html(item_6_html)
# first table includes the financial statements
df = tables[0]

# drop all columns with NaN values except if the first cell is not NaN
mask = (df.iloc[1:, :].isna()).all(axis=0)
financial_statements = df.drop(df.columns[mask], axis=1).fillna('')
df.to_json('/Users/crossrunway/vsCODE/project2team8/EDGAR/py-edgar/test_output/data.json', orient='records')
print('Consolidated financial statements as dataframe:')
financial_statements