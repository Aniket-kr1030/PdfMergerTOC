
# Flask PDF Merger Application

This application allows users to merge multiple PDF files and automatically generates a table of contents for the merged PDF. The table of contents includes clickable links to each merged PDF's starting page.

## Setup and Installation

1. Clone the repository:
```
git clone https://github.com/Aniket-kr1030/PdfMergerTOC
```

2. Navigate to the project directory:
```
cd PdfMergerTOC
```

3. Create a virtual environment:
```
python -m venv venv
```

4. Activate the virtual environment:
- On Windows:
```
venv\Scripts\activate
```
- On macOS and Linux:
```
source venv/bin/activate
```

5. Install the required dependencies:
```
pip install -r requirements.txt
```

6. Run the Flask application:
```
python app.py
```

7. Visit `http://127.0.0.1:5000/` in your web browser to access the application.

## Usage

1. Click on the "Choose Files" button to select multiple PDF files.
2. Click "Merge PDFs" to merge the selected PDFs and generate a table of contents.
3. Once the merging process is complete, click "Download Merged PDF" to download the final merged PDF with the table of contents.

## Features

- Merge multiple PDF files with ease.
- Automatically generates a table of contents based on the merged PDFs.
- Table of contents includes clickable links to each PDF's starting page.
