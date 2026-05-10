import cv2
import numpy as np
import time

class DomainExpansion:
    def __init__(self):
        self.active = False
        self.start_time = 0
        self.duration = 3.0  # seconds

    def trigger(self):
        self.active = True
        self.start_time = time.time()
        print("DOMAIN EXPANSION TRIGGERED")

    def is_active(self):
        if not self.active:
            return False
        if time.time() - self.start_time > self.duration:
            self.active = False
            return False
        return True

    def render(self, frame):
        if not self.is_active():
            return frame

        elapsed = time.time() - self.start_time
        progress = elapsed / self.duration

        h, w, _ = frame.shape

        # Phase 1 — darken screen
        if progress < 0.3:
            alpha = progress / 0.3
            dark = np.zeros_like(frame)
            cv2.addWeighted(dark, alpha * 0.8, frame, 1 - alpha * 0.8, 0, frame)

        # Phase 2 — purple flood
        elif progress < 0.6:
            dark = np.zeros_like(frame)
            cv2.addWeighted(dark, 0.7, frame, 0.3, 0, frame)
            tint = np.full((h, w, 3), (147, 112, 219), dtype=np.uint8)
            cv2.addWeighted(tint, 0.4, frame, 0.6, 0, frame)

        # Phase 3 — full effect
        else:
            dark = np.zeros_like(frame)
            cv2.addWeighted(dark, 0.6, frame, 0.4, 0, frame)
            tint = np.full((h, w, 3), (147, 112, 219), dtype=np.uint8)
            cv2.addWeighted(tint, 0.5, frame, 0.5, 0, frame)

        # Draw text
        if progress > 0.3:
            alpha = min(1.0, (progress - 0.3) / 0.2)
            text = "DOMAIN EXPANSION"
            font = cv2.FONT_HERSHEY_DUPLEX
            scale = 1.8
            thickness = 3
            size = cv2.getTextSize(text, font, scale, thickness)[0]
            x = (w - size[0]) // 2
            y = h // 2

            # Glow effect
            for offset in [6, 4, 2]:
                cv2.putText(frame, text, (x + offset, y + offset),
                           font, scale, (80, 0, 120), thickness + 2)

            cv2.putText(frame, text, (x, y),
                       font, scale, (220, 180, 255), thickness)

        # Glitch effect
        if 0.4 < progress < 0.7:
            for _ in range(3):
                gy = np.random.randint(0, h)
                gx = np.random.randint(0, 20) - 10
                frame[gy:gy+4, :] = np.roll(frame[gy:gy+4, :], gx, axis=1)

        return frame