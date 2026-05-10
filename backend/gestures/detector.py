import time
from backend.config.settings import GESTURE_COOLDOWN_SECONDS

class GestureDetector:
    def __init__(self):
        self._last_trigger_time = 0
        print("Gesture Detector ready!")

    def is_finger_up(self, points, tip, pip):
        return points[tip][1] < points[pip][1]

    def get_finger_states(self, points):
        return {
            "index":  self.is_finger_up(points, 8,  6),
            "middle": self.is_finger_up(points, 12, 10),
            "ring":   self.is_finger_up(points, 16, 14),
            "pinky":  self.is_finger_up(points, 20, 18),
        }

    def on_cooldown(self):
        return (time.time() - self._last_trigger_time) < GESTURE_COOLDOWN_SECONDS

    def trigger(self, event):
        self._last_trigger_time = time.time()
        print(f"Event: {event}")
        return event

    def detect(self, points):
        if self.on_cooldown():
            return "IDLE"

        fingers = self.get_finger_states(points)

        if all(fingers.values()):
            return self.trigger("DOMAIN EXPANSION")

        if fingers["index"] and fingers["middle"] and not fingers["ring"] and not fingers["pinky"]:
            return self.trigger("LIMITLESS")

        if fingers["index"] and not fingers["middle"] and not fingers["ring"] and not fingers["pinky"]:
            return self.trigger("CURSED TECHNIQUE")

        if not any(fingers.values()):
            return self.trigger("CURSED ENERGY")

        return "IDLE"