
import os
import json
import openai

class OpenAIClient:
    """
    Handles all calls to the OpenAI API for chat, analysis, suggestions, and drafting.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        openai.api_key = self.api_key

    # ---------- Simple chat completion ----------
    def chat_completion(self, messages: list[dict]) -> dict:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message
        except Exception as e:
            # Return a fallback dict so front‑end never crashes
            return {"role": "assistant", "content": f"[OpenAI error] {e}"}

    # ---------- Analyze achievements ----------
    def analyze_achievements(self, messages: list[dict], awardee_info: dict, refresh=False) -> dict:
        prompt = (
            "Analyze the following conversation and extract Coast Guard‑style achievements and impacts. "
            "Return JSON with keys achievements (list) and impacts (list). "
            "Respond ONLY with JSON."
        )
        if refresh:
            prompt += " Provide alternative phrasing."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an assistant that extracts award data."},
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": json.dumps(messages)},
                ],
                temperature=0.3,
            )
            data = json.loads(response.choices[0].message.content)
        except Exception:
            data = {"achievements": [], "impacts": []}

        # ---- Fallback: if empty, copy user lines ----
        if not data.get("achievements"):
            user_lines = [m["content"] for m in messages if m.get("role") == "user"]
            data["achievements"] = user_lines

        return data

    # ---------- Suggest improvement ----------
    def generate_improvement_suggestions(self, award: str, achievement_data: dict, awardee_info: dict) -> list[str]:
        prompt = (
            f"Given award '{award}', achievements {json.dumps(achievement_data)}, and awardee info "
            f"{json.dumps(awardee_info)}, list 3‑5 concrete ways to improve the recommendation."
        )
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You suggest improvements for award packages."},
                          {"role": "user", "content": prompt}],
                temperature=0.6,
            )
            suggestions = json.loads(resp.choices[0].message.content)
            if isinstance(suggestions, list):
                return suggestions
        except Exception:
            pass
        return ["Provide quantifiable impact", "Include scope of responsibility", "Highlight challenges overcome"]

    # ---------- Draft award citation ----------
    def draft_award(self, award: str, achievement_data: dict, awardee_info: dict) -> str:
        prompt = (
            f"Draft a formal Coast Guard {award} citation using achievements {json.dumps(achievement_data)} "
            f"and awardee info {json.dumps(awardee_info)}."
        )
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You draft official Coast Guard award citations."},
                          {"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"[Unable to draft citation] {e}"
