import streamlit as st
import pandas as pd
import os
import base64

# for audio metadata
import mutagen
import time

timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
from db_ftns import add_file_details
from datetime import datetime


def download_able(data):
    csv_file = data.to_csv(index=("false"))
    b64 = base64.b64encode(csv_file.encode()).decode()
    new_filename = "Audio_METADATA_RESULT_{}_.csv".format(timestr)
    st.markdown("### ** 📁 DOWNLOAD CSV FILE **")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click here!</a>'
    st.markdown(href, unsafe_allow_html=True)


def audio():
    st.subheader("Audio Metadata Extractor")

    audio_file = st.file_uploader("Upload Your Audio File", type=["mp3", "ogg", "m4a"])

    if audio_file is not None:
        # st.write(dir(audio_file))

        c1, c2 = st.columns(2)

        with c1:
            with st.expander("Your Audio File"):
                st.audio(audio_file.read())

        with c2:
            with st.expander("Audio File Stats"):
                audio_details = {
                    "File Name": audio_file.name,
                    "File Size": audio_file.size,
                    "File Type": audio_file.type,
                }
                st.write(audio_details)

                stat_info = os.stat(audio_file.readable())
                # st.write(stat_info)

                stat_Details = {
                    "Accessed_Time": stat_info.st_atime,
                    "Creation Time": stat_info.st_ctime,
                    "Modified Time": stat_info.st_mtime,
                }
                st.write(stat_Details)

                # file_details_combied
                file_details_combied = {
                    "File Name": audio_file.name,
                    "File Size": audio_file.size,
                    "File Type": audio_file.type,
                    "Accessed_Time": stat_info.st_atime,
                    "Creation Time": stat_info.st_ctime,
                    "Modified Time": stat_info.st_mtime,
                }

                DF_file_details_combied = pd.DataFrame(
                    list(file_details_combied.items()),
                    columns=["MetaData Tags", "Values"],
                )

                st.dataframe(DF_file_details_combied, use_container_width=True)

                add_file_details(
                    audio_file.name, audio_file.type, audio_file.size, datetime.now()
                )

        with st.expander("Metadata with Mutagen"):
            st.info("Metadata with Mutagen")

            Mutagen_tag = mutagen.File(audio_file)
            st.write(Mutagen_tag)
            # st.write(Mutagen_tag)
            # DF_Mutagen_tage = pd.DataFrame(list(Mutagen_tag.items()),columns=['MetaData Tags','Values'])

            # st.dataframe(DF_Mutagen_tage,use_container_width=True)

        with st.expander("Download Results"):
            DF_final = pd.DataFrame(DF_file_details_combied)
            st.dataframe(DF_final, use_container_width=True)
            download_able(DF_final)
