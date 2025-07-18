import pytest
from utils.pdf_loader import load_and_split_any_file

@pytest.mark.skip(reason="Requires actual document to fully test flow")
def test_document_loader_and_chain(tmp_path):
    dummy_file = tmp_path / "test.txt"
    dummy_file.write_text("Salesforce is a leading CRM platform.")
    chunks = load_and_split_any_file(str(dummy_file))
    assert chunks and len(chunks) > 0