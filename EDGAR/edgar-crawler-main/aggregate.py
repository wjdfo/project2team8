import edgar_crawler
import extract_items
import json
import os
from __init__ import DATASET_DIR
import datetime

def main():


    edgar_crawler.main()

    print('edgar_crawler done')

    extract_items.main()

    print('extarct_items done')

    # add something
    
        



if __name__ == "__main__":
    main()
