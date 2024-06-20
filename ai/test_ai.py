if __name__ == "__main__":
    from ultralytics import YOLO
    import os

    model = YOLO("runs/detect/colab-first/weights/best.pt")

    keyframes_list = os.listdir("keyframes")

    if not os.path.exists(os.path.join("keyframes", "results")):
        os.mkdir(os.path.join("keyframes", "results"))

    # Run batched inference on a list of images
    # Process results list
    for i, filename in enumerate(keyframes_list):
        abs_path = os.path.join("keyframes", filename)
        result = model(abs_path)[0]

        if i % 100 == 0:
            print(i)

        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        # result.show()  # display to screen
        result.save(
            filename=os.path.join("keyframes", "results", filename)
        )  # save to disk
