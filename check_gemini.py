import google.generativeai as genai

genai.configure(api_key="PASTE_YOUR_GEMINI_KEY_HERE")

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)
