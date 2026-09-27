# 🎥 YouTube Assistant

A containerized Retrieval-Augmented Generation (RAG) application built with **Streamlit**, **LangChain**, **FAISS**, and **Google Gemini**. It extracts transcripts from YouTube videos, embeds them using local CPU models, and generates factual answers to user questions based strictly on the video content.

---

> **A Note on Continuous Learning:**  
> Apologies in advance for any bugs, edge cases, or errors you might encounter while running this application. I am continuously learning and iterating on my projects. 
> 
> If you spot an error, please feel free to fix it, open a **Pull Request**, or leave a comment/issue with constructive feedback. Any guidance helps me learn from my mistakes and become a better engineer!



## ⚡ Features & Tech Stack

- **UI:** Streamlit
- **LLM:** Google Gemini (`gemini-1.5-flash` / `gemini-pro`) via `google-generativeai`
- **Embeddings:** Local HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (no quota or API cost)
- **Vector Search:** FAISS (CPU)
- **Containerization:** Docker & Docker Compose compatible

---

## 🚀 Quick Start (Docker)

### 1. Set up Environment Variables
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```
> **Important:** Do not include spaces around the `=` sign.

### 2. Build and Run Container
```bash
# Build the Docker image
docker build -t youtube-assistant .

# Run the container
docker run -d -p 8501:8501 --env-file .env --name yt-assistant-app youtube-assistant
```

Open your browser at:
```text
http://localhost:8501
```

### Useful Commands
- **Stop app:** `docker stop yt-assistant-app`
- **Start app:** `docker start yt-assistant-app`
- **View logs:** `docker logs -f yt-assistant-app`

---

## 💻 Local Setup (Without Docker)

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
```

---

## ⚠️ Note & Community Feedback

