import pypdf
import io

def extract_text(file_obj, filename: str) -> str:
    """Extracts text from an uploaded file object (.txt or .pdf)."""
    text = ""
    if filename.endswith(".pdf"):
        try:
            pdf_reader = pypdf.PdfReader(file_obj)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                # Extract text and append a newline to ensure separation
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            raise Exception(f"Failed to read PDF: {e}")
    elif filename.endswith(".txt"):
        try:
            text = file_obj.read().decode("utf-8")
        except Exception as e:
            raise Exception(f"Failed to read text file: {e}")
    else:
        raise Exception("Unsupported file format. Please upload a .pdf or .txt file.")
    return text
