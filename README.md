# Resume Template
Resume template written in HTML/CSS for optimal parsing by AI agents

## Instructions
1. Modify the `template/resume_template.html` file or copy it and create your own.
2. Convert your html resume into a PDF using the `to_pdf.py` script.

Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

Convert to PDF
```bash
python3 to_pdf.py <input_html_path> <output_pdf_path>
```

## Example Output
![Resume Template Page 1](images/resume_template_page_1.jpg)
![Resume Template Page 2](images/resume_template_page_2.jpg)