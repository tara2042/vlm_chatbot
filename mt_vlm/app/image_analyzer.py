# app/image_analyzer.py

import base64
import requests
import cv2
import os
from app.prompt import prompt_1  # Make sure prompt_1 is defined in app/prompt.py

class VLMAnalyzer:
    """
    Uses Ollama Vision-Language Models to analyze image frames.
    """
    def __init__(self, model: str = "llava"):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def encode_image(self, image) -> str:
        """
        Encodes a NumPy image array to base64 string.
        """
        if image is None or not hasattr(image, 'shape'):
            raise ValueError("Invalid image format. Expecting a NumPy array.")
        _, buffer = cv2.imencode(".jpg", image)
        return base64.b64encode(buffer).decode()

    def analyze_image(self, image, prompt: str) -> str:
        """
        Sends an image and prompt to the VLM (Ollama) and gets a response.
        """
        image_b64 = self.encode_image(image)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [image_b64],
            # "temperature": 0.0,  # Lower temperature reduces hallucination
            # "top_p": 0.9,
            # "max_tokens": 512,
            "stream": False
        }
        response = requests.post(self.api_url, json=payload)
        return response.json().get("response", "")

# # Checking if the class and functions work perfect
# sample_image_path = "mt_vlm/output/frame_12_ts_5550ms.jpg"
# model = "llava"
# if __name__ == "__main__":
#     # Sample image path
#     if not os.path.exists(sample_image_path):
#         raise FileNotFoundError(f"Image not found: {sample_image_path}")

#     # Read the image as a NumPy array
#     image = cv2.imread(sample_image_path)
#     if image is None:
#         raise ValueError("Image could not be loaded. Check the path and file format.")

#     # Initialize and analyze
#     analyzer = VLMAnalyzer(model= model)
#     result = analyzer.analyze_image(image, prompt=prompt_1)
#     print("\n---------------VLM Observations made in the sample image-------------\n", result)
