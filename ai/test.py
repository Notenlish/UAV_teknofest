import numpy as np


def find_best_epoch(results_path, categories):
    """
    Finds the best epoch based on specified categories in training results.

    Args:
        results_path (str): Path to the file containing training results (e.g., CSV, dictionary).
        categories (list): List of categories to consider (e.g., ["val/box_loss", "metrics/mAP50(B)"])

    Returns:
        tuple: A tuple containing the epoch number (int) and the corresponding results dictionary (dict).
    """

    # Load results (adapt based on your results format)
    if results_path.endswith(".csv"):
        results = np.genfromtxt(results_path, delimiter=",", skip_header=1, names=True)
    elif isinstance(results_path, dict):
        results = results_path
    else:
        raise ValueError(f"Unsupported results format: {results_path}")

    # Combine loss and metric categories for easier handling
    combined_categories = categories

    # Initialize best epoch and results with worst possible values (assuming minimization)
    best_epoch = None
    best_results = {cat: float("inf") for cat in combined_categories}

    # Iterate through epochs
    for epoch, row in enumerate(results):
        # Check if all categories improve or at least stay the same (assuming minimization)
        if all(row[cat] <= best_results[cat] for cat in combined_categories):
            # Update best epoch and results if conditions are met
            best_epoch = epoch
            best_results = {cat: row[cat] for cat in combined_categories}

    # Handle potential lack of improvement (assuming minimization)
    if best_epoch is None:
        print("Warning: No epoch found that consistently improves all categories.")

    return best_epoch, best_results


# Example usage (assuming results are in a CSV file)
categories = ["       metrics/mAP50(B)", "    metrics/mAP50-95(B)"]
results_path = "runs/detect/train15/results.csv"
best_epoch, best_results = find_best_epoch(results_path, categories)

if best_epoch is not None:
    print(f"Best epoch: {best_epoch + 1} (1-indexed)")
    print("Best results:", best_results)
else:
    print("No clear best epoch found.")
