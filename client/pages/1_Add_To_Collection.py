import os
import time
import streamlit as st
from datetime import datetime
from app.db.ve
st.set_page_config(page_title="Add to Collection", page_icon="📚", layout="centered")

st.markdown("<h1 style='text-align: center;'>📚 Add Books/Notes to Your Collection</h1>", unsafe_allow_html=True)

# Step 1: Collection Details
st.markdown("### 1️⃣ Collection Details")
col1, col2 = st.columns([2, 1])
with col1:
    collection_name = st.text_input("📌 Enter the Subject Name:", key="collection_name")
with col2:
    collection_type = st.selectbox("📂 Select Collection Type:", ["Book", "Notes"], key="collection_type")

# Step 2: File Upload
st.markdown("### 2️⃣ Upload Document")
pdf_file = st.file_uploader("📄 Upload a PDF, TXT, or MD file:", type=["pdf", "txt", "md"], key="uploaded_file")

# Initialize session state for upload status
if "file_saved" not in st.session_state:
    st.session_state.file_saved = None
if "upload_status" not in st.session_state:
    st.session_state.upload_status = None
if "metadata" not in st.session_state:
    st.session_state.metadata = {}

upload_status = st.empty()
progress_bar = st.empty()

# Handle file upload only if it's a new file and not already saved
if pdf_file and not st.session_state.file_saved:
    upload_status.info("⏳ Uploading file...")
    
    save_path = f"uploads/{pdf_file.name}"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    file_bytes = pdf_file.getbuffer()
    total_size = len(file_bytes)
    chunk_size = max(1024, total_size // 100)
    bytes_written = 0

    with open(save_path, "wb") as f:
        for i in range(0, total_size, chunk_size):
            f.write(file_bytes[i : i + chunk_size])
            bytes_written += chunk_size
            progress = min(100, int(bytes_written / total_size * 100))
            progress_bar.progress(progress)
            time.sleep(0.05)

    progress_bar.empty()
    st.session_state.file_saved = save_path  # Save file path to prevent re-upload
    st.session_state.upload_status = f"✅ File uploaded successfully!"

    # Default metadata
    st.session_state.metadata = {
        "document_name": pdf_file.name,
        "collection_name": collection_name,
        "collection_type": collection_type,
        "upload_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "author": None,  # Placeholder, can be extracted later
        "tags": "",
    }

# Show the saved upload status if present
if st.session_state.upload_status:
    upload_status.success(st.session_state.upload_status)

st.markdown("---")

# Step 3: Processing Type Selection (NO RE-UPLOAD WHEN CHANGED)
st.markdown("### 3️⃣ Choose Processing Type")
processing_type = st.radio("🔍 Select Processing Type:", ["Basic Processing", "Advanced Processing"], key="processing_type", horizontal=True)

# Advanced Processing Options
if processing_type == "Advanced Processing":
    with st.expander("⚙️ Advanced Processing Settings"):
        embedding_model = st.selectbox("🔢 Choose Embedding Model:", ["OpenAI", "HuggingFace", "Custom"], key="embedding_model")
        api_key = st.text_input("🔑 Enter API Key:", type="password", key="api_key")
        model_name = st.text_input("🔗 Enter Model Name:", key="model_name")
        chunk_size = st.slider("📏 Adjust Chunk Size:", min_value=100, max_value=2000, value=512, step=100, key="chunk_size")

# Step 4: Optional Metadata Tags
st.markdown("### 4️⃣ Add Metadata (Optional)")
metadata_tags = st.text_area("🏷️ Enter comma-separated tags (e.g., AI, Machine Learning, NLP)", key="metadata_tags")

# Store metadata tags in session state
st.session_state.metadata["tags"] = metadata_tags if metadata_tags else ""

st.markdown("---")

# Step 5: Indexing Button
if st.button("🚀 Start Indexing"):
    if not st.session_state.file_saved:
        st.error("❌ No file uploaded! Please upload a document first.")
    else:
        st.session_state.metadata["parse_instruction"] = st.text_area("✏️ Parsing Instructions (Optional)", key="parse_instructions")
        
        st.success("✅ Document Indexed Successfully!")
        st.write("### 🗂️ Metadata Summary:")
        st.json(st.session_state.metadata)
