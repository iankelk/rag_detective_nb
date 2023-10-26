import functions_framework
import os

os.environ.get("OPENAI_API_KEY")
WEAVIATE_IP_ADDRESS = "34.133.13.119"

import weaviate
from weaviate import Client
from llama_index import VectorStoreIndex
from llama_index.storage import StorageContext
from llama_index.vector_stores import WeaviateVectorStore
from llama_index.vector_stores.types import ExactMatchFilter, MetadataFilters
from llama_index.prompts import PromptTemplate

template = ("We have provided context information below. If the answer to a query is not contained in this context, "
            "please only reply that it is not in the context."
            "\n---------------------\n"
            "{context_str}"
            "\n---------------------\n"
            "Given this information, please answer the question: {query_str}\n"
)
qa_template = PromptTemplate(template)

@functions_framework.http
def query_llamaindex(request):

    request_json = request.get_json(silent=True)
    request_args = request.args

    website = "ai21.com"
    timestamp = "2023-10-06T18-11-24"
    # query = "How was AI21 Studio a game changer?"
    query = "Who is Kim Kardashian?"

    if request_json and 'website' in request_json:
        website = request_json['website']
    if request_args and 'timestamp' in request_args:
        timestamp = request_args['timestamp']
    if request_args and 'query' in request_args:
        query = request_args['query']

    # client setup
    client = weaviate.Client(url="http://" + WEAVIATE_IP_ADDRESS + ":8080")

    # construct vector store
    vector_store = WeaviateVectorStore(weaviate_client=client, index_name="Pages", text_key="text")

    # setting up the indexing strategy 
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # setup an index for the Vector Store
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

    # Create exact match filters for websiteAddress and timestamp
    website_address_filter = ExactMatchFilter(key="websiteAddress", value=website)
    timestamp_filter = ExactMatchFilter(key="timestamp", value=timestamp)

    # Create a metadata filters instance with the above filters
    metadata_filters = MetadataFilters(filters=[website_address_filter, timestamp_filter]) 

    # Create a query engine with the filters
    query_engine = index.as_query_engine(text_qa_template=qa_template, filters=metadata_filters)

    # Execute the query
    query_str = query
    response = query_engine.query(query_str)

    # Print the response 
    print(response)
    return f"Response: {response}"
