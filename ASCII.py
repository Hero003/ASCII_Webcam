#trying to get webcam data and convert it to ascii art


import numpy as np
import cv2

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

cap = cv2.VideoCapture(0) # initialize the webcam

#check if webcam is not opened correctly
if not cap.isOpened():

    print("Error: Cannot open Camera")
    exit()

print("Webcam opened successfully")


while True:

    # Capture fram-by-frame
    ret, frame = cap.read()

    # assuming frame wasnt grabbed
    if not ret:
        print("Error: cannot receive frame.")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # needs to preprocess the image to grayscale and focus on brightness rather than color

    # Resize the frame for the ASCII text dimension. Text characters are taller than wider, so we need to scale accordingly
    target_width = 120
    target_height = 45
    resized_frame = cv2.resize(gray_frame, (target_width, target_height))

    #Create a blank black background for our ASCII webcam

    canvas_width = 800
    canvas_height = 600
    ascii_window = np.zeros((canvas_height, canvas_width, 3), dtype = np.uint8)

    x_step = canvas_width // target_width
    y_step = canvas_height // target_height

    # Map the pixels into ACII values
    for row_id in range(target_height):
        for col_id in range(target_width):

            pixel_brightness = resized_frame[row_id, col_id]

            char_index = int((pixel_brightness / 255) * (len(ASCII_CHARS) - 1))
            ascii_char = ASCII_CHARS[char_index]

            x_pos = col_id * x_step
            y_pos = row_id * y_step + y_step

            cv2.putText(ascii_window, ascii_char, (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow("webcam feed", frame)
    cv2.imshow("ASCII Webcam", ascii_window)

    # Wait for the key 'q' pressed to exit the frame

    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

# clean everything up

cap.release()
cv2.destroyAllWindows()