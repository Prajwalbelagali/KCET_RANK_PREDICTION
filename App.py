import streamlit as st
import pdfplumber
import pandas as pd

st.title("KCET PDF to CSV Converter")

uploaded_file = st.file_uploader("Upload KCET Cutoff PDF", type=["pdf"])

if uploaded_file is not None:

    all_tables = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                df = pd.DataFrame(table)
                all_tables.append(df)

    if all_tables:
        final_df = pd.concat(all_tables)

        st.subheader("Extracted Table Preview")
        st.dataframe(final_df)

        csv = final_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="kcet_cutoff.csv",
            mime="text/csv"
        )
    else:
        st.warning("No tables detected in the PDF.")
