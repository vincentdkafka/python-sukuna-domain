import mediapipe as mp
import cv2

from backend.config.settings import MAX_HANDS, DETECTION_CONFIDENCE, TRACKING_CONFIDENCE

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            max_num_hands=MAX_HANDS,
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE,
        )
        print("Hand Tracker ready!")

    def process(self, rgb_frame):
        return self.hands.process(rgb_frame)

    def draw_landmarks(self, bgr_frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    bgr_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return bgr_frame
    
    def get_landmarks_list(self, hand_landmarks, frame_shape):
        h, w, _ = frame_shape
        points = []
        for lm in hand_landmarks.landmark:
            px = int(lm.x * w)
            py = int(lm.y * h)
            points.append((px, py))
        return points

    def close(self):
        self.hands.close()