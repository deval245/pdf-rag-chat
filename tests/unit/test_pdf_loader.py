# import pytest
# from utils.pdf_loader import load_and_split_any_file
#
# def test_load_and_split_unsupported_file(tmp_path):
#     fake_file = tmp_path / "file.xyz"
#     fake_file.write_text("dummy")
#     with pytest.raises(ValueError):
#         load_and_split_any_file(str(fake_file))
#
# @pytest.mark.skip(reason="Requires real PDF or DOCX sample to test actual splitting")
# def test_load_and_split_pdf_flow():
#     assert True

import pytest
from utils.pdf_loader import load_and_split_any_file

def test_load_and_split_unsupported_file(tmp_path):
    fake_file = tmp_path / "file.xyz"
    fake_file.write_text("dummy")
    with pytest.raises(ValueError):
        load_and_split_any_file(str(fake_file))

@pytest.mark.skip(reason="Requires real PDF or DOCX sample to test actual splitting")
def test_load_and_split_pdf_flow():
    assert True