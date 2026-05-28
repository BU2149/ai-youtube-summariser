"""
utils/ai_processor.py
----------------------
All AI logic:
- Summary generation
- Flashcard generation
- Quiz generation
- RAG-based Q&A chain using LangChain + FAISS + OpenAI
"""

import os
import json
import re
import google.generativeai as genai
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ── Model setup ───────────────────────────────────────────────────────────────
def _get_llm():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("models/gemini-2.5-flash")
    return model


# ── Helper: chunk long transcripts ───────────────────────────────────────────
def _get_first_chunk(transcript: str, max_chars: int = 12000) -> str:
    """Returns first N characters to stay within token limits."""
    return transcript[:max_chars]


# ── 1. Summary Generation ─────────────────────────────────────────────────────
def generate_summary(transcript: str) -> str:
    """
    Generates a structured bullet-point summary of the video transcript.

    Parameters
    ----------
    transcript : Full video transcript text

    Returns
    -------
    Formatted summary string
    """
    llm = _get_llm()
    text = _get_first_chunk(transcript, 12000)

    prompt = f"""You are an expert content summarizer.

Analyze the following YouTube video transcript and create a comprehensive summary.

TRANSCRIPT:
{text}

Create a well-structured summary with:
1. **🎯 Main Topic** (1-2 sentences)
2. **📌 Key Points** (5-8 bullet points)
3. **💡 Key Takeaways** (3-4 important lessons)
4. **🔑 Important Terms** (if any technical terms)

Keep it clear, concise, and valuable. Use bullet points and emojis for readability."""

    response = llm.generate_content(prompt)
    return response.text.strip()


# ── 2. Flashcard Generation ───────────────────────────────────────────────────
def generate_flashcards(transcript: str, num_cards: int = 10) -> list[dict]:
    """
    Generates Q&A flashcards from the transcript.

    Returns
    -------
    List of dicts: [{"question": "...", "answer": "..."}, ...]
    """
    llm = _get_llm()
    text = _get_first_chunk(transcript, 10000)

    prompt = f"""You are an expert educator creating study flashcards.

Based on this YouTube video transcript, create exactly {num_cards} flashcards.

TRANSCRIPT:
{text}

Return ONLY a JSON array in this exact format (no extra text, no markdown):
[
  {{"question": "What is...?", "answer": "The answer is..."}},
  {{"question": "How does...?", "answer": "It works by..."}}
]

Make questions clear and answers concise (1-3 sentences each).
Cover the most important concepts from the video."""

    response = llm.generate_content(prompt)
    response = response.text
    raw = response.strip()

    # Clean JSON if wrapped in markdown code blocks
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        cards = json.loads(raw)
        # Validate structure
        cards = [
            c for c in cards
            if isinstance(c, dict) and "question" in c and "answer" in c
        ]
        return cards
    except json.JSONDecodeError:
        # Fallback: parse manually
        return _parse_flashcards_fallback(raw)


def _parse_flashcards_fallback(raw: str) -> list[dict]:
    """Fallback parser if JSON parsing fails."""
    cards = []
    pairs = re.findall(r'"question":\s*"([^"]+)".*?"answer":\s*"([^"]+)"', raw, re.DOTALL)
    for q, a in pairs:
        cards.append({"question": q, "answer": a})
    return cards if cards else [{"question": "What is this video about?", "answer": raw[:200]}]


# ── 3. Quiz Generation ────────────────────────────────────────────────────────
def generate_quiz(transcript: str, num_questions: int = 5) -> list[dict]:
    """
    Generates multiple-choice quiz questions from the transcript.

    Returns
    -------
    List of dicts:
    [{"question": "...", "options": ["A","B","C","D"], "correct": "A"}, ...]
    """
    llm = _get_llm()
    text = _get_first_chunk(transcript, 10000)

    prompt = f"""You are a quiz creator. Create {num_questions} multiple-choice questions.

TRANSCRIPT:
{text}

Return ONLY a JSON array (no extra text, no markdown):
[
  {{
    "question": "What is...?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": "Option A"
  }}
]

Rules:
- 4 options per question
- Only 1 correct answer
- "correct" must exactly match one of the options
- Questions must be based on the transcript content"""

    response = llm.generate_content(prompt)
    raw = response.text.strip()
    
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        quiz = json.loads(raw)
        quiz = [
            q for q in quiz
            if isinstance(q, dict)
            and "question" in q
            and "options" in q
            and "correct" in q
            and q["correct"] in q["options"]
        ]
        return quiz
    except Exception:
        # Return a basic fallback question
        return [{
            "question": "What is the main topic of this video?",
            "options":  ["AI", "Technology", "Science", "Business"],
            "correct":  "Technology"
        }]


# ── 4. RAG Q&A Chain ──────────────────────────────────────────────────────────
def build_qa_chain(transcript: str):
    """
    Builds a LangChain RAG (Retrieval-Augmented Generation) chain
    using FAISS as the vector store.

    This is the core ML/AI feature:
    1. Splits transcript into chunks
    2. Creates embeddings using OpenAI
    3. Stores in FAISS vector DB
    4. Creates retrieval QA chain

    Returns
    -------
    LangChain RetrievalQA chain object
    """
    api_key = os.getenv("OPENAI_API_KEY")

    # Step 1: Split transcript into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size    = 1000,   # characters per chunk
        chunk_overlap = 150,    # overlap for context continuity
        separators    = ["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.create_documents([transcript])

    # Step 2: Create embeddings + FAISS vector store
    embeddings   = OpenAIEmbeddings(api_key=api_key)
    vector_store = FAISS.from_documents(chunks, embeddings)

    # Step 3: Create retriever
    retriever = vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k": 4}   # retrieve top 4 relevant chunks
    )

    # Step 4: Custom prompt for video Q&A context
    prompt_template = """You are an AI assistant helping users understand a YouTube video.
Use ONLY the provided transcript context to answer the question.
If the answer is not in the context, say "This information isn't covered in the video."

Context from video transcript:
{context}

User Question: {question}

Answer clearly and helpfully:"""

    qa_prompt = PromptTemplate(
        template      = prompt_template,
        input_variables=["context", "question"]
    )

    # Step 5: Build RetrievalQA chain
    llm = _get_llm()
    chain = RetrievalQA.from_chain_type(
        llm            = llm,
        chain_type     = "stuff",
        retriever      = retriever,
        chain_type_kwargs = {"prompt": qa_prompt},
        return_source_documents = False,
    )

    return chain
