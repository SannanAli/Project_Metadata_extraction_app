import streamlit as st

# for images
from PIL import Image  # pillow -> PIL


@st.cache_data
def load_images(image):
    image = Image.open(image)
    return image


def home():
    st.subheader("Home")
    img = st.image(load_images("resources\metadataextraction_app_jcharistech.png"))
    st.write(dir(img))
    c1, c2, c3 = st.columns(3)

    with c1:
        with st.expander("GET IMAGE METADATA :camera_with_flash:"):
            st.info("IMAGE METADATA")
            st.markdown(":camera_with_flash:")
            st.text("Upload JPEG,JPG,PNG Images")

    with c2:
        with st.expander("GET AUDIO METADATA :loud_sound:"):
            st.info("AUDIO METADATA")
            st.markdown(":loud_sound:")
            st.text("Upload MP3,Ogg")

    with c3:
        with st.expander("GET DOCUMENT METADATA :page_with_curl:"):
            st.info("DOCUMENT FILE METADATA")
            st.markdown(":page_with_curl:")
            st.text("Upload PDF,Docx")
