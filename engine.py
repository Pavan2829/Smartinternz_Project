import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

class SmartinternzEngine:
    def __init__(self):
        # Local embeddings for the "Offline" knowledge base
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Initialize Google Gemini 1.5 Flash
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3
        )
        self.db_path = "vector_db/faiss_index"
        self.db = None

    def build_index(self, data_path):
        if not os.path.exists(data_path):
            os.makedirs(os.path.dirname(data_path), exist_ok=True)
            with open(data_path, "w") as f: f.write("Rice needs urea in three stages.")
            
        with open(data_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        text_splitter = CharacterTextSplitter(chunk_size=700, chunk_overlap=100)
        docs = text_splitter.split_text(text)
        
        self.db = FAISS.from_texts(docs, self.embeddings)
        os.makedirs("vector_db", exist_ok=True)
        self.db.save_local(self.db_path)

    def query(self, user_question):
        if not self.db:
            if os.path.exists(self.db_path):
                self.db = FAISS.load_local(self.db_path, self.embeddings, allow_dangerous_deserialization=True)
            else:
                return "Knowledge base is empty. Please add data to data/agri_knowledge.txt."
        
        # 1. Retrieve relevant data from your local file
        docs = self.db.similarity_search(user_question, k=3)
        context = "\n".join([d.page_content for d in docs])

        # 2. Generate a professional response using Gemini
        prompt = (
            f"You are Smartinternz_Project, a helpful Indian agricultural AI assistant.\n"
            f"Use the provided context to answer the farmer's question. \n"
            f"If the answer isn't in the context, use your general knowledge but mention it's general advice.\n\n"
            f"Context: {context}\n"
            f"Question: {user_question}\n\n"
            f"Answer:"
        )
        
        response = self.llm.invoke(prompt)
        return response.content
