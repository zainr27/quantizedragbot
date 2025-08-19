from llama_index.core import SimpleDirectoryReader

docs_dir = "./docs"  # Path to your documents directory

loader = SimpleDirectoryReader(
    input_dir=docs_dir,
    required_exts=[".pdf", ".txt"],
    recursive=True
)

docs = loader.load_data()
documents = [doc.text for doc in docs]