import os
import numpy as np
import cv2 as cv

from fastapi import FastAPI, HTTPException, UploadFile

confidence = float(os.environ.get("CONFIDENCE", 0.7))
nms_confidence = float(os.environ.get("NMS_CONFIDENCE", 0.7))

size = (int(os.environ.get("IMG_WIDTH", 608)), int(os.environ.get("IMG_HEIGHT", 608)))
scale = float(os.environ.get("IMG_SCALING", 1/255))

weights_path = os.environ.get("WEIGHTS_PATH", "./yolo/yolov4-tiny.weights")
config_path = os.environ.get("CONFIG_PATH", "./yolo/yolov4-tiny.cfg")
labels_path = os.environ.get("LABELS_PATH", "./yolo/labels")

model = cv.dnn.DetectionModel(cv.dnn.readNet(weights_path, config_path))
model.setInputParams(size=size, scale=scale)

with open(labels_path, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

app = FastAPI()

supported_types = ["image/png", "image/jpeg", "image/webp"]

@app.post('/')
async def detect(file: UploadFile):

    if file.content_type not in supported_types:
        raise HTTPException(
            status_code=400,
            detail=f"Endpoint accepts only: {', '.join(supported_types)}"
        )

    image = cv.imdecode(np.frombuffer(await file.read(), dtype=np.uint8), cv.IMREAD_COLOR)
    classes, scores, boxes = model.detect(image, confidence, nms_confidence)

    return [
        {
            "label": labels[classes[i]],
            "box": np.array(boxes[i]).tolist(),
            "score": float(scores[i])
        } for i in range(len(classes))
    ]
