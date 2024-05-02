import csv
import matplotlib.pyplot as plt

# wont run with the environment activated

# Define metrics to consider (adjust based on your needs)
metrics = [
    "           val/box_loss",
    "           val/cls_loss",
    "       metrics/mAP50(B)",
    "    metrics/mAP50-95(B)"
]

# Load CSV data
data = []
with open("runs/detect/train2/results.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

# Find the best epoch based on the average of chosen metrics
best_epoch = 0
best_score = float("inf")  # Initialize with a high value

for i, row in enumerate(data):
    epoch_score = sum(float(row[metric]) for metric in metrics) / len(metrics)
    if epoch_score < best_score:
        best_score = epoch_score
        best_epoch = i

# Plot the chosen metrics vs. epochs
plt.figure(figsize=(10, 6))
for metric in metrics:
    epochs = [int(row["                  epoch"]) for row in data]
    values = [float(row[metric]) for row in data]
    plt.plot(epochs, values, label=metric)

plt.xlabel("Epoch")
plt.ylabel("Metric Value")
plt.title("Model Performance by Epoch")
plt.axvline(x=best_epoch, color="red", linestyle="--", label="Best Epoch")
plt.legend()
plt.grid(True)
plt.show()
