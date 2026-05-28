# 🎬 YouTube AI Summarizer

> Paste any YouTube link → Get instant AI-powered summary, flashcards, quiz & chat Q&A.
> Built with LangChain + OpenAI + FAISS + Streamlit.

---

## 🚀 What It Does

| Feature | Description |
|---|---|
| 📝 **Smart Summary** | Structured bullet-point summary with key takeaways |
| 🃏 **Flashcards** | Auto-generated Q&A study cards |
| 🧠 **Quiz Mode** | MCQ quiz with scoring to test your knowledge |
| 💬 **AI Chat (RAG)** | Ask anything about the video using RAG pipeline |
| 📄 **Full Transcript** | Download the complete transcript |

---

## 🧠 Architecture (RAG Pipeline)

```
YouTube URL
    │
    ▼
youtube-transcript-api ──► Raw Transcript Text
    │
    ▼
RecursiveCharacterTextSplitter ──► Text Chunks (1000 chars, 150 overlap)
    │
    ▼
OpenAI Embeddings ──► Vector Representations
    │
    ▼
FAISS Vector Store ──► Similarity Search Index
    │
    ▼
RetrievalQA Chain (LangChain) ──► Context-Aware Answers
    │
    ▼
GPT-4o-mini ──► Final Response to User
```

---

## ⚙️ Installation

### Step 1 — Clone / Download
```bash
git clone https://github.com/yourusername/youtube-ai-summarizer.git
cd youtube-ai-summarizer
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Add API Key
```bash
cp .env.example .env
# Open .env and paste your OpenAI API key
```

### Step 5 — Run
```bash
streamlit run app.py
```

---

## 🔑 Getting Your OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy and paste into your `.env` file

---

## 📁 Project Structure

```
youtube-summarizer/
│
├── app.py                    ← Main Streamlit UI
├── requirements.txt          ← Dependencies
├── .env.example              ← API key template
├── README.md                 ← This file
│
└── utils/
    ├── __init__.py
    ├── transcript.py         ← YouTube transcript extraction
    └── ai_processor.py       ← Summary, flashcards, quiz, RAG Q&A
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Streamlit** | Web UI |
| **LangChain** | RAG pipeline, prompt management |
| **OpenAI GPT-4o-mini** | Text generation |
| **FAISS** | Vector similarity search |
| **OpenAI Embeddings** | Text → vectors |
| **youtube-transcript-api** | Free transcript extraction |
| **yt-dlp** | Video metadata |

---

## 💡 How It Works

1. **Transcript Extraction** — `youtube-transcript-api` fetches subtitles for free (no YouTube API key needed)
2. **Chunking** — LangChain splits transcript into 1000-char chunks with 150-char overlap
3. **Embedding** — OpenAI converts chunks to vector embeddings
4. **FAISS Index** — Vectors stored in FAISS for fast similarity search
5. **RAG Chain** — User query → retrieve top 4 relevant chunks → GPT answers with context

---

## 🔮 Future Improvements
- [ ] Support for Hindi / multilingual videos
- [ ] Export flashcards to Anki format
- [ ] Playlist summarization
- [ ] Save summaries to database
- [ ] Share summaries via link

---

*Built with ❤️ using LangChain + OpenAI + Streamlit*
