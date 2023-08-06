# msds-library
A python library for working with MSDS files.

## Installing

```bash
pip install msds
```

## Usage

```python
import msds

print(msds.current_date_and_time())
```
OR
```python
from msds import current_date_and_time

print(current_date_and_time())
```

```bash
('04/01/2022', '20:53:02')
```

## Functions


### `extract_text_from_PDF(pdf_path)`

This function returns all text from a PDF as a string. It requires the path of the PDF in order to find the text. It raises `ValueError` if file is not a PDF.

**Args:**

    pdf_path (str): path of the PDF file

**Raises:**

    ValueError: If file is not of PDF format

**Returns:**

    str: all text found in the PDF


### `find_issue_revision_date(pdf_text, date_type)`

This function finds date of issue or revision in the MSDS PDF. It returns N/A if date doesn't exist. It requires text of the PDF and type of date.

**Args:**

    pdf_text (str): text in the PDF
    date_type (str): {'Issue', 'Revision'}
        Type of date required from the PDF

**Raises:**

    ValueError: When type of date requested is incorrect

**Returns:**

    str: issue or revision date as MM/DD/YYYY

### `current_date_and_time()`

Returns current date and time as a tuple

**Returns:**

    tuple: Returns current date and time as a tuple

### `find_index_of_substring(pdf_text, input_string)`

This function returns the start and end index of the input_string found in the string_from_MSDS

**Args:**

    pdf_text (str): main string from where index is returned
    input_string (str): string treated as a substring

**Returns:**

    list: start and end index of input_string found


### `find_substring(pdf_text, substr_type)`

Finds names of product, catalog number, hazard details, and signal word in `pdf_text`, based on the `substr_type` given.

**Args:**

    pdf_text (str): text in the PDF
    substr_type (str): {'CAS', 'Product, 'Hazard', 'Signal Text', 'Signal Word'}
        keyword to find substring of

**Raises:**

    ValueError: When `substr_type` given is not supported

**Returns:**

    str: words pertaining to the given `substr_type`

### `find_signal_word(pdf_text)`

Finds signal word from text in the pdf

**Args:**

    pdf_text (str): text in the pdf

**Returns:**

    str: returns Danger or Warning when a hazardous substance exists. Otherwise, it returns No labeling applicable

### `return_list_of_hazards_in_MSDS(pdf_text)`

finds list of hazards in the pdf after comparing from an existing database

**Returns:**

    list: a list of all hazards that match with hazards in the existing database.

### `analyze_sigma_aldrich_sheet(pdf_path)`

returns a summary of data found in the pdf as a dictionary

**Args:**

    pdf_path (str): file path of the PDF

**Raises:**

    ValueError: When incorrect arguments are passed to the functions.

**Returns:**

    dict: This dictionary contains summary of the hazard related data found in the MSDS PDF.

## Contributors

1. Soutick Saha - soutick2010@gmail.com
2. [Chintan Sawla](https://sawlachintan.github.io/personal-website) - sawlachintan@gmail.com

## Credits

1. Terri Bui
2. Stephen Ma
3. The Data Mine - [website](https://datamine.purdue.edu)