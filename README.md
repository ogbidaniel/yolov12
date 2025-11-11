# Poultry Vision Project

This repository contains a YOLOv12-based model for detecting and tracking poultry in a cage-free environment. The model is trained to identify hens, feeders, and waterers to support automated monitoring.

The ultimate goal of this research is to implement automated detection of key behavioral phenotypes, such as feeding and drinking, to assess animal welfare and thermotolerance, as outlined in the [accompanying research paper](https://www.mdpi.com/2624-7402/6/3/155).

## Model: `poultry-yolo12n-v1`

The current model is a YOLOv12n variant trained on a custom dataset of poultry images.

### Training Results
Here are the key performance metrics from the `poultry_yolo12n_run1` training run:

| Overall Results | Confusion Matrix |
| :---: | :---: |
| ![Training Results](assets/training_results/results.png) | ![Confusion Matrix](assets/training_results/confusion_matrix.png) |

| PR Curve | Validation Prediction |
| :---: | :---: |
| ![PR Curve](assets/training_results/PR_curve.png) | ![Validation Prediction](assets/training_results/val_batch0_pred.jpg) |

---

## Setup & Installation

This project is built on a forked version of YOLOv12. To set up the environment, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/ogbidaniel/yolov12.git](https://github.com/ogbidaniel/yolov12.git)
    cd yolov12
    ```

2.  **Create Conda Environment:**
    ```bash
    # Create a new environment
    conda create --name poultry-vision python=3.12

    # Activate the environment
    conda activate poultry-vision
    ```

3.  **Install Dependencies:**
    ```bash
    # 1. Install all required packages
    pip install -r requirements.txt

    # 2. Install this local ultralytics fork in editable mode
    pip install -e .
    ```

---

## How to Run Inference

You can run inference on a sample image using `main.py`. The model file (`poultry-yolo12n-v1.pt`) is expected to be in the `models/` directory (which is ignored by Git).

1.  Place your trained `.pt` file in a `models/` folder.
2.  Run the script:

    ```bash
    python main.py
    ```
3.  Results will be saved in the `runs/detect/predict` folder.