
import cv2
from typing import List, Tuple
import os

class FrameExtractor:
    """
    Extracts and samples frames from a video file.
    """
    def __init__(self, video_path: str, sample_rate: int = 2):
        self.video_path = video_path
        self.sample_rate = sample_rate

    def extract_frames(self) -> Tuple[List, List[float]]:
        cap = cv2.VideoCapture(self.video_path)
        frames, timestamps = [], []
        fps = cap.get(cv2.CAP_PROP_FPS)

        while cap.isOpened():
            frame_id = cap.get(cv2.CAP_PROP_POS_FRAMES)
            ret, frame = cap.read()
            if not ret:
                break
            if int(frame_id) % int(fps // self.sample_rate) == 0:
                frames.append(frame)
                timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))
        cap.release()
        return frames, timestamps

# video_path = r"C:\Users\Tarachand yadav\Downloads\eval_dataset\test_sample4.mp4"
# if __name__ == "__main__":
#     frame_ext = FrameExtractor(video_path)
#     frames, timestamps = frame_ext.extract_frames()
#     print(f"Total frames extracted: {len(frames)}")
#     # Loop over frames to display
#     for i, (frame, ts) in enumerate(zip(frames, timestamps)):
#         cv2.imshow(f"Frame {i} - Timestamp: {ts:.0f} ms", frame)

#         filename = f"frame_{i}_ts_{int(ts)}ms.jpg"
#         filepath = os.path.join("mt_vlm/output", filename)
#         cv2.imwrite(filepath, frame)

#         # Wait for key press or close window (e.g., wait 500ms)
#         key = cv2.waitKey(500)  # or use 0 to wait indefinitely
#         if key == 27:  # ESC to break
#             break
#         cv2.destroyAllWindows()
