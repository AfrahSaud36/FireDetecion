import cv2
import numpy as np
import pywhatkit as kit


def filter_fire(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_fire = np.array([0, 120, 70])
    upper_fire = np.array([10, 255, 255])


    mask = cv2.inRange(hsv, lower_fire, upper_fire)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

 

    fire_detected = False
    for contour in contours:

        area = cv2.contourArea(contour)

        if area > 5000: 

            print("Emergency!! fire has been detected 🔥")
            print("Emergency!! fire has been detected 🔥")
            print("Emergency!! fire has been detected 🔥")
            phone_num = "emergency number" # use your emergency number in here 
            message = "Hello, this is a fire alarm from drone1!!"
            hour=17
            minute=52
            kit.sendwhatmsg(phone_num, message, hour, minute)
            fire_detected = True

            break

    return fire_detected

def filter_smoke(frame):

 

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (15, 15), 0)


    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)


    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if smoke is detected 
    smoke_detected = False

    for contour in contours:

        area = cv2.contourArea(contour)

        if area > 50000:  # Adjust this threshold based on your needs
            print("Emergency!! Smoke has been detected💨")
            smoke_detected = True
            break

    return smoke_detected

 

#video from the camera

cap = cv2.VideoCapture(0)
while True:

    ret, frame = cap.read()
    fire_detected = filter_fire(frame)
    smoke_detected = filter_smoke(frame)
    if fire_detected:

        cv2.putText(frame, "Fire Detected!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    if smoke_detected:

        cv2.putText(frame, "Smoke Detected!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2, cv2.LINE_AA)
    cv2.imshow('Fire and Smoke Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('x'):

        break

cap.release()
cv2.destroyAllWindows()
