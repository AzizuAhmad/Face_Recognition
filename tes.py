import cv2
import face_recognition

# Open the video capture
video_capture = cv2.VideoCapture(1)  # Use 0 for the default webcam

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Convert the frame from BGR color (OpenCV format) to RGB color (face_recognition format)
    rgb_frame = frame[:, :, ::-1]

    # Find face locations in the frame
    face_locations = face_recognition.face_locations(rgb_frame)

    # Draw rectangles around each detected face
    for (top, right, bottom, left) in face_locations:
        # Draw the rectangle on the frame
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow("Video", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the windows
video_capture.release()
cv2.destroyAllWindows()
