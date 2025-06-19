import google.generativeai as genai
import os
import json
import re
os.environ["Google_API_KEY"]="your-api"




knowledge_base = {
    "Operating Systems - Process Scheduling": [
        "Round Robin is useful for time-sharing systems.",
        "Shortest Remaining Time First minimizes average waiting time but causes starvation.",
        "Multilevel Queue separates processes by priority."
    ],
    "Data Structures - Trees": [
        "AVL trees are height-balanced binary search trees.",
        "Heap data structures are useful for priority queues."
    ]
}





PROMPT_TEMPLATE = """
You are an AI assistant trained to generate high-quality academic questions for Computer Science students.

Your task is to generate **one structured question** for the following:

- Subject: {subject}
- Topic: {topic}
- Difficulty: {difficulty}

Requirements:
- Make the question **engaging**, **real-world-inspired**, or **thought-provoking**, where appropriate.
- It can be **theory-based**, **code-based**, or **case-study-based**, depending on the topic.
- Avoid generic or textbook-style phrasing.
- The question should be creative yet academically sound.
- Do not include explanations or additional commentary outside the JSON.

Return a valid JSON object in this format:

```json
{{
  "title": "Concise and creative title of the question",
  "problem": "Clear and complete problem statement. You may include a scenario or narrative.",
  "input_output": "Describe input/output format if this is a code-based problem, else omit or use null.",
  "solution_idea": "Optional brief hint or outline of the expected solution or key concept tested.",
  "tags": ["SubjectArea", "Topic", "Difficulty", "Style (e.g., Code, Theory, CaseStudy)"]
}}

"""



def build_prompt(user_input):
    context = retrieve_context(user_input["subject"], user_input["topic"])
    joined_context = "\n".join(context)
    
    prompt = PROMPT_TEMPLATE.format(
        subject=user_input["subject"],
        topic=user_input["topic"],
        difficulty=user_input["difficulty"]
    )
    
    return f"{joined_context}\n\n{prompt}"

def clean_and_parse_json(response_text):
    # Remove triple quotes or Markdown-style code blocks
    cleaned = re.sub(r"^```(json)?|```$|'''|\"\"\"", "", response_text.strip(), flags=re.MULTILINE)

    try:
        parsed = json.loads(cleaned)
        return parsed
    except json.JSONDecodeError as e:
        print("❌ JSON decode error:", e)
        print("🔎 Cleaned response was:\n", cleaned)
        return None




def retrieve_context(subject, topic):
    key = f"{subject} - {topic}"
    return knowledge_base.get(key, [])



# Configure Gemini
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Load Gemini model (use 'gemini-pro' or latest)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-8b")

def generate_question(prompt: str) -> str:
     try:
        response = model.generate_content(prompt)
        return response.text.strip()
     except Exception as e:
        print("Error during generation:", e)
        return "Generation failed."


user_input = {
    "subject": "Operating Systems",
    "topic": "Process Scheduling",
    "difficulty": "Medium"
}

# for m in genai.list_models():
#     print(f"{m.name} → {m.supported_generation_methods}")
prompt = build_prompt(user_input)
question_json = generate_question(prompt)
# print("RAW GEMINI OUTPUT:\n", question_json)
parsed = clean_and_parse_json(question_json)

if parsed:
    print("📌 Title:", parsed.get("title"))
    print("📝 Problem:", parsed.get("problem"))
else:
    print("⚠️ Could not parse Gemini output.")
