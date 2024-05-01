from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load an official model

metrics = model.val()  # no arguments needed, dataset and settings remembered