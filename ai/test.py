
from ultralytics.utils.benchmarks import benchmark
from ultralytics import YOLO

# Benchmark on GPU
benchmark(model='yolov8n.pt', data='coco128.yaml', imgsz=640, half=False, device="cuda")