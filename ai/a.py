if __name__ == "__main__":
    from ultralytics import YOLO

    model = YOLO("yolov5n.pt")

    metrics = model.train(data="datasets/deneme-5k/data.yaml", device="cuda", batch=-1)
