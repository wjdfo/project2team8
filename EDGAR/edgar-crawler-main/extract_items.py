import cssutils
import json
import logging
import numpy as np
import os
import pandas as pd
import re


import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from html.parser import HTMLParser
from tqdm import tqdm
from typing import Any, Dict, List, Optional, Tuple

from __init__ import DATASET_DIR

warnings.filterwarnings('ignore',category=XMLParsedAsHTMLWarning)

# Suppress cssutils stupid warnings
cssutils.log.setLevel(logging.CRITICAL)


regex_flags = re.IGNORECASE | re.DOTALL | re.MULTILINE

class HtmlStripper(HTMLParser):
    """
    Class to strip HTML tags from a string.

    The class inherits from the HTMLParser class, and overrides some of its methods
    to facilitate the removal of HTML tags. It also uses the feed method of the parent class
    to parse the HTML.

    Attributes:
            strict (bool): Not used, but inherited from parent class.
            convert_charrefs (bool): Whether to convert all character references. By default, it is True.
            fed (list): List to hold the data during parsing.
    """

    def __init__(self):
        """
        Initializes HtmlStripper by calling the constructor of the parent class, resetting the parser,
        and initializing some attributes.
        """
        super().__init__()
        self.reset()
        self.strict = False  # Not used, but necessary for inheritance
        self.convert_charrefs = True  # Convert all character references
        self.fed = []  # List to hold the data

    def handle_data(self, data: str) -> None:
        """
        Append the raw data to the list.

        This method is called whenever raw data is encountered. In the context of
        this class, we just append the data to the fed list.

        Args:
                data (str): The data encountered.
        """
        self.fed.append(data)

    def get_data(self) -> str:
        """
        Join the list to get the data without HTML tags.

        Returns:
                str: The data as a single string.
        """
        return "".join(self.fed)

    def strip_tags(self, html: str) -> str:
        """
        Strip the HTML tags from the string.

        This method feeds the HTML to the parser and returns the data without
        HTML tags.

        Args:
                html (str): The HTML string.

        Returns:
                str: The string without HTML tags.
        """
        self.feed(html)
        return self.get_data()


class ExtractItems:
    """
    A class used to extract certain items from the raw files.

    Attributes:
            remove_tables (bool): Flag to indicate if tables need to be removed.
            items_list (List[str]): List of all items that could be extracted.
            items_to_extract (List[str]): List of items to be extracted. If not provided, all items will be extracted.
            raw_files_folder (str): Path of the directory containing raw files.
            extracted_files_folder (str): Path of the directory to save the extracted files.
            skip_extracted_filings (bool): Flag to indicate if already extracted filings should be skipped.
    """

    def __init__(
        self,
        remove_tables: bool,
        items_to_extract: List[str],
        raw_files_folder: str,
        extracted_files_folder: str,
        skip_extracted_filings: bool,
    ) -> None:
        """
        Constructs all the necessary attributes for the ExtractItems object.

        Args:
                remove_tables (bool): Whether to remove tables.
                items_to_extract (List[str]): Items to be extracted. If None, all items are extracted.
                raw_files_folder (str): Path of the folder containing raw files.
                extracted_files_folder (str): Path of the folder where extracted files should be saved.
                skip_extracted_filings (bool): Whether to skip already extracted filings.
        """
        self.remove_tables = remove_tables
        # Default list of items to extract
        self.items_list = [
            "1",
            "1A",
            "1B",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "7A",
            "8",
            "9",
            "9A",
            "9B",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
        ]
        # If no specific items to extract are provided, use default list
        self.items_to_extract = (
            items_to_extract if items_to_extract else self.items_list
        )
        self.raw_files_folder = raw_files_folder
        self.extracted_files_folder = extracted_files_folder
        self.skip_extracted_filings = skip_extracted_filings

        self.json_instance = {}

    # json has a certain key ?
    def is_json_key_present(self, json, key):
        try:
            buf = json[key]
        except KeyError:
            return False

        return True

    def get_extracted_files_folder(self):
        return self.extracted_files_folder

    def get_skip_extracted_filings(self):
        return self.skip_extracted_filings
    def get_json_instance(self):
        return self.json_instance

    @staticmethod
    def strip_html(html_content: str) -> str:
        """
        Strip the HTML tags from the HTML content.

        Args:
                html_content (str): The HTML content.

        Returns:
                str: The stripped HTML content.
        """
        # Replace closing tags of certain elements with two newline characters
        html_content = re.sub(r"(<\s*/\s*(div|tr|p|li|)\s*>)", r"\1\n\n", html_content)
        # Replace <br> tags with two newline characters
        html_content = re.sub(r"(<br\s*>|<br\s*/>)", r"\1\n\n", html_content)
        # Replace closing tags of certain elements with a space
        html_content = re.sub(r"(<\s*/\s*(th|td)\s*>)", r" \1 ", html_content)
        # Use HtmlStripper to strip remaining HTML tags
        html_content = HtmlStripper().strip_tags(html_content)

        return html_content

    @staticmethod
    def remove_multiple_lines(text: str) -> str:
        """
        Replace consecutive new lines and spaces with a single new line or space.

        Args:
                text (str): The string containing the text.

        Returns:
                str: The string without multiple new lines or spaces.
        """
        # Replace multiple new lines and spaces with a temporary token
        text = re.sub(r"(( )*\n( )*){2,}", "#NEWLINE", text)
        # Replace all new lines with a space
        text = re.sub(r"\n", " ", text)
        # Replace temporary token with a single new line
        text = re.sub(r"(#NEWLINE)+", "\n", text).strip()
        # Replace multiple spaces with a single space
        text = re.sub(r"[ ]{2,}", " ", text)

        return text

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean the text by removing unnecessary blocks of text and substituting special characters.

        Args:
                text (str): The raw text string.

        Returns:
                str: The normalized, clean text.
        """
        # Replace special characters with their corresponding substitutions
        text = re.sub(r"[\xa0]", " ", text)
        text = re.sub(r"[\u200b]", " ", text)
        text = re.sub(r"[\x91]", "‘", text)
        text = re.sub(r"[\x92]", "’", text)
        text = re.sub(r"[\x93]", "“", text)
        text = re.sub(r"[\x94]", "”", text)
        text = re.sub(r"[\x95]", "•", text)
        text = re.sub(r"[\x96]", "-", text)
        text = re.sub(r"[\x97]", "-", text)
        text = re.sub(r"[\x98]", "˜", text)
        text = re.sub(r"[\x99]", "™", text)
        text = re.sub(r"[\u2010\u2011\u2012\u2013\u2014\u2015]", "-", text)

        def remove_whitespace(match):
            ws = r"[^\S\r\n]"
            return f'{match[1]}{re.sub(ws, r"", match[2])}{match[3]}{match[4]}'

        # Fix broken section headers
        text = re.sub(
            r"(\n[^\S\r\n]*)(P[^\S\r\n]*A[^\S\r\n]*R[^\S\r\n]*T)([^\S\r\n]+)((\d{1,2}|[IV]{1,2})[AB]?)",
            remove_whitespace,
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(
            r"(\n[^\S\r\n]*)(I[^\S\r\n]*T[^\S\r\n]*E[^\S\r\n]*M)([^\S\r\n]+)(\d{1,2}[AB]?)",
            remove_whitespace,
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"(ITEM|PART)(\s+\d{1,2}[AB]?)([\-•])",
            r"\1\2 \3 ",
            text,
            flags=re.IGNORECASE,
        )

        # Remove unnecessary headers
        regex_flags = re.IGNORECASE | re.MULTILINE
        text = re.sub(
            r"\n[^\S\r\n]*"
            r"(TABLE\s+OF\s+CONTENTS|INDEX\s+TO\s+FINANCIAL\s+STATEMENTS|BACK\s+TO\s+CONTENTS|QUICKLINKS)"
            r"[^\S\r\n]*\n",
            "\n",
            text,
            flags=regex_flags,
        )

        # Remove page numbers and headers
        text = re.sub(
            r"\n[^\S\r\n]*[-‒–—]*\d+[-‒–—]*[^\S\r\n]*\n", "\n", text, flags=regex_flags
        )
        text = re.sub(r"\n[^\S\r\n]*\d+[^\S\r\n]*\n", "\n", text, flags=regex_flags)

        text = re.sub(r"[\n\s]F[-‒–—]*\d+", "", text, flags=regex_flags)
        text = re.sub(
            r"\n[^\S\r\n]*Page\s[\d*]+[^\S\r\n]*\n", "", text, flags=regex_flags
        )

        return text

    def remove_html_tables(self, doc_10k: str, is_html: bool) -> str:
        """
        Remove HTML tables that contain numerical data
        Note that there are many corner-cases in the tables that have text data instead of numerical

        Args:
                doc_10k (str): The 10-K html
                is_html (bool): Whether the document contains html code or just plain text

        Returns:
                str: The 10-K html without numerical tables
        """

        if is_html:
            tables = doc_10k.find_all("table")

            items_list = []
            for item_index in self.items_list:
                # Modify the item index format for matching in the table
                if item_index == "9A":
                    item_index = item_index.replace("A", r"[^\S\r\n]*A(?:\(T\))?")
                elif "A" in item_index:
                    item_index = item_index.replace("A", r"[^\S\r\n]*A")
                elif "B" in item_index:
                    item_index = item_index.replace("B", r"[^\S\r\n]*B")
                items_list.append(item_index)

            # Detect tables that have numerical data
            for tbl in tables:
                tbl_text = ExtractItems.clean_text(ExtractItems.strip_html(str(tbl)))
                item_index_found = False
                for item_index in items_list:
                    if (
                        len(
                            list(
                                re.finditer(
                                    rf"\n[^\S\r\n]*ITEM\s+{item_index}[.*~\-:\s]",
                                    tbl_text,
                                    flags=regex_flags,
                                )
                            )
                        )
                        > 0
                    ):
                        item_index_found = True
                        break
                if item_index_found:
                    continue

                # Find all <tr> elements with style attribute and check for background color
                trs = (
                    tbl.find_all("tr", attrs={"style": True})
                    + tbl.find_all("td", attrs={"style": True})
                    + tbl.find_all("th", attrs={"style": True})
                )

                background_found = False
                for tr in trs:
                    # Parse given cssText which is assumed to be the content of a HTML style attribute
                    style = cssutils.parseStyle(tr["style"])

					# Check for background color
                    if (
                        style["background"]
                        and style["background"].lower()
                        not in ["none", "transparent", "#ffffff", "#fff", "white"]
                    ) or (
                        style["background-color"]
                        and style["background-color"].lower()
                        not in ["none", "transparent", "#ffffff", "#fff", "white"]
                    ): 
                        background_found = True
                        break

                # Find all <tr> elements with bgcolor attribute and check for background color
                trs = (
                    tbl.find_all("tr", attrs={"bgcolor": True})
                    + tbl.find_all("td", attrs={"bgcolor": True})
                    + tbl.find_all("th", attrs={"bgcolor": True})
                )

                bgcolor_found = False
                for tr in trs:
                    if tr["bgcolor"].lower() not in [
                        "none",
                        "transparent",
                        "#ffffff",
                        "#fff",
                        "white",
                    ]:
                        bgcolor_found = True
                        break

                # Remove the table if a background or bgcolor attribute with non-default color is found
                if bgcolor_found or background_found:
                    tbl.decompose()

        else:
            # If the input is plain text, remove the table tags using regex
            doc_10k = re.sub(r"<TABLE>.*?</TABLE>", "", str(doc_10k), flags=regex_flags)

        return doc_10k

    def parse_item(
        self,
        text: str,
        item_index: str,
        next_item_list: List[str],
        positions: List[int],
    ) -> Tuple[str, List[int]]:
        """
        Parses the specified item/section in a 10-K text.

        Args:
                text (str): The 10-K text.
                item_index (str): Number of the requested Item/Section of the 10-K text.
                next_item_list (List[str]): List of possible next 10-K item sections.
                positions (List[int]): List of the end positions of previous item sections.

        Returns:
                Tuple[str, List[int]]: The item/section as a text string and the updated end positions of item sections.
        """

        # Set the regex flags
        regex_flags = re.IGNORECASE | re.DOTALL

        # Modify the item index format for matching in the text
        if item_index == "9A":
            item_index = item_index.replace(
                "A", r"[^\S\r\n]*A(?:\(T\))?"
            )  # Regex pattern for item index "9A"
        elif "A" in item_index:
            item_index = item_index.replace(
                "A", r"[^\S\r\n]*A"
            )  # Regex pattern for other "A" item indexes
        elif "B" in item_index:
            item_index = item_index.replace(
                "B", r"[^\S\r\n]*B"
            )  # Regex pattern for "B" item indexes

        # Depending on the item_index, search for subsequent sections.
        # There might be many 'candidate' text sections between 2 Items.
        # For example, the Table of Contents (ToC) still counts as a match when searching text between 'Item 3' and 'Item 4'
        # But we do NOT want that specific text section; We want the detailed section which is *after* the ToC

        possible_sections_list = []
        for next_item_index in next_item_list:
            if possible_sections_list:
                break
            if next_item_index == "9A":
                next_item_index = next_item_index.replace(
                    "A", r"[^\S\r\n]*A(?:\(T\))?"
                )  # Regex pattern for next_item_index "9A"
            elif "A" in next_item_index:
                next_item_index = next_item_index.replace(
                    "A", r"[^\S\r\n]*A"
                )  # Regex pattern for other "A" next_item_indexes
            elif "B" in next_item_index:
                next_item_index = next_item_index.replace(
                    "B", r"[^\S\r\n]*B"
                )  # Regex pattern for "B" next_item_indexes

            # Find all the text sections between the current item and the next item
            for match in list(
                re.finditer(
                    rf"\n[^\S\r\n]*ITEM\s+{item_index}[.*~\-:\s]",
                    text,
                    flags=regex_flags,
                )
            ):
                offset = match.start()

                possible = list(
                    re.finditer(
                        rf"\n[^\S\r\n]*ITEM\s+{item_index}[.*~\-:\s].+?\n([^\S\r\n]*ITEM\s+{str(next_item_index)}[.*~\-:\s])",
                        text[offset:],
                        flags=regex_flags,
                    )
                )

                # If there is a match, add it to the list of possible sections
                if possible:
                    possible_sections_list += [(offset, possible)]

        # Extract the wanted section from the text
        item_section, positions = ExtractItems.get_item_section(
            possible_sections_list, text, positions
        )

        # If item is the last one (usual case when dealing with EDGAR's old .txt files), get all the text from its beginning until EOF.
        if positions:
            # If the item is the last one, get all the text from its beginning until EOF
            if item_index in self.items_list and item_section == "":
                item_section = ExtractItems.get_last_item_section(
                    item_index, text, positions
                )
            # Item 15 is the last one, get all the text from its beginning until EOF
            elif item_index == "15":
                item_section = ExtractItems.get_last_item_section(
                    item_index, text, positions
                )

        return item_section.strip(), positions

    @staticmethod
    def get_item_section(
        possible_sections_list: List[Tuple[int, List[re.Match]]],
        text: str,
        positions: List[int],
    ) -> Tuple[str, List[int]]:
        """
        Returns the correct section from a list of all possible item sections.

        Args:
                possible_sections_list: List containing all the possible sections between Item X and Item Y.
                text: The whole text.
                positions: List of the end positions of previous item sections.

        Returns:
                Tuple[str, List[int]]: The correct section and the updated list of end positions.
        """

        # Initialize variables
        item_section: str = ""
        max_match_length: int = 0
        max_match: Optional[re.Match] = None
        max_match_offset: Optional[int] = None

        # Find the match with the largest section
        for offset, matches in possible_sections_list:
            # Find the match with the largest section
            for match in matches:
                match_length = match.end() - match.start()
                # If there are previous item sections, check if the current match is after the last item section
                if positions:
                    if (
                        match_length > max_match_length
                        and offset + match.start() >= positions[-1]
                    ):
                        max_match = match
                        max_match_offset = offset
                        max_match_length = match_length
                # If there are no previous item sections, just get the first match
                elif match_length > max_match_length:
                    max_match = match
                    max_match_offset = offset
                    max_match_length = match_length

        # Return the text section inside that match
        if max_match:
            # If there are previous item sections, check if the current match is after the last item section and get it
            if positions:
                if max_match_offset + max_match.start() >= positions[-1]:
                    item_section = text[
                        max_match_offset
                        + max_match.start() : max_match_offset
                        + max_match.regs[1][0]
                    ]
            else:  # If there are no previous item sections, just get the text section inside that match
                item_section = text[
                    max_match_offset
                    + max_match.start() : max_match_offset
                    + max_match.regs[1][0]
                ]
            # Update the list of end positions
            positions.append(max_match_offset + max_match.end() - len(max_match[1]) - 1)

        return item_section, positions

    @staticmethod
    def get_last_item_section(item_index: str, text: str, positions: List[int]) -> str:
        """
        Returns the text section starting through a given item. This is useful in cases where Item 15 is the last item
        and there is no Item 16 to indicate its ending. Also, it is useful in cases like EDGAR's old .txt files
        (mostly before 2005), where there is no Item 15; thus, ITEM 14 is the last one there.

        Args:
                item_index (str): The index of the item/section in the 10-K ('14' or '15')
                text (str): The whole 10-K text
                positions (List[int]): List of the end positions of previous item sections

        Returns:
                str: All the remaining text until the end, starting from the specified item_index
        """

        # Find all occurrences of the item/section using regex
        item_list = list(
            re.finditer(
                rf"\n[^\S\r\n]*ITEM\s+{item_index}[.\-:\s].+?", text, flags=regex_flags
            )
        )

        item_section = ""
        for item in item_list:
            # Check if the item starts after the last known position
            if item.start() >= positions[-1]:
                # Extract the remaining text from the specified item_index
                item_section = text[item.start() :].strip()
                break

        return item_section

    def extract_items(self, filing_metadata: Dict[str, Any]) -> Any:
        """
        Extracts all items/sections for a 10-K file and writes it to a CIK_10K_YEAR.json file (eg. 1384400_10K_2017.json)

        Args:
                filing_metadata (Dict[str, Any]): a pandas series containing all filings metadata

        Returns:
                Any: The extracted JSON content
        """

        absolute_10k_filename = os.path.join(
            self.raw_files_folder, filing_metadata["filename"]
        )

        # Read the content of the 10-K file
        with open(absolute_10k_filename, "r", errors="backslashreplace") as file:
            content = file.read()

        # Remove all embedded pdfs that might be seen in few old 10-K txt annual reports
        content = re.sub(r"<PDF>.*?</PDF>", "", content, flags=regex_flags)

        # Find all <DOCUMENT> tags within the content
        documents = re.findall("<DOCUMENT>.*?</DOCUMENT>", content, flags=regex_flags)

        # Initialize variables
        doc_10k = None
        found_10k, is_html = False, False

        # Find the 10-K document
        for doc in documents:
            # Find the <TYPE> tag within each <DOCUMENT> tag to identify the type of document
            doc_type = re.search(r"\n[^\S\r\n]*<TYPE>(.*?)\n", doc, flags=regex_flags)
            doc_type = doc_type.group(1) if doc_type else None

            # Check if the document is a 10-K
            if doc_type.startswith("10"):
                # Check if the document is HTML or plain text
                doc_10k = BeautifulSoup(doc, "lxml")
                is_html = (True if doc_10k.find("td") else False) and (
                    True if doc_10k.find("tr") else False
                )
                if not is_html:
                    doc_10k = doc
                found_10k = True
                break

        if not found_10k:
            if documents:
                print(
                    f'\nCould not find document type 10K for {filing_metadata["filename"]}'
                )
            # If no 10-K document is found, parse the entire content as HTML or plain text
            doc_10k = BeautifulSoup(content, "lxml")
            is_html = (True if doc_10k.find("td") else False) and (
                True if doc_10k.find("tr") else False
            )
            if not is_html:
                doc_10k = content

        # Check if the document is plain text without <DOCUMENT> tags (e.g., old TXT format)
        if filing_metadata["filename"].endswith("txt") and not documents:
            print(f'\nNo <DOCUMENT> tag for {filing_metadata["filename"]}')

        # For non-HTML documents, clean all table items
        if self.remove_tables:
            doc_10k = self.remove_html_tables(doc_10k, is_html=is_html)


        corp_name = filing_metadata['Company']
        report_num = filing_metadata['Date']

        if not self.is_json_key_present(self.json_instance,corp_name):
            self.json_instance[corp_name] = {}
        
        if not self.is_json_key_present(self.json_instance[corp_name],report_num):
            self.json_instance[corp_name][report_num] = {}



        # Extract the text from the document and clean it
        text = ExtractItems.strip_html(str(doc_10k))
        text = ExtractItems.clean_text(text)

        positions = []
        all_items_null = True
        for i, item_index in enumerate(self.items_list):
            next_item_list = self.items_list[i + 1 :]

            # Parse each item/section and get its content and positions
            item_section, positions = self.parse_item(
                text, item_index, next_item_list, positions
            )

            # Remove multiple lines from the item section
            item_section = ExtractItems.remove_multiple_lines(item_section)
            
            self.json_instance[corp_name][report_num][f'item_{item_index}'] = []

            if item_index in self.items_to_extract:
                if item_section != "":
                    all_items_null = False
                temp = item_section.split('\n')
                for i in temp:
                    self.json_instance[corp_name][report_num][f'item_{item_index}'].append(i + '\n')


        if all_items_null:
            print(f"\nCould not extract any item for {absolute_10k_filename}")
            return None

        return 1



class Edgar_Extractor:
    '''
    This is a class which extarct in-need item from stored HTML filings.

    Method:
        doExtarctFromRAWs()

    set config.json - 'edgar_cralwer' field, and doExtarctFromRAWs()
    '''
    def __init__(self):
        with open("config.json") as fin:
            self.config = json.load(fin)["extract_items"]

        self.filings_metadata_filepath = os.path.join(
            DATASET_DIR, self.config["filings_metadata_file"]
        )

        # Check if the filings metadata file exists
        if os.path.exists(self.filings_metadata_filepath):
            self.filings_metadata_df = pd.read_csv(self.filings_metadata_filepath, dtype=str)
            self.filings_metadata_df = self.filings_metadata_df.replace({np.nan: None})
        else:
            print(f'No such file "{self.filings_metadata_filepath}"')
            return

        self.raw_filings_folder = os.path.join(DATASET_DIR, self.config["raw_filings_folder"])

        # Check if the raw filings folder exists
        if not os.path.isdir(self.raw_filings_folder):
            print(f'No such directory: "{self.raw_filings_folder}')
            return

        self.extracted_filings_folder = os.path.join(
            DATASET_DIR, self.config["extracted_filings_folder"]
        )

        # Create the extracted filings folder if it doesn't exist
        if not os.path.isdir(self.extracted_filings_folder):
            os.mkdir(self.extracted_filings_folder)
            
    
    def doExtractFromRAWs(self):
        '''
        Orchestrate whole extarct sequence.

        using ExtractItems Class - to Extract Items
        and store into json files.
        its path is determined by `config.json`

        '''
        extraction = ExtractItems(
            remove_tables=self.config["remove_tables"],
            items_to_extract=self.config["items_to_extract"],
            raw_files_folder=self.raw_filings_folder,
            extracted_files_folder=self.extracted_filings_folder,
            skip_extracted_filings=self.config["skip_extracted_filings"],
        )

        print("Starting extraction...\n")

        # get metadata
        list_of_series = list(zip(*self.filings_metadata_df.iterrows()))[1]
        json_filename = 'edgar_report.json'

        # Create the absolute path for the JSON file
        absolute_json_filename = os.path.join(
            extraction.get_extracted_files_folder(),json_filename
        )
        # Skip processing if the extracted JSON file already exists and skip flag is enabled
        if extraction.get_skip_extracted_filings() and os.path.exists(absolute_json_filename):
            print(f'{json_filename} : File already exists. You can disable skip flag in config.json . . . exiting')
            return 0

        for i in tqdm(list_of_series):
            _ = extraction.extract_items(i)

        with open(absolute_json_filename, "w", encoding='UTF-8') as filepath:
            json.dump(extraction.get_json_instance(), filepath, ensure_ascii=False,indent='\t')

        redundancy_check = {}
        for report in list_of_series :
            report_company = report["Company"]
            if report_company in redundancy_check : continue
            else: redundancy_check[report_company] = 1

            json_filename = f'{report["CIK"]}_report.json'
            
            temp = os.path.join( extraction.get_extracted_files_folder(), "report_per_corp" )
            if not os.path.exists(temp): os.mkdir(temp)
            # Create the absolute path for the JSON file
            absolute_json_filename = os.path.join(
                temp ,json_filename
            )

            # Skip processing if the extracted JSON file already exists and skip flag is enabled
            if extraction.get_skip_extracted_filings() and os.path.exists(absolute_json_filename):
                print(f'{json_filename} : File already exists. You can disable skip flag in config.json . . . exiting')
                return 0

            
            with open(absolute_json_filename, "w", encoding='UTF-8') as filepath:
                d = {}
                d[report_company] = extraction.get_json_instance()[report_company]
                json.dump(d, filepath, ensure_ascii=False,indent='\t')

        print("\nItem extraction is completed successfully.")
        print(f"Extracted filings are saved to: {self.extracted_filings_folder}")