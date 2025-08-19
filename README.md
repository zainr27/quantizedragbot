# Document Q&A with PDF Processing

A Streamlit application that allows you to upload documents (including PDFs) and ask questions about them using the Groq LLM API.

## Features

- **PDF Processing**: Automatically converts PDF files to markdown format for better LLM processing
- **Token Optimization**: Markdown conversion reduces token usage while preserving content structure
- **Multiple File Types**: Supports PDF, TXT, and Markdown files
- **Directory Loading**: Load documents from a specified directory
- **Chat Interface**: Interactive chat interface for asking questions about your documents

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the root directory with:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Upload PDF files through the sidebar or place them in the `./docs` directory

3. Ask questions about your documents in the chat interface

## PDF Processing Benefits

- **Reduced Token Usage**: Markdown format is more efficient than raw PDF text
- **Better Structure**: Preserves document hierarchy with headers and sections
- **Cleaner Text**: Removes PDF formatting artifacts and improves readability
- **Table Support**: Extracts and formats tables as markdown tables

## File Structure

```
GROQ/
├── app.py                      # Main Streamlit application
├── generate.py                 # Groq API integration
├── pdf_processor.py           # PDF to markdown conversion
├── test_pdf_processor.py      # Test script for PDF processing
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── docs/                      # Directory for documents (auto-loaded)
```

## How PDF Processing Works

1. **Text Extraction**: Uses PyMuPDF to extract text from PDF pages
2. **Text Cleaning**: Removes formatting artifacts and improves readability
3. **Structure Preservation**: Maintains document hierarchy with markdown headers
4. **Table Extraction**: Converts PDF tables to markdown table format
5. **Token Optimization**: Markdown format reduces token count while preserving meaning

## Testing

Run the test script to verify PDF processing:
```bash
python test_pdf_processor.py
```

## Troubleshooting

- **Import Error**: Make sure you're using the virtual environment and have installed all dependencies
- **PDF Processing Error**: Ensure the PDF file is not corrupted or password-protected
- **API Key Error**: Verify your GROQ_API_KEY is set correctly in the .env file 