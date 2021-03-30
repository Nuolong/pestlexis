#!/usr/bin/env python3

# imports
import sys
from PyPDF2 import PdfFileReader, PdfFileWriter

# adds encryption to all PDFs in paths with passcode password & saves under new name
def add_encryption(paths, lbl_file_explorer, password, new_name):

    for i, path in enumerate(paths):
        # empty
        if path == 0:
            continue

        pdf_writer = PdfFileWriter()
        pdf_reader = PdfFileReader(path)

        # check if file is encrypted already
        if pdf_reader.isEncrypted:
            error_msg = f"Error: File ({path}) is already encrypted."
            print(error_msg)
            lbl_file_explorer[i].configure(text = error_msg, fg = "red")
            continue

        # encrypt PDF
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

        pdf_writer.encrypt(user_pwd=password, owner_pwd=None,
                           use_128bit=True)

        # create new file
        with open(new_name[i].get(), 'wb') as fh:
            pdf_writer.write(fh)

        # success message
        lbl_file_explorer[i].configure(text = "Encrypted file \"" + new_name[i].get() + "\" created.", fg = "blue")

# removes encryption from all PDFs in paths with password & saves undder new name
def rm_encryption(paths, lbl_file_explorer, password, new_name):

    for i, path in enumerate(paths):
        # empty
        if path == 0:
            continue

        pdf_writer = PdfFileWriter()
        pdf_reader = PdfFileReader(path)

        if not pdf_reader.isEncrypted:
            error_msg = f"Error: File ({path}) is not encrypted."
            print(error_msg)
            lbl_file_explorer[i].configure(text = error_msg, fg = "red")
            continue

        # decrypt with password (has silent failure)
        pdf_reader.decrypt(password)

        try:
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))
        except: # still encrypted - most likely incorrect password provided
            error_msg = f"Error: Entered password could not unlock: ({path})"
            print(error_msg)
            lbl_file_explorer[i].configure(text = error_msg, fg = "blue")

        # create new file
        with open(new_name[i].get(), 'wb') as fh:
            pdf_writer.write(fh)
        lbl_file_explorer[i].configure(text = "Decrypted file \"" + new_name[i].get() + "\" created.", fg = "blue")

def merge_pdfs(paths, lbl_file_explorer, new_name):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open("merged.pdf", 'wb') as out:
        pdf_writer.write(out)

def slice(paths, lbl_file_explorer, start, end, new_name):
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output = f'{name_of_split}{page}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
