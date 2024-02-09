from PyPDF2 import PdfReader
import docx
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import GPT2TokenizerFast
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings
from langchain.document_loaders import PyPDFLoader

# import clean_data
# clean_data.clean_data()

def getText_word(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def getText_pdf(filename):
    doc = PdfReader(filename)
    fullText = []
    for para in doc.pages:
        fullText.append(para.extract_text())
    return ''.join(fullText)



tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

# Step 4: Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size =500,
    chunk_overlap  = 80,
    length_function = count_tokens,
)
# pdf_text = getText_pdf('eng.pdf')

from langchain.document_loaders import DirectoryLoader
loader = DirectoryLoader('data', glob="./*.pdf", loader_cls=PyPDFLoader)

documents = loader.load()
# print(documents)
chunks = text_splitter.split_documents(documents)
print(chunks[10])
# chunks = text_splitter.create_documents([pdf_text])

# print(chunks[10])
print("\n" , "________________________________________________________________")


model_name = "bert-base-multilingual-cased"  #"sentence-transformers/all-mpnet-base-v2"

hf = HuggingFaceEmbeddings(model_name=model_name)



############################################################
############################### for the first time that you want to stor into the chroma
persist_directory = 'db'

## Here is the nmew embeddings being used
embedding = hf

db  = Chroma.from_documents(documents=chunks,   # db = Chroma.from_documents(chunks, OpenAIEmbeddings())
                                 embedding=embedding,
                                 persist_directory=persist_directory)

######################################################################
#######################################################################
