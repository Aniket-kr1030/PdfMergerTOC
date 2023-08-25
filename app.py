
from flask import Flask, render_template, request, send_from_directory
import fitz
import os
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
MERGED_PDF_PATH = "merged_pdf.pdf"

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the list of uploaded files
        uploaded_files = request.files.getlist("pdf_files")

        # Save the uploaded files to the server
        pdf_paths = []
        for file in uploaded_files:
            if file.filename.endswith('.pdf'):
                save_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(save_path)
                pdf_paths.append(save_path)

        # Merge the uploaded PDFs
        create_and_merge_with_visible_toc_v18(pdf_paths, ["Section " + str(i+1) for i in range(len(pdf_paths))], MERGED_PDF_PATH)

        return render_template('download.html')

    return render_template('upload.html')

@app.route('/download', methods=['GET'])
def download():
    return send_from_directory(".", "merged_pdf.pdf")

def create_and_merge_with_visible_toc_v18(pdf_paths, titles, output_path):
    
    # Append each PDF to the merged document and keep track of start pages for TOC
    start_pages = [1]  # TOC will be the first page

    titles = []
    
    for path in pdf_paths:
        pdf = fitz.open(path)
        first_page = pdf[0]
        first_line = first_page.get_text("text").splitlines()[0]
        
        # Truncate long titles and add an ellipsis
        max_title_length = 50
        if len(first_line) > max_title_length:
            first_line = first_line[:max_title_length - 3] + "..."
        titles.append(first_line)
# Create a new merged PDF
    merged_pdf = fitz.open()

    # Append each PDF to the merged document
    current_page_num = 0
    for path in pdf_paths:
        pdf = fitz.open(path)
        merged_pdf.insert_pdf(pdf)
        start_pages.append(start_pages[-1] + len(pdf))
        

        current_page_num += len(pdf)
    print(pdf_paths)
    
    print(start_pages)

    # Insert a TOC page at the beginning of the merged PDF
    toc_page = merged_pdf.new_page(0)

    # Manually center the heading "TABLE OF CONTENTS" on the page
    toc_title = "TABLE OF CONTENTS"
    text_width = fitz.get_text_length(toc_title, fontname="times-bold", fontsize=20)
    x_centered_position = (toc_page.rect.width - text_width) * 0.5
    toc_page.insert_text((x_centered_position, 70), toc_title, fontsize=20, fontname="times-bold")

    # Initialize starting position for TOC entries
    y_position = 120

    # Add titles to the TOC page and create clickable links
    current_page_num = 1  # TOC will be the first page
    k = 1
    for index, title in enumerate(titles):
        text = f"{k}. {title}"
        k+=1
        page_text = f"{start_pages[index]}"  # +1 to account for the TOC page itself
        toc_page.insert_text((100, y_position), text, fontsize=11)
        toc_page.insert_text((500, y_position), page_text, fontsize=9)  # Aligned to the right
        
        # Create a clickable rectangle aligned with the text
        rect = fitz.Rect(100, y_position -8, toc_page.rect.width - 100, y_position+12 )
        toc_page.insert_link({
            "from": rect,
            "kind": fitz.LINK_GOTO,
            "page": start_pages[index]
        })
        
        y_position += 30
        current_page_num += 1

    # Add page numbers to each page excluding the TOC page
    for i, page in enumerate(merged_pdf):
         # Skip the TOC page
        page.insert_text((50, toc_page.rect.height-20), str(i), fontsize=8)  # Add centered page number at the bottom

    # Save the merged PDF
    merged_pdf.save(output_path)
    merged_pdf.close()


if __name__ == "__main__":
    app.run(debug=True)
