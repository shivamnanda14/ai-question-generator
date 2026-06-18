import streamlit as st
import google.generativeai as genai
import pypdf
import json

# Page Configuration
st.set_page_config(page_title="AI Question Paper Generator", page_icon="📝", layout="wide")

# App Header
st.title("📝 AI Question Paper Generator")
st.subheader("Generate tailored exam papers using NLP & LLMs instantly.")
st.markdown("---")

# 🔒 HIDE API KEY LOADING IN THE BACKGROUND
try:
    # Looks for your key silently behind the scenes
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    # ⚠️ EMERGENCY FALLBACK: If your secrets file isn't configured yet, 
    # just paste your raw key string between the quotes below to keep it hidden from the UI!
    api_key = "PASTE_YOUR_ACTUAL_GEMINI_API_KEY_HERE"

# Sidebar Configuration (Completely cleaned up)
with st.sidebar:
    st.header("📋 Paper Settings")
    
    # Difficulty and Question Mix
    difficulty = st.selectbox("Select Difficulty Level:", ["Easy", "Medium", "Hard"])
    
    num_mcq = st.slider("Number of MCQs:", 0, 15, 5)
    num_short = st.slider("Number of Short Answer Questions:", 0, 10, 3)
    num_long = st.slider("Number of Long Answer Questions:", 0, 5, 2)

# Helper function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = pypdf.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Core Function: Generate Questions via LLM
def generate_questions(context, difficulty, num_mcq, num_short, num_long):
    if not api_key or "PASTE_YOUR" in api_key:
        raise ValueError("API Key is missing. Please configure your background secrets or placeholder string.")
        
    # Configure the API client
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Constructing a rigid JSON-enforcing prompt
    prompt = f"""
    You are an expert academic evaluator. Your task is to generate an educational question paper based STRICTLY on the following reference material.
    
    Reference Material:
    \"\"\"{context}\"\"\"
    
    Difficulty Level: {difficulty}
    
    Requirements:
    1. Generate exactly {num_mcq} Multiple Choice Questions (MCQs). Each must have 4 options and a clear correct answer.
    2. Generate exactly {num_short} Short Answer Questions. Include an ideal short marking guideline/answer key.
    3. Generate exactly {num_long} Long Answer Questions. Include key structural points expected in the response.
    
    You MUST respond with a single, valid JSON object exactly matching this schema. Do not include markdown formatting or wrappers like ```json outside the raw string.
    
    {{
      "mcqs": [
        {{
          "question": "Question text here?",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "answer": "Option A"
        }}
      ],
      "short_answers": [
        {{
          "question": "Question text here?",
          "ideal_answer": "Expected brief answer."
        }}
      ],
      "long_answers": [
        {{
          "question": "Question text here?",
          "key_points": ["Point 1", "Point 2", "Point 3"]
        }}
      ]
    }}
    """
    
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)

# Layout: Input Methods
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📥 Source Educational Content")
    input_method = st.radio("Choose Input Method:", ["Paste Text", "Upload PDF Document"])
    
    extracted_text = ""
    if input_method == "Paste Text":
        extracted_text = st.text_area("Paste your textbook chapters or lecture notes here:", height=300)
    else:
        uploaded_file = st.file_uploader("Upload an educational PDF:", type=["pdf"])
        if uploaded_file is not None:
            with st.spinner("Extracting text from PDF..."):
                extracted_text = extract_text_from_pdf(uploaded_file)
            st.success("PDF text extracted successfully!")

# Action Button
with col2:
    st.markdown("### 🚀 Execution")
    st.write("Review your settings in the sidebar and trigger the generation engine.")
    
    if st.button("Generate Question Paper", type="primary"):
        if not api_key or "PASTE_YOUR" in api_key:
            st.error("Please provide your API key in the code background configuration.")
        elif not extracted_text.strip():
            st.error("Please provide some source content first.")
        else:
            with st.spinner("Analyzing content and designing questions..."):
                try:
                    paper_data = generate_questions(extracted_text, difficulty, num_mcq, num_short, num_long)
                    st.session_state['generated_paper'] = paper_data
                    st.success("Question Paper Successfully Generated!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Display Section for the Generated Output
if 'generated_paper' in st.session_state:
    st.markdown("---")
    st.header("📋 Generated Question Paper")
    
    data = st.session_state['generated_paper']
    tab1, tab2, tab3 = st.tabs(["🧩 Multiple Choice (MCQs)", "📝 Short Answer", "📚 Long Answer"])
    
    with tab1:
        if data.get("mcqs"):
            for idx, item in enumerate(data["mcqs"], 1):
                st.markdown(f"**Q{idx}. {item['question']}**")
                for opt in item['options']:
                    st.write(f"- {opt}")
                with st.expander("Show Answer"):
                    st.success(f"Correct Answer: {item['answer']}")
                st.write("")
            
    with tab2:
        if data.get("short_answers"):
            for idx, item in enumerate(data["short_answers"], 1):
                st.markdown(f"**Q{idx}. {item['question']}**")
                with st.expander("Show Marking Scheme/Ideal Answer"):
                    st.info(f"Answer Guideline: {item['ideal_answer']}")
                st.write("")
            
    with tab3:
        if data.get("long_answers"):
            for idx, item in enumerate(data["long_answers"], 1):
                st.markdown(f"**Q{idx}. {item['question']}**")
                with st.expander("Show Evaluation Metrics / Key Points"):
                    for pt in item['key_points']:
                        st.write(f"✔️ {pt}")
                st.write("")

    st.markdown("---")
    raw_json_string = json.dumps(data, indent=2)
    st.download_button(
        label="Download Paper as JSON",
        data=raw_json_string,
        file_name="question_paper.json",
        mime="application/json"
    )