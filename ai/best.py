if __name__ == "__main__":
    from ultralytics import YOLO

    model = YOLO("./runs/detect/train15/weights/best.pt")

    metrics = model.benchmark(
        data="datasets/deneme-5k/data.yaml", device="cuda", batch=-1
    )
