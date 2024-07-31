if __name__ == "__main__":
    import os
    from ultralytics import YOLO

    model = YOLO("yolov8n.pt")

    path = os.path.join(os.getcwd(), "datasets", "iha", "data.yaml")

    metrics = model.train(data=path, device="cuda", batch=-1)
    #
