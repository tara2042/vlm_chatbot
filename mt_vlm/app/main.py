
import json
from app.video_handler import VideoHandler


def main(path: str ):
    # video_path = "data/traffic_sample.mp4"
    vh = VideoHandler(video_path)
    analysis_results = vh.process()

    with open("mt_vlm/output/summary_output.json", "w") as f:
        json.dump(analysis_results, f, indent = 2)

    for result in analysis_results:
        print(f"{result['timestamp_ms']}ms | {result['label']} ➝ {result['summary']}")


video_path = r"C:\Users\Tarachand yadav\Downloads\eval_dataset\test_sample4.mp4"

if __name__ == "__main__":
    main(video_path)
