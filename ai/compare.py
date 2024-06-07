import csv

import matplotlib.pyplot as plt
import numpy as np

models = {
    "yolov8n": "train15",
    "yolov8s": "train",
    "yolov5n": "train2",
}

metrics = [
    "           val/box_loss",
    "           val/cls_loss",
    "       metrics/mAP50(B)",
    "    metrics/mAP50-95(B)",
]

colors = {
    "           val/box_loss",
    "           val/cls_loss",
    "       metrics/mAP50(B)",
    "    metrics/mAP50-95(B)",
}

results = {key: {"name": val} for key, val in models.items()}


fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)

model_num = 0
for key, val in results.items():
    # load data
    data = []
    path = f"runs/detect/{val['name']}/results.csv"
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    val["data"] = data

    # Find the best epoch based on the average of chosen metrics
    best_epoch = 0
    best_score = float("inf")  # Initialize with a high value

    for i, row in enumerate(data):
        epoch_score = sum(float(row[metric]) for metric in metrics) / len(metrics)
        if epoch_score < best_score:
            best_score = epoch_score
            best_epoch = i
    val["best_epoch"] = best_epoch

    # Plot the chosen metrics vs. epochs
    for metric_id, metric in enumerate(metrics):
        metric = metrics[metric_id]
        x = [model_num + 1]
        y = [data[best_epoch][metric]]
        if metric_id == 0:
            ax1.set_title(metric)
            ax1.scatter(x, y, 300, label=key)

        if metric_id == 1:
            ax2.set_title(metric)
            ax2.scatter(x, y, 300, label=key)
        if metric_id == 2:
            ax3.set_title(metric)
            ax3.scatter(x, y, 300, label=key)
        if metric_id == 3:
            ax4.set_title(metric)
            ax4.scatter(x, y, 300, label=key)

    model_num += 1
handles, labels = fig.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
fig.legend(by_label.values(), by_label.keys())

plt.subplots_adjust(
    left=0.1, bottom=0.1, right=0.85, top=0.85, wspace=0.4, hspace=0.4
)

ax1.set_ylim(-1, 7)
ax2.set_ylim(-1, 7)
ax3.set_ylim(-1, 7)
ax4.set_ylim(-1, 7)

ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
ax4.grid(True)

plt.show()
