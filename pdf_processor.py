import fitz  # PyMuPDF
import re
import io
from typing import List, Tuple

def pdf_to_markdown(pdf_content: bytes, filename: str = "document.pdf") -> str:
    """
    Convert PDF content to markdown format.
    
    Args:
        pdf_content: PDF file content as bytes
        filename: Original filename for reference
    
    Returns:
        Markdown formatted text
    """
    try:
        # Open PDF from bytes
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        
        markdown_content = []
        markdown_content.append(f"# {filename}\n")
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Extract text
            text = page.get_text()
            
            if text.strip():
                # Clean up the text
                text = clean_text(text)
                
                # Add page header
                markdown_content.append(f"\n## Page {page_num + 1}\n")
                markdown_content.append(text)
                markdown_content.append("\n")
        
        pdf_document.close()
        
        return "\n".join(markdown_content)
    
    except Exception as e:
        return f"Error processing PDF {filename}: {str(e)}"

def clean_text(text: str) -> str:
    """
    Clean and format extracted text for better markdown output.
    
    Args:
        text: Raw text from PDF
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    # Fix common PDF extraction issues
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between lowercase and uppercase
    text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)  # Add space after punctuation
    
    # Remove orphaned characters
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    
    # Clean up line breaks
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            # If line ends with a period, exclamation, or question mark, it's likely a complete sentence
            if line.endswith(('.', '!', '?')):
                cleaned_lines.append(line)
            else:
                # Check if next line continues the sentence
                cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def extract_tables_from_pdf(pdf_content: bytes) -> List[str]:
    """
    Extract tables from PDF and convert to markdown table format.
    
    Args:
        pdf_content: PDF file content as bytes
        
    Returns:
        List of markdown formatted tables
    """
    try:
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        tables = []
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Extract tables (this is a simplified approach)
            # For more complex table extraction, you might want to use tabula-py or similar
            table_areas = page.find_tables()
            
            for table in table_areas:
                markdown_table = convert_table_to_markdown(table)
                if markdown_table:
                    tables.append(markdown_table)
        
        pdf_document.close()
        return tables
    
    except Exception as e:
        return [f"Error extracting tables: {str(e)}"]

def convert_table_to_markdown(table) -> str:
    """
    Convert a table object to markdown format.
    
    Args:
        table: Table object from PyMuPDF
        
    Returns:
        Markdown formatted table
    """
    try:
        rows = table.extract()
        if not rows:
            return ""
        
        markdown_lines = []
        
        # Add header
        if rows:
            header = "| " + " | ".join(str(cell) for cell in rows[0]) + " |"
            markdown_lines.append(header)
            
            # Add separator
            separator = "| " + " | ".join("---" for _ in rows[0]) + " |"
            markdown_lines.append(separator)
            
            # Add data rows
            for row in rows[1:]:
                data_row = "| " + " | ".join(str(cell) for cell in row) + " |"
                markdown_lines.append(data_row)
        
        return "\n".join(markdown_lines)
    
    except Exception as e:
        return f"Error converting table: {str(e)}"

def process_uploaded_file(file_content: bytes, filename: str) -> str:
    """
    Process uploaded file and convert to appropriate format.
    
    Args:
        file_content: File content as bytes
        filename: Original filename
        
    Returns:
        Processed content as string
    """
    file_extension = filename.lower().split('.')[-1]
    
    if file_extension == 'pdf':
        return pdf_to_markdown(file_content, filename)
    elif file_extension in ['txt', 'md']:
        try:
            return file_content.decode('utf-8')
        except UnicodeDecodeError:
            return file_content.decode('latin-1')
    else:
        return f"Unsupported file type: {file_extension}" 