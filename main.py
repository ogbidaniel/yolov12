from ultralytics import YOLO

print("Running inference on the specified test image...")

# model path
model_path = "models/poultry-yolov12n-v1.pt"
model_inference = YOLO(model_path)

# image path
img_path = "sampleimages/poultry-test-1.jpg"

# Run inference
results = model_inference(img_path, save=False)


if results:
    # Call the .show() method to display the image in a window
    results[0].show()
    
    print("Inference complete. Press 'q' in the image window to close.")
else:
    print("No results were returned.")