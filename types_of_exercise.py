import numpy as np
from body_part_angle import BodyPartAngle
from utils import *
import pygame


class TypeOfExercise(BodyPartAngle):
    def __init__(self, landmarks):
        super().__init__(landmarks)
        pygame.mixer.init()

        # Load sound files
        self.correct_sound = pygame.mixer.Sound("ting-sound-197759.mp3")
        #self.incorrect_sound = pygame.mixer.Sound("alarma-131582.mp3")

    def push_up(self, counter, status):
        left_arm_angle = self.angle_of_the_left_arm()
        right_arm_angle = self.angle_of_the_left_arm()
        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2

        if status:
            if avg_arm_angle < 70:
                counter += 1
                status = False
                self.correct_sound.play()
        else:
            if avg_arm_angle > 160:
                #counter += 1
                status = True
                #self.incorrect_sound.play()

        return counter, status

    def display_wrong_posture(self):
        # Add code here to display a message indicating wrong posture
        print("Wrong posture detected!")   

    def pull_up(self, counter, status):
        nose = detection_body_part(self.landmarks, "NOSE")
        left_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        right_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        avg_shoulder_y = (left_elbow[1] + right_elbow[1]) / 2

        if status:
            if nose[1] > avg_shoulder_y:
                counter += 1
                status = False
                self.correct_sound.play()

        else:
            if nose[1] < avg_shoulder_y:
                counter += 1
                status = True

        return [counter, status]

    def squat(self, counter, status):
        left_leg_angle = self.angle_of_the_right_leg()
        right_leg_angle = self.angle_of_the_left_leg()
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2

        if status:
            if avg_leg_angle < 70:
                counter += 1
                status = False
                self.correct_sound.play()
        else:
            if avg_leg_angle > 160:
                counter += 1
                status = True


        return [counter, status]

    def walk(self, counter, status):
        right_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")
        left_knee = detection_body_part(self.landmarks, "LEFT_KNEE")

        if status:
            if left_knee[0] > right_knee[0]:
                counter += 1
                status = False
                self.correct_sound.play()

        else:
            if left_knee[0] < right_knee[0]:
                counter += 1
                status = True

        return [counter, status]

    def sit_up(self, counter, status):
        angle = self.angle_of_the_abdomen()
        if status:
            if angle < 55:
                counter += 1
                status = False
                self.correct_sound.play()
        else:
            if angle > 105:
                counter += 1
                status = True

        return [counter, status]

    def calculate_exercise(self, exercise_type, counter, status):
        if exercise_type == "push-up":
            counter, status = TypeOfExercise(self.landmarks).push_up(
                counter, status)
        #    counter, status = self.push_up(
        #        counter, status)

        # Check if the user transitions from true to intermediate state and back to true without reaching false state
        #    if not status and self.prev_status and counter > 0:
            # Add sound playback logic for intermediate state here
        #        print("Intermediate state detected!")
        #    elif not status and counter > 0:
        #        self.display_wrong_posture()
            # Add sound playback logic for wrong posture here
        #        self.incorrect_sound.play()
        #    elif status and not self.prev_status and counter > 0:
            # Add sound playback logic for correct posture here
        #        self.correct_sound.play()
        #        counter += 1

        # Update previous status
        #    self.prev_status = status

        #    return counter, status 
        elif exercise_type == "pull-up":
            counter, status = TypeOfExercise(self.landmarks).pull_up(
                counter, status)
        elif exercise_type == "squat":
            counter, status = TypeOfExercise(self.landmarks).squat(
                counter, status)
        elif exercise_type == "walk":
            counter, status = TypeOfExercise(self.landmarks).walk(
                counter, status)
        elif exercise_type == "sit-up":
            counter, status = TypeOfExercise(self.landmarks).sit_up(
                counter, status)

        return [counter, status]
