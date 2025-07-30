import requests
from typing import List, Dict
from app.prompt import prompt_1, prompt_2, prompt_3

class SceneLabeler:
    """
    Labels the scene based on VLM-generated frame-level descriptions and creates a final summary.
    """
    def __init__(self, llm_model: str = "deepseek-coder:6.7b"):
        self.violation_keywords = ["ran red light", "crossed against", "illegal", "threat", "accident", "theft"]
        self.normal_keywords = ["no issue", "normal", "followed rules"]
        self.llm_model = llm_model
        self.llm_url = "http://localhost:11434/api/generate"

    def label_summary(self, summary: str) -> str:
        summary_lower = summary.lower()
        if any(k in summary_lower for k in self.violation_keywords):
            return "Violation"
        elif any(k in summary_lower for k in self.normal_keywords):
            return "Normal"
        else:
            return "Needs Review"

    def generate_final_summary(self, frame_summaries: List[str]) -> Dict:
        """
        Analyzes multiple frame summaries using an LLM and returns final summary + classification.
        """
        joined_summary = "\n".join(f"- {s}" for s in frame_summaries)

        payload = {
            "model": self.llm_model,
            "prompt": prompt_2,
            "stream": False
        }

        response = requests.post(self.llm_url, json=payload)
        raw_output = response.json().get("response", "").strip()

        # Try to parse JSON from LLM response (may require clean-up in real-world use)
        try:
            import json
            parsed = json.loads(raw_output)
        except Exception:
            parsed = {"summary": raw_output, "observations": [], "classification": "Needs Review"}

        return parsed
