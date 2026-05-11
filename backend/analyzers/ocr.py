import easyocr
import numpy as np

_reader = None


def get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(["en"], gpu=False, verbose=False)
    return _reader


def extract_text(image: np.ndarray) -> str:
    try:
        reader = get_reader()
        results = reader.readtext(image, detail=0, paragraph=True)
        full_text = " ".join(results).strip()
        return full_text
    except Exception:
        return ""
