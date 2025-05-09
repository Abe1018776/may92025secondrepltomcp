"""
Validation prompt template for filtering documents with GPT-4o.
"""

VALIDATION_PROMPT_TEMPLATE = """
User Question (Hebrew):
\"{user_question}\"

Text Paragraph (Paragraph {paragraph_index}):
Hebrew:
---
{hebrew_text}
---
English:
---
{english_text}
---

Instruction:
Analyze the Text Paragraph. Determine if it contains information that *directly* answers or significantly contributes to answering the User Question.
Respond ONLY with valid JSON: {{\"contains_relevant_info\": boolean, \"justification\": \"Brief Hebrew explanation\"}}.
Output only the JSON object.
""" 