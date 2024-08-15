import cv2
import argparse
import numpy as np
import mediapipe as mp
from types_of_exercise import TypeOfExercise
import pygame

# Parse command-line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--exercise_type", type=str, help='Type of activity to do', required=True)
ap.add_argument("-vs", "--video_source", type=str, help='Type of activity to do', required=False)
args = vars(ap.parse_args())

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Initialize video capture
if args["video_source"] is not None:
    cap = cv2.VideoCapture("Exercise Videos/" + args["video_source"])
else:
    cap = cv2.VideoCapture(0)  # Webcam

cap.set(3, 1200)  # Width
cap.set(4, 580)  # Height

# Initialize exercise detection
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    counter = 0  # Movement counter
    status = True  # State of movement
    paused = True  # Start in paused state

    # Initialize Pygame for sound playback
    pygame.mixer.init()

    # Load sound files
    correct_sound = pygame.mixer.Sound("ting-sound-197759.mp3")
    #incorrect_sound = pygame.mixer.Sound("alarma-131582.mp3")

    def click_event(event, x, y, flags, param):
        global paused
        # Check if the left mouse button was clicked within the button area
        if event == cv2.EVENT_LBUTTONDOWN:
            if 20 <= x <= 120 and 20 <= y <= 70:
                paused = not paused

    # Main loop for video processing
    while cap.isOpened():
        ret, frame = cap.read()

        # Resize frame to a specific size
        frame = cv2.resize(frame, (1200, 580), interpolation=cv2.INTER_AREA)

        if not paused:
            # Recolor frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False

            # Make detection
            results = pose.process(frame)

            # Recolor back to BGR
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                counter, status = TypeOfExercise(landmarks).calculate_exercise(args["exercise_type"], counter, status)
            except:
                pass

            # Render detections (for landmarks)
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(174, 139, 45), thickness=2, circle_radius=2),
            )

        # Draw the pause/resume button
        cv2.rectangle(frame, (20, 20), (120, 70), (0, 0, 255), -1)
        button_text = "Resume" if paused else "Pause"
        cv2.putText(frame, button_text, (25, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Display exercise information on the frame
        cv2.putText(frame, "Activity: " + args["exercise_type"].replace("-", " "), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "Counter: " + str(counter), (10, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "Status: " + str(status), (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

        # Check for wrong posture and play sound
        if status and counter > 0:
            print("posture detected!")
            #incorrect_sound.play()

        # Display the frame
        cv2.imshow('Video', frame)
        cv2.setMouseCallback('Video', click_event)

        # Check for user input to quit the application
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Release video capture and close windows
    cap.release()
    cv2.destroyAllWindows()
