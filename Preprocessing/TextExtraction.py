import fitz
import sys
import os
#extracting with partial ocr
#https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/jupyter-notebooks/partial-ocr.ipynb

def extract_normally( in_base : str, out_base: str, relative_file_path : str): 
    in_path = os.path.join(in_base, relative_file_path)
    print(in_path)
    file_name = os.path.basename(relative_file_path).replace(".pdf", ".txt")
    out_path = os.path.join(out_base, file_name)
    try: 

        print(in_path)
        doc = fitz.open(in_path)  # Open the PDF document
        # Ensure the output directory exists
        os.makedirs(out_base, exist_ok=True)

        # Create output file name (replace .pdf with .txt)

        with open(out_path, "w", encoding="utf-8") as out:
            for page in doc:  # Iterate through pages
                partial_tp = page.get_textpage(flags=0, full = False)
                text = page.get_text(textpage=partial_tp)  # Get page text
                out.write(text)  # Write text to file
                out.write("\n" + ("-" * 50) + "\n")  # Page separator
        print(f"Extracted text saved to: {out_path}") 
    except Exception as e:
        print("Error when extracting pure text: ", e)

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         sys.exit(1)
#     extract_normally(sys.argv[1], sys.argv[2], sys.argv[3])