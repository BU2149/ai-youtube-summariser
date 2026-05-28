"""
app.py — YouTube Video Summarizer & Q&A
----------------------------------------
Main entry point. Handles UI and page routing.
"""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="YouTube AI Summarizer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Premium CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 50%, #0a0f1a 100%);
    color: #e2e8f0;
}

.hero {
    background: linear-gradient(135deg, #1a0a2e 0%, #0d1117 50%, #0a1628 100%);
    border: 1px solid #ff000020;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #ff0000, transparent);
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ff4444, #ff8800);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero p { color: #64748b; margin: 0.5rem 0 0; font-size: 1rem; }

.feature-card {
    background: #0f0f1a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    transition: border-color 0.2s, transform 0.2s;
}
.feature-card:hover { border-color: #ff444440; transform: translateY(-2px); }
.feature-card .icon  { font-size: 1.8rem; }
.feature-card .title { font-size: 0.88rem; font-weight: 600; color: #e2e8f0; margin-top: 0.4rem; }
.feature-card .desc  { font-size: 0.75rem; color: #475569; margin-top: 0.2rem; }

.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e2e8f0;
    border-left: 3px solid #ff4444;
    padding-left: 0.75rem;
    margin: 1.5rem 0 1rem;
}

.result-box {
    background: #0f0f1a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    line-height: 1.8;
    font-size: 0.9rem;
    color: #cbd5e1;
}

.flashcard {
    background: linear-gradient(135deg, #1a1030, #0f1a2e);
    border: 1px solid #ff444420;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}
.flashcard .q { color: #ff6644; font-weight: 600; font-size: 0.88rem; }
.flashcard .a { color: #94a3b8; font-size: 0.85rem; margin-top: 0.4rem; line-height: 1.6; }

.video-info {
    background: #0f0f1a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    font-size: 0.85rem;
}
.video-info .vtitle { font-size: 1rem; font-weight: 600; color: #e2e8f0; }
.video-info .vmeta  { color: #475569; margin-top: 0.3rem; font-size: 0.8rem; }

.chat-user {
    background: linear-gradient(135deg, #1e3a5f, #1a2a4a);
    border-radius: 12px 12px 4px 12px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: #93c5fd;
    text-align: right;
}
.chat-ai {
    background: #0f0f1a;
    border: 1px solid #1e293b;
    border-radius: 12px 12px 12px 4px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.7;
}

.quiz-option {
    background: #0f1a2e;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin: 0.3rem 0;
    cursor: pointer;
    font-size: 0.85rem;
    transition: border-color 0.2s;
}

.stButton > button {
    background: linear-gradient(135deg, #ff4444, #cc2200) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px #ff444430 !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0f0f1a !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #0f0f1a !important;
    border-radius: 10px !important;
    border: 1px solid #1e293b !important;
    padding: 4px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #ff4444, #cc2200) !important;
    color: white !important;
    border-radius: 8px !important;
}
.stTabs [data-baseweb="tab"] { color: #475569 !important; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎬 YouTube AI Summarizer</h1>
    <p>Paste any YouTube link → Get instant summary, flashcards, quiz & AI Q&A</p>
</div>
""", unsafe_allow_html=True)

# ── Feature cards ─────────────────────────────────────────────────────────────
f1, f2, f3, f4 = st.columns(4)
features = [
    (f1, "📝", "Smart Summary",  "Key points in seconds"),
    (f2, "🃏", "Flashcards",     "Auto Q&A cards"),
    (f3, "🧠", "Quiz Mode",      "Test your knowledge"),
    (f4, "💬", "Ask Anything",   "Chat with the video"),
]
for col, icon, title, desc in features:
    col.markdown(f"""
    <div class="feature-card">
        <div class="icon">{icon}</div>
        <div class="title">{title}</div>
        <div class="desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── URL Input ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔗 Enter YouTube URL</div>',
            unsafe_allow_html=True)

col_url, col_btn = st.columns([4, 1])
with col_url:
    youtube_url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )
with col_btn:
    process_btn = st.button("🚀 Analyze Video", use_container_width=True)

# ── Process Video ─────────────────────────────────────────────────────────────
if process_btn and youtube_url:
    from utils.transcript import get_transcript, get_video_info
    from utils.ai_processor import (
        generate_summary, generate_flashcards,
        generate_quiz, build_qa_chain
    )

    with st.spinner("🎬 Fetching video transcript..."):
        transcript, error = get_transcript(youtube_url)

    if error:
        st.error(f"❌ {error}")
        st.info("💡 Make sure the video has subtitles/captions enabled.")
        st.stop()

    # Save to session state
    st.session_state["transcript"]   = transcript
    st.session_state["youtube_url"]  = youtube_url
    st.session_state["chat_history"] = []

    # Get video info
    info = get_video_info(youtube_url)
    st.session_state["video_info"] = info

    # Pre-generate summary
    with st.spinner("🤖 AI is analyzing the video..."):
        summary = generate_summary(transcript)
        st.session_state["summary"] = summary

    st.success("✅ Video analyzed successfully!")

elif process_btn and not youtube_url:
    st.warning("⚠️ Please enter a YouTube URL first.")

# ── Results Section ───────────────────────────────────────────────────────────
if "transcript" in st.session_state:
    transcript  = st.session_state["transcript"]
    video_info  = st.session_state.get("video_info", {})

    # Video info banner
    if video_info:
        st.markdown(f"""
        <div class="video-info">
            <div class="vtitle">🎬 {video_info.get('title','Video')}</div>
            <div class="vmeta">
                📺 {video_info.get('channel','—')} &nbsp;|&nbsp;
                ⏱️ {video_info.get('duration','—')} &nbsp;|&nbsp;
                📝 {len(transcript.split())} words transcribed
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Summary", "🃏 Flashcards", "🧠 Quiz", "💬 Q&A Chat", "📄 Transcript"
    ])

    # ── Tab 1: Summary ────────────────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">📝 AI-Generated Summary</div>',
                    unsafe_allow_html=True)

        summary = st.session_state.get("summary", "")
        if not summary:
            from utils.ai_processor import generate_summary
            with st.spinner("Generating summary..."):
                summary = generate_summary(transcript)
                st.session_state["summary"] = summary

        st.markdown(f'<div class="result-box">{summary}</div>',
                    unsafe_allow_html=True)

        # Download
        st.download_button(
            "⬇️ Download Summary",
            summary,
            file_name="video_summary.txt",
            mime="text/plain"
        )

    # ── Tab 2: Flashcards ─────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">🃏 Flashcards</div>',
                    unsafe_allow_html=True)

        if "flashcards" not in st.session_state:
            if st.button("✨ Generate Flashcards"):
                from utils.ai_processor import generate_flashcards
                with st.spinner("Creating flashcards..."):
                    cards = generate_flashcards(transcript)
                    st.session_state["flashcards"] = cards
        else:
            cards = st.session_state["flashcards"]
            st.markdown(f"**{len(cards)} flashcards generated**")
            for i, card in enumerate(cards, 1):
                with st.expander(f"Card {i}: {card.get('question','')[:60]}..."):
                    st.markdown(f"""
                    <div class="flashcard">
                        <div class="q">❓ {card.get('question','')}</div>
                        <div class="a">💡 {card.get('answer','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Download flashcards
            fc_text = "\n\n".join(
                [f"Q: {c['question']}\nA: {c['answer']}" for c in cards]
            )
            st.download_button(
                "⬇️ Download Flashcards",
                fc_text,
                file_name="flashcards.txt",
                mime="text/plain"
            )

        if "flashcards" not in st.session_state:
            pass
        else:
            if st.button("🔄 Regenerate Flashcards"):
                del st.session_state["flashcards"]
                st.rerun()

    # ── Tab 3: Quiz ───────────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">🧠 Test Your Knowledge</div>',
                    unsafe_allow_html=True)

        if "quiz" not in st.session_state:
            if st.button("🎯 Generate Quiz"):
                from utils.ai_processor import generate_quiz
                with st.spinner("Creating quiz questions..."):
                    quiz = generate_quiz(transcript)
                    st.session_state["quiz"]       = quiz
                    st.session_state["quiz_score"] = 0
                    st.session_state["quiz_done"]  = []
        else:
            quiz  = st.session_state["quiz"]
            score = st.session_state.get("quiz_score", 0)
            done  = st.session_state.get("quiz_done",  [])

            st.markdown(f"**Score: {score}/{len(quiz)}**")
            st.progress(len(done) / max(len(quiz), 1))

            for i, q in enumerate(quiz):
                if i in done:
                    continue
                st.markdown(f"**Q{i+1}: {q['question']}**")
                choice = st.radio(
                    f"q{i}", q["options"],
                    label_visibility="collapsed",
                    key=f"quiz_q_{i}"
                )
                if st.button(f"Submit Answer", key=f"submit_{i}"):
                    if choice == q["correct"]:
                        st.success("✅ Correct!")
                        st.session_state["quiz_score"] += 1
                    else:
                        st.error(f"❌ Wrong! Answer: {q['correct']}")
                    st.session_state["quiz_done"].append(i)
                    st.rerun()
                break  # show one question at a time

            if len(done) == len(quiz):
                st.balloons()
                st.success(f"🎉 Quiz Complete! Score: {score}/{len(quiz)}")
                if st.button("🔄 Restart Quiz"):
                    del st.session_state["quiz"]
                    del st.session_state["quiz_score"]
                    del st.session_state["quiz_done"]
                    st.rerun()

    # ── Tab 4: Q&A Chat ───────────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-header">💬 Ask Anything About the Video</div>',
                    unsafe_allow_html=True)

        # Build QA chain once
        if "qa_chain" not in st.session_state:
            st.session_state["qa_chain"] = "disabled"

        # Show chat history
        for msg in st.session_state.get("chat_history", []):
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai">🤖 {msg["content"]}</div>',
                            unsafe_allow_html=True)

        # Input
        user_q = st.text_input(
            "Ask a question",
            placeholder="What is the main topic? Who is the speaker? Explain XYZ...",
            label_visibility="collapsed",
            key="chat_input"
        )
        if st.button("💬 Ask", use_container_width=True) and user_q:
            chain = st.session_state["qa_chain"]
            with st.spinner("Thinking..."):
                answer = chain.invoke({"query": user_q})
                if isinstance(answer, dict):
                    answer = answer.get("result", str(answer))

            st.session_state["chat_history"].append(
                {"role": "user",      "content": user_q}
            )
            st.session_state["chat_history"].append(
                {"role": "assistant", "content": answer}
            )
            st.rerun()

        if st.session_state.get("chat_history"):
            if st.button("🗑️ Clear Chat"):
                st.session_state["chat_history"] = []
                st.rerun()

    # ── Tab 5: Transcript ─────────────────────────────────────────────────────
    with tab5:
        st.markdown('<div class="section-header">📄 Full Transcript</div>',
                    unsafe_allow_html=True)
        st.markdown(f'<div class="result-box">{transcript[:3000]}{"..." if len(transcript)>3000 else ""}</div>',
                    unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download Full Transcript",
            transcript,
            file_name="transcript.txt",
            mime="text/plain"
        )

# ── Empty state ───────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="text-align:center; padding:3rem; color:#334155;">
        <div style="font-size:3rem;">🎬</div>
        <div style="font-size:1rem; margin-top:0.5rem;">
            Paste a YouTube URL above and click Analyze Video
        </div>
        <div style="font-size:0.8rem; margin-top:0.3rem; color:#1e293b;">
            Works with any video that has subtitles/captions
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#1e293b; font-size:0.75rem; margin-top:2rem;">
    YouTube AI Summarizer | Built with LangChain + OpenAI + Streamlit
</div>
""", unsafe_allow_html=True)
