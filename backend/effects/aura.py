import cv2
import numpy as np

EVENT_COLORS = {
    "DOMAIN EXPANSION": (147, 112, 219),  # purple
    "LIMITLESS":        (100, 149, 237),  # blue
    "CURSED TECHNIQUE": (220, 20,  60),   # red
    "CURSED ENERGY":    (255, 140,  0),   # orange
}

def draw_aura(frame, event):
    if event == "IDLE":
        return frame

    color = EVENT_COLORS.get(event, (255, 255, 255))
    h, w, _ = frame.shape
    overlay = frame.copy()

    # Multiple glowing borders
    for thickness in [60, 40, 20]:
        alpha = 0.15
        cv2.rectangle(overlay, (0, 0), (w, h), color, thickness)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Dark vignette in corners
    mask = np.zeros((h, w), dtype=np.float32)
    cv2.circle(mask, (w//2, h//2), int(min(w, h) * 0.7), 1.0, -1)
    mask = cv2.GaussianBlur(mask, (201, 201), 0)
    mask = 1.0 - mask * 0.5

    for c in range(3):
        frame[:, :, c] = (frame[:, :, c] * mask).astype(np.uint8)

    # Color tint over whole frame
    tint = np.full((h, w, 3), color, dtype=np.uint8)
    cv2.addWeighted(tint, 0.15, frame, 0.85, 0, frame)

    return frame