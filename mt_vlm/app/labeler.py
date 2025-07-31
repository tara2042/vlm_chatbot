import requests
from typing import List, Dict
from app.prompt import prompt_1, prompt_2, prompt_3, prompt_4

# deepseek-coder:6.7b
class SceneLabeler:
    """
    Labels the scene based on VLM-generated frame-level descriptions and creates a final summary.
    """
    def __init__(self, llm_model: str = "llama3"):
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

    def generate_final_summary(self, frame_summaries: List[str]) -> str:
        """
        Analyzes multiple frame summaries using an LLM and returns final summary + classification.
        """
        # print('Input list - ', frame_summaries, '\n\n')
        joined_summary = "\n".join(f"- {s}" for s in frame_summaries)
        # print('\n\njoined output - ', joined_summary)

        payload = {
            "model": self.llm_model,
            "prompt": prompt_4.format(joined_summaries = joined_summary),
            "stream": False
        }

        response = requests.post(self.llm_url, json=payload)
        # print('\n')
        # print(f'Response from LLM - {self.llm_model} \n', response)
        raw_output = response.json().get("response", "").strip()
        # print('\n')
        # print('final summary from the llm\n', raw_output)

        return raw_output

# sum_list =  [' The image shows a man and woman walking down a street, passing by an unpaved road with a small patch of grass on its side. They appear to be in an urban area, as there is a building visible in the background. There are no traffic signals or signs, and no vehicles or pedestrians are visible nearby. The scene appears normal and safe, following any traffic or public safety rules that might apply in this setting. ', " The image shows an outdoor scene at what appears to be a residential area with dirt pathways and a roadway. There are two individuals walking on a narrow dirt road; one of them is carrying a handbag. They seem to be in casual attire, possibly engaged in daily activities or errands. The surroundings include small structures that could be part of a temporary settlement or informal housing. There are no visible traffic signals or signs, and the roadway does not appear to be a designated route for vehicles. Traffic rules do not seem to be followed strictly as there are vehicles parked or on the roadway. While there is no immediate evidence of any unusual, dangerous, or suspicious activity, the scene may suggest some level of informality in urban planning and infrastructure maintenance, which could impact safety and public order. However, without more context or information about local customs and practices, it's difficult to make definitive conclusions about the overall safety or compliance with rules in this specific location. ", ' The image is a still from a video, showing a person standing in the middle of a rural street with vehicles and people in the background. The individual appears to be in a normal posture, and there are no visible signs of violation or danger. ']
# if __name__ == "__main__":
#     summary = SceneLabeler()
#     final_sum = summary.generate_final_summary(sum_list)
#     print(final_sum)