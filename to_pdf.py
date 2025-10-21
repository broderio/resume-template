from playwright.sync_api import sync_playwright
import sys
import os

def html_to_pdf(input_html_path, output_pdf_path):
    # Ensure the input HTML file exists
    if not os.path.isfile(input_html_path):
        print(f"Error: The file {input_html_path} does not exist.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Load the HTML file
        page.goto(f"file://{os.path.abspath(input_html_path)}")
        
        # Generate PDF
        page.pdf(path=output_pdf_path, format="Letter")
        
        browser.close()
        print(f"PDF generated successfully at {output_pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python to_pdf.py <input_html_path> <output_pdf_path>")
    else:
        input_html_path = sys.argv[1]
        output_pdf_path = sys.argv[2]
        html_to_pdf(input_html_path, output_pdf_path)
