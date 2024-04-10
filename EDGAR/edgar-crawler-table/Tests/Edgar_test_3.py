# To avoid pull of all company data from sec.gov on Edgar initialization,
# pass in a local path to the data
from edgar import Edgar
edgar = Edgar("/Users/crossrunway/vsCODE/project2team8/EDGAR/py-edgar/test_output/cik-lookup-data.txt")
possible_companies = edgar.find_company_name("Apple Inc.")
