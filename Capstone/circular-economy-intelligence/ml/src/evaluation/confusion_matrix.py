import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

def save_confusion_matrix(y_true, y_pred, labels, path):
    fig, ax = plt.subplots(figsize=(10, 8))
    ConfusionMatrixDisplay.from_predictions(y_true, y_pred, display_labels=labels, xticks_rotation=45, ax=ax)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
