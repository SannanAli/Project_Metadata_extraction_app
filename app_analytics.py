import streamlit as st
import pandas as pd

# Database
import sqlite3

from db_ftns import view_all_data

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")


def analytics():
    st.subheader("ANALYTICS")
    all_uploaded_file = view_all_data()
    DF = pd.DataFrame(
        all_uploaded_file, columns=["Filename", "Filetype", "Filesize", "UploadTime"]
    )
    # Monitor all uploads

    with st.expander("Monitor"):
        st.success("View All Uploaded Files")
        st.dataframe(DF, use_container_width=True)

    # stats of all files
    with st.expander("Distribution Of Filestypes"):
        fig = plt.figure()
        sns.countplot(x=DF["Filetype"])
        st.write(fig)
