from langchain_core.prompts import ChatPromptTemplate

REVIEW_PROMPT = """
You are an expert UI reviewer.

You will be given:
1) A screenshot of a UI
2) HTML code generated from that screenshot

Carefully compare the screenshot and the HTML and FIX ALL differences.

Pay extreme attention to:
- Background colors
- Text colors
- Font sizes
- Spacing, padding, margins
- Layout alignment (rows/columns)
- Missing elements
- Incorrect text
- Overall color theme

Return the FULL corrected HTML.

Do not explain anything.
Return only <html></html> code.
"""

def build_review_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", REVIEW_PROMPT),
        ("human", [
            {"type": "image_url", "image_url": {"url": "{image_url}"}},
            {"type": "text", "text": "Here is the generated HTML:\n\n{html_code}"}
        ])
    ])
