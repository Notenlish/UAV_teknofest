import json

with open("datasets/coco_custom/annotations/instances_val2017.json", "r") as f:
    data = json.load(f)
    # images, annotations, categories
    print(data["images"][0])
    print(data["categories"][0])
    print(data["annotations"][0])

    # format for ultralytics: class x_center y_center width height
    # xywh format(0-1)
    # divide width and xcenter by img width
    # divide height and ycenter by img height

    images_r = {}
    for img in data["images"]:
        images_r[img["id"]] = {
            "file_name": img["file_name"],
            "width": img["width"],
            "height": img["height"],
        }

    for annotation in data["annotations"]:
        img_id = annotation["image_id"]
        left, top, boxwidth, boxheight = annotation["bbox"]
        category_id = annotation["category_id"]

        if category_id > 79:
            continue

        xcenter = left + (boxwidth / 2)
        ycenter = top + (boxheight / 2)

        image_r = images_r[img_id]
        xcenter /= image_r["width"]
        boxwidth /= image_r["width"]
        ycenter /= image_r["height"]
        boxheight /= image_r["height"]

        file_name: str = image_r["file_name"]
        file_name = file_name.replace(".jpg", ".txt")
        msg = f"{category_id} {xcenter} {ycenter} {boxwidth} {boxheight}\n"
        FILE = f"datasets/coco_custom/labels/val/{file_name}"
        try:
            with open(FILE, "a") as f:
                f.write(msg)
        except FileNotFoundError:
            with open(FILE, "w") as f:
                f.write(msg)

    # for category in data["categories"]:
    #    print(f"{category['id']}: {category['name']}")
