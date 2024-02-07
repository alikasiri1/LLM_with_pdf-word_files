from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings

model_name = "sentence-transformers/all-mpnet-base-v2"

persist_directory = 'db'
embedding = HuggingFaceEmbeddings(model_name=model_name)

db = Chroma(persist_directory=persist_directory, #### use database that already created
                  embedding_function=embedding,
                   )

query = "Effects of ESWT on calcific rotator cuff tendinitis pain"
docs = db.similarity_search(query)
for doc in docs:
    print(doc)
    print("\n" , "________________________________________________________________")

##########
# retriever = db.as_retriever()
# docs = retriever.get_relevant_documents(query)      ##another way to ger similarity
# print(docs)
##########