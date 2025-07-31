import json
from app.video_handler import VideoHandler


def main(path: str):
    vh = VideoHandler(path)
    analysis_results = vh.process(max_samples=2) # Change this sample size numbers or no. of frames to send to vlm for summary. Processing all frames would be time consuming

    # Save full output to file
    with open("mt_vlm/output/summary_output.json", "w") as f:
        json.dump(analysis_results, f, indent=2)

    print("\nFinal Summary:\n", analysis_results)
    

video_path = r"C:\Users\Tarachand yadav\Downloads\eval_dataset\test_sample2.mp4"
if __name__ == "__main__":
    main(video_path)
