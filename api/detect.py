# api/detect.py
import base64
from PIL import Image
import torch
import io
import json

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)

def handler(request):
    if request.method != "POST":
        return {"statusCode": 405, "body": "Method Not Allowed"}

    try:
        data = request.body
        image = Image.open(io.BytesIO(data)) 
        results = model(image)
        detections = results.pandas().xyxy[0].to_dict(orient="records")
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(detections)
        }
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
