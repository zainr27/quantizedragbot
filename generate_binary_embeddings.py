import numpy as np
from llama_index.embeddings import HuggingFaceEmbedding
from data_loader import documents

def batch_iterate(items, batch_size):
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5",
    trust_remote_code=True,
    cache_folder='./hf_cache'
)

binary_embeddings = []

for context in batch_iterate(documents, batch_size=512):
    #Generate float32 vector embeddings
    batch_embds = embed_model.get_text_embeddings(context)
    #Convert float31 vectors to binary vectors
    embeds_array = np.array(batch_embds)
    binary_embeds = np.where(embeds_array > 0, 1, 0).astype(np.uint8)
    #Convert to bytes array
    packed_embeds = np.packbits(binary_embeds, axis=1)
    byte_embeds = [vec.tobytes() for vec in packed_embeds]

    binary_embeddings.extend(byte_embeds)