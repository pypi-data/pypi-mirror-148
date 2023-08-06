import pdfplumber
import pandas as pd
from datetime import datetime


def extract_text_from_PDF(pdf_path: str) -> str:
    """This function returns all text from a PDF as a string.

    It requires the path of the PDF in order to find the text.
    It raises ``ValueError`` if file is not a PDF.

    Args:
        pdf_path (str): path of the PDF file

    Raises:
        ValueError: If file is not of PDF format

    Returns:
        str: all text found in the PDF
    """
    path_check = ".pdf"
    if pdf_path[-4:] != path_check:
        err_msg = "File type is incorrect. A PDF format is required"
        raise ValueError(err_msg)

    pdf_string = ""
    with pdfplumber.open(pdf_path) as pdf:
        page_list = [page.extract_text() for page in pdf.pages]
        pdf_string = ''.join(page_list).replace("\n", " ").replace("\t", " ")

    return pdf_string


def find_issue_revision_date(pdf_text: str, date_type: str) -> str:
    """This function finds date of issue or revision in the MSDS PDF.
    It returns N/A if date doesn't exist.

    It requires text of the PDF and type of date.

    Args:
        pdf_text (str): text in the PDF
        date_type (str): {'Issue', 'Revision'}
            Type of date required from the PDF

    Raises:
        ValueError: When type of date requested is incorrect

    Returns:
        str: issue or revision date as MM/DD/YYYY
    """

    if date_type != "Revision" and date_type != "Issue":
        raise ValueError("date_type is not valid. Specify Issue or Revision.")

    date_substr = "Print Date "

    if date_type == "Revision":
        date_substr = "Revision Date "

    substr_index = pdf_text.find(date_substr)

    # check if date exists
    if substr_index == -1:
        return "N/A"

    date_index = substr_index + len(date_substr)
    date = pdf_text[date_index: date_index + 10]
    return date


def current_date_and_time() -> tuple:
    """Returns current date and time as a tuple

    Returns:
        tuple: Returns current date and time as a tuple
    """
    now = datetime.now()
    # mm/dd/YYYY H:M:S
    date_string = now.strftime("%m/%d/%Y")
    time_string = now.strftime("%H:%M:%S")
    return date_string, time_string


def find_index_of_substring(pdf_text: str, input_string: str) -> list:
    """This function returns the start and end index of the input_string found in the string_from_MSDS

    Args:
        pdf_text (str): main string from where index is returned
        input_string (str): string treated as a substring

    Returns:
        list: start and end index of input_string found
    """

    position_list = []  # intitialising list of positions
    full_string = pdf_text  # Extracting the full string
    # Extracting the start position of the string
    resultstart = full_string.find(input_string)
    if resultstart == -1:
        return [-1, -1]
    position_list.append(resultstart)
    resultend = resultstart + len(input_string) - 1
    position_list.append(resultend)
    return position_list


def find_substring(pdf_text: str, substr_type: str) -> str:
    """Finds names of product, catalog number, hazard details, and signal word 
        in `pdf_text`, based on the `substr_type` given.

    Args:
        pdf_text (str): text in the PDF
        substr_type (str): {'CAS', 'Product, 'Hazard', 'Signal Text', 'Signal Word'}
            keyword to find substring of

    Raises:
        ValueError: When `substr_type` given is not supported

    Returns:
        str: words pertaining to the given `substr_type`
    """
    substr_dict = {
        "Product": {
            "start_text": "Product name  :  ",
            "end_text": "Product Number  :  ",
            "function": lambda x: x.strip(),
        },
        "CAS": {
            "start_text": "CAS-No.  : ",
            "end_text": "1.2  Relevant identified uses of the substance or mixture and uses advised against",
            "function": lambda x: x.replace(" ", ""),
        },
        "Hazard": {
            "start_text": "2.1  Classification of the substance or mixture",
            "end_text": "2.2  GHS Label elements, including precautionary statements",
            "function": lambda x: x.replace("(", "").replace(")", "").lower(),
        },
        "Signal Text": {
            "start_text": "GHS Label elements, including precautionary statements",
            "end_text": "Hazards not otherwise classified (HNOC) or not covered by GHS",
            "function": lambda x: x,
        },
        "Signal Word": {
            "start_text": "Signal word  ",
            "end_text": "Hazard statement(s)",
            "function": lambda x: x.replace(" ", ""),
        }
    }

    if substr_type not in substr_dict.keys():
        raise ValueError("Please specify the right substring type to find")

    if substr_type == "Signal Word" and 'Not a hazardous substance or mixture' in pdf_text:
        return "No labeling applicable"

    start_text = substr_dict[substr_type]["start_text"]
    end_text = substr_dict[substr_type]["end_text"]

    str_start_index = find_index_of_substring(pdf_text, start_text)
    if str_start_index[0] == -1:
        return "N/A"
    str_end_index = find_index_of_substring(pdf_text, end_text)
    if str_end_index[0] == -1:
        return "N/A"
    output = pdf_text[str_start_index[1]: str_end_index[0]]

    return substr_dict[substr_type]["function"](output)


def find_signal_word(pdf_text: str) -> str:
    """Finds signal word from text in the pdf

    Args:
        pdf_text (str): text in the pdf

    Returns:
        str: returns Danger or Warning when a hazardous substance exists. Otherwise, it returns No labeling applicable
    """
    signal_text = find_substring(pdf_text, "Signal Text")
    return find_substring(signal_text, "Signal Word")


def return_list_of_hazards_in_MSDS(pdf_text: str) -> list:
    """finds list of hazards in the pdf after comparing from an existing database

    Returns:
        list: a list of all hazards that match with hazards in the existing database.
    """

    read_file = pd.read_excel(r'./Hazard_list_detailed.xlsx')
    read_file.to_csv(r'Hazard_list_detailed.csv', index=None, header=True)
    hazard_data = pd.read_csv("Hazard_list_detailed.csv")
    hazard_classes = hazard_data["Hazard class "].tolist()
    codes = hazard_data["Code "].tolist()

    hazard_codes = [
        x.replace(u'\xa0 ', u'').replace(' ', '') for x in codes]

    hazard_details = find_substring(pdf_text, "Hazard")
    hazard_words = hazard_details.split()
    hazard_list = []

    for code_index in range(len(hazard_codes)):
        for word in hazard_words:
            if hazard_codes[code_index].lower() == word.lower():
                hazard_list.append(hazard_classes[code_index])
    return hazard_list


def analyze_sigma_aldrich_sheet(pdf_path: str) -> dict:
    """returns a summary of data found in the pdf as a dictionary

    Args:
        pdf_path (str): file path of the PDF

    Raises:
        ValueError: When incorrect arguments are passed to the functions.

    Returns:
        dict: This dictionary contains summary of the hazard related data found in the MSDS PDF.
    """
    err_msg = "For the current version please use MSDS of the form -https://www.sigmaaldrich.com/US/en/sds/sial/251275so that it contains hazard codes. For example, in Section 2.1 the hazard code is H319. For more details on hazard codes please check -https://unece.org/DAM/trans/danger/publi/ghs/ghs_rev07/English/06e_annex3.pdf"
    try:
        pdf_text = extract_text_from_PDF(pdf_path)
        issue_date = find_issue_revision_date(pdf_text, "Issue")
        revision_date = find_issue_revision_date(pdf_text, "Revision")
        catalog_number = find_substring(pdf_text, "CAS")
        product_name = find_substring(pdf_text, "Product")
        upload_date, upload_time = current_date_and_time()
        hazard_list = return_list_of_hazards_in_MSDS(pdf_text)
        signal_word = find_signal_word(pdf_text)
        output = {
            "Issue Date": issue_date,
            "Revision Date": revision_date,
            "CAS Number": catalog_number,
            "Product Name": product_name,
            "Upload Date": upload_date,
            "Upload Time": upload_time,
            "List of Hazards": hazard_list,
            "Signal Word": signal_word
        }
        if "N/A" in output.values():
            raise ValueError(f"Error: {err_msg}")

        return output
    except ValueError:
        print(f"Error: {err_msg}")
