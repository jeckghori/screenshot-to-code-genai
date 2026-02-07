import streamlit as st
import base64
import os
import sys

backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from backend.codegen.utils import extract_html_content
from backend.prompts.prompt_builder import build_screenshot_prompt
from backend.prompts.review_prompt import build_review_prompt
from backend.prompts.layout_prompt import build_layout_prompt
from prompts.types import Stack
from prompts.imported_code_prompts import IMPORTED_CODE_SYSTEM_PROMPTS

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


# ---------- Helpers ----------

def image_to_data_url(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    base64_str = base64.b64encode(bytes_data).decode("utf-8")
    mime_type = uploaded_file.type
    return f"data:{mime_type};base64,{base64_str}"


def get_llm(provider, api_key, model_name):
    if provider == "openai":
        return ChatOpenAI(api_key=api_key, model=model_name, temperature=0)
    elif provider == "anthropic":
        return ChatAnthropic(api_key=api_key, model=model_name, temperature=0)
    else:
        return ChatGoogleGenerativeAI(api_key=api_key, model=model_name, temperature=0)


# ---------- UI ----------

st.set_page_config(layout="wide")
st.title("📸 Screenshot → Code (Self Correcting + Safe Edit)")

with st.sidebar:
    provider = st.radio("Provider", ["openai", "anthropic", "gemini"])

    if provider == "openai":
        api_key = st.text_input("OpenAI API Key", type="password")
        model_name = st.text_input("OpenAI Model", value="gpt-4o")
    elif provider == "anthropic":
        api_key = st.text_input("Anthropic API Key", type="password")
        model_name = st.text_input("Anthropic Model", value="claude-3-5-sonnet")
    else:
        api_key = st.text_input("Google Gemini API Key", type="password")
        model_name = st.text_input("Gemini Model", value="gemini-1.5-flash")

    stack: Stack = st.selectbox(
        "Stack",
        ["html_tailwind", "react_tailwind", "bootstrap", "html_css", "ionic_tailwind", "vue_tailwind", "svg"],
    )

uploaded_file = st.file_uploader("Upload Screenshot", type=["png", "jpg", "jpeg"])
edit_text = st.text_input("✏️ Edit this UI safely (optional)", "")


# ---------- Generation Pipeline ----------

if uploaded_file and api_key:
    data_url = image_to_data_url(uploaded_file)

    llm = get_llm(provider, api_key, model_name)
    parser = StrOutputParser()

    # -------- Step 0: Layout reasoning --------
    with st.spinner("Analyzing layout from screenshot..."):
        layout_chain = build_layout_prompt() | llm | parser
        layout_description = layout_chain.invoke({"image_url": data_url})

    # -------- Step 1: Initial generation --------
    with st.spinner("Generating initial HTML..."):
        gen_chain = build_screenshot_prompt(stack) | llm | parser
        html = gen_chain.invoke({
            "image_url": data_url,
            "extra_instructions": layout_description
        })

    first_pass = html

    # -------- Step 2: Review loop (2 passes) --------
    review_chain = build_review_prompt() | llm | parser

    for i in range(2):
        with st.spinner(f"AI reviewing & fixing pass {i+1}..."):
            html = review_chain.invoke({
                "image_url": data_url,
                "html_code": html
            })

    final_pass = html

    # -------- Step 3: SAFE Edit Mode --------
    if edit_text.strip():
        with st.spinner("Applying safe edit..."):

            system_prompt = IMPORTED_CODE_SYSTEM_PROMPTS[stack]

            edit_prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", f"""
You previously built this HTML:

{final_pass}

User wants this change:
{edit_text}

Modify ONLY what is required.
Do not change layout, spacing, colors, or structure unless necessary.
Return full updated HTML.
""")
            ])

            edit_chain = edit_prompt | llm | parser
            final_pass = edit_chain.invoke({})

    clean_html = extract_html_content(final_pass)

    # -------- UI Output --------
    st.subheader("🔍 Pass Comparison")
    view = st.radio("View", ["First Pass", "Final Pass"])

    if view == "First Pass":
        st.code(first_pass, language="html")
    else:
        st.code(clean_html, language="html")

    st.subheader("🌐 Live Preview")
    st.components.v1.html(clean_html, height=650, scrolling=True)

    st.download_button("⬇️ Download HTML", clean_html, "index.html")
