
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
import uuid
from app.video_handler import VideoHandler
import uvicorn


app = FastAPI(title="VLM Video Summary API")

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    """
    Endpoint to upload a video and return frame-level + final summary
    """
    # Save uploaded file to disk
    video_id = str(uuid.uuid4())
    video_path = os.path.join(UPLOAD_DIR, f"{video_id}_{file.filename}")

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process video
    try:
        vh = VideoHandler(video_path)
        frame_summaries = vh.process(max_samples=2)  # summarized per-frame

        # summaries = [f["summary"] for f in frame_summaries]
        # final_result = vh.labeler.generate_final_summary(summaries)

        # return JSONResponse(content={
        #     "frame_summaries": frame_summaries,
        #     "final_summary": final_result
        # })
        return frame_summaries
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.app_fastapi:app", host="127.0.0.1", port=8000, reload=True)
