
from app.frame_extractor import FrameExtractor
from app.image_analyzer import VLMAnalyzer
from app.labeler import SceneLabeler
from app.prompt import prompt_1

class VideoHandler:
    """
    Coordinates the full video analysis pipeline.
    """
    def __init__(self, video_path: str, prompt: str = prompt_1):
        self.extractor = FrameExtractor(video_path)
        self.analyzer = VLMAnalyzer()
        self.labeler = SceneLabeler()
        # self.analysis_prompt = "Describe any traffic events, rule adherence, or violations in this frame."
        self.analysis_prompt = prompt

    # def process_(self):
    #     """
    #     Returns final summary of entire video clip
    #     """
    #     frames, timestamps = self.extractor.extract_frames()
    #     print(f'total frames  - {len(frames)}')
    #     output = []

    #     cnt = 1
    #     for frame, ts in zip(frames, timestamps):
            
    #         if cnt%5 == 0:    
    #             print(f'processing frame {cnt}/{len(frames)}')
    #             summary = self.analyzer.analyze_image(frame, self.analysis_prompt)
    #             label = self.labeler.label_summary(summary)
    #             output.append({
    #                 "timestamp_ms": ts,
    #                 "summary": summary,
    #                 "label": label
    #             })

    #         cnt += 1
            
    #     return output
    
    # function to process sample frames and generate text from the image
    def process(self, max_samples: int = 3):
        """
        Returns a summary for a few representative frames from the video.
        
        Args:
            max_samples (int): Number of frames to sample and process with VLM.
        """
        frames, timestamps = self.extractor.extract_frames()
        total = len(frames)
        print(f'[INFO] Total frames extracted: {total}')

        if total == 0:
            return []

        # Sample evenly spaced frame indices
        indices = list(range(0, total, max(1, total // max_samples)))[:max_samples]

        output = []

        for i in indices:
            frame, ts = frames[i], timestamps[i]
            print(f'[INFO] Processing sampled frame {i+1}/{total} (Index: {i})')
            summary = self.analyzer.analyze_image(frame, self.analysis_prompt)
            label = self.labeler.label_summary(summary)
            output.append({
                "frame_index": i,
                "timestamp_ms": ts,
                "summary": summary,
                "label": label
            })
        summaries = [entry["summary"] for entry in output]
        print(f"All summaries:\n", "\n".join(summaries))

        # print(f'All the summary from sample frames {output['summary']}')
        parsed_summary = self.labeler.generate_final_summary(summaries)

        return parsed_summary


# video_path = r"C:\Users\Tarachand yadav\Downloads\eval_dataset\test_sample4.mp4"
# if __name__ == "__main__":
#     vh = VideoHandler(video_path, prompt=prompt_1)
#     result = vh.process()
#     print(result)
