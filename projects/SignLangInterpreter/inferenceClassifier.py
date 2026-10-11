import pickle 
import cv2
import mediapipe as mp        
import numpy as np 

model_dict = pickle.load(open('./model.p', 'rb')) # load file saved in dataset.py
model = model_dict['model']

#Start video capture
cap = cv2.VideoCapture(0)

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# static_image_mode=True: treat frames independently 
# min_detection_confidence=0.3: only accept detections above this confidence
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {0: 'A', 1: 'B', 2: 'L'}

while True:

    data_aux = []

    x_ = []
    y_ = []

    # read a frame from the camera
    ret, frame = cap.read()

    # get frame dimensions
    H, W, _ = frame.shape

    # convert from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # run MediaPipe hand detection
    results = hands.process(frame_rgb)

    # run if one or more hands are detected
    if results.multi_hand_landmarks:

        # draw landmarks on the frame
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # where to draw
                hand_landmarks,  # detected hand landmarks
                mp_hands.HAND_CONNECTIONS,  # which connections to draw
                mp_drawing_styles.get_default_hand_landmarks_style(),      # style for joints
                mp_drawing_styles.get_default_hand_connections_style()     # style for bones/lines
            )

        # store all x and y values for this frame (across landmarks/hand(s))
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            # build normalised features
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        # convert normalized landmark extents to a pixel bounding box
        x1 = int(min(x_) * W) - 10  # left
        y1 = int(min(y_) * H) - 10  # top
        x2 = int(max(x_) * W) - 10  # right
        y2 = int(max(y_) * H) - 10  # bottom

        # --- Predict class using the ML model ---
        # model.predict expects a batch, so we wrap data_aux into a list and convert to numpy array
        prediction = model.predict([np.asarray(data_aux)])

        # prediction[0] is the predicted class index (e.g., 0,1,2)
        predicted_character = labels_dict[int(prediction[0])]

        # --- Draw the prediction on the frame ---
        # Draw a rectangle around the hand region
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)

        # Put the predicted letter near the top-left of the box
        cv2.putText(
            frame,
            predicted_character,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.3,              # font scale
            (0, 0, 0),       # text color (black)
            3,                # thickness
            cv2.LINE_AA       # anti-aliased line type
        )

    # Show the updated frame in a window
    cv2.imshow('frame', frame)

    # waitKey(1) keeps the window responsive; also allows OpenCV event handling
    cv2.waitKey(1)

# Cleanup when the loop ends
cap.release()
cv2.destroyAllWindows()
