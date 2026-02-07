from langchain_core.prompts import ChatPromptTemplate
from prompts.imported_code_prompts import IMPORTED_CODE_SYSTEM_PROMPTS
from prompts.screenshot_system_prompts import SYSTEM_PROMPTS
from prompts.text_prompts import SYSTEM_PROMPTS as TEXT_SYSTEM_PROMPTS
from prompts.types import Stack


USER_PROMPT = """
Generate code for a web page that looks exactly like the provided screenshot(s).
If multiple screenshots are provided, organize them meaningfully. If they appear to be
different pages in a website, make them distinct pages and link them. If they look like
different tabs or views in an app, connect them with appropriate navigation. If they
appear unrelated, create a scaffold that separates them into "Screenshot 1", "Screenshot 2",
"Screenshot 3", etc. so it is easy to navigate.
For mobile screenshots, do not include the device frame or browser chrome; focus only on
the actual UI mockups.
"""

SVG_USER_PROMPT = """
Generate code for a SVG that looks exactly like the provided screenshot(s).
"""


# ✅ Screenshot → Code Prompt
def build_screenshot_prompt(stack: Stack) -> ChatPromptTemplate:
    system_content = SYSTEM_PROMPTS[stack]
    user_prompt = USER_PROMPT if stack != "svg" else SVG_USER_PROMPT

    return ChatPromptTemplate.from_messages([
        ("system", system_content),
        ("human", [
            {"type": "image_url", "image_url": {"url": "{image_url}"}},
            {"type": "text", "text": user_prompt + "\n\nAdditional instructions: {extra_instructions}"}
        ])
    ])


# ✅ Existing Code → Edit Prompt
def build_imported_code_prompt(stack: Stack) -> ChatPromptTemplate:
    system_content = IMPORTED_CODE_SYSTEM_PROMPTS[stack]

    return ChatPromptTemplate.from_messages([
        ("system", system_content),
        ("human", "Here is the code:\n\n{code}")
    ])


# ✅ Text → UI Prompt (no image)
def build_text_prompt(stack: Stack) -> ChatPromptTemplate:
    system_content = TEXT_SYSTEM_PROMPTS[stack]

    return ChatPromptTemplate.from_messages([
        ("system", system_content),
        ("human", "Generate UI for: {text_prompt}")
    ])
