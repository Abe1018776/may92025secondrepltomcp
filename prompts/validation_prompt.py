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
Your job is to help me back up my dvar torah ideas that i come up with and back it up with sources that can support the concept or concepts that im basing my dvar torah on 

You have to carefully evaluate each dvar torah to see if and how it can help back up the dvar torah of mine and how , you have to use some creativity and reasoning in order to get to that.

Analyze the Text Paragraph. Determine if it contains information that *directly* answers or significantly contributes to answering the User Question.
Respond ONLY with valid JSON: {{\"contains_relevant_info\": boolean, \"justification\": \"Brief Hebrew explanation\"}}.
Output only the JSON object.
""" 