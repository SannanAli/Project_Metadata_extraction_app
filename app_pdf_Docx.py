import streamlit as st
import os
import time
import base64
import pandas as pd
from PyPDF2 import PdfReader
import docx2txt
from db_ftns import add_file_details
from datetime import datetime


def loadPDF(PdfFile):
    pdfFile = PdfReader(PdfFile)
    count = len(pdfFile.pages)
    all_pages_text = ""
    for i in range(count):
        pages = pdfFile.pages[i]
        all_pages_text += pages.extract_text()
    return all_pages_text


def download_able(data):
    csv_file = data.to_csv(index=("false"))
    b64 = base64.b64encode(csv_file.encode()).decode()
    new_filename = "PDF_METADATA_RESULT_{}_.csv".format(timestr)
    st.markdown("### ** 📁 DOWNLOAD CSV FILE **")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click here!</a>'
    st.markdown(href, unsafe_allow_html=True)


timestr = time.strftime("%Y-%m-%d-%H-%M-%S")


def pdfdocx():
    st.subheader("PDF & Docx Metadata Extractor")

    text_file = st.file_uploader("Upload Your Documnet here ", type=["PDF", "Docx"])

    if st.button("Extract Metadata"):
        if text_file is not None:
            if text_file.type == "application/pdf":
                with st.expander("Original File"):
                    pdf_file = loadPDF(text_file)
                    st.write(pdf_file)

                with st.expander("Image Stats"):
                    image_details = {
                        "Document Name": text_file.name,
                        "Document Size": text_file.size,
                        "Document Type": text_file.type,
                    }
                    st.write(image_details)

                    stat_info = os.stat(text_file.readable())
                    st.write(stat_info)

                    stat_Details = {
                        "Accessed_Time": stat_info.st_atime,
                        "Creation Time": stat_info.st_ctime,
                        "Modified Time": stat_info.st_mtime,
                    }
                    # st.write(stat_Details)

                    # file_details_combied
                    PDF_file_details_combied = {
                        "Document Name": text_file.name,
                        "Document Size": text_file.size,
                        "Document Type": text_file.type,
                        "Accessed_Time": stat_info.st_atime,
                        "Creation Time": stat_info.st_ctime,
                        "Modified Time": stat_info.st_mtime,
                    }

                    DF_PDF_file_details_combied = pd.DataFrame(
                        list(PDF_file_details_combied.items()),
                        columns=["MetaData Tags", "Values"],
                    )

                    st.dataframe(DF_PDF_file_details_combied)
                    add_file_details(
                        text_file.name, text_file.type, text_file.size, datetime.now()
                    )

                with st.expander("Metadata with Pypdf2"):
                    st.info("Metadata with Mutagen")

                    pdf_file = PdfReader(text_file)
                    pdf_info = pdf_file.metadata
                    st.write(pdf_info)

                    DF_PDF = pd.DataFrame(
                        list(pdf_info.items()), columns=["MetaData Tags", "Values"]
                    )
                    st.table(DF_PDF)

                with st.expander("Download Results"):
                    DF_final = pd.concat([DF_PDF_file_details_combied, DF_PDF])
                    st.dataframe(DF_final, use_container_width=True)
                    download_able(DF_final)
            else:
                with st.expander("Original File"):
                    Docx_file = docx2txt.process(text_file)
                    st.write(dir(Docx_file))

                # with st.expander('Docx Stats'):

                #     image_details = {'Document Name': Docx_file.title,'Document Size': Docx_file.size,'Document Type': Docx_file.type}
                #     st.write(image_details)

                #     stat_info = os.stat(Docx_file.readable())
                #     st.write(stat_info)

                #     #stat_Details = {'Accessed_Time':stat_info.st_atime,'Creation Time':stat_info.st_ctime,'Modified Time':stat_info.st_mtime}
                #     #st.write(stat_Details)

                #     #file_details_combied
                #     Docx_file_details_combied = {
                #         'Document Name': Docx_file.name,'Document Size': Docx_file.size,'Document Type': Docx_file.type,
                #             'Accessed_Time':stat_info.st_atime,
                #             'Creation Time':stat_info.st_ctime,
                #             'Modified Time':stat_info.st_mtime
                #         }

                #     DF_Docx_file_details_combied = pd.DataFrame(list(Docx_file_details_combied.items()),
                #                                         columns=['MetaData Tags','Values'])

                #     st.dataframe(DF_Docx_file_details_combied)

                # with st.expander('Metadata with Pypdf2'):

                #     st.info('Metadata with Mutagen')

                #     pdf_file = PdfReader(text_file)
                #     pdf_info = pdf_file.metadata
                #     st.write(pdf_info)

                #     DF_PDF = pd.DataFrame(list(pdf_info.items()), columns=['MetaData Tags','Values'])
                #     st.table(DF_PDF)

                # with st.expander('Download Results'):
                #     DF_final = pd.concat([DF_PDF_file_details_combied,DF_PDF])
                #     st.dataframe(DF_final,use_container_width=True)
                #     download_able(DF_final)
