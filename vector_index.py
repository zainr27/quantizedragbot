from pymilvus import MilvusClient, DataType
from generate_binary_embeddings import binary_embeddings
from generate_binary_embeddings import batch_context
from data_loader import documents

#Initialize client and schema
client = MilvusClient("milvus_binary_quantized_db")
schema = client.create_schema(auto_id=True, enable_dynamic_fields=True)

#Create index parameters for binary vectors
index_params = client.preapre_index_params()
index_params.add_index(
    field_name ="binary_vector",
    index_name="binary_vector_index",
    index_type="BIN_FLAT", #Exact search for binary vectors
    metric_type="HAMMING", #Hamming distance for binary vectors
)

#Create collection with schema and index 

client.create_collection(
    collection_name="fastest-rag",
    schema=schema,
    index_params=index_params
)

#Insert data to index
client.insert(
    collection_name="fastest-rag",
    data=[
        {"context": context, "binary_vector": binary_embedding}
        for context, binary_embedding in zip(batch_context, binary_embeddings)


    ]
)