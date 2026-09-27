import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Free, fast, local CPU embeddings (no quota, no API key needed)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def create_db_from_youtube_video_url(video_url: str) -> FAISS:
    try:
        loader = YoutubeLoader.from_youtube_url(
            video_url,
            language=["en", "en-US", "hi"],
        )
        transcript = loader.load()
    except Exception:
        loader = YoutubeLoader.from_youtube_url(video_url)
        transcript = loader.load()

    if not transcript:
        raise ValueError("Could not extract any transcript from this video.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    db = FAISS.from_documents(docs, embeddings)
    return db


def get_response_from_query(db: FAISS, query: str, k: int = 4):
    docs = db.similarity_search(query, k=k)
    docs_page_content = "\n\n".join([d.page_content for d in docs])

    # Direct official Google Generative AI client (bypasses LangChain 404 endpoint bug)
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    # Determine which model is available on your key automatically
    available_models = [
        m.name
        for m in genai.list_models()
        if "generateContent" in m.supported_generation_methods
    ]

    # Select the best available model
    chosen_model = "gemini-1.5-flash"
    for candidate in [
        "models/gemini-1.5-flash",
        "models/gemini-1.5-flash-latest",
        "models/gemini-2.0-flash",
        "models/gemini-1.5-pro",
    ]:
        if candidate in available_models:
            chosen_model = candidate
            break
    else:
        if available_models:
            chosen_model = available_models[0]

    model = genai.GenerativeModel(chosen_model)

    prompt = f"""
    You are a helpful assistant that can answer questions about YouTube videos 
    based on the video's transcript.

    Answer the following question in English: {query}
    By searching the following video transcript:
    {docs_page_content}

    Only use the factual information from the transcript to answer the question.
    If you feel like you don't have enough information to answer the question, say "I don't know".

    Your answer should be verbose and detailed.
    """

    response = model.generate_content(prompt)
    return response.text, docs