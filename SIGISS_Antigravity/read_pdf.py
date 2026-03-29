import sys
try:
    from pypdf import PdfReader
except ImportError:
    print("pypdf not installed", file=sys.stderr)
    sys.exit(1)

reader = PdfReader("c:/SIGISS_Antigravity/layout_tomador_SIGISS.pdf")
for page in reader.pages:
    print(page.extract_text())
