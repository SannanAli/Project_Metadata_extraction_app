import streamlit as st
import pandas as pd
import os
from app_home import load_images
from datetime import datetime
import exifread
import base64
import time

timestr = time.strftime("%Y%m%d-%H%M%S")
from db_ftns import add_file_details


def get_readable_time(my_time):
    return datetime.fromtimestamp(my_time).strftime("%Y-%m-%d-%H%-M-%S")


def download_able(data):
    csv_file = data.to_csv(index=("false"))
    b64 = base64.b64encode(csv_file.encode()).decode()
    new_filename = "Image_METADATA_RESULT_{}_.csv".format(timestr)
    st.markdown("### ** 📁 DOWNLOAD CSV FILE **")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click here!</a>'
    st.markdown(href, unsafe_allow_html=True)


def image():
    image_file = st.file_uploader("Upload Your Image Here", ["png", "jpeg", "jpg"])
    # upload file(UPloadfile class) is a binary file
    if image_file is not None:
        with st.expander("Image Stats"):
            image_details = {
                "Image Name": image_file.name,
                "Image Size": image_file.size,
                "Image Type": image_file.type,
            }
            st.write(image_details)

            stat_info = os.stat(image_file.readable())
            st.write(stat_info)

            stat_Details = {
                "Accessed_Time": stat_info.st_atime,
                "Creation Time": stat_info.st_ctime,
                "Modified Time": stat_info.st_mtime,
            }
            st.write(stat_Details)

            # file_details_combied
            file_details_combied = {
                "Image Name": image_file.name,
                "Image Size": image_file.size,
                "Image Type": image_file.type,
                "Accessed_Time": stat_info.st_atime,
                "Creation Time": stat_info.st_ctime,
                "Modified Time": stat_info.st_mtime,
            }

            DF_file_details_combied = pd.DataFrame(
                list(file_details_combied.items()), columns=["MetaData Tags", "Values"]
            )

            st.dataframe(DF_file_details_combied)

            add_file_details(
                image_file.name, image_file.type, image_file.size, datetime.now()
            )

        c1, c2 = st.columns(2)
        with c1:
            with st.expander("Image View"):
                img = load_images(image_file)
                st.image(img, use_column_width="auto")
        with c2:
            with st.expander("Default Image"):
                st.info("Using PILLOW")
                img = load_images(image_file)
                st.write(dir(img))
                image_details = {
                    "Format": img.format,
                    "Format Desc": img.format_description,
                    "File Name": "",
                    "size": img.size,
                    "Height": img.height,
                    "Width": img.width,
                    "Info": img.info,
                    "Encoder": "",
                }

                DF_file_details_PILLO = pd.DataFrame(
                    list(image_details.items()), columns=["MetaData Tags", "Values"]
                )

                st.dataframe(DF_file_details_PILLO, use_container_width=True)

        with st.expander("Exifread Tool"):
            st.info("Metadata using Exifread Tool")

            exif_meta_tags = exifread.process_file(image_file)
            st.write(exif_meta_tags)

            DF_exif_meta_tags = pd.DataFrame(
                list(exif_meta_tags.items()), columns=["MetaData Tags", "Values"]
            )

            st.dataframe(DF_exif_meta_tags, use_container_width=True)

        with st.expander("Download Results"):
            DF_final = pd.concat(
                [DF_file_details_combied, DF_file_details_PILLO, DF_exif_meta_tags]
            )
            st.dataframe(DF_final, use_container_width=True)
            download_able(DF_final)
