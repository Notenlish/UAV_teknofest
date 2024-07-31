if __name__ == "__main__":
    import os
    from ultralytics import YOLO
    from ultralytics.engine.results import Results
    from PIL import Image, ImageDraw, FontFile

    img_path = r"datasets\iha\test\images\0_jpg.rf.7054faa777eb292e1fdc4df0f8b79d78.jpg"

    model = YOLO("iha.pt")
    results: Results = model.predict(
        img_path,
        device="cuda",
    )

    image = Image.open(img_path).convert("RGB")

    class_names = ["-", "Lying_Person", "Person", "soldier"]

    # Extract bounding boxes and class labels
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs

        draw = ImageDraw.Draw(image)
        for box in boxes:
            bbox = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = bbox
            # print(x1, y2, x2, y2)
            # print(box.data)
            # print(result.names)
            # print(box.id)
            class_id = int(box.cls)
            class_name = class_names[class_id]
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            draw.text(
                (x1, y1),
                class_names[class_id],
                fill="red",
            )
        # image.show(f"{1 + 2**8 % 7 + 3**3}")

    image.save("g.jpg")
    # result.show()  # display to screen
    # result.save(filename="result.jpg")  # save to disk
