# vlm_chatbot
Video clip and image analysis uising vision language model (VLM). Takes video clips and converts into frames and summary on each frame is generated (image to text using LLAVA VLM). Finally, a single summary is output with classification/tag such as "normal", "violation", etc.



# 🧠 Multimodal Video Understanding using LLaVA (Ollama)

This project is a **vision-language pipeline** for analyzing video clips frame-by-frame using the **LLaVA VLM (Vision Language Model)**. The system extracts frames from a video, summarizes each frame using the VLM, and sends those summaries to a second **language model** to generate a **final summary with labels** like `"Violation"`, `"Normal"`, or `"Threat"`.

---

## 🚀 Features

- 🎞️ Video frame sampling using OpenCV
- 🤖 Vision-to-text using **LLaVA model from Ollama**
- 🧠 LLM-based summary synthesis across multiple frames
- ✅ Scene classification (e.g., Violation, Normal, Threat, Needs Review)
- ⚡ Efficient sampling (only a few representative frames processed)
- 🧩 Modular design using clean Python classes and functions

---

## 📂 Project Structure

```bash
multimodal_chat_assistant/
│
├── app/
│   ├── main.py                   # Entrypoint
│   ├── video_handler.py          # Coordinates frame extraction, VLM calls, aggregation
│   ├── frame_extractor.py        # Extracts sample frames from video
│   ├── image_analyzer.py         # LLaVA-based vision-to-text summarizer
│   ├── labeler.py                # Labels + final LLM summary
│   ├── prompt.py                 # Reusable prompt strings
│   └── config.py                 # Settings and model configuration
│
├── output/
│   └── summary_output.json       # Output summaries and labels
└── README.md
```

---

## ⚙️ Setup Instructions

1. **Install Python dependencies**
```bash
pip install opencv-python requests
```

2. **Start Ollama with LLaVA model**
```bash
ollama run llava
ollama run llama3
```

> (Optional for summary step): Load another text-only model like `llama3`
```bash
ollama run llama3
```

3. **Run the pipeline**
```bash
python app/video_handler.py
```

---

## 🧱 Key Components

### 🔹 FrameExtractor (`frame_extractor.py`)
Extracts evenly spaced sample frames from a video.


### 🔹 VLMAnalyzer (`image_analyzer.py`)
Encodes each image and sends it to the LLaVA model via Ollama.


### 🔹 SceneLabeler (`labeler.py`)
Labels each frame's summary and combines all summaries to produce a final scene-level report.


### 🔹 VideoHandler (`video_handler.py`)
Core orchestrator: extracts frames → summarizes → labels → final summary.

### 🧠 Final Scene-Level Summary

```
**Classification:** Normal

The classification is "Normal" as there are no indications of rule violations, potential risks, or needs for review in the provided frame-level image summaries.
Based on the frame-level image summaries, I will synthesize the information and provide a brief summary capturing the key events or common themes.     

**Summary:** The video appears to show everyday scenes of people engaging in ordinary activities in residential areas. The images depict walking, possibly with pedestrian crossing concerns, and individuals performing tasks near roadways without any immediate signs of rule violations, threats, disputes, or thefts. The overall environment seems normal and safe.

**Classification:** Normal

The classification is "Normal" as there are no indications of rule violations, potential risks, or needs for review in the provided frame-level image summaries.

```