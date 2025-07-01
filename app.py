import streamlit as st
import pandas as pd

def split_sku(sku):
    parts = sku.strip().split("_")
    
    # Extract size if last part is alpha
    size = parts[-1] if parts[-1].isalpha() else None
    data_parts = parts[:-1] if size else parts

    extracted_skus = []
    i = 0

    while i < len(data_parts):
        prefix = data_parts[i]

        j = i + 1
        while j < len(data_parts) and data_parts[j].isdigit():
            extracted_skus.append(f"{prefix}_{data_parts[j]}")
            j += 1

        i = j  # move to next prefix

    return extracted_skus, size

# -----------------------
# Streamlit App
# -----------------------

st.title("SKU Design Processing App 😊📊")
st.subheader("Created By : Arun Kumar 💁🏻‍♂️")
st.write("Upload an Excel file containing Columns names SKU & QTY to get processed results.")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Ensure required columns exist
    if "SKU" in df.columns and "QTY" in df.columns:
        # Apply updated split function
        df[["SKU_Split", "Size"]] = df["SKU"].apply(lambda x: pd.Series(split_sku(x)))
        df = df.explode("SKU_Split").drop(columns=["SKU"]).rename(columns={"SKU_Split": "SKU"})
        df = df[["SKU", "Size", "QTY"]].reset_index(drop=True)

        st.write("Processed Data:")
        st.dataframe(df)

        # Download processed file
        output_file = "processed_output.xlsx"
        df.to_excel(output_file, index=False)

        with open(output_file, "rb") as f:
            st.download_button("Download Processed File", f, file_name="processed_output.xlsx")
    else:
        st.error("Uploaded file must contain 'SKU', 'QTY' columns.")
