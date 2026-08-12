import os
import random
import requests
import warnings
from django.conf import settings

try:
    from urllib3.exceptions import NotOpenSSLWarning
    warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
except ImportError:
    pass

class AIEngineService:
    @classmethod
    def call_gemma(cls, prompt: str, system_prompt: str = "You are PlacePrep AI's expert Aptitude & Campus Placement Mentor.") -> str:
        """
        Sends a request to OpenRouter using free models (Gemma / Llama / Mistral / DeepSeek / Gemini).
        Automatically tries fallback free models if primary is busy or rate-limited.
        """
        api_key = getattr(settings, "OPENROUTER_API_KEY", "").strip()
        primary_model = getattr(settings, "OPENROUTER_MODEL", "openrouter/free").strip()
        base_url = getattr(settings, "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions").strip()

        if not api_key or api_key == "your_openrouter_api_key_here":
            print("OpenRouter Warning: API key is missing or set to placeholder.")
            return None

        # Free models to attempt in order of preference
        models_to_try = [
            primary_model,
            "openrouter/free",
            "google/gemini-2.0-flash-lite-001:free",
            "meta-llama/llama-3.2-3b-instruct:free",
            "qwen/qwen-2.5-coder-32b-instruct:free",
            "deepseek/deepseek-r1:free",
            "mistralai/mistral-small-24b-instruct-2501:free",
            "google/gemma-2-9b-it:free",
        ]
        
        # Deduplicate while preserving order
        seen = set()
        models = [m for m in models_to_try if not (m in seen or seen.add(m))]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost:8001",
            "X-Title": "PlacePrep AI",
            "Content-Type": "application/json"
        }

        last_error = ""
        for model in models:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }

            try:
                response = requests.post(base_url, headers=headers, json=payload, timeout=15)
                print(f"[OpenRouter Debug] Model: {model} | Status: {response.status_code} | Text: {response.text[:200]}")
                if response.status_code == 200:
                    data = response.json()
                    if "choices" in data and len(data["choices"]) > 0:
                        content = data["choices"][0]["message"]["content"]
                        if content and content.strip():
                            return content.strip()
                else:
                    last_error = f"API Error ({response.status_code}): {response.text[:150]}"
            except Exception as e:
                last_error = f"Connection Error: {str(e)}"
                print(f"[OpenRouter Exception]: {e}")

        if last_error:
            return f"⚠️ {last_error}"
        return None

    @classmethod
    def generate_personalized_insights(cls, weak_topics, strong_topics, user_level, streak):
        """
        Generates personalized study insights using OpenRouter Gemma LLM.
        Falls back to rule-based insights if LLM key is absent or unreachable.
        """
        weak_names = [m.topic.name for m in weak_topics] if weak_topics else []
        strong_names = [m.topic.name for m in strong_topics] if strong_topics else []

        if weak_names or strong_names:
            prompt = (
                f"Analyze performance for a student at Level {user_level} with a {streak}-day streak.\n"
                f"Strong Topics: {', '.join(strong_names) if strong_names else 'None registered yet'}\n"
                f"Weak Topics: {', '.join(weak_names) if weak_names else 'None registered yet'}\n\n"
                f"Provide a 3-sentence motivating, highly actionable study plan focusing on improving weak areas "
                f"and cracking campus placement aptitude exams (like TCS NQT, Infosys, Wipro)."
            )
            ai_response = cls.call_gemma(prompt)
            if ai_response:
                return ai_response

        # Fallback rule-based system
        if not weak_topics and not strong_topics:
            return "Hey there! I'm your AI Study Assistant powered by Gemma. Take your first practice test so I can analyze your aptitude strengths!"

        greeting = random.choice([
            "Here is your personalized analysis:",
            "I've analyzed your recent performance.",
            "AI Study Insight:",
            "Based on your aptitude data, here's what I recommend:"
        ])

        insight_parts = [greeting]

        if strong_topics:
            strong_text = " and ".join(strong_names[:2])
            insight_parts.append(f"You're doing fantastic in {strong_text}! Keep up the great work.")

        if weak_topics:
            weak_text = " and ".join(weak_names[:2])
            insight_parts.append(f"I noticed you're struggling a bit with {weak_text}. I recommend spending 30 minutes today practicing these specific topics.")
        else:
            insight_parts.append("You don't have any major weak areas right now. You're well-rounded!")

        if streak >= 3:
            insight_parts.append(f"Also, incredible job maintaining a {streak}-day streak! Consistency is key.")

        return " ".join(insight_parts)

    @classmethod
    def generate_aptitude_shortcut(cls, question_text: str, options: dict, correct_option: str) -> str:
        """
        Generates 10-second mental math shortcuts for any aptitude question.
        """
        prompt = (
            f"Question: {question_text}\n"
            f"Options: {options}\n"
            f"Correct Answer Key: {correct_option}\n\n"
            f"Explain:\n"
            f"1. ⚡ 10-Second Mental Math / Vedic Math Shortcut\n"
            f"2. 🎯 Option Elimination Trick (how to spot wrong options instantly)\n"
            f"Keep it concise, clear, and easy to understand for competitive aptitude exams."
        )
        ai_response = cls.call_gemma(prompt)
        if ai_response:
            return ai_response
        return "10-Second Shortcut: Look for divisibility rules or unit digit patterns to eliminate incorrect options quickly!"

    @classmethod
    def generate_socratic_hint(cls, question_text: str, options_str: str) -> str:
        """
        Generates a progressive Socratic hint without revealing the final answer option.
        """
        prompt = (
            f"The student is stuck on this aptitude question:\n"
            f"\"{question_text}\"\n"
            f"Options: {options_str}\n\n"
            f"Provide a helpful 2-sentence Socratic hint that guides the student on which formula, rule, or concept "
            f"to use (e.g. Unit Digit, LCM, Speed Conversion, Syllogism rule), WITHOUT revealing the final answer choice."
        )
        ai_response = cls.call_gemma(prompt)
        if ai_response:
            return ai_response
        return "💡 Hint: Identify the core mathematical pattern or formula. Pay close attention to units or given conditions!"

    @classmethod
    def answer_question_doubt(cls, question_text: str, options_str: str, explanation: str, user_query: str) -> str:
        """
        Answers student doubts and detailed follow-up questions about a specific problem.
        """
        prompt = (
            f"Aptitude Question: \"{question_text}\"\n"
            f"Options: {options_str}\n"
            f"Standard Solution: {explanation}\n\n"
            f"Student Question: \"{user_query}\"\n\n"
            f"Answer the student's question clearly, encouragingly, and concisely in simple terms."
        )
        ai_response = cls.call_gemma(prompt)
        if ai_response:
            return ai_response
        return "Thanks for asking! Check the core formula and verify each step carefully."


