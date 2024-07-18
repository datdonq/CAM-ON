import cv2

# Open a connection to the webcam (usually the first webcam is index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly ret is True
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv2.imshow('Webcam Test', frame)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture and close the windows
cap.release()
cv2.destroyAllWindows()

