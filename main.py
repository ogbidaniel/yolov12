# main.py
from ultralytics import YOLO
import cv2
from behavior_monitor import HenBehaviorMonitor

# --- CONFIGURATION ---
MODEL_PATH = "models/poultry-yolov12n-v1.pt"
VIDEO_PATH = "samplevideos/poultry-vid-01.mp4"

# Class Map
CLASS_MAP = {
    0: 'feeder',   
    1: 'hen',   
    2: 'waterer'   
}

# Visualization Colors (BGR Format)
COLOR_HEN_IDLE = (0, 255, 0)      # Green
COLOR_FEEDER = (0, 140, 255)      # Orange
COLOR_WATERER = (235, 206, 135)     # Sky Blue
COLOR_TEXT_BG = (0, 0, 0)         # Black background for text
COLOR_TEXT = (255, 255, 255)      # White text
# ---------------------

def main():
    print(f"Loading model from {MODEL_PATH}...")
    model = YOLO(MODEL_PATH)

    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0: fps = 30.0
    
    monitor = HenBehaviorMonitor(fps=fps)

    print(f"Starting inference on {VIDEO_PATH} at {fps:.1f} FPS...")
    print("Press 'q' in the window to stop.")

    cv2.namedWindow("Poultry Vision System", cv2.WINDOW_AUTOSIZE)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Run Tracking
        results = model.track(frame, persist=True, verbose=False)
        
        current_hens = []
        current_feeders = []
        current_waterers = []

        # Extract detections
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().numpy()
            class_ids = results[0].boxes.cls.int().cpu().numpy()

            for box, track_id, cls_id in zip(boxes, track_ids, class_ids):
                class_name = CLASS_MAP.get(cls_id)
                
                if class_name == 'hen':
                    current_hens.append({'id': track_id, 'box': box})
                elif class_name == 'feeder':
                    current_feeders.append(box)
                elif class_name == 'waterer':
                    current_waterers.append(box)
        
        # Update Logic
        monitor.update(current_hens, current_feeders, current_waterers)

        # --- VISUALIZATION ---
        # 1. Draw Zones (Feeders/Waterers) first
        for box in current_feeders:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), COLOR_FEEDER, 2)
            cv2.putText(frame, "Feeder", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_FEEDER, 2, cv2.LINE_AA)

        for box in current_waterers:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), COLOR_WATERER, 2)
            cv2.putText(frame, "Waterer", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WATERER, 2, cv2.LINE_AA)

        # 2. Draw Hens and Stats
        for hen in current_hens:
            hen_id = hen['id']
            stats = monitor.get_stats(hen_id)
            
            if stats:
                x1, y1, x2, y2 = map(int, hen['box'])
                
                # Determine color based on action
                action = stats['current_action']
                box_color = COLOR_HEN_IDLE
                
                if action == 'Feeding': 
                    box_color = COLOR_FEEDER
                elif action == 'Drinking': 
                    box_color = COLOR_WATERER

                # Draw Hen Bounding Box
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)

                # Prepare Label Text
                label_main = f"Hen {hen_id}"
                label_sub = f"{action}"
                label_stats = f"Feeding: {stats['food_time']:.1f}s | Drinking: {stats['water_time']:.1f}s"

                # Draw Text Background (Semi-transparent black box look)
                # We draw a solid rectangle above the box to hold the text
                cv2.rectangle(frame, (x1, y1 - 45), (x2, y1), box_color, -1)
                
                # Draw Text (White) with Anti-Aliasing (cv2.LINE_AA)
                # Row 1: ID and Action
                cv2.putText(frame, label_main, (x1 + 5, y1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2, cv2.LINE_AA)
                cv2.putText(frame, label_sub, (x1 + 85, y1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2, cv2.LINE_AA)
                
                # Row 2: Timers
                cv2.putText(frame, label_stats, (x1 + 5, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1, cv2.LINE_AA)

        # Show Frame
        cv2.imshow("Poultry Vision System", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Inference complete.")

if __name__ == "__main__":
    main()