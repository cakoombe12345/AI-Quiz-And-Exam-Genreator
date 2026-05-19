import os
import streamlit as st

from ai_engine import generate_quiz
from pdf_processor import extract_text
from pdf_exporter import create_exam_pdf

# --- HARDCODED API KEY ---
GEMINI_API_KEY = "AIzaSyDzmaiGlQA_OGuk-CVpkG7IJF96lg1be1g"

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Quiz & Exam Generator",
    layout="wide",
    page_icon="🎓",
)

# --- GLOBAL CUSTOM THEME & CSS INJECTION (TOP-OF-PAGE) ---
st.markdown(
    """
<style>
/* =========================
   Premium Dark SaaS Theme
   ========================= */
:root{
  --bg0:#09090b;
  --bg1:#0b0f19;
  --card:#18181b;
  --card2:#111117;
  --border:#27272a;
  --text:#f4f4f5; /* crisp zinc-ish */
  --muted:#a1a1aa;
  --muted2:#71717a;

  --accent1:#6366f1;
  --accent2:#3b82f6;

  --good:#22c55e;
  --warn:#f59e0b;
  --bad:#ef4444;

  --shadow: 0 18px 60px rgba(0,0,0,.45);
}

html, body, [class*="stApp"]{
  background: radial-gradient(1200px 700px at 10% -10%, rgba(99,102,241,.20), transparent 55%),
              radial-gradient(900px 600px at 90% 0%, rgba(59,130,246,.18), transparent 45%),
              linear-gradient(180deg, var(--bg1), var(--bg0)) !important;
  color: var(--text);
}

/* Streamlit top padding tweaks */
.block-container{
  padding-top: 1.2rem;
}

/* Inputs / containers base */
.stCard, .st-emotion-cache-1e3u2q{
  background-color: var(--card);
  border: 1px solid rgba(39,39,42,.95);
  border-radius: 16px;
}

/* Make all text areas, select, inputs match */
textarea, input[type="text"], input[type="password"], input[type="number"]{
  background: rgba(17,17,23,.75) !important;
  border: 1px solid rgba(39,39,42,.95) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
}

/* Focus rings for a more premium feel */
textarea:focus, input:focus{
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,.25), 0 0 0 1px rgba(59,130,246,.25) !important;
}

/* =========================
   Widget global styling
   ========================= */
.stSidebar{
  background: rgba(11,15,25,.65) !important;
  backdrop-filter: blur(14px);
  border-right: 1px solid rgba(39,39,42,.85) !important;
}

/* Buttons */
.stButton > button{
  background: linear-gradient(135deg, rgba(99,102,241,1), rgba(59,130,246,1)) !important;
  color: white !important;
  border: none !important;
  border-radius: 14px !important;
  padding: 0.65rem 1rem !important;
  font-weight: 700 !important;
  font-size: 0.88rem !important;
  line-height: 1.1 !important;
  letter-spacing: .1px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  box-shadow: 0 14px 35px rgba(99,102,241,.18), 0 2px 0 rgba(255,255,255,.06) inset;
  transition: transform .14s ease, box-shadow .14s ease, filter .14s ease !important;
}
.stButton > button:hover{
  transform: translateY(-1px) !important;
  box-shadow: 0 18px 50px rgba(99,102,241,.26), 0 2px 0 rgba(255,255,255,.09) inset !important;
  filter: saturate(1.05) !important;
}
.stButton > button:focus{
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,.30), 0 18px 50px rgba(99,102,241,.26) !important;
}

/* Medium difficulty button - neutral (normal) style */
div[data-testid="stSidebar"] button[kind="secondary"][data-testid="baseButton-diff_med"]{
  background: rgba(24,24,27,.95) !important;
  color: #e4e4e7 !important;
  border: 1px solid rgba(63,63,70,.95) !important;
  box-shadow: none !important;
  font-size: 0.74rem !important;
  line-height: 1.05 !important;
  white-space: nowrap !important;
}
div[data-testid="stSidebar"] button[kind="secondary"][data-testid="baseButton-diff_med"]:hover{
  background: rgba(39,39,42,.95) !important;
  transform: none !important;
  filter: none !important;
  box-shadow: none !important;
}

/* Download button sometimes uses stButton too; keep consistent */
.stDownloadButton > button{
  background: linear-gradient(135deg, rgba(99,102,241,1), rgba(59,130,246,1)) !important;
  color: white !important;
  border-radius: 14px !important;
  border: none !important;
  font-weight: 700 !important;
}

/* Checkbox / radio */
.css-1cpxqw2 span, .css-1cpxqw2 label{
  color: var(--muted) !important;
}
.stCheckbox, .stRadio, .stSelectbox{
  color: var(--text) !important;
}

/* File uploader (dropzone look)
   Keep overrides minimal to avoid breaking click/drag interaction. */
.stFileUploader{
  background: rgba(17,17,23,.65) !important;
  border: 1px dashed rgba(99,102,241,.55) !important;
  border-radius: 16px !important;
  padding: 18px !important;
  pointer-events: auto !important;
}
.stFileUploader:hover{
  border-color: rgba(59,130,246,.85) !important;
}

/* Ensure uploader internals remain clickable */
.stFileUploader *{
  pointer-events: auto !important;
}

/* Style only labels (avoid overriding generic div/section structures) */
.stFileUploader label{
  color: var(--text) !important;
  font-weight: 700 !important;
  letter-spacing: .2px;
}

/* Sliders */
.stSlider > div[data-testid="stSlider"]{
  color: var(--accent2) !important;
}
.stSlider .stSliderTrack{
  background: rgba(59,130,246,.35) !important;
}
.stSlider .stSliderBar{
  background: linear-gradient(135deg, var(--accent1), var(--accent2)) !important;
}
.stSlider input[type="range"]{
  accent-color: var(--accent2) !important;
}

/* Tabs */
div[data-baseweb="tab-list"]{
  background: rgba(17,17,23,.55) !important;
  border: 1px solid rgba(39,39,42,.9) !important;
  border-radius: 16px !important;
  padding: 6px !important;
  box-shadow: 0 10px 30px rgba(0,0,0,.25);
}
div[role="tab"]{
  background: transparent !important;
  color: var(--muted) !important;
  font-weight: 700 !important;
  border-radius: 12px !important;
  padding: 10px 14px !important;
}
div[role="tab"][aria-selected="true"]{
  color: white !important;
  background: linear-gradient(135deg, rgba(99,102,241,.95), rgba(59,130,246,.95)) !important;
  box-shadow: 0 12px 34px rgba(99,102,241,.22) !important;
}

/* Expander / details */
.stExpander > div{
  border: 1px solid rgba(39,39,42,.9);
  border-radius: 14px;
  background: rgba(17,17,23,.55);
}
.stExpander section{
  background: transparent !important;
}

/* =========================
   Custom layout / cards
   ========================= */
.hero{
  text-align: center;
  padding: 22px 0 14px 0;
}
.hero-title{
  font-size: clamp(2rem, 4.5vw, 3.15rem);
  font-weight: 900;
  letter-spacing: -0.02em;
  margin: 0.2rem 0 0.3rem 0;
  background: linear-gradient(90deg, #c7d2fe 0%, #60a5fa 35%, #6366f1 70%, #93c5fd 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.hero-sub{
  font-size: 1.05rem;
  color: var(--muted);
  margin: 0 auto;
  max-width: 900px;
  line-height: 1.5;
}
.pill-badge{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 8px 14px;
  border-radius: 999px;
  border: 1px solid rgba(39,39,42,.95);
  background: rgba(17,17,23,.60);
  box-shadow: 0 18px 60px rgba(0,0,0,.25);
  margin-bottom: 12px;
}
.pill-dot{
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent1), var(--accent2));
  box-shadow: 0 0 18px rgba(99,102,241,.55);
  animation: pulseGlow 1.8s ease-in-out infinite;
}
@keyframes pulseGlow{
  0%,100%{ transform: scale(1); opacity: .85; }
  50%{ transform: scale(1.2); opacity: 1; }
}

.dashboard-card{
  background: rgba(17,17,23,.55);
  border: 1px solid rgba(39,39,42,.95);
  border-radius: 18px;
  padding: 18px 18px 16px 18px;
  box-shadow: var(--shadow);
}

/* Question cards stay aligned with premium theme */
.question-card{
  background-color: rgba(17,17,23,.55) !important;
  padding: 1.3rem 1.3rem;
  border-radius: 16px !important;
  margin-bottom: 1rem;
  border: 1px solid rgba(39,39,42,.95) !important;
  box-shadow: 0 18px 50px rgba(0,0,0,.25);
}
.answer-key{
  background-color: rgba(34,197,94,.08) !important;
  padding: 1rem;
  border-radius: 14px !important;
  border: 1px solid rgba(34,197,94,.30) !important;
  margin-top: 1rem;
}

/* Subtle separator */
.streamlit-expanderContent{
  color: var(--text);
}

/* Hide default Streamlit subheaders spacing for cleaner look (optional) */
.stSubheader{
  color: var(--text) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- STATE INITIALIZATION ---
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"
if "num_questions" not in st.session_state:
    st.session_state.num_questions = 5
if "question_types" not in st.session_state:
    st.session_state.question_types = ["Multiple Choice", "True/False", "Short Answer"]
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False
if "input_method" not in st.session_state:
    st.session_state.input_method = "upload"

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown(
        """
<div style="display:flex; align-items:center; gap:12px; padding: 8px 0 16px 0;">
  <div style="
    width:44px; height:44px; border-radius: 14px;
    background: linear-gradient(135deg, rgba(99,102,241,1), rgba(59,130,246,1));
    box-shadow: 0 0 0 1px rgba(39,39,42,.9), 0 18px 50px rgba(99,102,241,.25);
    display:flex; align-items:center; justify-content:center;
  ">
    <span style="font-size:20px; filter: drop-shadow(0 8px 18px rgba(0,0,0,.25));">🎓</span>
  </div>
  <div>
    <div style="font-weight:900; font-size:1.05rem; line-height:1.15; color:#f4f4f5;">ExamAI Pro</div>
    <div style="color:#a1a1aa; font-weight:650; font-size:.9rem;">AI Quiz Generator</div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("⚙️ Quiz Settings")

    st.markdown("**Difficulty Level**")
    # Styled segmented control (HTML visuals) backed by st.radio for actual state update
    diff_col = st.columns([1, 1, 1])
    with diff_col[0]:
        if st.button(
            "Easy",
            use_container_width=True,
            key="diff_easy",
            help="Set difficulty to Easy",
        ):
            st.session_state.difficulty = "Easy"
    with diff_col[1]:
        if st.button(
            "Medium",
            use_container_width=True,
            key="diff_med",
            help="Set difficulty to Medium",
        ):
            st.session_state.difficulty = "Medium"
    with diff_col[2]:
        if st.button(
            "Hard",
            use_container_width=True,
            key="diff_hard",
            help="Set difficulty to Hard",
        ):
            st.session_state.difficulty = "Hard"

    # Gentle visual indicator for selection
    st.markdown(
        f"""
<div style="margin-top:10px; margin-bottom:10px; padding: 10px 12px; border-radius: 14px; border: 1px solid rgba(39,39,42,.95); background: rgba(17,17,23,.45);">
  <div style="color:#a1a1aa; font-weight:700; font-size:.9rem;">Selected</div>
  <div style="color:#f4f4f5; font-weight:900; font-size:1.05rem;">{st.session_state.difficulty}</div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Number of Questions**")
    st.slider(
        "Question count",
        min_value=1,
        max_value=30,
        value=int(st.session_state.num_questions),
        step=1,
        key="num_questions_slider",
        on_change=lambda: st.session_state.update(num_questions=st.session_state.get("num_questions_slider")),
    )

    st.markdown("**Question Types**")
    use_mcq = st.checkbox("Multiple Choice (MCQ)", value=True)
    use_tf = st.checkbox("True / False", value=True)
    use_sa = st.checkbox("Short Answer", value=True)

    qtypes = []
    if use_mcq:
        qtypes.append("Multiple Choice")
    if use_tf:
        qtypes.append("True/False")
    if use_sa:
        qtypes.append("Short Answer")
    st.session_state.question_types = qtypes

# --- MAIN: HERO ---
st.markdown(
    """
<div class="hero">
  <div class="pill-badge">
    <div class="pill-dot"></div>
  </div>
  <div class="hero-title">AI Quiz &amp; Exam Generator System</div>
  <div class="hero-sub">Transform your study materials into structured exams instantly using AI.</div>
</div>
""",
    unsafe_allow_html=True,
)

# --- MAIN CONTENT AREA (DASHBOARD CARD) ---
st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.subheader("📚 1. Input Study Material")

tab1_label = "📁 Upload File (PDF/TXT)"
tab2_label = "✍️ Paste Text"

input_tabs = st.tabs([tab1_label, tab2_label])

# Persist text across reruns so Generate button can reliably use selected source.
if "uploaded_context_text" not in st.session_state:
    st.session_state.uploaded_context_text = ""
if "pasted_context_text" not in st.session_state:
    st.session_state.pasted_context_text = ""

with input_tabs[0]:
    uploaded_file = st.file_uploader(
        "Upload your document",
        type=["pdf", "txt"],
        label_visibility="visible",
        key="study_material_uploader",
    )
    if uploaded_file is not None:
        try:
            with st.spinner("Extracting text from file..."):
                extracted_text = extract_text(uploaded_file, uploaded_file.name)
            st.session_state.uploaded_context_text = extracted_text
            st.session_state.input_method = "upload"
            st.success(f"Successfully extracted text ({len(extracted_text)} characters).")
            with st.expander("Preview Extracted Text"):
                st.text(extracted_text[:1000] + ("..." if len(extracted_text) > 1000 else ""))
        except Exception as e:
            st.error(f"Error reading file: {e}")

with input_tabs[1]:
    pasted_text = st.text_area(
        "Paste your study material here:",
        height=260,
        placeholder="Paste notes, articles, or any text here...",
        value=st.session_state.pasted_context_text,
    )
    st.session_state.pasted_context_text = pasted_text
    if pasted_text.strip():
        st.session_state.input_method = "paste"

if st.session_state.input_method == "paste":
    context_text = st.session_state.pasted_context_text.strip()
else:
    context_text = st.session_state.uploaded_context_text.strip()

st.caption(f"Input Source: {st.session_state.input_method.title()} • Characters: {len(context_text)}")

st.markdown("</div>", unsafe_allow_html=True)

# --- PRIMARY CTA BUTTON ---
st.write("")
is_ready = bool(context_text and context_text.strip())
selected_types = st.session_state.get("question_types", [])

btn_col1, btn_col2, btn_col3 = st.columns([2, 6, 2])
with btn_col2:
    generate_clicked = st.button(
        "🚀 Generate Exam",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.is_generating,  # Streamlit supports this in newer versions
    )

if generate_clicked and not st.session_state.is_generating:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "INSERT YOUR AI API KEY HERE":
        st.error("Missing API Key! Please insert your Gemini API Key directly into the `app.py` file.")
    elif not is_ready:
        st.error("Missing Material! Please provide some study material (either by uploading a file or pasting text).")
    elif len(selected_types) == 0:
        st.error("Missing Configuration! Please select at least one question type.")
    else:
        st.session_state.is_generating = True
        try:
            with st.spinner(
                f"Generating a {st.session_state.difficulty} quiz with {st.session_state.num_questions} questions using AI... This may take a moment."
            ):
                quiz = generate_quiz(
                    api_key=GEMINI_API_KEY,
                    context_text=context_text,
                    difficulty=st.session_state.difficulty,
                    question_types=selected_types,
                    num_questions=int(st.session_state.num_questions),
                )

            if quiz and quiz.questions:
                st.session_state.quiz_data = quiz
                st.success("Quiz generated successfully!")
            else:
                st.error("Failed to generate quiz. The AI might have returned malformed data or your API key is invalid. Please try again.")
        finally:
            st.session_state.is_generating = False

# --- DISPLAY QUIZ AND EXPORT ---
if st.session_state.quiz_data:
    st.divider()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("📝 2. Interactive Exam")
        st.markdown(
            f"**Difficulty:** {st.session_state.difficulty} | **Questions:** {len(st.session_state.quiz_data.questions)}"
        )

    with col2:
        pdf_buffer = create_exam_pdf(st.session_state.quiz_data)
        st.download_button(
            label="📥 Export as PDF",
            data=pdf_buffer,
            file_name="AI_Generated_Exam.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.write("")

    for i, q in enumerate(st.session_state.quiz_data.questions, 1):
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.markdown(f"**Q{i}. {q.question_text}**")

        if q.type == "mcq" and q.options:
            for j, opt in enumerate(q.options):
                st.write(f"{chr(65 + j)}) {opt}")
        elif q.type == "true_false":
            st.radio("Your Answer:", ["True", "False"], key=f"tf_{i}", index=None)
        else:
            st.text_area("Your Answer:", key=f"sa_{i}", height=100)

        with st.expander("👁️ View Answer Key & Explanation"):
            st.markdown('<div class="answer-key">', unsafe_allow_html=True)
            st.markdown(f"**Correct Answer:** `{q.correct_answer}`")
            st.markdown(f"**Explanation:** {q.explanation}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
