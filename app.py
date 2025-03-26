import streamlit as st
import pandas as pd

def split_sku(sku):
    parts = sku.strip().split("_")  # Remove extra spaces and split
    
    # Extract size (last part of SKU if alphabetic)
    size = parts[-1] if parts[-1].isalpha() else None
    
    # Remove the size part from SKU
    sku_core = parts[:-1] if size else parts

    extracted_skus = []
    prefix = sku_core[0]  # First part is always the initial prefix

    i = 1
    while i < len(sku_core):
        if sku_core[i].isdigit():
            extracted_skus.append(f"{prefix}_{sku_core[i]}")
        else:
            prefix = sku_core[i]  # If we find a new prefix, update it
        i += 1  

    return extracted_skus, size

# Streamlit App
st.title("SKU Design Processing App 😊📊")
st.subheader("Created By : Arun Kumar 💁🏻‍♂️")
st.write("Upload an Excel file containing Columns names SKU &  QTY to get processed results.")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Ensure required columns exist
    if "SKU" in df.columns and "QTY" in df.columns:
        df[["SKU_Split", "Size"]] = df["SKU"].apply(lambda x: pd.Series(split_sku(x)))
        df = df.explode("SKU_Split").drop(columns=["SKU"]).rename(columns={"SKU_Split": "SKU"})

        # Keep only necessary columns
        df = df[["SKU", "QTY","Size"]].reset_index(drop=True)

        st.write("Processed Data:")
        st.dataframe(df)

        # Download processed file
        output_file = "processed_output.xlsx"
        df.to_excel(output_file, index=False)

        with open(output_file, "rb") as f:
            st.download_button("Download Processed File", f, file_name="processed_output.xlsx")
    else:
        st.error("Uploaded file must contain 'SKU', 'QTY' columns.")
