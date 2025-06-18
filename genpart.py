import os
import re
import json
from pathlib import Path
from typing import List
import google.generativeai as genai # or use OpenAI/GPT if preferred
os.environ["Google_API_KEY"]="your api"
# -- Config --
  # or switch to OpenAI if needed
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Load Gemini model (use 'gemini-pro' or latest)
models = genai.GenerativeModel(model_name="models/gemini-1.5-flash-8b")


def clean_json_output(text: str) -> str:
    # Remove triple quotes or markdown
    text = re.sub(r"```(json)?", "", text)
    text = text.strip("`'\n ")
    return text

# --- Load document ---
def load_document(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# --- Split into sections/topics ---
def split_into_chunks(content: str, max_len=1000) -> List[str]:
    paragraphs = content.split('\n\n')
    chunks, current_chunk = [], ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < max_len:
            current_chunk += para + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# --- Question generation prompt ---
def build_chunk_prompt(text_chunk: str,difficulty: str) -> str:
    return f"""
You are an AI assistant trained to generate high-quality academic questions from study material.Based on {difficulty}.

Your task:
- Read the content provided.
- Generate ONE structured and insightful question based on it.
- Focus on real-world scenarios or practical use-cases where applicable.
- Be concise, context-aware, and avoid repeating textbook definitions.
- The question can be theory-based, code-driven, or scenario-based depending on the context.

Content:
\"\"\"
{text_chunk}
\"\"\"

Return output strictly in raw JSON with the following keys:

{{
  "title": "Short and meaningful title",
  "problem": "Clear problem statement with context (max 100 words)",
  "input_output": "Input/output format if needed, else null",
  "solution_idea": "Brief approach or thought process (optional)",
  "tags": ["Relevant", "Concept", "Keywords"]
}}

❌ Do not wrap the response in markdown/code blocks.
❌ Do not include any explanation or additional text.
"""
DIFFICULTY_GUIDE = {
    "Easy": "Ask straightforward, concept-based or example-driven questions without too much abstraction.",
    "Medium": "Ask questions involving application of concepts, small real-world scenarios, or reasoning.",
    "Hard": "Frame complex problems that involve abstraction, trade-offs, or multi-step reasoning from the topic."
}



def generate_question(text_chunk: str, model,difficulty:str) -> dict:
    prompt = build_chunk_prompt(text_chunk, DIFFICULTY_GUIDE[difficulty])
    try:
        response = model.generate_content(prompt)
        cleaned = re.sub(r"```.*?```|'''|\"\"\"", "", response.text.strip(), flags=re.DOTALL)
        print("🔍 Raw LLM output:\n", response.text)
        cleaned = clean_json_output(response.text)
        parsed = json.loads(cleaned)
        return parsed
    except Exception as e:
        print("❌ Error:", e)
        return {}

# --- Main Pipeline ---
def generate_questions_from_document(path: str):
    # Initialize model
    model = models
    difficulties=["Easy","Medium","Hard"]
    content = load_document(path)
    chunks = split_into_chunks(content)
    questions = []
    for difficulty in difficulties:
        for i, chunk in enumerate(chunks):
            print(f"\n📚 Generating from chunk {i+1}/{len(chunks)}...")
            q = generate_question(chunk, model,difficulty)

            if q:
                questions.append(q["problem"])

    print(f"\n✅ Generated {len(questions)} questions.")
    return questions

# --- Example usage ---
if __name__ == "__main__":
    file_path = "notes/OperatingSystems.txt"  # Your course material
    output = generate_questions_from_document(file_path)

    # Save to JSON
    with open("generated_questions.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
        
    for i,j in enumerate(output):
        
        print(i,":",j)
