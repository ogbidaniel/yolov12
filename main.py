from ultralytics import YOLO

print("Running inference on the specified test image...")

# Fix: Use forward slashes to avoid syntax warnings
model_path = "models/poultry-yolov12n-v1.pt"
model_inference = YOLO(model_path)

# Use forward slashes here too
img_path = "sampleimages/poultry-test-1.jpg"

# Run inference, but do not save the file
results = model_inference(img_path, save=False)

# results is a list, so get the first result
if results:
    # Call the .show() method to display the image in a window
    results[0].show()
    
    print("Inference complete. Press 'q' in the image window to close.")
else:
    print("No results were returned.")