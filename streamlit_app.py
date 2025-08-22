# ui.py
import streamlit as st
import requests
import time
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

API_URL = "http://127.0.0.1:8000/predict/"

st.set_page_config(page_title="AI Research Assistant", layout="wide")

# Sidebar history navigation
st.sidebar.title("📜 Query History")
if "history" not in st.session_state:
    st.session_state.history = []

for idx, item in enumerate(reversed(st.session_state.history), 1):
    if st.sidebar.button(f"Q{idx}: {item['question'][:30]}..."):
        st.session_state.selected = item

# Main Title
st.title("🤖 AI Research Assistant")
st.markdown("Ask scientific or academic questions and get **summaries, references, and suggestions**.")

field = st.text_input("📘 Field of Study (optional):", value="General")
prompt = st.text_area("💬 Enter your research question:", height=120)

if st.button("Ask"):
    if prompt.strip():
        st.markdown("---")
        st.markdown(f"**Q:** {prompt}")
        answer_placeholder = st.empty()
        full_answer = ""

        try:
            payload = {"prompt": prompt, "field": field}
            with requests.post(API_URL, json=payload, stream=True) as response:
                if response.status_code == 200:
                    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                        full_answer += chunk
                        # Format sections dynamically
                        formatted_answer = full_answer.replace("Actionable suggestions:", "### ✅ Suggestions")\
                                                      .replace("References:", "### 📚 References")\
                                                      .replace("Limitation:", "⚠️ **Limitation**")
                        answer_placeholder.markdown(f"**A:**\n\n{formatted_answer}")
                        time.sleep(0.01)

                    st.session_state.history.append({"question": prompt, "answer": full_answer})
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"🚨 Request failed: {e}")
    else:
        st.warning("⚠️ Please enter a question before submitting.")

# --- Download Answer Feature ---
if st.session_state.history:
    last_answer = st.session_state.history[-1]["answer"]

    def export_pdf(text):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        elements = [Paragraph(p, styles["Normal"]) for p in text.split("\n")]
        doc.build(elements)
        buffer.seek(0)
        return buffer

    st.download_button(
        "📄 Download Last Answer (PDF)",
        data=export_pdf(last_answer),
        file_name="research_answer.pdf",
        mime="application/pdf"
    )

    st.download_button(
        "📝 Download Last Answer (Markdown)",
        data=last_answer,
        file_name="research_answer.md",
        mime="text/markdown"
    )
