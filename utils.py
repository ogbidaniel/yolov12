# utils.py

def get_box_center(box):
    """
    Calculates the center (x, y) of a bounding box.
    Paper Eq (5).
    Args:
        box: [x1, y1, x2, y2]
    """
    x1, y1, x2, y2 = box
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return cx, cy

def calculate_overlap_area(box1, box2):
    """
    Calculates the intersection area between two bounding boxes.
    Replicates Algorithm 3 from the paper.
    
    Args:
        box1: [x1, y1, x2, y2] (e.g., Hen)
        box2: [x1, y1, x2, y2] (e.g., Feeder/Waterer)
    Returns:
        area (float): The area of overlap (0 if no overlap)
    """
    # Unpack coordinates
    left1, top1, right1, bottom1 = box1
    left2, top2, right2, bottom2 = box2

    # Calculate overlap dimensions (Algorithm 3)
    x_overlap = max(0, min(right1, right2) - max(left1, left2))
    y_overlap = max(0, min(bottom1, bottom2) - max(top1, top2))

    return x_overlap * y_overlap

def check_overlap(hen_box, zone_box):
    """
    Replicates Algorithm 2 from the paper.
    Returns True if there is an overlap, and the area.
    """
    left1, top1, right1, bottom1 = hen_box
    left2, top2, right2, bottom2 = zone_box

    # Check if boxes are disjoint (Algorithm 2 logic)
    if (left1 >= right2) or (right1 <= left2) or \
       (top1 >= bottom2) or (bottom1 <= top2):
        return False, 0
    
    # Calculate area if they are not disjoint
    area = calculate_overlap_area(hen_box, zone_box)
    return True, area