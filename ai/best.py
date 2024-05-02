if __name__ == "__main__":
    from ultralytics import YOLO

    # train15 = yolov8 nano
    # train = yolov8 small
    # train2 = yolov5 nano

    model = YOLO("./runs/detect/train2/weights/best.pt")

    metrics = model.benchmark(
        data="datasets/deneme-5k/data.yaml", device="cuda", batch=-1
    )
