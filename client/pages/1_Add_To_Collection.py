import os
import streamlit as st
from app.questgen.paper import Paper
from app.db.vector_db import VectorDB
from app.prompts.basic import basic_prompt,inst

st.set_page_config(
    page_title="Add To Collection",
    page_icon="👋",
)

st.write("# Hi add more books/notes to your collection. 👋")

collection_name = st.text_input("Enter the Subject name:")

# Ask for the collection type
collection_type = st.selectbox("Select the collection type:", ["Book", "Notes"])

    # Ask for a PDF file upload
pdf_file = st.file_uploader("Upload a PDF file:", type=["pdf", "txt"])

if collection_name and collection_type and pdf_file:
        st.write(f"Collection Name: {collection_name}")
        st.write(f"Collection Type: {collection_type}")
        st.write("PDF file uploaded successfully!")

        # Save the uploaded PDF file to disk
        save_path = f"uploads/{pdf_file.name}"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        st.write(f"PDF file saved to: {save_path}")

