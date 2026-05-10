import cv2
import time
# from backend.effects.domain_expansion import DomainExpansion
from backend.camera.capture import CameraCapture
from backend.gestures.hand_tracker import HandTracker
from backend.gestures.detector import GestureDetector
# from backend.effects.aura import draw_aura

camera = CameraCapture()
camera.start()

tracker = HandTracker()
detector = GestureDetector()
# domain = DomainExpansion()

current_event = "IDLE"
event_display_time = 0

while True:
    success, bgr_frame, rgb_frame = camera.read_frame()
    
    if not success:
        continue

    results = tracker.process(rgb_frame)
    tracker.draw_landmarks(bgr_frame, results)

    # bgr_frame = draw_aura(bgr_frame, current_event)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            points = tracker.get_landmarks_list(hand_landmarks, bgr_frame.shape)
            event = detector.detect(points)
            if event != "IDLE":
                current_event = event
                event_display_time = time.time()
                # if event == "DOMAIN EXPANSION":
                #     domain.trigger()

    if current_event != "IDLE" and (time.time() - event_display_time) < 2.5:
        cv2.putText(bgr_frame, current_event, (20, 80),
                    cv2.FONT_HERSHEY_DUPLEX, 2, (147, 112, 219), 3)
    else:
        current_event = "IDLE"

        
    # bgr_frame = domain.render(bgr_frame)
    cv2.imshow("JJK Vision", bgr_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.stop()
tracker.close()
cv2.destroyAllWindows()