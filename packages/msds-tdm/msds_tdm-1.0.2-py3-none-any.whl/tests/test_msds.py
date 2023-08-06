import pytest
import msds


def test_bad_file_type():
    with pytest.raises(ValueError):
        msds.extract_text_from_PDF("sigma_text.fgy")


def test_bad_date_type():
    with pytest.raises(ValueError):
        msds.find_issue_revision_date("lorem ipsum", 'FooBar')


def test_wrong_index_substring():
    assert msds.find_index_of_substring("Lorem ipsum", "lorefs") == [-1, -1]


def test_wrong_substring():
    with pytest.raises(ValueError):
        msds.find_substring("lorem ipsum", 'FooBar')
