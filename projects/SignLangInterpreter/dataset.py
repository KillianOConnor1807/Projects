import os
import pickle  # import for saving python objects to file

import mediapipe as mp
import cv2
import matplotlib.pyplot as plt


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

#Creates a MediaPipe Hands detector , treats each image independently (not video tracking) , only accept detections with confidence ≥ 0.3.#
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# path to data 
DATA_DIR = './data'

data = []
labels = []

#loops through each subfolder in directory , loops through every folder path
for dir_ in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        data_aux = [] # will hold data for each image

        x_ = []
        y_ = []

        #reads image using OpenCV , converts to RGB from BGR
        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        #runs mediapipe hands model on image 
        results = hands.process(img_rgb)
        # chechks for hands detected
        if results.multi_hand_landmarks:
            #iterates through each hand
            for hand_landmarks in results.multi_hand_landmarks:
                # for each landmark , gets the x and y coordinates and appends to lists
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)
                #loop through every landmark , extract the coordinates , normalises the coordinates by subtracting the minimum x and y
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            data.append(data_aux)
            labels.append(dir_)

f = open('data.pickle', 'wb') # Opens a file named data.pickle for writing in binary
pickle.dump({'data': data, 'labels': labels}, f) # write the dict into data.pickle 
f.close()