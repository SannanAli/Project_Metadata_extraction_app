import streamlit as st
from app_home import home
from app_image import image
from app_audio import audio
from app_pdf_Docx import pdfdocx
from app_analytics import analytics
from db_ftns import create_uploadfile_table

import streamlit.components.v1 as stc

from PIL import Image


@st.cache_data
def load_images(image):
    image = Image.open(image)
    return image


HTML_BANNER = """
    <div style="background-color:#3872fb;padding:10px;border-radius:10px;border-style:ridge;">
    <h1 style="color:white;text-align:center;">Metadata Extractor</h1>
    </div>
    """


def main():
    st.set_page_config(layout="wide", initial_sidebar_state="auto")
    stc.html(HTML_BANNER)
    menu = ["HOME", "IMAGE", "AUDIO", "DOCUMENTS", "ANALYTICS", "ABOUT"]
    create_uploadfile_table()

    choise = st.sidebar.selectbox("Menu", menu)

    if choise == "HOME":
        home()
    elif choise == "IMAGE":
        image()
    elif choise == "AUDIO":
        audio()
    elif choise == "DOCUMENTS":
        pdfdocx()
    elif choise == "ANALYTICS":
        analytics()
    else:
        st.subheader("ABOUT")
        st.image(load_images("resources\metadataextraction_app_jcharistech.png"))


if __name__ == "__main__":
    main()
