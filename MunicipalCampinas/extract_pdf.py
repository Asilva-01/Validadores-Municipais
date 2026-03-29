import PyPDF2

def extract_pdf():
    text = ""
    with open('Manual_de_importacao_de_Servicos_Tomados (1).pdf', 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
            
    with open('manual_campinas.md', 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == '__main__':
    extract_pdf()
