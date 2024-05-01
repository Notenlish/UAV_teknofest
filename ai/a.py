
if __name__ == '__main__':
    from ultralytics import YOLO

    model = YOLO('yolov8n.pt')

    metrics = model.train(data="datasets/deneme-5k/data.yaml", device="cuda", batch=16)