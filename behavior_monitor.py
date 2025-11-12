# behavior_monitor.py
from utils import check_overlap

class HenBehaviorMonitor:
    def __init__(self, fps=30.0):
        self.fps = fps
        # Dictionary to store data: { tracking_id: { 'food_time': 0.0, 'water_time': 0.0, 'current_action': 'Idle' } }
        self.hen_stats = {}

    def update(self, hens, feeders, waterers):
        """
        Process a single frame of detections.
        
        Args:
            hens: List of dicts {'id': int, 'box': [x1,y1,x2,y2]}
            feeders: List of [x1,y1,x2,y2]
            waterers: List of [x1,y1,x2,y2]
        """
        for hen in hens:
            hen_id = hen['id']
            hen_box = hen['box']

            # Initialize stats for new hen ID
            if hen_id not in self.hen_stats:
                self.hen_stats[hen_id] = {'food_time': 0.0, 'water_time': 0.0, 'current_action': 'Idle'}

            action_detected = False

            # Check Feeding (Algorithm 2 application)
            for feeder_box in feeders:
                is_overlapping, area = check_overlap(hen_box, feeder_box)
                # Threshold: e.g., overlap area > 0 or center logic from Eq 6
                if is_overlapping and area > 0:
                    self.hen_stats[hen_id]['food_time'] += (1.0 / self.fps)
                    self.hen_stats[hen_id]['current_action'] = 'Feeding'
                    action_detected = True
                    break # Assume interacting with one feeder at a time

            # Check Drinking (if not feeding)
            if not action_detected:
                for waterer_box in waterers:
                    is_overlapping, area = check_overlap(hen_box, waterer_box)
                    if is_overlapping and area > 0:
                        self.hen_stats[hen_id]['water_time'] += (1.0 / self.fps)
                        self.hen_stats[hen_id]['current_action'] = 'Drinking'
                        action_detected = True
                        break

            # If no overlap, set to Idle
            if not action_detected:
                self.hen_stats[hen_id]['current_action'] = 'Idle'

    def get_stats(self, hen_id):
        return self.hen_stats.get(hen_id, None)