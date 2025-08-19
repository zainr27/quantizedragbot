import streamlit as st
import os
import tempfile
from pathlib import Path
from generate import generate_response, prompt_template
from llama_index.core import SimpleDirectoryReader
from pdf_processor import process_uploaded_file

st.title("Answer any question about your documents! ")

# Initialize session state for documents
if "documents" not in st.session_state:
    st.session_state.documents = []
    # Auto-load documents from ./docs directory on startup
    if os.path.exists("./docs"):
        try:
            documents_from_docs = []
            for file_path in Path("./docs").rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt', '.md']:
                    try:
                        with open(file_path, 'rb') as f:
                            file_content = f.read()
                        
                        content = process_uploaded_file(file_content, file_path.name)
                        documents_from_docs.append(content)
                    except Exception as e:
                        st.sidebar.warning(f"⚠️ Could not process {file_path.name}: {str(e)}")
            
            st.session_state.documents.extend(documents_from_docs)
        except Exception as e:
            st.sidebar.warning(f"⚠️ Could not auto-load documents from ./docs: {str(e)}")

# Sidebar for document upload
st.sidebar.header("📁 Document Upload")

# File uploader
uploaded_files = st.sidebar.file_uploader(
    "Upload your documents",
    type=['txt', 'pdf', 'md', 'docx'],
    accept_multiple_files=True,
    help="Upload multiple files to query"
)

# Auto-load uploaded files
if uploaded_files:
    st.sidebar.write("📋 **Uploaded files:**")
    for file in uploaded_files:
        st.sidebar.write(f"• {file.name} ({file.size} bytes)")
    
    # Check if we need to load these files
    uploaded_file_names = [f.name for f in uploaded_files]
    if "uploaded_file_names" not in st.session_state or st.session_state.uploaded_file_names != uploaded_file_names:
        with st.spinner("Processing uploaded files..."):
            documents = []
            for uploaded_file in uploaded_files:
                try:
                    # Get file content as bytes
                    file_content = uploaded_file.getvalue()
                    
                    # Process file based on type
                    content = process_uploaded_file(file_content, uploaded_file.name)
                    documents.append(content)
                    st.sidebar.success(f"✅ Processed: {uploaded_file.name}")
                except Exception as e:
                    st.sidebar.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
            
            # Update session state
            st.session_state.documents = documents
            st.session_state.uploaded_file_names = uploaded_file_names
            st.rerun()

# Directory uploader (using folder path input)
st.sidebar.subheader("Or specify a directory path:")
directory_path = st.sidebar.text_input(
    "Enter directory path:",
    value="./docs",
    help="Enter the path to a folder containing your documents"
)

# Load documents button
if st.sidebar.button("🔄 Load Documents"):
    with st.spinner("Loading documents..."):
        documents = []
        
        # Process uploaded files
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                # Get file content as bytes
                file_content = uploaded_file.getvalue()
                
                # Process file based on type
                content = process_uploaded_file(file_content, uploaded_file.name)
                documents.append(content)
                st.sidebar.success(f"✅ Processed: {uploaded_file.name}")
            except Exception as e:
                st.sidebar.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
    
    # Process directory
    if directory_path and os.path.exists(directory_path):
        try:
            # For directory loading, we'll use a custom approach to handle PDFs properly
            documents_from_dir = []
            for file_path in Path(directory_path).rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt', '.md']:
                    try:
                        with open(file_path, 'rb') as f:
                            file_content = f.read()
                        
                        content = process_uploaded_file(file_content, file_path.name)
                        documents_from_dir.append(content)
                        st.sidebar.success(f"✅ Processed: {file_path.name}")
                    except Exception as e:
                        st.sidebar.error(f"❌ Error processing {file_path.name}: {str(e)}")
            
            documents.extend(documents_from_dir)
            st.sidebar.success(f"✅ Processed {len(documents_from_dir)} documents from directory")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading directory: {str(e)}")
    
    # Update session state
    st.session_state.documents = documents
    st.rerun()

# Display document info
st.sidebar.header("📊 Document Information")
st.sidebar.write(f"Loaded {len(st.session_state.documents)} documents")

# Clear documents button
if st.session_state.documents and st.sidebar.button("🗑️ Clear All Documents"):
    st.session_state.documents = []
    st.rerun()

# Show document previews
if st.session_state.documents:
    with st.sidebar.expander("📄 Document Previews"):
        for i, doc in enumerate(st.session_state.documents[:5]):  # Show first 5 docs
            st.write(f"**Document {i+1}:**")
            st.text(doc[:200] + "..." if len(doc) > 200 else doc)
            st.divider()

# Main chat interface
st.header("Ask questions about your documents")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know about the documents?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Check if documents are loaded
            if not st.session_state.documents:
                st.error("❌ No documents loaded. Please upload files or specify a directory first.")
                st.stop()
            
            # Create context from documents
            full_context = "\n".join(st.session_state.documents)
            
            # Format prompt
            formatted_prompt = prompt_template.format(context=full_context, query=prompt)
            
            # Get response
            response_text = generate_response(formatted_prompt)
            
            st.markdown(response_text)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text}) 