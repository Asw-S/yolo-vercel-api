# api/detect.py
import base64
from PIL import Image
import torch
import io
import json
import sys

# Load YOLOv5s model from ultralytics
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)

def main():
    try:
        if len(sys.argv) < 2:
            print(json.dumps({"error": "No input data"}))
            return

        # Load JSON input passed via command-line
        input_data = json.loads(sys.argv[1])
        
        # Check if 'image_base64' is present
        if 'image_base64' not in input_data:
            print(json.dumps({"error": "Missing 'image_base64' in input"}))
            return

        # Decode base64 image
        image_data = base64.b64decode(input_data['image_base64'])
        image = Image.open(io.BytesIO(image_data))

        # Perform YOLOv5 inference
        results = model(image)
        detections = results.pandas().xyxy[0].to_dict(orient="records")

        # Output JSON result
        print(json.dumps(detections))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == '__main__':
    main()
