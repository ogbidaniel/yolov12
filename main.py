from ultralytics import YOLO
print("Running inference on the specified test image...")

# Use forward slashes to avoid syntax warnings
model_path = "models/poultry-yolo12n-v1.pt"
model_inference = YOLO(model_path)

# Use forward slashes here too
img_path = "data/sampleimages/poultry-test-1.jpg"

# Run inference
results = model_inference(img_path, save=True)

print("Inference complete. Results saved.")