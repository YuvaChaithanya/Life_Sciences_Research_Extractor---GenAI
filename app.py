import streamlit as st
from google import genai
from dotenv import load_dotenv
import fitz
import os

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Research Insight Extractor",
    page_icon="📄",
    layout="wide"
)

# ---------------------------
# Load Environment Variables
# ---------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("📌 About This App")

st.sidebar.write("""
This application helps you:

✅ Upload research papers  
✅ Generate summaries  
✅ Ask questions about papers  
✅ Extract key insights quickly
""")

st.sidebar.info(
    "Upload a Life Sciences research paper PDF to begin."
)

# ---------------------------
# Main Title
# ---------------------------
st.title("🧜‍♂️ Life Sciences Research Article Insight Extractor")

st.markdown(
    "Upload a research paper and let AI summarize it for you."
)

# ---------------------------
# Upload PDF
# ---------------------------
uploaded_file = st.file_uploader(
    "Upload Research Paper PDF",
    type="pdf"
)

if uploaded_file is not None:

    st.success("👍 PDF uploaded successfully!")

    # Read PDF
    document = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    all_text = ""

    for page_number in range(len(document)):
        page = document[page_number]
        text = page.get_text()
        all_text += text

    # ---------------------------
    # Generate Summary
    # ---------------------------
    if st.button("Generate Summary"):

        with st.spinner("Generating summary... Please wait ⏳"):

            prompt = f"""
            You are a scientific research assistant.

            Summarize the research paper into:

            Background:
            Methods:
            Results:
            Conclusion:

            Explain in simple language.

            Research Paper:
            {all_text}
            """

            try:
                response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            except Exception:
                st.error(
                    "Gemini is currently busy. Please try again in a minute."
                )
                st.stop()

            summary = response.text

        st.success("Summary generated successfully!")

        st.subheader("📚 Research Paper Summary")

        with st.expander("📌 View Summary", expanded=True):
            st.write(summary)

    # ---------------------------
    # Question Answering
    # ---------------------------
    st.subheader("🙋‍♂️ Ask Questions About the Paper")

    user_question = st.text_input(
        "Enter your question"
    )

    if st.button("Ask Question"):

        if user_question.strip() == "":
            st.warning("Please enter a question.")
        else:

            with st.spinner("Thinking... 🤔"):

                question_prompt = f"""
                You are a scientific research assistant.

                Answer ONLY using the research paper.

                If answer is unavailable, say:
                'The paper does not provide this information.'

                Research Paper:
                {all_text}

                User Question:
                {user_question}
                """

                try:
                    response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=question_prompt
    )

                except Exception:
                    st.error(
                        "Gemini is currently busy. Please try again in a minute."
                    )
                    st.stop()

            st.subheader("💡 Answer")
            st.info(response.text)