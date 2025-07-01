# create open source vector store database
# This file is used to create a vector store database using the langchain library.
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set.")
# Initialize HuggingFace embeddings



# load documents from text files
path = "./resources/data"

query = "How to run Automated Test cases "

llm = "llama3-8b-8192"
# Initialize GroqAI with the specified model and API key

# Create the system prompt as a template for later use
system_prompt_template = """You are a helpful assistant. You will be provided with a question and a role and your task is to answer the question based only from the documents falling under the role.
Don't provide any information that is not related to the role. 
Answer the question based on the documents provided only. Don't make any assumptions."""

# Initialize ChatGroq without system_prompt parameter
groq_chat = ChatGroq(model_name=llm, api_key=GROQ_API_KEY)

class VectorStoreManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None

    def load_existing_vector_store(self):
        """Load existing vector store if it exists"""
        if os.path.exists("./vector_store_db"):
            print("Loading existing vector store...")
            return Chroma(persist_directory="./vector_store_db", embedding_function=self.embeddings)
        return None
        
class DocumentLoader:
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(path):
            raise ValueError(f"Path {path} does not exist.")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    def documents_load(self, path: str):
        """Load documents from the specified path, split them into chunks, and create a vector store."""
        print(f"Loading documents from path: {path}")
        all_docs = []  # Collect all documents first
        
        if not os.path.exists(path):
            raise ValueError(f"Path {path} does not exist.")
        
        folders = os.listdir(path)
        for folder in folders:
            folder_path = os.path.join(path, folder)
            if os.path.isdir(folder_path):
                print(f"Processing folder: {folder}")
                # list all the files in the folder
                files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                
                for file in files:
                    file_path = os.path.join(folder_path, file)
                    if file_path.endswith((".txt", ".docx", ".pdf", ".md", ".csv")): 
                        try:
                            print(f"Processing file: {file_path}")
                            # load the document
                            loader = TextLoader(file_path, encoding="utf-8")
                            documents = loader.load()
                            
                            # split the document into smaller chunks and add metadata with folder name
                            text_splitter = RecursiveCharacterTextSplitter(
                                chunk_size=1000, chunk_overlap=200
                            )
                            docs = text_splitter.split_documents(documents)
                            
                            # add metadata with folder name which is nothing but the user role
                            for doc in docs:
                                doc.metadata['role'] = folder
                                doc.metadata['source_file'] = file  # Add source file info
                            
                            all_docs.extend(docs)  # Add to collection instead of overwriting
                            print(f"Added {len(docs)} chunks from {file}")
                            
                        except Exception as e:
                            print(f"Error processing file {file_path}: {e}")
                            continue
        
        if not all_docs:
            print("No documents found to index.")
            return None
        
        print(f"Creating vector store with {len(all_docs)} total document chunks...")
        # Create vector store once with all documents
        vector_store = Chroma.from_documents(
            all_docs, self.embeddings, persist_directory="./vector_store_db"
        )
        
        print("Vector store created successfully!")
        return vector_store
    
class ChatRepository:
    """ ChatRepository class to handle chat related requests """
    
    def __init__(self, loader=None, vector_store_manager=None, llm=None):
        self.loader = loader or DocumentLoader("./resources/data")
        self.vector_store_manager = vector_store_manager or VectorStoreManager()
        self.llm = llm or groq_chat
    


    # fetch all the  files from the path , break into smaller chunks and add folder name as metadata and
    # store them in the vector store database

   

    def fetch_documents(self, path: str, query: str, role: str = None):
        try:
            # Try to load existing vector store first
            vector_store = self.vector_store_manager.load_existing_vector_store()
            
            # If no existing store, create new one
            if not vector_store:
                print("No existing vector store found. Creating new one...")
                vector_store = self.loader.documents_load(path)
                
            if not vector_store:
                raise ValueError("Vector store is not initialized. Please check the path and files.")
            
            # Configure search filter for role-based access
            search_kwargs = {"k": 3}  # Return top 3 most relevant chunks
            if role:
                search_kwargs["filter"] = {"role": role}
                print(f"Searching documents for role: {role}")
            else:
                print("Searching all documents (no role filter)")
            
            # Create a custom prompt template for the QA chain
            prompt_template = """You are a helpful assistant. Answer the question based only on the provided context documents for the specified role.
    Don't provide any information that is not related to the role or not found in the context.

    Context: {context}

    Question: {question}

    Answer based only on the context provided:"""
            
            prompt = ChatPromptTemplate.from_template(prompt_template)
            
            # Create the RetrievalQA chain with custom prompt
            chain = RetrievalQA.from_chain_type(
                llm=groq_chat,
                chain_type="stuff",
                retriever=vector_store.as_retriever(search_kwargs=search_kwargs),
                chain_type_kwargs={"prompt": prompt}
            )
        
            
            print(f"Processing query: {query}")
            response = chain.invoke({"query": query})
            
            result = response.get('result', 'No answer generated.')
            print(f"Generated response: {result}")
            return result
            
        except Exception as e:
            print(f"Error in fetch_documents: {e}")
            return f"Error processing your request: {str(e)}"
                    

   



if __name__ == "__main__":
    chatRepository = ChatRepository()
    output = chatRepository.fetch_documents(path, query, role="engineering")
    print("printing output ", output)
