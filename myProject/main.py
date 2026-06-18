import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from pathlib import Path

prompt_path = Path("prompts") / "prompt3.md"

load_dotenv()

client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

with open(prompt_path, "r", encoding="utf-8") as f:
    system_prompt = f.read();

def response(user_text, history):
    messages = [{"role": "system", "content": system_prompt}]

    for turn in history:
        # Gradio 4.x passes dicts: {"role": ..., "content": ...}
        if isinstance(turn, dict):
            messages.append({
                "role": turn.get("role"),
                "content": turn.get("content")
            })
        else:
            # Gradio 3.x passes tuples: (user_msg, assistant_msg)
            if turn[0]: messages.append({"role": "user",      "content": turn[0]})
            if turn[1]: messages.append({"role": "assistant", "content": turn[1]})

    messages.append({"role": "user", "content": user_text})

    result = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return result.choices[0].message.content

# n f"ERROR: {type(e).__name__}: {e}"

gr.ChatInterface(
    fn=response,
    title="CLI Command Generator"
).launch()

