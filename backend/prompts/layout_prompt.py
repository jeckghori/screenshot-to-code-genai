from langchain_core.prompts import ChatPromptTemplate

LAYOUT_PROMPT = """
You are an expert UI analyst.

Look at this screenshot and describe the UI layout in detail.

Describe:
- Sections (header, sidebar, cards, tables, etc.)
- Layout structure (rows, columns, grids)
- Spacing and alignment
- Color theme
- Font sizes and styles
- Important UI elements

This description will be used to generate accurate HTML.
"""

def build_layout_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", LAYOUT_PROMPT),
        ("human", [
            {"type": "image_url", "image_url": {"url": "{image_url}"}},
            {"type": "text", "text": "Describe this UI layout in detail."}
        ])
    ])
