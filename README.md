# Resume Generator
Generate a polished resume from a simple YAML configuration file—no HTML editing required.

# Usage
Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Generate HTML:
```bash
python resume_generator.py resume.yaml --format html
```

Generate PDF:
```bash
python resume_generator.py resume.yaml --format pdf
```

Specify an output file:
```bash
python resume_generator.py resume.yaml --format pdf --output resume.pdf
```

The only file that normally needs to be edited is `resume.yaml`.
The HTML template and CSS control the presentation, while the YAML file contains the resume content.