import subprocess
import PyPDF2
import shutil
import os


def list_files_in_folder(folder_path):
    files_in_dir = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            files_in_dir.append(file)
    return files_in_dir

def carry_invoice_PDFs(folder_path, ghostscript_path):
    files = list_files_in_folder(folder_path)
    i = 0
    for invoice_file in files:
        if "DJT" in invoice_file:
            i += 1
            input_file = folder_path + "\\" + invoice_file
            output_file = '{}.pdf'.format(str(i))

            # Use Ghostscript to convert the input file to PDF
            command = [ghostscript_path, '-sDEVICE=pdfwrite', '-o', output_file, input_file]
            subprocess.call(command)

def split_pdf_pages(input_file_path):
    with open(input_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[page_num])
            output_file_path = f"page_{page_num + 1}.pdf"
            with open(output_file_path, 'wb') as output_file:
                writer.write(output_file)
            print(f"Page {page_num + 1} saved as {output_file_path}.")

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def extract_data_from_pdf(pdf_file):
    extracted_text = read_pdf(pdf_file)

    var_symbol_index = extracted_text.find("Var. symbol: ") + 12
    end_index = var_symbol_index + 9
    invoice_no = extracted_text[var_symbol_index: end_index].replace(" ", '')

    despatch_date_index = extracted_text.find("Despatch date: ") + 14
    despatch_date_end_index = despatch_date_index + 11
    despatch_date = extracted_text[despatch_date_index: despatch_date_end_index].replace(" ", "")

    VIN_start_index = extracted_text.find("VIN ") + 4
    VIN_end_index = VIN_start_index + 17
    VIN = extracted_text[VIN_start_index: VIN_end_index].replace(" ", '')

    return(invoice_no, despatch_date, VIN)

def rename_pdf(old_name, new_name):
    try:
        os.rename(old_name, new_name + ".pdf")
        print(f"File renamed from '{old_name}' to '{new_name}' successfully.")
    except FileNotFoundError:
        print(f"File '{old_name}' not found.")
    except FileExistsError:
        print(f"A file with the name '{new_name}' already exists.")

def pdf_folder_job():
    folder_name = r"C:\+-+Users\+-+yuceappadmin\+-+Desktop\+-+pdfs".replace("+-+","")

    pdf_files = [file for file in os.listdir() if file.endswith(".pdf")]

    if len(pdf_files) == 0:
        return

    for file in pdf_files:
        new_path = os.path.join(folder_name, file)
        shutil.move(file, new_path)

def search_and_copy_files(source_folder, target_folder, search_string):
    file_found = False
    # Walk through the source folder and its subfolders
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if search_string in file:
                source_path = os.path.join(root, file)
                target_path = os.path.join(target_folder, file)
                # Copy the file to the target folder
                shutil.copy(source_path, target_path)
                #print(f"Copied file: {source_path} to {target_path}")
                file_found = True
                break
    if file_found == False:
        return search_string
    else:
        return None

def count_files_in_folder(directory):
    file_count = 0
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            file_count += 1
    return file_count
